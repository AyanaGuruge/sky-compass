"""
allsky_overlay.py

What the Turun Ursa all sky archive is good for, and what it is not.

The Kevola all sky camera near Turku records the whole hemisphere on a colour
sensor with no polarising optic in front of it, so its frames carry no
polarisation information whatsoever and the dark band can never be recovered
from them. Any attempt to extract polarisation from ordinary colour photographs
is unsound and should not be attempted.

The archive is still worth using, for three separate purposes.

    1. Independent validation of the solar model and the projection. The sun is
       visible in a clear daytime frame. Predicting where it should fall from
       turku_sun.py and the equidistant fisheye model, then showing that the
       prediction lands on the actual sun in a real photograph, validates both
       the ephemeris and the pixel to sky mapping against real imagery. This is
       a genuine experimental result and it needs no polarisation at all.

    2. Settling the handedness of an all sky image. A camera pointing at the
       zenith records the sky mirrored with respect to a map. Which way azimuth
       runs in the stored image depends on the sensor and the capture path. The
       Kevola view is described as north up with east to the left. Running this
       script with both mirror settings and seeing which one puts the marker on
       the real sun resolves the question empirically instead of by argument.

    3. An independent record of the sky condition. Frames from the same
       timestamps as a capture session document whether the sky was clear,
       hazy, or overcast, which is what the accuracy against sky condition
       section of the results chapter needs.

Usage
    python3 allsky_overlay.py --image kevola_frame.jpg --utc 2026-07-24T09:00:00
    python3 allsky_overlay.py --image kevola_frame.jpg --utc 2026-07-24T09:00:00 \\
                              --centre 640 480 --radius 460 --up-azimuth 0
    python3 allsky_overlay.py --image mycapture.png     (timestamp read from the name)

The archive lives at turunursa.fi/allsky/images/. Frames are downloaded by
hand or with wget rather than by this script, so that nothing here depends on
the layout of somebody else's web server staying the same.
"""

from __future__ import annotations

import argparse
import os
import re
from datetime import datetime, timezone

import numpy as np

from skyframe import find_disc, load_gray
from turku_sun import sun_position

TIMESTAMP_RE = re.compile(r"(\d{8})[T_-]?(\d{6})")


def parse_time(args, path):
    if args.utc:
        t = datetime.fromisoformat(args.utc.replace("Z", "+00:00"))
        return t if t.tzinfo else t.replace(tzinfo=timezone.utc)
    m = TIMESTAMP_RE.search(os.path.basename(path))
    if m:
        return datetime.strptime(m.group(1) + m.group(2),
                                 "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
    raise SystemExit("no timestamp given and none found in the filename, "
                     "pass --utc 2026-07-24T09:00:00")


def project_sun(az_deg, el_deg, cx, cy, radius, fov_deg=180.0,
                up_azimuth_deg=0.0, mirror=False):
    """Pixel position of the sun under the equidistant fisheye model."""
    theta = np.deg2rad(90.0 - el_deg)
    rho = (theta / np.deg2rad(fov_deg / 2.0)) * radius
    sign = -1.0 if mirror else 1.0
    phi = np.pi / 2.0 - sign * np.deg2rad(az_deg - up_azimuth_deg)
    col = cx + rho * np.cos(phi)
    row = cy - rho * np.sin(phi)
    return float(col), float(row)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--utc", default=None)
    ap.add_argument("--centre", nargs=2, type=float, default=None,
                    metavar=("CX", "CY"))
    ap.add_argument("--radius", type=float, default=None)
    ap.add_argument("--fov", type=float, default=180.0)
    ap.add_argument("--up-azimuth", type=float, default=0.0,
                    help="world azimuth that the top of the image points to")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    t = parse_time(args, args.image)
    az, el = sun_position(t)
    print("{}  sun azimuth {:.2f} deg from North, elevation {:.2f} deg"
          .format(t.strftime("%Y-%m-%d %H:%M UTC"), az, el))
    if el < 0:
        print("the sun is below the horizon at this time, nothing to mark")

    gray = load_gray(args.image)
    if args.centre and args.radius:
        cx, cy, radius = args.centre[0], args.centre[1], args.radius
        print("using the supplied circle: centre ({:.1f}, {:.1f}) radius {:.1f}"
              .format(cx, cy, radius))
    else:
        cx, cy, radius = find_disc(gray)
        print("estimated circle: centre ({:.1f}, {:.1f}) radius {:.1f}. "
              "Pass --centre and --radius if this looks wrong."
              .format(cx, cy, radius))

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    for ax, mirror in zip(axes, (False, True)):
        ax.imshow(gray, cmap="gray")
        col, row = project_sun(az, el, cx, cy, radius, fov_deg=args.fov,
                               up_azimuth_deg=args.up_azimuth, mirror=mirror)
        ax.plot([col], [row], marker="o", markersize=18, markerfacecolor="none",
                markeredgecolor="red", markeredgewidth=2.5)
        ax.plot([col], [row], marker="+", markersize=10, color="red")
        circle = plt.Circle((cx, cy), radius, fill=False, color="#22d3ee",
                            linewidth=1.2, linestyle="--")
        ax.add_patch(circle)
        ax.set_title("azimuth runs {} in the image"
                     .format("counter clockwise" if mirror else "clockwise"))
        ax.set_xticks([])
        ax.set_yticks([])
        print("  predicted sun pixel, {:18s} ({:.0f}, {:.0f})"
              .format("mirrored:" if mirror else "not mirrored:", col, row))

    fig.suptitle("Predicted sun position, {}, azimuth {:.1f} deg, "
                 "elevation {:.1f} deg\nthe correct handedness is the panel "
                 "where the marker sits on the real sun"
                 .format(t.strftime("%Y-%m-%d %H:%M UTC"), az, el))
    fig.tight_layout()
    out = args.out or (os.path.splitext(args.image)[0] + "_sun_overlay.png")
    fig.savefig(out, dpi=110)
    print()
    print("annotated comparison written to " + out)
    print("Whichever panel puts the marker on the sun tells you the handedness "
          "of that camera. Record it, and use the same setting for your own "
          "frames in estimate_azimuth.py.")


if __name__ == "__main__":
    main()
