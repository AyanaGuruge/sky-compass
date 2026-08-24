"""
capture.py

Capture sky frames on Ubuntu at a fixed interval, with the UTC time written
into every filename so that each frame labels itself through the solar model.
Automatic exposure and automatic white balance are assumed to have been turned
off already by setup_camera.sh, because an automatic gain loop will fight the
dark polarisation band and change the brightness between successive frames,
which destroys the comparison the estimator depends on.

The script is deliberately small. Start it, walk away, and go back to writing.

Usage
    python3 capture.py --out captures/2026-07-25 --interval 300 --heading 0
    python3 capture.py --out captures/test --interval 5 --frames 3   (quick check)

Orientation
    A camera pointing at the zenith records the sky mirrored with respect to a
    map. With image up pointing North the raw frame puts West on the right, so
    world azimuth runs counter clockwise in it. Frames are therefore flipped
    left to right before they are written, which puts East on the right and
    makes azimuth run clockwise, the same sense as a compass. The live view is
    deliberately left unflipped, because a mirrored preview is the natural one
    to aim and focus against while standing in front of the lens. Use
    --flip none to keep the sensor orientation instead; whatever is chosen is
    recorded in session.json so the estimator can be told which handedness the
    frames carry.

Notes
    Never leave the lens pointed at the sun with a long exposure. Use a short
    exposure, and if the sun sits high in the frame, place a small physical
    occluder over the sun disc on the dome.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--device", type=int, default=4, help="/dev/videoN index")
    ap.add_argument("--interval", type=float, default=300.0,
                    help="seconds between frames")
    ap.add_argument("--frames", type=int, default=0,
                    help="stop after this many frames, 0 means run forever")
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--height", type=int, default=1200)
    ap.add_argument("--exposure", type=int, default=100,
                    help="exposure_time_absolute in units of 100 microseconds")
    ap.add_argument("--heading", type=float, default=None,
                    help="world azimuth, degrees clockwise from North, that "
                         "the top of the image points to. Measured once with a "
                         "compass and recorded in the session metadata.")
    ap.add_argument("--flip", choices=("h", "v", "hv", "none"), default="h",
                    help="geometry applied to every frame before it is written. "
                         "h mirrors left to right, which is the default and "
                         "undoes the mirroring of an upward pointing fisheye. "
                         "v mirrors top to bottom, hv does both, which is a 180 "
                         "degree rotation, none keeps the sensor orientation.")
    ap.add_argument("--note", default="", help="free text for the session log")
    args = ap.parse_args()

    try:
        import cv2
    except ImportError:
        sys.exit("OpenCV is not installed. Run: pip install opencv-python")

    # cv2.flip codes: 1 left to right, 0 top to bottom, -1 both, which is a
    # 180 degree rotation. None means the frame is written as the sensor gives it.
    flip_code = {"h": 1, "v": 0, "hv": -1, "none": None}[args.flip]

    os.makedirs(args.out, exist_ok=True)

    cap = cv2.VideoCapture(args.device, cv2.CAP_V4L2)
    if not cap.isOpened():
        sys.exit("could not open /dev/video{}. Check v4l2-ctl --list-devices"
                 .format(args.device))
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"YUYV"))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    # V4L2 controls must be re-applied after OpenCV opens the device because
    # OpenCV re-enables the automatics on open. Order matters: disable
    # auto_exposure before writing exposure_time_absolute (inactive until then),
    # and white_balance_automatic before white_balance_temperature.
    dev = "/dev/video{}".format(args.device)
    for ctrl in [
        "auto_exposure=1",
        "exposure_time_absolute={}".format(args.exposure),
        "white_balance_automatic=0",
        "white_balance_temperature=5000",
        "gain=0",
        "backlight_compensation=0",
        "sharpness=0",
    ]:
        subprocess.run(["v4l2-ctl", "-d", dev, "--set-ctrl", ctrl],
                       capture_output=True)
    readback = subprocess.run(
        ["v4l2-ctl", "-d", dev, "--list-ctrls"],
        capture_output=True, text=True,
    )
    applied = {}
    for line in readback.stdout.splitlines():
        if any(k in line for k in ("exposure_time_absolute", "white_balance_automatic",
                                   "white_balance_temperature", "gain ", "gamma")):
            print(line)
            # parse  name (type)  : ... value=N ...
            if ":" in line:
                key, _, val = line.partition(":")
                key = key.split()[0].strip()
                if "value=" in val:
                    try:
                        applied[key] = int(val.split("value=")[1].split()[0])
                    except (ValueError, IndexError):
                        applied[key] = val.strip()
                else:
                    try:
                        applied[key] = int(val.strip())
                    except ValueError:
                        applied[key] = val.strip()
    # PNG is lossless. JPEG compression smooths exactly the gentle intensity
    # gradient the estimator reads, so it is not used here.

    meta = {
        "session_started_utc": datetime.now(timezone.utc).isoformat(),
        "device_path": dev,
        "device": args.device,
        "requested_resolution": [args.width, args.height],
        "fourcc": "YUYV",
        "exposure_time_absolute": applied.get("exposure_time_absolute", args.exposure),
        "gain": applied.get("gain", 0),
        "white_balance_temperature": applied.get("white_balance_temperature", 5000),
        "gamma": applied.get("gamma"),
        "interval_seconds": args.interval,
        "image_up_heading_deg_from_north": args.heading,
        "note": args.note,
        "azimuth_convention": "degrees clockwise from North",
        "flip": args.flip,
        "azimuth_handedness_in_image":
            "counter clockwise" if args.flip in ("none", "hv") else "clockwise",
    }
    with open(os.path.join(args.out, "session.json"), "w") as f:
        json.dump(meta, f, indent=2)

    if args.heading is None:
        print("WARNING: no heading recorded. The estimator can still fit the "
              "heading from the frames themselves, but a compass reading taken "
              "now is a useful independent check. Pass --heading next time.")

    print("capturing into {} every {:.0f} s. Press Ctrl+C to stop."
          .format(args.out, args.interval))
    print("flip {}, so world azimuth runs {} in the written frames."
          .format(args.flip, meta["azimuth_handedness_in_image"]))
    n = 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("frame grab failed, retrying in 5 s")
                time.sleep(5)
                continue
            if flip_code is not None:
                frame = cv2.flip(frame, flip_code)
            name = os.path.join(args.out, "sky_{}.png".format(utc_stamp()))
            cv2.imwrite(name, frame)
            n += 1
            mean = float(frame.mean())
            flag = ""
            if mean > 240:
                flag = "  <- close to saturation, shorten the exposure"
            elif mean < 12:
                flag = "  <- very dark, lengthen the exposure"
            print("{:4d}  {}  mean level {:6.1f}{}".format(
                n, os.path.basename(name), mean, flag))
            if args.frames and n >= args.frames:
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nstopped by user")
    finally:
        cap.release()
    print("{} frames written to {}".format(n, args.out))


if __name__ == "__main__":
    main()
