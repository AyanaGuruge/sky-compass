# skycompass — Ubuntu working set

Everything needed to run the sky polarisation compass experiment end to end.
Written for the Ubuntu machine, PiCam360 fisheye, single sheet of polarising
film. Azimuth is measured in degrees **clockwise from North** everywhere in
this folder. The supervisor's MATLAB model measures it from South, and the two
differ by exactly 180 degrees; `turku_sun.azimuth_south_to_north()` converts.

## Install, about two minutes

```bash
sudo apt install -y v4l-utils python3-pip
pip3 install numpy matplotlib pillow opencv-python
cd skycompass
python3 turku_sun.py          # should print "All checks passed."
python3 skyframe.py           # should print "self test passed."
```

If `pip3 install` complains about an externally managed environment, add
`--break-system-packages`.

## Run order

**1. Confirm the solar model.** Already done by the install check above. It
reproduces 6.110 degrees at winter solstice noon and 52.986 at summer solstice
noon, against analytic values of 6.108 and 52.988.

**2. Produce the figures and the accuracy numbers, no hardware needed.**

```bash
python3 make_figures.py
python3 evaluate.py --n 60                              # clear sky
python3 evaluate.py --n 60 --dmax 0.45 --clutter 0.3    # thin cloud
python3 evaluate.py --n 60 --dmax 0.20 --clutter 0.6    # heavy cloud
python3 evaluate.py --n 60 --radial                     # the gore dome
```

This is the whole simulation accuracy section of the results chapter, and it
runs in a few minutes whatever the weather is doing.

**3. Set up the camera.**

```bash
./setup_camera.sh                 # inspect only, read the control names
./setup_camera.sh --apply         # then fix exposure and white balance
python3 capture.py --out captures/test --interval 2 --frames 3
```

Open the three test frames. They should be a full circle of sky with black
corners, not washed out and not nearly black. If they are wrong, rerun with
`EXPOSURE=100 ./setup_camera.sh --apply` and try again.

**4. Capture.** Mount the film over the lens, level, then note with a compass
which world direction the top of the image points to.

```bash
python3 capture.py --out captures/$(date +%F) --interval 300 --heading 0
```

Leave it running. Every filename carries its UTC time, which is the label.

**5. Calibrate the rig, once, on frames from at least three clearly different
times of day.**

```bash
python3 estimate_azimuth.py calibrate --dir captures/2026-07-25
```

This fits three things that are properties of the mounting rather than of the
sky: the heading of image up, the angle of the film axis in the image, and
whether azimuth runs clockwise or counter clockwise in the stored image. A
residual spread below about 10 degrees means the geometry is consistent.

**6. Estimate and report.**

```bash
python3 estimate_azimuth.py estimate --dir captures/2026-07-25 --calib calib.json
```

Prints the estimate, the truth from the ephemeris, the error, and a confidence
value for every frame, then the summary statistics.

**7. Turun Ursa frames.** Download a clear daytime frame from
`turunursa.fi/allsky/images/` by hand, then:

```bash
python3 allsky_overlay.py --image kevola.jpg --utc 2026-07-24T09:00:00
```

## What each file is

| file | purpose |
|---|---|
| `turku_sun.py` | NOAA solar position for Turku, azimuth from North. Ground truth and self labelling. |
| `synthetic_sky_polarizer.py` | Rayleigh sky through a linear polariser, flat filter and radial dome modes. |
| `skyframe.py` | Turns a real photograph into the same geometry the generator uses. Disc finding, resampling, masking, correlation. |
| `capture.py` | Unattended interval capture with UTC filenames. |
| `setup_camera.sh` | Inspects the V4L2 controls and fixes exposure and white balance. |
| `estimate_azimuth.py` | The estimator, plus the calibration that fits heading, film axis and handedness. |
| `evaluate.py` | Accuracy against the ephemeris on synthetic frames at real sun positions. |
| `allsky_overlay.py` | Projects the predicted sun onto a real all sky frame. |
| `make_figures.py` | Rebuilds the four thesis figures. |
| `turku_sun_positions_*.csv` | 11442 daylight sun positions at ten minute steps. |

## An honesty note about the synthetic accuracy

The estimator compares a measured frame against the same forward model that
generated the synthetic frames, so on clean synthetic data it recovers the
azimuth to a fraction of a degree almost by construction. That number
demonstrates that the search, the geometry, and the coordinate conventions are
correct. It is not evidence that the physical model matches the real sky. Say
this plainly in the thesis rather than letting a reader assume otherwise. The
degraded runs, where the assumed maximum degree of polarisation no longer
matches the one used to render, are the more informative figures, and the real
frames are what settle the question.
