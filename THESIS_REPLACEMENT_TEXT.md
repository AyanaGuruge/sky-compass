# Replacement text, ready to paste

Every block below is finished thesis prose, written in the style of the existing draft: flowing
sentences, no lists, no dashes used as punctuation, passive voice where it suits a formal tone.
Each block states exactly what it replaces. Numbers are the measured ones from the 30 July runs.

Blocks are ordered as they appear in the thesis. Where a block says REPLACES, delete the named
passage entirely and paste this in its place. Where it says INSERT, add it at the point named.

---

## 1. Abstract

**REPLACES** the line "Something here, maybe 3 paragraphs."

> Navigation without a satellite fix remains a persistent difficulty for mobile robots, because an
> inertial measurement unit accumulates heading error over time and the alternatives each fail
> under some common condition. Many insects solve the same problem with a sky compass, reading the
> polarisation pattern of scattered sunlight through a specialised band of photoreceptors along the
> dorsal margin of the eye. That pattern is fixed geometrically to the position of the sun and
> survives partial cloud, which makes it an attractive basis for a passive heading reference that
> requires no external infrastructure and draws very little power.
>
> This thesis designs and evaluates such a compass for operation at high latitude. A low cost
> fisheye camera images the sky hemisphere through a passive dome of linear polarising film,
> assembled from eight gores of radius 40 millimetres whose transmission axes fan radially outward
> from the apex, so that the whole sky polarisation pattern is recorded in a single exposure through
> a single lens. Heading is recovered by analysis by synthesis, in which the expected intensity
> pattern is rendered for every candidate azimuth and the candidate correlating most strongly with
> the measurement is selected. Ground truth is supplied by a solar position model for Turku at
> latitude 60.45 degrees North, implemented twice from independent derivations that agree to within
> 0.01 degrees at both solstices, so that every frame labels itself through its capture time.
>
> Evaluated in simulation against 200 sun positions drawn from the real Turku daylight record, the
> estimator recovers the solar azimuth with a median absolute error of 0.08 degrees under a clear
> sky, rising to 0.78 degrees under thin cloud and 4.10 degrees under heavy cloud, where a minority
> of frames fail by close to 180 degrees through the solar and antisolar ambiguity. Two findings
> qualify the design. The radial dome, expected on geometric grounds to be the more robust of the
> two optical arrangements considered, proves indistinguishable from a single flat filter under a
> clear sky and consistently worse under cloud, because its lower pattern contrast leaves less
> signal above the same clutter. The confidence value produced alongside each estimate fails to
> separate reliable estimates from failed ones, which prevents its intended use in weighting a
> heading within a fusion filter. The acquisition chain was verified end to end against captured
> frames, and the radiometric conditions a field measurement will require are established and
> reported, but validation of the forward model against the real sky remains outstanding.

**Keywords:** sky compass, polarised skylight, celestial navigation, GNSS-denied navigation,
fisheye camera, bio-inspired robotics, dorsal rim area, high-latitude operation

---

## 2. Section 3.3, the iso-contour correction

**REPLACES** the sentence at line 1342 beginning "At any point in the sky, the Angle of
Polarisation (AoP) is perpendicular to the arc" through "as the sun moves across the sky [28]."

> At any point in the sky the angle of polarisation lies perpendicular to the great circle that
> joins that point to the sun. Contours of constant scattering angle, and with them contours of
> constant degree of polarisation, form rings centred on the solar position, while the contours of
> the angle of polarisation itself follow the family of great circles through the sun and are not
> rings. The whole pattern rotates rigidly with the sun rather than changing shape, which is the
> property a sky compass exploits, since the orientation of the pattern gives the direction of the
> sun even when the solar disk is obscured.

---

## 3. Section 3.3, the dome transmission paragraph

**REPLACES** the final paragraph of 3.3, from "The way the film axes are arranged across the dome
therefore fixes where the low transmission band falls" to the end of the section.

