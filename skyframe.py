"""
skyframe.py

Everything that turns a real photograph into the same geometry the synthetic
generator produces. The estimator compares a measured frame against a rendered
one, so the two must live in identical coordinates or the comparison is
meaningless. This module is that bridge.

Canonical geometry (identical to synthetic_sky_polarizer.make_sky_image)
    square image, size x size pixels
    the circular sky fills the square exactly, centre pixel is the zenith
    equidistant projection, zenith angle grows linearly with pixel radius
    image +x to the right, image +y up
    image up corresponds to some world azimuth, fitted during calibration

Handedness
    A camera pointing at the zenith records the sky mirrored with respect to a
    map. Depending on the sensor, the driver, and any flips applied in the
    capture path, world azimuth may run clockwise or counter clockwise in the
    stored image. Rather than reasoning about this once and hoping, the
    `mirror` flag is carried explicitly and is fitted from labelled frames in
    calibrate.py, alongside the heading offset.

Dependencies
    numpy. Pillow or OpenCV, whichever is installed, only for reading files.
"""

from __future__ import annotations

import numpy as np


# ----------------------------------------------------------------------------
# file reading
# ----------------------------------------------------------------------------

def load_gray(path: str) -> np.ndarray:
    """Load an image file as a float grayscale array scaled to 0 to 1."""
    try:
        from PIL import Image
        arr = np.asarray(Image.open(path).convert("L"), dtype=np.float64)
    except ImportError:
        import cv2
        raw = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if raw is None:
            raise IOError("could not read " + path)
        arr = raw.astype(np.float64)
    if arr.max() > 1.5:
        arr = arr / 255.0
    return arr


# ----------------------------------------------------------------------------
# locating the circular image of the sky
# ----------------------------------------------------------------------------

def find_disc(gray: np.ndarray, threshold: float | None = None):
    """Estimate the centre and radius of the bright circular fisheye image.

    Returns (cx, cy, radius) in pixels. The method is deliberately crude: it
    thresholds the frame, takes the centroid of the lit pixels as the centre,
    and derives the radius from the lit area. For a lens that vignettes to
    black outside the image circle this is accurate to a pixel or two, which is
    well below the angular error of the compass itself. Measure the circle by
    hand once and hard code it if the automatic estimate ever looks wrong.
    """
    if threshold is None:
        threshold = 0.5 * (gray.min() + gray.max())
    lit = gray > threshold
    if lit.sum() < 100:
        raise ValueError("the frame appears almost entirely dark, "
                         "check the exposure before trusting find_disc")
    ys, xs = np.nonzero(lit)
    # the bounding box is used rather than the centroid, because the dark
    # polarisation band makes one side of the disc much dimmer than the other
    # and a centroid would be pulled away from the true centre.
    x0, x1 = np.percentile(xs, [0.2, 99.8])
    y0, y1 = np.percentile(ys, [0.2, 99.8])
    cx = float((x0 + x1) / 2.0)
    cy = float((y0 + y1) / 2.0)
    radius = float(((x1 - x0) + (y1 - y0)) / 4.0)
    return cx, cy, radius


# ----------------------------------------------------------------------------
# resampling into the canonical square
# ----------------------------------------------------------------------------

def to_canonical(gray: np.ndarray, cx: float, cy: float, radius: float,
                 size: int = 128, mirror: bool = False,
                 roll_deg: float = 0.0):
    """Resample a frame so the sky disc exactly fills a size x size square.

    Parameters
        cx, cy, radius   the fisheye circle in the source image, in pixels
        size             side length of the canonical output
        mirror           flip left to right, which reverses the handedness of
                         azimuth in the image
        roll_deg         rotate the sky by this angle, counter clockwise, used
                         only if the camera is mounted rotated on purpose

    Returns (canonical_image, mask) where mask is True inside the sky circle.
    """
    r_out = size / 2.0
    ys, xs = np.mgrid[0:size, 0:size].astype(float)
    dx = xs - (r_out - 0.5)
    dy = (r_out - 0.5) - ys              # image y up, matching the generator
    rho = np.hypot(dx, dy)
    mask = rho <= r_out

    if mirror:
        dx = -dx
    if roll_deg:
        a = np.deg2rad(roll_deg)
        dx, dy = dx * np.cos(a) - dy * np.sin(a), dx * np.sin(a) + dy * np.cos(a)

    # map canonical pixel offsets back into source pixel coordinates
    scale = radius / r_out
    src_x = cx + dx * scale
    src_y = cy - dy * scale              # source rows increase downward

    h, w = gray.shape
    x0 = np.clip(np.floor(src_x).astype(int), 0, w - 2)
    y0 = np.clip(np.floor(src_y).astype(int), 0, h - 2)
    fx = np.clip(src_x - x0, 0.0, 1.0)
    fy = np.clip(src_y - y0, 0.0, 1.0)

    out = ((1 - fx) * (1 - fy) * gray[y0, x0]
           + fx * (1 - fy) * gray[y0, x0 + 1]
           + (1 - fx) * fy * gray[y0 + 1, x0]
           + fx * fy * gray[y0 + 1, x0 + 1])
    out = np.where(mask, out, 0.0)
    return out, mask


