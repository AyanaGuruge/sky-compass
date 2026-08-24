"""
synthetic_sky_polarizer.py

Generate synthetic all sky (fisheye) images as they would appear through a
SINGLE fixed linear polarising film, for a known sun position. Each image
comes with its ground truth sun azimuth and elevation, so a sun direction
estimation pipeline can be trained and validated even when very little real
data has been collected.

Model
    Rayleigh single scattering sky.
        degree of polarisation  DoP(g) = d_max * sin^2(g) / (1 + cos^2(g))
        where g is the scattering angle (the angular distance from a sky point
        to the sun). The e vector (electric field direction) of the scattered
        light is perpendicular to the scattering plane, which is the plane that
        contains the viewing direction and the sun.
    A single linear polariser at image angle alpha transmits, by Malus law,
        I_out = I_in * (0.5 + 0.5 * DoP * cos(2 * (chi_img - alpha)))
    where chi_img is the sky e vector angle expressed in the image plane.

Camera
    Equidistant fisheye,  r = f * theta,  optical axis pointing at the zenith.

Dependencies
    numpy only for the physics. matplotlib is used just to save preview PNGs.

Author note
    This is a first order radiometric model. It reproduces the geometry of the
    dark polarisation band correctly, which is what a sun azimuth estimator
    relies on. Absolute intensities are not calibrated. Validate against a few
    real captures and adjust d_max and the exposure to taste.
"""

import numpy as np


def make_sky_image(
    size=256,
    fov_deg=180.0,
    sun_az_deg=90.0,
    sun_el_deg=20.0,
    polariser_axis_deg=0.0,
    image_up_azimuth_deg=0.0,
    d_max=0.75,
    base_intensity=1.0,
    radial_axis=False,
):
    """Render one synthetic frame.

    Parameters
        size                 output image is size x size pixels
        fov_deg              full field of view of the fisheye (180 for a full sky)
        sun_az_deg           sun azimuth, degrees clockwise from North
        sun_el_deg           sun elevation, degrees above the horizon
        polariser_axis_deg   transmission axis angle in the IMAGE plane,
                             measured counter clockwise from image +x (to the right).
                             Ignored when radial_axis is True.
        image_up_azimuth_deg world azimuth that image up (+y) points to,
                             that is the camera heading
        d_max                maximum degree of polarisation of a clear sky
        base_intensity       overall scale of the unpolarised sky radiance
        radial_axis          if True, model a dome whose transmission axis points
                             radially outward at every point (a fan arrangement).
                             Along the solar meridian the sky e vector is tangential
                             while the analyser axis is radial, so the two stand a
                             quarter turn apart and transmission is minimised along
                             the whole meridian, from the sun through the zenith to
                             the antisolar point. The two ends are not equally dark:
                             the degree of polarisation is low near the sun and high
                             a quarter turn from it, so the ANTISOLAR end is the
                             darker one. The dark axis therefore fixes the solar
                             meridian, and the brightness asymmetry between its ends
                             is what identifies which end holds the sun.
                             If False, model one flat filter with a single fixed axis,
                             whose dark band is set by that axis and bears no fixed
                             relation to the sun.

    Returns
        intensity  the grayscale frame the camera would record
        dop        degree of polarisation map
        chi_img    sky e vector angle in the image plane (radians)
        mask       boolean, True inside the circular fisheye
    """
    R = size / 2.0
    ys, xs = np.mgrid[0:size, 0:size].astype(float)

    # image x to the right, image y UP (rows increase downward, so flip)
    dx = xs - (R - 0.5)
    dy = (R - 0.5) - ys
    rho = np.hypot(dx, dy)
    mask = rho <= R
    phi_img = np.arctan2(dy, dx)                    # pixel polar angle, ccw from +x

    # equidistant fisheye: zenith angle grows linearly with pixel radius
    theta = (rho / R) * np.deg2rad(fov_deg / 2.0)   # 0 at the centre (zenith)

    # world azimuth of every pixel.
    # convention: image up (phi_img = +90 deg) points to image_up_azimuth_deg,
    # and world azimuth increases clockwise (as seen looking up) with -phi_img.
    az = np.deg2rad(image_up_azimuth_deg) + (np.pi / 2.0 - phi_img)

    # sky direction unit vectors, frame is (East, North, Up)
    sx = np.sin(theta) * np.sin(az)
    sy = np.sin(theta) * np.cos(az)
    sz = np.cos(theta)

    # sun direction unit vector in the same frame
    A = np.deg2rad(sun_az_deg)
    E = np.deg2rad(sun_el_deg)
    sun = np.array([np.cos(E) * np.sin(A), np.cos(E) * np.cos(A), np.sin(E)])

    # scattering angle and Rayleigh degree of polarisation
    cos_g = np.clip(sx * sun[0] + sy * sun[1] + sz * sun[2], -1.0, 1.0)
    sin2_g = 1.0 - cos_g ** 2
    dop = np.clip(d_max * sin2_g / (1.0 + cos_g ** 2), 0.0, 1.0)

    # e vector in 3D is perpendicular to the scattering plane, so it is s x sun
    ex = sy * sun[2] - sz * sun[1]
    ey = sz * sun[0] - sx * sun[2]
    ez = sx * sun[1] - sy * sun[0]
    enorm = np.sqrt(ex ** 2 + ey ** 2 + ez ** 2) + 1e-12
    ex, ey, ez = ex / enorm, ey / enorm, ez / enorm

    # local tangent basis at each pixel
    # e_theta points along increasing zenith angle (the image radial direction)
    # e_phi points along increasing azimuth (the image tangential direction)
    et_x = np.cos(theta) * np.sin(az)
    et_y = np.cos(theta) * np.cos(az)
    et_z = -np.sin(theta)
    ep_x = np.cos(az)
    ep_y = -np.sin(az)

    a = ex * et_x + ey * et_y + ez * et_z       # e vector component along e_theta
    b = ex * ep_x + ey * ep_y                    # e vector component along e_phi
    psi = np.arctan2(b, a)                        # e vector angle in the tangent frame

    # e_theta maps to the image radial direction (angle phi_img),
    # e_phi maps to the tangential direction (phi_img + 90 deg),
    # so the e vector angle in image coordinates is:
    chi_img = phi_img + psi

    # polariser transmission axis in the image plane.
    # a flat filter has one fixed angle. a radial dome has an axis that points
    # outward at every pixel, so alpha follows the pixel polar angle.
    if radial_axis:
        alpha = phi_img
    else:
        alpha = np.deg2rad(polariser_axis_deg)
    transmission = 0.5 + 0.5 * dop * np.cos(2.0 * (chi_img - alpha))
    intensity = base_intensity * transmission

    intensity[~mask] = 0.0
    dop[~mask] = 0.0
    chi_img[~mask] = 0.0
    return intensity, dop, chi_img, mask


