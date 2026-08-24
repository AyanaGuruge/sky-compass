# Robot Orientation by Solar Polarization

**A bio-inspired sky-compass sensor for GNSS-denied navigation at high latitude.**

Master of Science thesis, University of Turku, Department of Computing —
Information and Communication Technology: Robotics and Autonomous Systems, July 2026.

**Author:** Ayana Kotuwegoda Guruge
**Supervisors:** Paavo Nevalainen, Jukka Heikkonen

![Frame recorded through the polarizing dome, with the eight gores and the measured per-gore levels](Doc%20images/NEW_fig_6_4_dome_frame_annotated.png)

*A real frame through the eight-gore polarizing dome, 31 July 2026. Every mark is an
overlay — no shading or contrast adjustment was applied to the image data, and the
per-gore levels on the right are measured from the unmodified pixels.*

---

## The problem

Drones and mobile robots lose GNSS underground, under dense forest canopy, and in
high-interference environments. When the fix drops they fall back on inertial dead
reckoning, which is excellent over seconds and useless over minutes — the error
accumulates until it dominates the position estimate. What is missing is an
**absolute heading reference** that does not depend on a satellite or on a magnetic
field that steel structures distort.

Bees and desert ants solved this. Their dorsal rim area reads the polarization
pattern that sunlight leaves in scattered skylight, and it gives them a solar
bearing even when the sun itself is behind cloud. This thesis asks whether that
strategy can be rebuilt cheaply, passively, and — the part that distinguishes it
from the prior literature — **at 60.45° North**.

Latitude is the whole difficulty. Over one Turku summer day the solar azimuth
sweeps roughly **290° of the compass circle** while the sun climbs to only about
**53° elevation**. Earlier sky-compass systems were built and tested nearer the
equator, where the sun passes close to the zenith and the polarization pattern is
correspondingly well-conditioned. A low, fast-moving sun is a different sensing
problem.

<img src="Other%20images/WhatsApp%20Image%202026-07-28%20at%2020.46.01.jpeg" width="480" alt="Two sheets of linear polarizing film held against blue sky at different rotations, one bright and one dark">

*The effect the sensor lives on, by hand: two sheets of the same linear polarizing
film held against clear sky at different rotations. Skylight is partially polarized,
so rotating the transmission axis changes how much of it gets through.*

## The approach

A fisheye camera looks straight up from underneath a **passive hemispherical dome
built from linear polarizing film**, cut into eight gores whose transmission axes
fan out radially from the apex.

That radial arrangement is the point. It samples the sky's polarization across the
whole visible hemisphere **in a single exposure, with no moving parts** — no
rotating filter, no mechanical chopper — which is as close as a rigid optic gets to
the fan-like angular sampling of the insect dorsal rim area. Polarization angle is
thereby converted into a **spatial intensity pattern**: a dark band across the image
whose orientation encodes the solar meridian.

Four models tie the sun's position to the pattern the dome records:

| Model | Role |
|---|---|
| NOAA solar position (after Meeus) | Ground truth azimuth and elevation for Turku |
| Equidistant fisheye projection, `r = f·θ` | Sky direction ↔ pixel |
| Malus's law | Transmission through a linear polarizer at a given axis angle |
| Rayleigh single-scattering sky | Degree and angle of polarization across the hemisphere |

The estimator is **analysis by synthesis**: sweep candidate sun azimuths around the
full circle, render the expected pattern for each, and take the candidate whose
rendering correlates best with the measured frame. Nothing is trained, so it works
from the first frame onward and there is no dataset dependency to defend.

![Processing pipeline: capture, preprocessing, estimation, validation](Doc%20images/NEW_fig_4_4_processing_pipeline.png)

## Results

Accuracy of the recovered azimuth on synthetic frames rendered at **real Turku sun
positions** — 200 positions drawn from 5 972 daylight positions (elevation ≥ 5°)
between 14 May and 14 July 2026. `gross` counts estimates wrong by more than 45°.

| condition | mean | median | p90 | max | within 5° | gross |
|---|---|---|---|---|---|---|
| flat, clear    | 0.078° | 0.075° | 0.138° | 0.272° | 100.0 % | 0 |
| flat, thin cloud | 1.020° | 0.777° | 2.188° | 4.224° | 100.0 % | 0 |
| flat, heavy cloud | 17.972° | 4.103° | 15.639° | 179.951° | 56.5 % | 15 |
| radial dome, clear | 0.079° | 0.075° | 0.142° | 0.269° | 100.0 % | 0 |
| radial dome, thin cloud | 5.687° | 2.120° | 8.432° | 179.911° | 75.0 % | 3 |
| radial dome, heavy cloud | 65.634° | 20.783° | 177.324° | 179.839° | 18.5 % | 75 |

![Median and mean absolute azimuth error by optic and sky condition, log scale](Doc%20images/NEW_fig_6_3a_error_by_condition.png)

**Read those clear-sky numbers with the caveat they deserve.** The estimator
compares a measured frame against the *same forward model* that rendered the
synthetic frame, so on clean synthetic data it recovers the azimuth to a fraction of
a degree very nearly by construction. What that demonstrates is that the search, the
projection geometry, and the coordinate conventions are correct — **not** that the
physical model matches the real sky. The degraded rows, where the assumed maximum
degree of polarization no longer matches the one used to render, are the informative
ones. The 180° failures are the expected antipodal ambiguity of a polarization
pattern that is symmetric about the solar meridian.