> The way the film axes are arranged across the dome fixes where the low transmission band falls in
> the image, and the two build options behave differently in a way that matters for estimation. A
> single flat filter with one fixed axis places its band of low transmission according to that axis
> alone, so the band sits across the sky without regard to the sun and carries no direct information
> about the solar azimuth. A dome whose axes are arranged radially behaves otherwise. Along the
> solar meridian the electric field vector of the scattered light is tangential in the image while
> the transmission axis of the dome is radial, so the two stand a quarter turn apart and the
> transmitted intensity is minimised along the whole great circle that runs from the sun through the
> zenith to the antisolar point. The dark axis of the image therefore marks the solar meridian. The
> two ends of that axis are not equally dark, because the degree of polarisation is small close to
> the sun and largest a quarter turn away from it, with the consequence that the antisolar end is
> the deeper of the two. What identifies which end of the meridian holds the sun is thus the
> brightness asymmetry between the ends rather than the position of the darkest point, and this
> asymmetry is what the estimator relies upon to resolve the solar and antisolar ambiguity. The
> behaviour was checked by rendering both cases with the polarisation model, and the result is
> reported quantitatively in Section 6.2.

---

## 4. Section 4.1, the closing sentence

**REPLACES** the sentence "The radial dome matches the fan like sampling of the insect dorsal rim
area more closely than a single flat filter, and as shown in Chapter 6 it places the low
transmission band of the image in a more useful relationship to the sun."

> The radial dome matches the fan like sampling of the insect dorsal rim area more closely than a
> single flat filter, and as shown in Chapter 6 it ties the dark axis of the image to the solar
> meridian rather than to an arbitrary fixed direction. Chapter 6 also shows that this geometric
> advantage does not carry through to performance under cloud, which is discussed in Section 7.1.

---

## 5. Section 4.2, complete replacement

**REPLACES** the whole of Section 4.2, from "The dome is modelled as a hemisphere of radius R" to
the end of the section, including the NOTE block. Figure references assume the renumbering
proposed in the figure guide.

> The dome is modelled as a hemisphere of radius R covered by N identical gores. Each gore is a
> petal whose length from the base ring to the apex at the zenith equals a quarter of the
> circumference of a great circle derived by standard circle geometry [30] and is therefore given by
>
> L = pi R / 2,
>
> while the width of each gore at the base is obtained by dividing the circumference of the
> hemispherical base by the number of gores,
>
> W = 2 pi R / N,
>
> where L is the gore length, W is the gore width at the base, R is the radius of the dome and N is
> the total number of identical gores. The width at an intermediate point follows from the same
> geometry, so that a gore measured at a distance s from the apex has a half-width of (pi R / N)
> sin(s / R), which is zero at the apex where all N gores meet and rises to half the base width at
> the base ring.
>
> The prototype was built with R equal to 40 millimetres and N equal to 8, chosen so that the dome
> clears the PiCam360 board, whose half diagonal is 26.9 millimetres, without standing so high above
> the lens that its rim intrudes on the horizon. These values give a gore length of 62.83
> millimetres and a base width of 31.42 millimetres, and therefore a base circumference of 251.3
> millimetres. All eight gores were cut from a single sheet of polarising film measuring 200 by 150
> millimetres, with three further sheets left as spares, which is a considerable saving over an
> earlier and larger design that would have consumed four sheets. The template, the sheet layout and
> the mount pattern are shown in Figure 4.1.
>
> The optical function of the dome depends entirely on each gore carrying its transmission axis at
> the intended angle, so the axis of the film was established before any material was cut. A crossed
> polariser test against a display locates the axis but leaves a ninety degree ambiguity between the
> pass axis and the block axis, and a dome built on the wrong branch of that ambiguity would be
> optically inverted while appearing correct to the eye. The axis was therefore fixed by three
> independent observations that agree with one another. Glare reflected from a horizontal surface at
> a shallow angle was viewed through the film and the film rotated until the glare was dimmest, the
> film was held against a liquid crystal display whose own polarisation is known, and a pair of
> polarising sunglasses with a known vertical axis was used as a further cross check. All three
> observations go dark with the sheet held in landscape orientation, which places the transmission
> axis parallel to the long two hundred millimetre edge. Each gore was then cut with its long
> dimension, apex to base, lying along that edge, so that in the assembled dome the transmission
> axes fan outward from the apex in the radial arrangement described in Section 4.1. Figure 4.2
> records one of these confirmation tests.
>
> The dome is carried on a mount cut from the lid of a shipping box, which is a modest arrangement
> but a reversible one, and it holds the geometry well enough for a prototype. A regular octagon of
> circumradius 40 millimetres was drawn on the lid, giving an edge length of 30.61 millimetres and
> an inradius of 36.96 millimetres, and a slit was cut along each of the eight edges. Each gore
> carries a tuck tab measuring 8 by 28 millimetres below its base line, and the tabs fold through
> ninety degrees and pass into the slits, so that the bases sit on the octagon and the tips rise to
> meet at the apex roughly forty millimetres above the lid. The long seams are taped from outside
> and the apex from inside. No adhesive is applied at the base ring, which leaves a misplaced gore
> correctable until the seams are taped. The camera board is fixed flat at the centre of the lid
> with the lens pointing up, a cable slit is cut clear of the octagon, the lid is brought level with
> a phone level, and North is marked on the rim with a compass. The assembled dome is shown in
> Figure 4.3 and the complete rig in Figure 4.4.
>
> Two dimensions were measured on the finished assembly and are recorded here so that the built
> object can be compared against its design. The assembled dome measured [INSERT MEASURED VALUE]
> millimetres in radius against a design value of 40.0 millimetres, and the octagonal mount measured
> [INSERT MEASURED VALUE] millimetres in circumradius against the same design value. A departure of
> one millimetre in the dome radius corresponds to an angular error of rather less than two degrees
> in the direction assigned to a point near the rim, which is small beside the other error sources
> identified in Chapter 6 but is recorded for completeness.

