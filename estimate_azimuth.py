"""
estimate_azimuth.py

Recover the sun azimuth from a single frame taken through the polarising film,
by analysis by synthesis. Candidate sun azimuths are swept across the full
circle, the expected pattern is rendered for each candidate, and the candidate
whose rendering correlates best with the measured frame is taken as the
estimate. Nothing is trained, so this works from the first frame onward.

Two modes
    calibrate   fit the three fixed unknowns of the rig from labelled frames:
                the world azimuth that image up points to, the angle of the
                film transmission axis in the image, and the handedness of the
                image. These are properties of the mounting, not of the sky, so
                they are fitted once and then held fixed.
    estimate    run the estimator on one frame or a directory of frames and
                report the azimuth, the confidence, and, when the frames are
                timestamped, the error against the ephemeris.

Filename convention
    Frames are expected to be named  sky_YYYYmmddTHHMMSSZ.png  with the time in
    UTC, which is what capture.py writes. The timestamp is the label: it gives
    the true sun azimuth and elevation through turku_sun.py, so no frame ever
    has to be annotated by hand.

Usage
    python3 estimate_azimuth.py calibrate --dir captures/2026-07-25
    python3 estimate_azimuth.py estimate  --dir captures/2026-07-25 --calib calib.json
    python3 estimate_azimuth.py estimate  --image captures/sky_20260725T060000Z.png \\
                                          --calib calib.json
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
from datetime import datetime, timezone

import numpy as np

from synthetic_sky_polarizer import make_sky_image
from skyframe import (analysis_mask, ncc, normalise, prepare_real_frame)
from turku_sun import sun_position

SIZE = 128
FOV_DEG = 180.0
TIMESTAMP_RE = re.compile(r"(\d{8}T\d{6})Z")


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------

def timestamp_from_name(path: str) -> datetime | None:
    """Pull the UTC capture time out of a filename, or return None."""
    m = TIMESTAMP_RE.search(os.path.basename(path))
    if not m:
        return None
    return datetime.strptime(m.group(1), "%Y%m%dT%H%M%S").replace(
        tzinfo=timezone.utc)


def angular_error(a: float, b: float) -> float:
    """Smallest absolute difference between two azimuths, in degrees."""
    return abs((a - b + 180.0) % 360.0 - 180.0)


def render(az_rel_deg: float, el_deg: float, axis_deg: float,
           radial: bool = False, size: int = SIZE):
    """Render the expected frame for a sun azimuth measured from image up."""
    img, _, _, mask = make_sky_image(
        size=size, fov_deg=FOV_DEG, sun_az_deg=az_rel_deg, sun_el_deg=el_deg,
        polariser_axis_deg=axis_deg, image_up_azimuth_deg=0.0,
        radial_axis=radial)
    return img, mask


# ----------------------------------------------------------------------------
# the estimator
# ----------------------------------------------------------------------------

def estimate(frame: np.ndarray, mask: np.ndarray, el_deg: float,
             axis_deg: float = 0.0, radial: bool = False,
             step_deg: float = 2.0, refine: bool = True):
    """Estimate the sun azimuth relative to image up.

    Returns (azimuth_rel_deg, confidence, curve) where curve is the array of
    correlation scores over the swept azimuths, kept so the peak can be plotted
    or inspected.

    Confidence is the height of the correlation peak above the mean of the
    curve, expressed in standard deviations of the curve. A sharp isolated peak
    gives a high value. A broad flat curve, which is what thick cloud produces,
    gives a low one, and the estimate should then be treated as unreliable.
    """
    coarse = np.arange(0.0, 360.0, step_deg)
    obs = normalise(frame, mask)
    scores = np.empty_like(coarse)
    for i, az in enumerate(coarse):
        pred, pmask = render(az, el_deg, axis_deg, radial)
        scores[i] = ncc(obs, pred, mask & pmask)

    best_i = int(np.argmax(scores))
    best_az = float(coarse[best_i])

    if refine:
        lo, hi = best_az - step_deg, best_az + step_deg
        fine = np.arange(lo, hi + 0.25, 0.25)
        fine_scores = []
        for az in fine:
            pred, pmask = render(az % 360.0, el_deg, axis_deg, radial)
            fine_scores.append(ncc(obs, pred, mask & pmask))
        best_az = float(fine[int(np.argmax(fine_scores))] % 360.0)

    sd = scores.std()
    confidence = float((scores[best_i] - scores.mean()) / sd) if sd > 1e-9 else 0.0
    return best_az, confidence, scores


# ----------------------------------------------------------------------------
# calibration
# ----------------------------------------------------------------------------

def calibrate(paths, radial: bool = False, size: int = SIZE,
              axis_step: float = 10.0, verbose: bool = True):
    """Fit image up azimuth, film axis angle and handedness from labelled frames.

    Every frame carries its own true sun azimuth through its timestamp. For a
    trial film axis and a trial handedness, the estimator returns an azimuth
    measured from image up, and the difference between that and the true
    azimuth should be the same constant for every frame, namely the heading of
    image up. The correct film axis and handedness are the pair for which that
    difference is most consistent, so the fit is a small grid search scored by
    the spread of the residuals.
    """
    labelled = []
    for p in sorted(paths):
        t = timestamp_from_name(p)
        if t is None:
            continue
        az_true, el_true = sun_position(t)
        if el_true < 3.0:
            continue
        labelled.append((p, t, az_true, el_true))
    if len(labelled) < 3:
        raise SystemExit("calibration needs at least three timestamped frames "
                         "taken at clearly different times of day, found "
                         + str(len(labelled)))

    best = None
    for mirror in (False, True):
        prepared = []
        for p, t, az_true, el_true in labelled:
            img, dmask, _ = prepare_real_frame(p, size=size, mirror=mirror)
            amask = analysis_mask(size, dmask, horizon_margin_deg=15.0)
            prepared.append((img, amask, az_true, el_true))
        for axis in np.arange(0.0, 180.0, axis_step):
            offsets = []
            for img, amask, az_true, el_true in prepared:
                az_rel, _, _ = estimate(img, amask, el_true, axis_deg=axis,
                                        radial=radial, step_deg=4.0,
                                        refine=False)
                offsets.append(np.deg2rad((az_true - az_rel) % 360.0))
            offsets = np.array(offsets)
            # circular mean and circular spread of the residual offsets
            c, s = np.cos(offsets).mean(), np.sin(offsets).mean()
            up_az = float(np.rad2deg(np.arctan2(s, c)) % 360.0)
            spread = float(np.rad2deg(np.sqrt(-2.0 * np.log(max(np.hypot(c, s), 1e-9)))))
            if verbose:
                print("  mirror {:5s} axis {:5.1f} deg  ->  image up {:6.1f} deg, "
                      "spread {:5.1f} deg".format(str(mirror), axis, up_az, spread))
            if best is None or spread < best["spread"]:
                best = {"mirror": bool(mirror), "axis_deg": float(axis),
                        "image_up_azimuth_deg": up_az, "spread": spread,
                        "radial": bool(radial), "size": int(size),
                        "n_frames": len(labelled)}
    return best


# ----------------------------------------------------------------------------
# command line
# ----------------------------------------------------------------------------

def _collect(args):
    if args.image:
        return [args.image]
    return sorted(glob.glob(os.path.join(args.dir, "*.png"))
                  + glob.glob(os.path.join(args.dir, "*.jpg")))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("calibrate", help="fit the fixed rig parameters")
    c.add_argument("--dir", required=True)
    c.add_argument("--radial", action="store_true",
                   help="the optic is the radial gore dome, not a flat filter")
    c.add_argument("--out", default="calib.json")

    e = sub.add_parser("estimate", help="estimate the sun azimuth")
    e.add_argument("--dir")
    e.add_argument("--image")
    e.add_argument("--calib", default="calib.json")
    e.add_argument("--step", type=float, default=2.0)

    args = ap.parse_args()

    if args.cmd == "calibrate":
        paths = sorted(glob.glob(os.path.join(args.dir, "*.png"))
                       + glob.glob(os.path.join(args.dir, "*.jpg")))
        print("calibrating on {} files in {}".format(len(paths), args.dir))
        best = calibrate(paths, radial=args.radial)
        with open(args.out, "w") as f:
            json.dump(best, f, indent=2)
        print()
        print("best fit written to " + args.out)
        print(json.dumps(best, indent=2))
        print()
        print("A spread below about 10 degrees means the rig geometry is "
              "consistent and the estimates can be trusted. A large spread "
              "usually means the frames were taken under cloud, or that the "
              "mount moved between frames.")
        return

    with open(args.calib) as f:
        cal = json.load(f)
    paths = _collect(args)
    errors = []
    print("{:34s} {:>9s} {:>9s} {:>9s} {:>6s}".format(
        "frame", "estimate", "truth", "error", "conf"))
    for p in paths:
        img, dmask, _ = prepare_real_frame(p, size=cal["size"],
                                           mirror=cal["mirror"])
        amask = analysis_mask(cal["size"], dmask, horizon_margin_deg=15.0)
        t = timestamp_from_name(p)
        if t is None:
            print("{:34s} skipped, no UTC timestamp in the filename".format(
                os.path.basename(p)[:34]))
            continue
        az_true, el_true = sun_position(t)
        az_rel, conf, _ = estimate(img, amask, el_true,
                                   axis_deg=cal["axis_deg"],
                                   radial=cal["radial"], step_deg=args.step)
        az_est = (az_rel + cal["image_up_azimuth_deg"]) % 360.0
        err = angular_error(az_est, az_true)
        errors.append(err)
        print("{:34s} {:9.2f} {:9.2f} {:9.2f} {:6.1f}".format(
            os.path.basename(p)[:34], az_est, az_true, err, conf))

    if errors:
        errors = np.array(errors)
        print()
        print("frames {:d}, mean absolute error {:.2f} deg, median {:.2f} deg, "
              "90th percentile {:.2f} deg".format(
                  len(errors), errors.mean(), np.median(errors),
                  np.percentile(errors, 90)))


if __name__ == "__main__":
    main()
