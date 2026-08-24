# Exposure bracket through the dome, 31 July 2026, 13:05 UTC

Taken to answer the question in `HANDOFF_MORNING_dome_photo.md` §6.2: what exposure does the
dome need. The handoff predicted the dome would attenuate and that a **longer** exposure than
the bare-lens value of about 50 would be needed. **The opposite is true.**

## The bracket

`exposure_time_absolute` is in units of 100 microseconds. Sky statistics are taken over the
inner half radius, which is zenith angle below 45 degrees.

| exposure | mean, sky | clipped, sky | mean, disc | fitted radius | notes |
|---|---|---|---|---|---|
| 3 | 114.6 | 0.21% | 82.6 | 250.8 | outer field lost |
| 5 | 115.8 | 0.21% | 83.1 | 246.0 | outer field lost |
| **8** | **159.6** | 3.15% | 104.0 | 298.0 | gores clearly resolved |
| **12** | **189.1** | 7.88% | 123.6 | 313.5 | gores clearly resolved, brightest usable |
| 20 | 231.6 | 30.2% | 144.7 | 350.6 | sky saturating |
| 32 | 242.6 | 61.7% | 145.0 | 389.5 | gone |
| 50 | 237.9 | 75.3% | 137.3 | 459.1 | gone |
| 100 | 239.1 | 68.5% | 146.9 | 553.8 | whole sky at 255, no pattern at all |

**Recommended: `--exposure 10`**, bracketing 8 to 12. Anything at or above 20 destroys the
signal on a sky of this brightness.

## Two traps in the handoff's acceptance criteria

1. **`mean_disc` is not a useful target on this site.** The handoff asks for a mean of 120 to 180.
   The exposure-100 frame hits that (146.9) while the entire sky is clipped at 255, because
   roughly half the disc is dark trees and building and the two average out. Judge the exposure
   on the sky region only.
2. **The fitted radius is not a fixed property here.** The handoff says a correct frame fits a
   radius near 565 and that 380 means underexposure. `find_disc` thresholds at the midpoint of
   the frame's own range, so on a correctly exposed dome frame the dark outer field falls below
   threshold and the radius reads 300 or so. The true lens disc is still near 566 px. Fit the
   disc from a deliberately over-exposed frame, or hard code 566, and do not use the radius as
   an exposure check on this site.

## Azimuth-wedge profile, exposure 12

Over the 15 to 60 degree annulus, 45 degree wedges, image azimuth measured counter clockwise
from image +x. Obstructed pixels (below level 60) dropped.

| wedge | mean | fraction that is sky |
|---|---|---|
| 0-45 | 209.3 | 38% |
| 45-90 | 221.5 | 68% |
| 90-135 | 186.4 | 71% |
| 135-180 | 172.4 | 46% |
| 180-225 | 137.6 | 48% |
| 225-270 | 114.1 | 32% |
| 270-315 | 130.6 | 8% |
| 315-360 | 189.5 | 10% |

There is a clear azimuthal modulation of roughly a factor of two, and the eight gores and their
seams are plainly visible in the frames. **That already demonstrates the analyser converts sky
polarisation into recorded intensity**, which is the empirical answer to the supervisor's
question. But this profile must **not** be quoted as a measurement, for the reasons below.

## Why these frames are not the thesis figure

- **Cloud.** The sky is broken to mostly cloudy. Cloud depolarises, which is the one condition
  §7.1 already concedes leaves the instrument without a signal.
- **Obstruction.** Only about 40 per cent of the working annulus is open sky, and two wedges are
  under 10 per cent. The wedge profile above is therefore mostly a map of where the trees are,
  not of the sky polarisation.
- **No heading.** No compass reading was taken, and "front of the camera" does not identify
  which image edge points North. Heading error maps one to one onto azimuth error.
- **No control pair.** No matching bare-lens frame of the same sky was taken.

## What to redo

1. Open sky. A clear or mostly clear day, and a spot with the sky open well down towards the
   horizon, away from that building and those trees.
2. `--exposure 10`, and bracket 6, 8, 10, 12, 16 anyway, since sky brightness changes.
3. Level the lid, take a compass bearing, and write down which image edge it corresponds to.
4. The control pair: one frame through the dome, one without, seconds apart, same sky.
5. If possible three or more clearly separated times of day, for `estimate_azimuth.py calibrate`.
