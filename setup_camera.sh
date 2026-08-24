#!/usr/bin/env bash
# setup_camera.sh
#
# Inspect the camera and fix the exposure and white balance. Control names vary
# between drivers, so the script prints what the device actually offers before
# it tries to set anything. Read that list, then adjust the values below if a
# name does not match.
#
#   ./setup_camera.sh            just inspect
#   ./setup_camera.sh --apply    inspect and then apply the fixed settings
#
# Why this matters: an automatic exposure loop raises the gain when the dark
# polarisation band enters the frame, which partly erases the very signal the
# compass reads, and it changes the brightness between frames so that two
# captures are no longer comparable.

set -u
DEV="${DEV:-/dev/video0}"
EXPOSURE="${EXPOSURE:-250}"
GAIN="${GAIN:-0}"

echo "=== USB devices ==="
lsusb || true
echo
echo "=== video devices ==="
v4l2-ctl --list-devices || true
echo
echo "=== formats offered by $DEV ==="
v4l2-ctl -d "$DEV" --list-formats-ext || true
echo
echo "=== controls offered by $DEV ==="
v4l2-ctl -d "$DEV" --list-ctrls || true
echo

if [ "${1:-}" != "--apply" ]; then
  echo "Inspection only. Read the control list above, then rerun with --apply."
  exit 0
fi

echo "=== applying fixed settings ==="
# auto_exposure: 1 means manual mode on most UVC drivers, 3 means aperture
# priority, which is the automatic one. Older drivers call this
# exposure_auto instead.
v4l2-ctl -d "$DEV" -c auto_exposure=1 2>/dev/null \
  || v4l2-ctl -d "$DEV" -c exposure_auto=1 2>/dev/null \
  || echo "  could not set manual exposure mode, check the control name"

v4l2-ctl -d "$DEV" -c exposure_time_absolute="$EXPOSURE" 2>/dev/null \
  || v4l2-ctl -d "$DEV" -c exposure_absolute="$EXPOSURE" 2>/dev/null \
  || echo "  could not set the exposure time, check the control name"

v4l2-ctl -d "$DEV" -c white_balance_automatic=0 2>/dev/null \
  || v4l2-ctl -d "$DEV" -c white_balance_temperature_auto=0 2>/dev/null \
  || echo "  could not disable automatic white balance, check the control name"

v4l2-ctl -d "$DEV" -c gain="$GAIN" 2>/dev/null || true

echo
echo "=== resulting control values ==="
v4l2-ctl -d "$DEV" --list-ctrls
echo
echo "Now grab one test frame and look at it:"
echo "  python3 capture.py --out captures/test --interval 2 --frames 3"
echo
echo "If the frames are washed out, lower EXPOSURE and rerun:"
echo "  EXPOSURE=100 ./setup_camera.sh --apply"