**You must fill the two bracketed values.** Measure the dome and the lid with a ruler. If you
cannot, delete the final paragraph rather than inventing numbers.

---

## 6. Section 5.1, the camera settings paragraph

**REPLACES** the NOTE block beginning "Record the exact V4L2 values you fixed".

> The settings used throughout are recorded here so that the capture is reproducible. The camera
> presents itself as device video4 and was operated at a resolution of 1600 by 1200 pixels in the
> YUYV format. Gain was fixed at zero, the white balance temperature at 5000 kelvin with automatic
> white balance disabled, and gamma at 100. The exposure control was placed under manual command and
> bracketed across the values 1, 5, 20, 50, 100 and 300 in the units the driver exposes, and a fixed
> number of frames is discarded after the controls are applied, for the reason given at the end of
> this section.

---

## 7. Section 5.1, the exposure bracket

**INSERT** after the paragraph ending "the longest exposure time that resulted in not saturating
the relevant part of the sky was chosen for the further measurements."

> The bracket is shown in Figure 5.2, and its behaviour is not the simple monotonic one that might
> be expected. Between the settings of 5 and 20 the recorded level does not change at all, which
> indicates that the driver quantises the control at the short end of its range rather than
> honouring every value, and this places a limit on how finely the exposure can be tuned. More
> striking is that the shortest setting of 1 returns a brighter frame than either of them. That
> reading is not a property of the exposure at all but an instance of the settling behaviour
> described below, since each bracket step was run as a separate short session and its first frame
> was captured before the manual controls had taken effect. The bracket therefore measures two
> things at once, and separating them requires the discard of initial frames that the acquisition
> software now performs.

---

## 8. Section 5.3, the confidence definition

**INSERT** after the sentence "The sharpness of the correlation peak provides a measure of
confidence, since a sharp and isolated peak indicates a well constrained estimate while a broad or
multiple peak indicates an ambiguous one [39]."

> That measure is defined precisely as the height of the correlation peak above the mean of the
> correlation curve, expressed in units of the standard deviation of the same curve, so that it
> reports how far the winning candidate stands above the general run of candidates rather than how
> strongly it correlates in absolute terms. The search itself proceeds in two stages, with a coarse
> sweep at two degree steps around the full circle followed by a refinement at quarter degree steps
> within two degrees of the coarse peak. Section 7.1 reports that this definition of confidence does
> not succeed in distinguishing a reliable estimate from a failed one, and proposes an alternative.

