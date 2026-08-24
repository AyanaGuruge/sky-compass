"""
liveview.py

Live preview from the fisheye camera with two numbers overlaid: a focus score
and the percentage of the frame that is saturated. Use it to adjust the lens
barrel, to aim the camera, and to find a working exposure without repeatedly
capturing and opening files.

It applies the same fixed V4L2 settings that capture.py applies, so the levels
you see here are the levels capture.py will record. The geometry differs by one
step: this preview shows the raw sensor frame, which for an upward pointing
fisheye is mirrored with respect to a map, while capture.py flips each frame
left to right before writing it so that azimuth runs clockwise from North.
The preview is left mirrored on purpose, because that is the natural view to
aim and focus against while standing in front of the lens.

Usage
    python3 liveview.py                        device 4, exposure 20
    python3 liveview.py --exposure 5
    python3 liveview.py --device 4 --exposure 50 --width 1600 --height 1200

Keys, with the preview window focused
    q or Esc   quit
    + and -    step the exposure up or down
    s          save the current frame into captures/focus/
    space      print the current numbers to the terminal

Reading the numbers
    FOCUS      variance of the Laplacian. Higher is sharper. The absolute value
               is meaningless on its own; what matters is turning the barrel
               slowly and watching for the peak. Aim at something distant and
               textured, such as a tree line or a roof edge, not at flat sky,
               because flat sky has no detail for the metric to measure.
    SAT        percentage of pixels at or near maximum. Anything above about 1
               percent in the sky region means the polarisation signal is being
               clipped away. Lower the exposure until this is near zero.
    MEAN       average level over the whole frame, on a 0 to 255 scale.

Safety
    Do not leave the lens pointed at the direct solar disc, especially at a long
    exposure. Point at the blue or overcast sky away from the sun.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import datetime, timezone

import cv2
import numpy as np

CONTROLS = ["auto_exposure=1", "white_balance_automatic=0",
            "white_balance_temperature=5000", "gain=0",
            "backlight_compensation=0", "sharpness=0"]


def apply_controls(dev: str, exposure: int) -> None:
    for ctrl in CONTROLS[:1] + ["exposure_time_absolute={}".format(exposure)] + CONTROLS[1:]:
        subprocess.run(["v4l2-ctl", "-d", dev, "-c", ctrl], capture_output=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", type=int, default=4)
    ap.add_argument("--exposure", type=int, default=20)
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--height", type=int, default=1200)
    ap.add_argument("--scale", type=float, default=0.5,
                    help="preview window scale, the capture itself is full size")
    args = ap.parse_args()

    dev = "/dev/video{}".format(args.device)
    cap = cv2.VideoCapture(args.device, cv2.CAP_V4L2)
    if not cap.isOpened():
        sys.exit("could not open {}. Check v4l2-ctl --list-devices".format(dev))

    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"YUYV"))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    exposure = args.exposure
    apply_controls(dev, exposure)
    os.makedirs("captures/focus", exist_ok=True)

    print("live view running. q quits, + and - change exposure, s saves a frame.")
    print("turn the lens barrel slowly and watch FOCUS rise then fall.")

    best_focus = 0.0
    while True:
        ok, frame = cap.read()
        if not ok:
            print("frame grab failed")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        focus = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        sat = 100.0 * float((gray >= 250).mean())
        mean = float(gray.mean())
        best_focus = max(best_focus, focus)

        disp = cv2.resize(frame, None, fx=args.scale, fy=args.scale)
        lines = [
            "FOCUS {:8.1f}   best {:8.1f}".format(focus, best_focus),
            "SAT   {:8.2f} %".format(sat),
            "MEAN  {:8.1f}".format(mean),
            "EXP   {:8d}".format(exposure),
        ]
        colour = (0, 0, 255) if sat > 1.0 else (0, 255, 0)
        for i, text in enumerate(lines):
            cv2.putText(disp, text, (12, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 0, 0), 4, cv2.LINE_AA)
            cv2.putText(disp, text, (12, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, colour if i == 1 else (255, 255, 255), 2, cv2.LINE_AA)
        if sat > 1.0:
            cv2.putText(disp, "CLIPPING, lower the exposure", (12, 160),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow("PiCam360 live view", disp)
        key = cv2.waitKey(1) & 0xFF

        if key in (ord("q"), 27):
            break
        elif key in (ord("+"), ord("=")):
            exposure = min(5000, int(exposure * 1.5) + 1)
            apply_controls(dev, exposure)
            best_focus = 0.0
        elif key in (ord("-"), ord("_")):
            exposure = max(1, int(exposure / 1.5))
            apply_controls(dev, exposure)
            best_focus = 0.0
        elif key == ord("s"):
            name = "captures/focus/focus_{}_exp{}.png".format(
                datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"), exposure)
            cv2.imwrite(name, frame)
            print("saved {}  focus {:.1f}  sat {:.2f}%  mean {:.1f}".format(
                name, focus, sat, mean))
        elif key == ord(" "):
            print("focus {:.1f}  sat {:.2f}%  mean {:.1f}  exposure {}".format(
                focus, sat, mean, exposure))

    cap.release()
    cv2.destroyAllWindows()
    print()
    print("final exposure {}. Use it with capture.py:".format(exposure))
    print("  python3 capture.py --out captures/$(date +%F) --device {} "
          "--exposure {} --interval 120 --heading <COMPASS>"
          .format(args.device, exposure))


if __name__ == "__main__":
    main()