The gross-error column also shows the honest cost of the radial dome: it degrades
under cloud considerably faster than a single flat filter, because depolarization
attacks the between-gore contrast the radial design depends on.

### The physical dome

The dome was built (R = 40 mm, 8 gores, PiCam360 fisheye) and it does produce
resolvable gore structure on real sky. An exposure bracket taken on 31 July 2026
established the working point and overturned the prediction going in:

> The dome was expected to attenuate, and to need a **longer** exposure than the
> bare-lens value of ~50. The opposite is true. Anything at or above exposure 20
> saturates the sky and destroys the signal entirely. **The usable window is 8–12.**

That is the kind of result that only falls out of building the thing. The figure at
the top of this page is a frame from that session.

![Exposure bracket through the dome](Doc%20images/NEW_fig_5_1_exposure_bracket.png)

### What has not been demonstrated

Stated plainly, as it is in the thesis: **no stored frame is yet a complete
sky-compass measurement.** The dome resolves its gores, the acquisition chain works,
and the geometry is validated — but a end-to-end outdoor heading measurement needs a
levelled mount, a compass-registered camera heading, and a clear sky at the same
time, and that combination was not achieved within the thesis window. The
contribution is the feasibility demonstration, the working optic, the radiometric
operating point, and a calibrated pipeline ready for that campaign — not a validated
field heading. Section 6.4 reports this directly rather than dressing it up.

---

## Repository contents

### Code

| File | Purpose |
|---|---|
| `turku_sun.py` | NOAA solar position for Turku, azimuth clockwise from North. Ground truth and self-labelling. Self-tests against analytic solstice values. |
| `synthetic_sky_polarizer.py` | Rayleigh sky viewed through a linear polarizer. Flat-filter and radial-dome modes. Generates labelled datasets. |
| `skyframe.py` | Bridge from a real photograph into the generator's exact geometry — disc finding, resampling, masking, correlation. |
| `estimate_azimuth.py` | The estimator, plus the calibration that fits the three rig unknowns: heading of image-up, film axis angle, and image handedness. |
| `evaluate.py` | Accuracy against the ephemeris on synthetic frames at real sun positions, with a sensor-noise and cloud degradation model. |
| `capture.py` | Unattended interval capture with the UTC time in every filename, so each frame labels itself. |
| `liveview.py` | Live preview with focus score and saturation percentage, for aiming and focusing the lens. |
| `setup_camera.sh` | Inspects V4L2 controls and fixes exposure and white balance. |
| `allsky_overlay.py` | Projects the predicted sun onto a real Turun Ursa all-sky frame — independent validation of the ephemeris and the projection. |
| `make_figures.py` | Rebuilds the simulation figures from the models. |
| `make_fig_6_4.py` | Builds the annotated dome figure from the real 31 July frame. Measures the per-gore levels from unmodified pixels, so the caption cannot drift from the data. |

### Data, figures, hardware

- `turku_sun_positions_2026-05-14_to_2026-08-31.csv` — 11 442 daylight sun positions at 10-minute steps.
- `Doc images/` — the numbered thesis figures.
- `outputs/` — generated figures and the accuracy tables reproduced above.
- `captures/2026-07-31_dome/` — the real dome exposure bracket, with `EXPOSURE_NOTES.md`.
- `Other images/` — photographs of the film, the gores, and the assembled dome.
- `dome_build_guide_R40_picam360.html`, `dome_cutting_guide.html` — printable build and gore-cutting worksheets, including the glare test for identifying the film's transmission axis.

### Thesis documents

`Master_s_Thesis___Ayana-1.pdf` is the submitted thesis. The markdown and `.docx`
files (`3.md`, `draft2.md`, `draft3.md`, `thesis1.md`, `THESIS_*`) are the writing
iterations, kept for provenance. `RUNBOOK.md` is the original operator's runbook for
the Ubuntu rig.

---

## Running it

```bash
sudo apt install -y v4l-utils python3-pip
pip3 install numpy matplotlib pillow opencv-python
```

Reproduce the whole simulation section — no hardware, no weather dependency:

```bash
python3 turku_sun.py && python3 skyframe.py
```

```bash
python3 make_figures.py
```

```bash
python3 evaluate.py --n 200 --radial --dmax 0.45 --clutter 0.3
```

With the camera attached, see `RUNBOOK.md` for the capture, calibration and
estimation sequence.

### One convention that matters

Azimuth is **degrees clockwise from North** everywhere in this repository — North 0,
East 90, South 180, West 270. The supervisor's MATLAB model measures from South, and
the two differ by exactly 180°; `turku_sun.azimuth_south_to_north()` converts. A
mixed convention still runs and still returns a plausible number, which is precisely
why it is stated here.

---

## Citation

```
Kotuwegoda Guruge, A. (2026). Robot orientation by solar polarization.
Master of Science thesis, Department of Computing, University of Turku, Finland.
```

**Keywords:** sky compass · polarised skylight · celestial navigation · GNSS-denied
navigation · fisheye camera · bio-inspired robotics · dorsal rim area ·
high-latitude operation