---

## 9. Section 5.3, the honesty caveat

**INSERT** at the end of Section 5.3, replacing the sentences about the learned regressor, which
move to Section 7.3.

> One property of this arrangement should be stated before any accuracy figure is reported. The
> estimator renders its candidate patterns with the same forward model that generates the synthetic
> frames of Section 5.4, so on clean synthetic data it recovers the azimuth to a fraction of a
> degree partly by construction. What such a result establishes is that the search, the projection
> geometry and the coordinate conventions are mutually consistent, which is a necessary condition
> and not a sufficient one. The degraded conditions, in which the assumed maximum degree of
> polarisation no longer matches the value used to render the frame, are the more informative
> figures, and only measurements against the real sky can settle whether the forward model resembles
> it.

---

## 10. Section 5.4, the dataset paragraph

**REPLACES** the NOTE block beginning "Once generated, state how many synthetic frames you
produced".

> Two labelled sets were produced with this generator, one for each optical arrangement. Each
> contains two thousand frames at a resolution of one hundred and twenty eight pixels square,
> rendered at sun positions drawn without replacement from the five thousand nine hundred and
> seventy two real daylight positions computed for Turku over the two month window, which span solar
> azimuths from 50.2 to 310.7 degrees and elevations from 5.0 to 53.0 degrees. Each frame is
> labelled with the coordinated universal time of the position that produced it together with the
> corresponding azimuth and elevation, so the ground truth is exact rather than estimated and the
> labelling requires no manual annotation. Three sky conditions were rendered by varying the maximum
> degree of polarisation, taking 0.75 for a clear sky, 0.45 for thin cloud and 0.20 for heavy cloud,
> and each frame was then degraded with zero mean Gaussian sensor noise at a standard deviation of
> two per cent of the base intensity together with a smooth large scale brightness gradient standing
> in for the uneven illumination an overcast sky produces. The two arrangements under the three
> conditions give the six cell design whose results are reported in Section 6.3.

---

## 11. Section 6.1, the coverage correction

**REPLACES** the paragraph beginning "The total number of daylight solar positions calculated over
the evaluation window is 5972."

> Two populations of solar positions are referred to in this chapter and it is worth separating them
> plainly. Figure 6.1 plots every position at which the sun stands at or above the horizon over the
> evaluation window, of which there are 6740, and these span azimuths from about 35 to 325 degrees.
> The estimator, however, was tested only on positions at which the sun stands at least five degrees
> above the horizon, of which there are 5972, and these span a narrower range of about 50 to 311
> degrees. The five degree floor is deliberate, since both the Rayleigh model and the horizon mask
> lose their meaning close to the horizon, where the single scattering assumption is weakest and the
> optical path through the atmosphere is longest. The test set used in Section 6.3 is a random
> sample drawn from the 5972 positions above that floor. Sampling in this way allows the evaluation
> to span a wide range of azimuths, elevations, times of day and dates rather than a few hand picked
> solar positions.

---

## 12. Section 6.2, complete replacement

**REPLACES** the whole of Section 6.2 down to the NEW note block, and the NEW note block itself.