def sun_pixel(size, fov_deg, sun_az_deg, sun_el_deg, image_up_azimuth_deg=0.0):
    """Return the (col, row) pixel where the sun projects, for previews."""
    R = size / 2.0
    theta_sun = np.deg2rad(90.0 - sun_el_deg)
    r_sun = (theta_sun / np.deg2rad(fov_deg / 2.0)) * R
    phi = np.pi / 2.0 - (np.deg2rad(sun_az_deg) - np.deg2rad(image_up_azimuth_deg))
    col = (R - 0.5) + r_sun * np.cos(phi)
    row = (R - 0.5) - r_sun * np.sin(phi)
    return col, row


def generate_dataset(
    out_dir,
    n_samples=400,
    size=128,
    fov_deg=180.0,
    polariser_axis_deg=0.0,
    image_up_azimuth_deg=0.0,
    az_range=(0.0, 360.0),
    el_range=(5.0, 60.0),
    d_max=0.75,
    seed=0,
):
    """Create a labelled dataset of synthetic frames.

    Writes
        images.npy   float array, shape (n_samples, size, size)
        labels.csv   columns index, sun_az_deg, sun_el_deg
    """
    import os
    import csv

    os.makedirs(out_dir, exist_ok=True)
    rng = np.random.default_rng(seed)
    images = np.zeros((n_samples, size, size), dtype=np.float32)
    rows = []
    for i in range(n_samples):
        az = float(rng.uniform(*az_range))
        el = float(rng.uniform(*el_range))
        img, _, _, _ = make_sky_image(
            size=size,
            fov_deg=fov_deg,
            sun_az_deg=az,
            sun_el_deg=el,
            polariser_axis_deg=polariser_axis_deg,
            image_up_azimuth_deg=image_up_azimuth_deg,
            d_max=d_max,
        )
        images[i] = img.astype(np.float32)
        rows.append((i, round(az, 3), round(el, 3)))

    np.save(os.path.join(out_dir, "images.npy"), images)
    with open(os.path.join(out_dir, "labels.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["index", "sun_az_deg", "sun_el_deg"])
        w.writerows(rows)
    return os.path.join(out_dir, "images.npy"), os.path.join(out_dir, "labels.csv")


if __name__ == "__main__":
    # quick self test: render a grid of sun azimuths and mark the true sun, so
    # you can confirm the pattern rotates rigidly with the sun. Note this grid
    # uses the FLAT filter, whose dark band is fixed by the film axis and does
    # not track the sun. For the radial dome see the radial_axis docstring.
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    size = 256
    fov = 180.0
    axis = 0.0            # polariser transmission axis pointing "right" in the image
    up_az = 0.0           # image up points North
    azimuths = [0, 45, 90, 135, 180, 225, 270, 315]
    el = 25.0

    fig, axes = plt.subplots(2, 4, figsize=(14, 7))
    for ax_plt, A in zip(axes.ravel(), azimuths):
        img, dop, chi, mask = make_sky_image(
            size=size, fov_deg=fov, sun_az_deg=A, sun_el_deg=el,
            polariser_axis_deg=axis, image_up_azimuth_deg=up_az,
        )
        disp = img.copy()
        disp[~mask] = np.nan
        ax_plt.imshow(disp, cmap="gray", vmin=0.0, vmax=1.0)
        c, r = sun_pixel(size, fov, A, el, up_az)
        ax_plt.plot([c], [r], marker="+", markersize=14, color="red", markeredgewidth=2)
        ax_plt.set_title(f"sun az {A} deg, el {el:.0f} deg")
        ax_plt.set_xticks([]); ax_plt.set_yticks([])
    fig.suptitle("Synthetic sky through a single linear polariser. Red plus marks the true sun.", fontsize=13)
    fig.tight_layout()
    fig.savefig("/home/claude/preview_grid.png", dpi=90)
    print("saved /home/claude/preview_grid.png")
