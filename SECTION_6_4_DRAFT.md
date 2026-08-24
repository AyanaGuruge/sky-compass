# Draft Section 6.4, written from the stored captures

**Read this covering note before pasting the section into the thesis.**

## What the captures turned out to be

I measured all 32 stored frames across the seven capture sessions. The finding that shapes
this section, and that corrects what I told you earlier, is this:

**None of the stored frames is a sky-compass measurement.** Every outdoor frame was taken
with the bare fisheye lens. The polarising optic is not fitted in any of them, the optical
axis is not vertical in any of them, and the camera was hand held rather than mounted on a
levelled base. In the two 30 July frames the ground, a building, trees and the operator fill
most of the field, and the sky occupies rather less than half the disc.

When I first ran the pipeline over these frames I described them as saturated and
near-simultaneous, which was true but understated the problem. They are not frames of the sky
through a polariser at all, so the estimator output on them has no physical meaning as a
heading. Section 6.4 therefore cannot be the "captured image validation" that Chapter 7
currently promises. What it can be, and what is drafted below, is an honest report of what the
acquisition chain established and of the radiometric obstacle that stands between the present
state and a real measurement. That is a legitimate results section and it is considerably
better than an empty forward reference.

**One thing you must confirm before submitting:** I am reading the absence of the polarising
optic off the images themselves, since no session recorded which optic was fitted. If any of
these frames was in fact taken through the film or the dome, tell me and the section changes.

**A second thing to check:** `captures/2026-07-30/session.json` records
`image_up_heading_deg_from_north: 0.0`. If that is the script default rather than a compass
reading you took, it must not be presented as a measured registration. The draft below treats
it as unmeasured.

## The measurements the section rests on

Disc radius fitted by taking the largest connected region above a low threshold and computing
the minimum enclosing circle, on every frame:

| exposure regime | fitted disc radius | implied angular scale |
|---|---|---|
| correctly exposed | 563 to 580 px | 0.155 to 0.160 deg/px |
| underexposed (exposure 5 and 20) | 378 to 466 px | 0.193 to 0.238 deg/px |
| clipped, bloom around the bright sky | up to 967 px | 0.093 deg/px |

Median across all 32 frames is 566 px, which agrees with the 565 px quoted in Section 5.1.

Clipping inside the disc, and frame-to-frame repeatability:

- least clipped geometrically complete outdoor frame: 11.6 per cent of disc pixels at 250 or above
- worst: 68.9 per cent
- frames both geometrically complete and unclipped: **none** of the 31 outdoor frames
- estimator spread on two frames 10 s apart: **14.0 deg**; on two frames 11 s apart: **14.8 deg**
- true solar motion over those intervals: **0.04 deg**

---

# 6.4 Captured frames and the radiometric limit on measurement

The preceding sections establish the behaviour of the estimator against a modelled sky. This
section reports what was obtained from the camera itself. Thirty two frames were recorded
across seven sessions on 26 and 30 July 2026, all of them through the Video4Linux2 interface at
a resolution of 1600 by 1200 pixels in the YUYV format, with gain fixed at zero, white balance
fixed at 5000 K, gamma fixed at 100, and the exposure control stepped through the values 1, 5,
20, 50, 100 and 300 in order to bracket the correct setting. The solar elevation across these
sessions ranged from 26 to 40 degrees and the solar azimuth from 128 to 263 degrees, so the
frames span both a morning and an afternoon sun geometry.

The first result is that the acquisition chain works from end to end. The camera is enumerated
correctly under Ubuntu, frames are delivered at the requested resolution and pixel format, the
exposure, gain and white balance controls take effect, each frame is written with its
coordinated universal time in the filename, and every stored frame can be reopened by the
processing code, resampled into the canonical geometry, masked, and passed to the estimator
without intervention. Since the timestamp in the filename is enough to recover the true solar
azimuth and elevation from the model of Chapter 3, each frame labels itself, and the path from
a photon arriving at the sensor to a heading estimate accompanied by a ground truth value
requires no manual annotation at any stage. This is a necessary foundation for any capture
campaign and it is now in place.