> The geometric argument for the radial dome was tested by rendering the intensity pattern each
> build option produces for the same sun, so that any difference between them comes from the optic
> alone. Figure 6.2 shows the two cases for a sun at an azimuth of 135 degrees and an elevation of
> 30 degrees, with image up corresponding to North. Both panels display a four lobed pinwheel
> structure, which arises from the factor cos(2(AoP minus alpha)) in Malus's law, since the
> transmitted intensity completes two full cycles as the analyser angle turns once around the
> circle. The flat filter produces markedly higher contrast between its light and dark lobes, while
> the radial arrangement produces a smoother and flatter field.
>
> The rendering does not support the expectation that the radial dome places a dark band on the sun,
> and the quantitative form of the comparison is given in Figure 6.5, which reports the mean
> transmitted intensity in five degree azimuth wedges taken between a quarter and 0.95 of the disc
> radius. For the flat filter the two minima fall at about 10 and 270 degrees, positions fixed by
> the film axis and bearing no relation to the sun at 135 degrees. For the radial dome the deepest
> minimum falls at 315 degrees, which is the antisolar azimuth, with a shallower minimum toward the
> sun itself. Averaged over a forty degree wedge, the mean intensity toward the sun is 0.489 against
> 0.293 toward the antisolar point. The same behaviour was found at solar elevations of 10, 30 and
> 50 degrees and at four widely separated solar azimuths, with the deepest wedge falling at the
> antisolar azimuth in every case.
>
> The explanation follows from the geometry set out in Section 3.3. Along the solar meridian the
> electric field vector of the scattered light is tangential in the image while the transmission axis
> of the radial dome is radial, so transmission is minimised along the entire meridian and not at
> one end of it. The asymmetry between the ends arises because the degree of polarisation is small
> near the sun and largest a quarter turn from it. What the radial arrangement achieves, then, is to
> tie the dark axis of the image to the solar meridian, which fixes the solar azimuth up to a
> reflection, while the brightness difference between the two ends of that axis is what resolves the
> reflection. This is a weaker relationship than a band pointing at the sun would be, and Section
> 6.3 shows that it is also a more fragile one, since the reflection becomes hard to resolve as soon
> as cloud flattens the pattern.
>
> A measure of that fragility is available from the same renderings. Defining pattern contrast as
> the difference between the largest and smallest wedge means divided by the mean over all wedges,
> the flat filter returns 1.18 and the radial dome 0.79. The radial arrangement therefore carries
> about two thirds of the modulation depth of the flat filter, which is the price of distributing
> the analyser orientation across the field, and it is the quantity that governs how much
> degradation the pattern can absorb before the estimate fails.
>
> Figure 6.3 shows four synthetic frames rendered through the flat filter at the true solar
> positions for 21 June 2026 at Turku, corresponding to 03:00, 07:00, 11:00 and 15:00 coordinated
> universal time, at which the sun stands at azimuths of 59, 111, 190 and 262 degrees and elevations
> of 10, 38, 53 and 32 degrees respectively. The marked solar position moves clockwise around the
> image and inward toward the centre as the elevation rises, reaching its closest approach at 11:00
> when the sun is highest, then moving outward again, which is the equidistant projection of Section
> 3.2 behaving as it should. The intensity pattern rotates rigidly with the sun rather than changing
> shape, and that rigidity is the property the estimator exploits when it searches over candidate
> azimuths. The frame at 11:00 is visibly flatter than the others, since the pattern contrast falls
> as the sun climbs, which is one reason the elevation is supplied from the ephemeris rather than
> estimated from the image.

---

## 13. Section 6.3, complete replacement of the prose

**REPLACES** the two paragraphs of Section 6.3 that surround Table 6.1. The table itself is
replaced by the six row version given in the figure guide.