# ----------------------------------------------------------------------------
# masking and normalisation
# ----------------------------------------------------------------------------

def analysis_mask(size: int, mask: np.ndarray,
                  horizon_margin_deg: float = 15.0,
                  fov_deg: float = 180.0,
                  sun_az_deg: float | None = None,
                  sun_el_deg: float | None = None,
                  sun_mask_deg: float = 12.0,
                  image_up_azimuth_deg: float = 0.0,
                  mirror: bool = False) -> np.ndarray:
    """Build the mask of pixels the estimator is allowed to use.

    Two regions are excluded. The outermost ring near the horizon is dropped,
    because that is where trees, buildings, and the mount intrude and where the
    equidistant model is least accurate. The region immediately around the sun
    is dropped as well, because it saturates and because single scattering does
    not describe the circumsolar sky well.
    """
    r_out = size / 2.0
    ys, xs = np.mgrid[0:size, 0:size].astype(float)
    dx = xs - (r_out - 0.5)
    dy = (r_out - 0.5) - ys
    rho = np.hypot(dx, dy)
    theta = (rho / r_out) * np.deg2rad(fov_deg / 2.0)

    keep = mask & (np.rad2deg(theta) <= (90.0 - horizon_margin_deg))

    if sun_az_deg is not None and sun_el_deg is not None and sun_el_deg > 0:
        phi_img = np.arctan2(dy, dx)
        sign = -1.0 if mirror else 1.0
        az = np.deg2rad(image_up_azimuth_deg) + sign * (np.pi / 2.0 - phi_img)
        sx = np.sin(theta) * np.sin(az)
        sy = np.sin(theta) * np.cos(az)
        sz = np.cos(theta)
        A, E = np.deg2rad(sun_az_deg), np.deg2rad(sun_el_deg)
        sun = np.array([np.cos(E) * np.sin(A), np.cos(E) * np.cos(A), np.sin(E)])
        cos_g = np.clip(sx * sun[0] + sy * sun[1] + sz * sun[2], -1.0, 1.0)
        keep &= np.rad2deg(np.arccos(cos_g)) > sun_mask_deg

    return keep


def normalise(img: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Zero mean, unit standard deviation over the masked pixels."""
    vals = img[mask]
    mu = vals.mean()
    sd = vals.std()
    if sd < 1e-9:
        sd = 1.0
    out = np.zeros_like(img)
    out[mask] = (img[mask] - mu) / sd
    return out


def ncc(a: np.ndarray, b: np.ndarray, mask: np.ndarray) -> float:
    """Normalised cross correlation of two frames over a shared mask."""
    va = a[mask]
    vb = b[mask]
    va = va - va.mean()
    vb = vb - vb.mean()
    denom = np.sqrt((va ** 2).sum() * (vb ** 2).sum())
    if denom < 1e-12:
        return 0.0
    return float((va * vb).sum() / denom)


def prepare_real_frame(path: str, size: int = 128, mirror: bool = False,
                       disc=None, roll_deg: float = 0.0):
    """Convenience wrapper: file on disk to canonical frame and mask."""
    gray = load_gray(path)
    if disc is None:
        disc = find_disc(gray)
    cx, cy, radius = disc
    img, mask = to_canonical(gray, cx, cy, radius, size=size, mirror=mirror,
                             roll_deg=roll_deg)
    return img, mask, (cx, cy, radius)


if __name__ == "__main__":
    # self test: push a synthetic frame through the resampler and check that the
    # geometry survives the round trip.
    from synthetic_sky_polarizer import make_sky_image

    src, _, _, m = make_sky_image(size=400, sun_az_deg=130.0, sun_el_deg=35.0)
    cx, cy, radius = find_disc(np.where(m, src + 0.2, 0.0))
    print("disc found at centre ({:.1f}, {:.1f}) radius {:.1f}, "
          "true centre (199.5, 199.5) radius 200.0".format(cx, cy, radius))

    canon, cmask = to_canonical(src, 199.5, 199.5, 200.0, size=128)
    ref, _, _, rmask = make_sky_image(size=128, sun_az_deg=130.0, sun_el_deg=35.0)
    shared = cmask & rmask
    print("correlation between resampled and directly rendered frame: {:.4f}"
          .format(ncc(canon, ref, shared)))
    assert ncc(canon, ref, shared) > 0.99
    print("skyframe.py self test passed.")