The second result concerns the geometry of the illuminated disc, and it qualifies the angular
calibration of Section 5.1 in a way that matters for any future campaign. The disc was fitted
on every frame by taking the largest connected region above a low intensity threshold and
computing its minimum enclosing circle. Across all 32 frames the median fitted radius is 566
pixels, in close agreement with the 565 pixels reported in Section 5.1, but the spread around
that median is not measurement noise and is not random. On correctly exposed frames the fitted
radius lies between 563 and 580 pixels, which corresponds to an angular scale between 0.155 and
0.160 degrees per pixel. On the underexposed frames taken at exposure settings of 5 and 20 the
fitted radius falls to between 378 and 466 pixels, because the dim outer annulus of the field,
where vignetting is strongest, drops below the threshold and is lost. On the most heavily
clipped frames the fitted radius rises as far as 967 pixels, because bloom around the saturated
sky spills light into the dark surround and inflates the apparent extent of the field. The
consequence is that the scale factor relating pixel radius to sky angle cannot be recovered
from an arbitrary frame. Had the calibration been taken from the worst of the clipped frames it
would have returned 0.093 degrees per pixel instead of 0.159, understating the angular scale by
a factor of about 1.7 and introducing an error into every subsequent conversion from pixel
position to sky direction. The calibration frame must therefore be chosen for its exposure and
not merely for its availability, and the fitted radius should be checked against the value
obtained at a known good exposure before it is used.

The third result is the obstacle that prevents these frames from yielding a heading. Two
conditions must hold simultaneously for a frame to support a polarisation measurement. The
whole hemisphere must be present, so that the mapping from pixel radius to zenith angle holds
out to the horizon, and the sky region must lie below the saturation limit, so that the
intensity differences that carry the polarisation signal survive quantisation. Of the 31
outdoor frames recorded, not one satisfies both. The frames that are geometrically complete are
clipped across between 11.6 and 68.9 per cent of the disc, and the frames that are free of
clipping have lost the outer part of the field to underexposure. The single frame in the whole
set that satisfies both conditions was taken indoors, out of focus, before the manual controls
had taken effect, and shows no sky at all. The exposure latitude available from this sensor,
with the controls as they were configured, is therefore narrower than the dynamic range of a
summer sky at this latitude, where a low sun places the brightest part of the hemisphere near
the horizon in direct competition with much darker regions elsewhere in the same frame, as
noted in Section 6.1.

Two further limitations of the stored set should be recorded plainly. The polarising optic was
not fitted for any of these sessions, and the optical axis was not vertical, so the frames test
the capture chain and the lens geometry rather than the sky compass, in the same sense as the
bench frame of Figure 5.1. In the outdoor frames the camera was hand held, with the result that
vegetation occupies between 17 and 26 per cent of the disc and a building, the horizon and the
operator fill much of the remainder, leaving the usable sky confined to a wedge rather than
spread across the hemisphere. The consequence for the estimator is visible directly. Two frames
recorded 10 seconds apart return azimuths that differ by 14.0 degrees, and a second pair
recorded 11 seconds apart differ by 14.8 degrees, whereas the sun moved 0.04 degrees over each
of those intervals. A spread three orders of magnitude larger than the quantity being tracked
confirms that these frames carry no stable directional signal, which is the expected outcome
given that no polarising element was in the optical path.

For the same reason the rig calibration of Section 5.3 could not be run. That procedure fits
the heading of image up, the film axis angle in the image and the handedness of the stored
image by requiring the residual offset between the estimated and the true azimuth to be
constant across frames, and it therefore needs frames from at least three clearly separated
times of day, taken through the polarising optic on a mount that does not move between them.
The stored frames fall into two tight clusters, one in the afternoon of 26 July and one on 30
July, they were taken without the optic, and the mount was not fixed, so none of the three
conditions is met. The heading of image up recorded in the session metadata is a default value
rather than a compass reading and is not treated here as a measurement.

Taken together these results place the system at a definite and describable point. The
geometry, the search and the coordinate conventions are validated in simulation, as Section 6.3
reports. The acquisition chain, the self labelling through the coordinated universal timestamp,
the fisheye geometry and the processing path from a stored file to an estimate with a
confidence value are validated against real frames. What remains untested is the step between
them, namely whether the forward model of Chapter 3 describes the sky as it appears through the
physical dome, and that step requires frames that do not yet exist. What those frames demand is
now precisely specified rather than merely anticipated. The dome must be fitted and the optical
axis brought to vertical on a levelled base, the heading of a reference mark must be recorded
against a compass, the exposure must be set from a bracket taken through the dome rather than
through the bare lens, since the film attenuates the incoming light and shifts the working
point, and the exposure must be verified to leave the sky region below saturation while the
full disc remains present. Frames must then be collected at three or more clearly separated
times of day without disturbing the mount. None of these requirements is onerous, and each of
them is a direct consequence of a difficulty encountered and measured here rather than an
assumption carried in from the literature.