> This section reports the azimuth error of the estimator on synthetic frames across the full range
> of sun positions covered in Section 6.1. Because the synthetic frames carry an exact ground truth,
> the error here isolates the behaviour of the estimator from any error in capture or calibration,
> subject to the caveat recorded in Section 5.3 that the estimator inverts the same forward model
> that renders the frames.
>
> The estimator was evaluated on 200 solar positions drawn at random from the 5972 real daylight
> positions of Section 6.1, under six conditions formed by pairing each of the two optical
> arrangements with a clear sky, thin cloud and heavy cloud. Figure 6.6 summarises the outcome and
> Table 6.1 gives the full figures.
>
> The median is quoted before the mean throughout, and the reason is visible in the table wherever
> the sky is degraded. The error distribution in those conditions is bimodal rather than
> concentrated, as Figure 6.7 shows, with the great majority of frames accurate and a minority
> failing by close to 180 degrees through the solar and antisolar ambiguity. A mean computed over
> such a distribution is dominated by the failures and is unstable against the number of them a
> particular sample happens to contain. An earlier run over 60 positions returned a mean of 11.59
> degrees for the radial dome under thin cloud where the run over 200 positions returns 5.69, while
> the median moved only from 2.116 to 2.120 degrees between the same two runs. The same effect
> explains the rows in which the ninetieth percentile is smaller than the mean, which would
> otherwise look like an arithmetic error. The proportion of estimates falling within five degrees
> is reported alongside, five degrees being a threshold below which a heading remains useful for
> bounding the drift of an inertial estimate over the intervals of interest.
>
> Under a clear sky both optical arrangements recover the azimuth to within a tenth of a degree and
> are indistinguishable from one another, which confirms that the search, the projection geometry
> and the coordinate conventions are mutually consistent for both. As the sky degrades the two
> separate, and they separate in the direction opposite to the one the design argument of Chapter 4
> anticipated. Under thin cloud the flat filter returns a median error of 0.78 degrees with no
> failures at all, while the radial dome returns 2.12 degrees with three failures in 200. Under
> heavy cloud the flat filter returns 4.10 degrees with 15 failures and keeps 56.5 per cent of
> estimates within five degrees, while the radial dome returns 20.78 degrees with 75 failures and
> keeps only 18.5 per cent.
>
> The cause is the contrast measurement reported in Section 6.2. The radial arrangement produces a
> pattern whose contrast is 0.79 against 1.18 for the flat filter, so it carries less signal above
> the same clutter, and the two ends of its dark axis become confusable sooner as the degree of
> polarisation falls and the brightness gradient grows. Since it is precisely the asymmetry between
> those ends that resolves the solar and antisolar ambiguity, the failure mode that appears is the
> one the geometry predicts. This result qualifies the case for the radial dome rather than
> overturning it, since the dome samples the whole hemisphere without committing to a single film
> orientation and matches the flat filter exactly under a clear sky, but the robustness advantage
> claimed for it on geometric grounds is not borne out under the cloud model used here, and that is
> reported as a finding rather than set aside.
>
> Figure 6.8 shows the error against sun elevation for each condition. Failures under cloud are
> distributed across the elevation range rather than concentrated at low sun, which indicates that
> the difficulty lies in the depolarisation of the pattern rather than in the geometry of a low sun
> as such. It is worth recalling that at this latitude the elevation never exceeds 53 degrees, so
> the estimator is at no point tested against a sun near the zenith, a regime in which the pattern
> would be arranged quite differently around the image centre.

---

## 14. Section 7.1, the confidence limitation

**REPLACES** the first bullet of the NEW note block in Section 7.1.

> A second limitation concerns the confidence value, and it is a weakness that the experiments of
> Chapter 6 identify rather than one that was anticipated. The value is defined in Section 5.3 as
> the height of the correlation peak above the mean of the correlation curve in units of the
> standard deviation of that curve, and its purpose was twofold, namely to weight the heading
> appropriately within a fusion filter and to allow the solar and antisolar failures to be rejected
> before they reach the filter at all. Neither purpose is served by the metric as it stands. Across
> the six conditions of Table 6.1 the mean confidence takes the values 1.80, 1.80, 1.75, 1.78, 1.74
> and 1.53, a spread of about fifteen per cent, while the mean error across the same conditions runs
> from 0.078 to 65.6 degrees, a spread of nearly three orders of magnitude. Examined frame by frame
> rather than condition by condition the position is no better. Estimates falling within five
> degrees of the truth carry a mean confidence of 1.773 with a standard deviation of 0.179, and
> estimates falling further away carry 1.620 with a standard deviation of 0.227, so the two
> populations overlap across some sixty one per cent of the observed range and no threshold placed
> on the value separates them. Figure 7.1 shows both views. The near-180 degree failures in
> particular occur at every confidence value, including the highest, which is the worst possible
> behaviour for a metric intended to catch them.
>
> The reason is not difficult to see once the failure mode is understood. A frame in which the solar
> and antisolar ends of the dark axis have become confusable produces a correlation curve with two
> peaks of comparable height half a circle apart, and the winning peak of such a curve may stand
> just as far above the mean of the curve as the single peak of an unambiguous frame does. The
> quantity that would discriminate is therefore not the height of the peak above the mean but the
> ratio of the primary peak to the second highest local maximum, which measures the ambiguity
> directly. Redefining the metric in those terms is a small change to the estimator and is the first
> improvement that should be made to it, but it has not been carried out here and the confidence
> values reported in Table 6.1 should accordingly be read as a diagnostic of the correlation surface
> rather than as a usable reliability estimate.

---

## 15. Section 7.1, the radial dome limitation

**INSERT** after the block above.

> A further limitation attaches to the optical design itself. The radial dome was adopted as the
> target arrangement on the grounds that it samples the sky in the fan like manner of the insect
> dorsal rim area and ties the dark axis of the image to the solar meridian, and both of those
> properties hold. What does not hold is the expectation that these properties would make it the
> more robust of the two arrangements. Section 6.3 shows it to be indistinguishable from a single
> flat filter under a clear sky and consistently worse under cloud, for the reason that distributing
> the analyser orientation across the field reduces the contrast of the resulting pattern by about a
> third. The design remains defensible, since it requires no choice of a privileged film
> orientation and would be expected to degrade more gracefully under partial occlusion, which was
> not among the conditions tested here. It should nonetheless be said plainly that the simulation
> conducted for this thesis does not demonstrate the advantage that motivated the design, and that
> establishing whether the advantage exists under occlusion rather than under uniform
> depolarisation would require an experiment that has not been performed.

---

## 16. Section 7.2, the October paragraph

**REPLACES** the NOTE block in Section 7.2.

> The reason October offers a useful second test lies in the declination of the sun. At midsummer
> the declination stands near its maximum of 23.44 degrees north, which at the latitude of Turku
> lifts the noon sun to about 53 degrees and carries it through a very wide arc from a northeasterly
> rising to a northwesterly setting. By the middle of October the declination has turned some eight
> degrees south of the equator, so the sun rises later and considerably further south, reaches a
> noon elevation near 20 degrees rather than 53, sweeps a much narrower range of azimuths and sets
> earlier, as Figure 7.2 shows. The consequence for the compass is that the entire polarisation
> pattern is pressed toward the horizon, into the region where the analysis mask discards
> measurements and where the single scattering assumption of the Rayleigh model is least secure, so
> the October geometry tests the method where it is weakest rather than where it is strongest. The
> capture campaign envisaged for that period would follow the same procedure as the one described in
> Section 6.4, with snapshot sequences taken at three or more clearly separated times of day through
> the dome on a levelled and registered mount, supplemented by the annual movement record already
> held for the site.

---

## 17. Section 7.3, the rain paragraph

**REPLACES** the NOTE block in Section 7.3.

> The interest of collecting data during rain lies in the fact that rain does not merely attenuate
> the signal but removes the quantity being measured. Water standing on the outer surface of the
> film and droplets suspended in the air both scatter light through many successive events rather
> than the single event assumed by the Rayleigh model, and multiple scattering destroys the linear
> polarisation that single scattering produces. A rain shower therefore depolarises the sky in a way
> that no amount of exposure or gain can recover, which places a boundary on the operating envelope
> of the method rather than a penalty within it. Establishing where that boundary lies, and in
> particular how much rain is required before the heading becomes unusable, would make the dome a
> more predictable instrument in poor weather even though it cannot make it a functional one in
> heavy rain.

---

## 18. Section 7.3, the learned regressor

**INSERT** into Section 7.3, having removed the corresponding sentences from Section 5.3.

> A learned estimator remains an obvious alternative to the model based search used here. Trained on
> the labelled synthetic sets of Section 5.4 and on whatever real frames a completed campaign
> supplies, a regressor mapping an image directly to an azimuth would dispense with the explicit
> search and could be compared against the present estimator on identical data. It is worth noting
> that such a comparison would be more informative than it might appear, since a learned estimator
> trained on synthetic frames and tested on real ones would measure the gap between the forward
> model and the sky, which is the question this thesis leaves open.

---

## 19. Chapter 8, Conclusion, complete

**REPLACES** the empty Chapter 8.

> This thesis asked whether a low cost fisheye camera paired with a passive dome of polarising film,
> built to follow the geometry of the insect dorsal rim area, can produce reliable heading estimates
> for a robot operating outdoors at high latitude. The work carried out gives a partial answer, and
> the parts that are settled and the parts that remain open should be separated clearly.
>
> What has been established is the following. A solar position model for Turku was implemented twice
> from independent derivations and agrees with the analytic solstice elevations to within 0.01
> degrees at both solstices, which gives a ground truth that can be trusted and allows every frame
> to label itself through its capture time. A polarising dome of radius 40 millimetres was designed,
> cut and assembled from eight gores whose transmission axes were fixed by three independent
> observations and which fan radially outward from the apex, and the whole set was cut from a single
> sheet of film. An estimator was built that recovers the solar azimuth by rendering the expected
> pattern for every candidate heading and selecting the best correlated, and it was evaluated over
> 200 sun positions drawn from the real Turku daylight record under six combinations of optic and
> sky condition. Under a clear sky it recovers the azimuth with a median error of 0.08 degrees,
> under thin cloud 0.78 degrees through the flat filter, and under heavy cloud 4.10 degrees, with
> the failures that occur taking the characteristic form of a near reversal by 180 degrees. The
> acquisition chain from sensor through the operating system to a stored and self labelled frame was
> verified end to end against real captures, and the angular scale of the lens was measured at 0.159
> degrees per pixel from a disc radius of 566 pixels.
>
> Three findings qualify the design and are reported as results rather than as difficulties. The
> radial dome does not place a dark band on the sun, as had been supposed, but aligns the dark axis
> of the image with the solar meridian, leaving the identity of the solar end to be settled by a
> brightness asymmetry between the two ends. That asymmetry is a weaker cue than a band pointing at
> the sun would be, and the consequence appears in the accuracy figures, where the radial dome
> proves indistinguishable from a single flat filter under a clear sky and consistently worse under
> cloud, because distributing the analyser orientation across the field costs about a third of the
> pattern contrast. The confidence value produced alongside each estimate does not separate reliable
> estimates from failed ones, and since its intended use was to weight a heading within a fusion
> filter and to reject the solar and antisolar failures, neither use is available until the metric is
> redefined in terms of the ratio between the two highest peaks of the correlation curve.
>
> What remains open is the question the synthetic experiments cannot answer. The estimator inverts
> the same forward model that renders the frames it is tested on, so the accuracy reported in
> Chapter 6 demonstrates internal consistency of the geometry, the search and the coordinate
> conventions rather than fidelity to the sky. Section 6.4 reports what the captured frames
> established and what they did not. The acquisition chain works, but no frame in the set was
> recorded through the polarising optic with the axis vertical, and the exposure latitude available
> from this sensor proved narrower than the dynamic range of a summer sky at this latitude, so that
> no captured frame both shows the whole hemisphere and leaves the sky below saturation. Closing
> that gap does not require new theory or new software. It requires the dome fitted over a levelled
> and registered mount, an exposure chosen from a bracket taken through the dome rather than through
> the bare lens, and frames collected at three or more clearly separated times of day, all of which
> are specified precisely in Section 6.4 as a consequence of difficulties measured here rather than
> anticipated from the literature.
>
> The wider value of the work lies in what it establishes about operating a sky compass at 60.45
> degrees North. The sun at this latitude sweeps almost the whole azimuth circle over a summer day
> yet never climbs above 53 degrees, so the brightest region of the sky sits close to the horizon
> and competes with much darker regions in the same frame, which turns exposure selection from a
> convenience into a calibration step in its own right. The polarisation pattern the compass must
> read is correspondingly pressed toward the edge of the field, where the projection is least
> forgiving and the single scattering model least secure. These are not incidental difficulties of
> one prototype but properties of the site, and a compass intended for northern latitudes will have
> to address them whatever its optical arrangement. The design presented here, together with the
> measurements that qualify it, is offered as a starting point for that work.
