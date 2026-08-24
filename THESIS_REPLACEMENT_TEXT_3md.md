# Outstanding replacement text, anchored to `3.md`

Sixteen items. Everything else from `THESIS_REPLACEMENT_TEXT_draft3.docx` has already been
applied in `3.md` and is not repeated here.

Line numbers are `3.md` (3485 lines). Note that `3.md` is a text extraction of the PDF: page
headers sit inside paragraphs, words are run together, and Table 6.1's columns are scrambled.
**Use these line numbers to locate the passage, then make the edit in the source that produces
the PDF, not in `3.md` itself.**

Items 1 to 7 are cases where the thesis now contradicts itself. Do those first.

---

## 1. §3.3, the iso-contour sentence contradicts itself

**ANCHOR** lines 1467 to 1481, from "The angle of polarisation is always right angles" to the
end of the sentence beginning "The whole pattern rotates in unison with the sun".

The present text says in a single sentence that contours of constant angle of polarisation
*are* rings and that contours of the angle of polarisation are *not* rings. The first clause
should refer to the scattering angle and the degree of polarisation.

**REPLACE WITH**

> At any point in the sky the angle of polarisation lies perpendicular to the great circle
> that joins that point to the sun. Contours of constant scattering angle, and with them
> contours of constant degree of polarisation, form rings centred on the solar position, while
> the contours of the angle of polarisation itself follow the family of great circles through
> the sun and are not rings. The whole pattern rotates rigidly with the sun rather than
> changing shape, which is the property a sky compass exploits, since the orientation of the
> pattern gives the direction of the sun even when the solar disk is obscured.

---

## 2. §3.3, the second instance, never corrected

**ANCHOR** lines 1489 to 1495, from "The electric field vibrates at all times" to "as the Sun
travels through the sky."

This still says "concentric rings centered on the position of the sun" and now contradicts the
corrected sentence twenty lines above it as well as your Figure 3.2 caption.

**REPLACE WITH**

> The electric field vibrates at all times at right angles to the scattering plane, and
> contours of constant degree of polarisation are seen as rings centred on the position of the
> sun, while the contours of the angle of polarisation follow the great circles that pass
> through it. The whole pattern rotates as a rigid body but maintains the same shape as the
> Sun travels through the sky.

---

## 3. §6.2 still says the band points at the sun

**ANCHOR** lines 2438 to 2444, from "A radial dome, whose transmission axis points away" to
"directly to the quantity being estimated."

§3.3 has been corrected but §6.2 has not, so Chapters 3 and 6 currently disagree on the central
claim of the thesis.

**REPLACE WITH**

> A radial dome, whose transmission axis points away from the zenith at every azimuth, behaves
> otherwise. Along the solar meridian the electric field of the scattered light is tangential
> in the image while the transmission axis of the dome is radial, so the two stand a quarter
> turn apart and the transmitted intensity is minimised along the whole great circle that runs
> from the sun through the zenith to the antisolar point. The dark axis of the image therefore
> marks the solar meridian, which ties the most visible feature of the image directly to the
> quantity being estimated. The two ends of that axis are not equally dark, because the degree
> of polarisation is small close to the sun and largest a quarter turn away from it, with the
> consequence that the antisolar end is the deeper of the two, and it is the brightness
> asymmetry between the two ends that identifies which end holds the sun.

---

## 4. §3.3, the paste stopped one sentence early

**ANCHOR** insert after line 1620, after "the zenith to the antisolar point." and before "This
is the reason the radial dome is the target design".

As it stands §3.3 establishes that the dark axis marks the meridian but never says how the two
ends are told apart, which is what §7.1 relies on when it discusses the solar and antisolar
ambiguity.

**INSERT**

> The dark axis of the image therefore marks the solar meridian. The two ends of that axis are
> not equally dark, because the degree of polarisation is small close to the sun and largest a
> quarter turn away from it, with the consequence that the antisolar end is the deeper of the
> two. What identifies which end of the meridian holds the sun is thus the brightness asymmetry
> between the two ends rather than the position of the dark axis alone.

---

## 5. §3.1, a number that does not reproduce

**ANCHOR** line 1223, "The implementation returns 6.11◦ and 52.97◦, respectively, which
confirms its correctness to within the precision of the input constants."

`turku_sun.py` returns 6.110 and 52.986. The value 52.97 appears nowhere in the output.

**REPLACE WITH**

> The implementation returns 6.110◦ and 52.986◦ respectively, which agrees with the analytic
> values to within two thousandths of a degree and confirms its correctness to within the
> precision of the input constants.

Re-run `turku_sun.py` and quote what it prints before pasting.

---

## 6. The sample size, in four places at once

Figure 6.4 already says 200 positions while Table 6.1 and the surrounding prose still say 60.
All four must move together.

**6a. ANCHOR** lines 2402 to 2404, "The test set for evaluating the estimator in Section 6.3
was a random sample of 60 of this population."

> The test set for evaluating the estimator in Section 6.3 was a random sample of 200 of this
> population.

**6b. ANCHOR** lines 2611 to 2617, from "The estimator was evaluated on 60 solar positions" to
"The results are collected in Table 6.1."

> The estimator was evaluated on 200 solar positions drawn at random from the 5972 real
> daylight positions of Section 6.1, under six conditions formed by pairing each of the two
> optical arrangements, the single flat filter and the radial gore dome, with a clear sky,
> with thin cloud and with heavy cloud. The results are collected in Table 6.1.

**6c. ANCHOR** the Table 6.1 caption, lines 2635 to 2638.

> Table 6.1: Absolute azimuth error in degrees over 200 solar positions drawn at random from
> the 5972 real daylight positions at Turku between 14 May and 14 July 2026 with the sun at
> least five degrees above the horizon. The film axis was 35 degrees and the image up heading
> 0 degrees throughout, with sensor noise of 0.020 in all six runs.

**6d. ANCHOR** the List of Tables entry, lines 417 to 419. Make it identical to 6c.

**6e.** The table body itself, from `outputs/results_table.txt`:

| Condition | Optic | d_max | Clutter | Mean | Median | P90 | Max err. | Within 5° | Conf. | Gross |
|---|---|---|---|---|---|---|---|---|---|---|
| Clear | Flat filter | 0.75 | 0.00 | 0.078 | 0.075 | 0.138 | 0.272 | 100.0 % | 1.80 | 0 |
| Thin cloud | Flat filter | 0.45 | 0.30 | 1.020 | 0.777 | 2.188 | 4.224 | 100.0 % | 1.80 | 0 |
| Heavy cloud | Flat filter | 0.20 | 0.60 | 17.972 | 4.103 | 15.639 | 179.951 | 56.5 % | 1.75 | 15 |
| Clear | Radial dome | 0.75 | 0.00 | 0.079 | 0.075 | 0.142 | 0.269 | 100.0 % | 1.78 | 0 |
| Thin cloud | Radial dome | 0.45 | 0.30 | 5.687 | 2.120 | 8.432 | 179.911 | 75.0 % | 1.74 | 3 |
| Heavy cloud | Radial dome | 0.20 | 0.60 | 65.634 | 20.783 | 177.324 | 179.839 | 18.5 % | 1.53 | 75 |

"Gross" counts estimates in error by more than 45 degrees, out of 200. Values are copied from
`outputs/results_table.txt`; d_max and Clutter carry over unchanged from the existing table.

---

## 7. §6.3, the divergence between the two optics is not reported

**ANCHOR** insert after line 2629, at the end of §6.3's prose.

The six row table shows something the four row table could not, and the reader should be told
what it is rather than left to infer it.

**INSERT**

> Under a clear sky the two optical arrangements are indistinguishable, both recovering the
> azimuth to within a tenth of a degree, which confirms that the search, the projection
> geometry and the coordinate conventions are mutually consistent for both. As the sky
> degrades the two separate, and they separate in favour of the flat filter. Under thin cloud
> the median error of the radial dome is 2.120 degrees against 0.777 degrees, and under heavy
> cloud it is 20.783 degrees against 4.103 degrees. The median is quoted before the mean
> throughout because the error distribution in the degraded conditions is bimodal rather than
> concentrated, with the majority of frames accurate and a minority failing by close to 180
> degrees through the solar and antisolar ambiguity, so a mean describes neither population.

---

## 8. §7.1, the first limitation is now a non-sequitur

**ANCHOR** lines 2968 to 2980, from "Several limitations follow directly from the design" to
"only the captured image validation of Section 6.4 tests the latter."

The sentence that "This is a reasonable substitute" referred to was removed in the earlier
paste, so the phrase now has no antecedent. This is also the passage that prompted the
supervisor's question, and as it stands it still does not answer it.

**REPLACE WITH**

> Several limitations follow directly from the design and should be stated plainly. The first
> concerns the use of synthetic data. A photograph taken without a polarising element in the
> optical path records intensity alone and retains no information about the orientation of the
> electric field, so an archive of ordinary sky imagery cannot be used to develop or test a
> polarisation compass however large that archive is. This is a property of unfiltered
> photography rather than a limitation of the instrument, since the dome is precisely the
> element that converts the polarisation of the sky into an intensity pattern the sensor can
> record. Synthetic frames rendered at real solar positions were therefore used during
> development. This is a reasonable substitute, but it means that the simulation accuracy
> reflects the fidelity of the model rather than the behaviour of the physical dome, and only
> the captured image validation of Section 6.4 tests the latter.

---

## 9. §7.1, the confidence paragraph has a meaningless sentence

**ANCHOR** lines 3014 to 3018, "The metric as it's currently formulated, therefore, is not a
good indicator of accuracy, but of a good estimate—or a poor one. The motivation for this use
is especially significant, as the confidence level could be used to exclude unreliable
estimates".

**REPLACE WITH**

> As currently formulated the metric therefore does not separate a good estimate from a poor
> one. This matters because the confidence value is exactly what would be used to exclude
> unreliable estimates, or to decide how much weight to give the sky compass heading when it
> is merged with other navigation sensors.

If you want the supporting numbers, the frames accurate to within five degrees returned a mean
confidence of 1.773 with a standard deviation of 0.179, and the failed frames returned 1.620
with a standard deviation of 0.227, the two distributions overlapping across 61 per cent of
the range.

---

## 10. §7.1, the radial dome limitation is still missing

**ANCHOR** insert after line 3024, after the confidence paragraph.

Your own Table 6.1 shows the radial dome performing worse than the flat filter as soon as the
sky degrades, while Chapters 3, 4 and 6 all present it as the target design. The thesis should
say this before an examiner does.

**INSERT**

> A further limitation concerns the radial dome itself, and it is one that the simulation
> results identify rather than one that was anticipated. Under a clear sky the radial dome and
> the single flat filter are indistinguishable, but as the sky degrades the two separate, and
> they separate in favour of the flat filter. Under heavy cloud the median error of the radial
> dome is 20.783 degrees against 4.103 degrees for the flat filter, and the proportion of
> frames in error by more than 45 degrees rises to 75 in 200 against 15 in 200. The cause is
> the lower contrast of the pattern that the radial arrangement produces, measured at 0.79
> against 1.18 for the flat filter, which leaves the correlation search less to work with once
> the degree of polarisation falls. The radial dome remains the closer analogue of the insect
> dorsal rim area and the better match to the circular mean algorithm under a clear sky, but
> the claim that it is the superior arrangement in all conditions is not supported by these
> results.

---

## 11. §7.1, a sentence written twice

**ANCHOR** lines 3028 to 3036. The sentence "The synthetic experiments prove that the geometry,
the projection, the coordinate system and the estimation technique are consistent within the
framework of the model." is immediately followed by the same sentence rephrased, with no space
after the full stop ("model.The synthetic experiments verify the consistency of the geometry,
the projection, the coordinate system, and the estimation method within the framework of the
model.").

Delete the first of the two and keep the second.

---

## 12. §6.4 is a stub that promises results

**ANCHOR** the whole of §6.4, lines 2835 to 2843, from "This section reports the azimuth error
of the estimator on real images" to "once the capture campaign has produced a validation set."

It currently says the dome is yet to be built, which is no longer true, and it promises results
that the submitted document would not contain. §7.1 points at §6.4 twice as the only thing that
tests the physical instrument.

**REPLACE WITH**

> The simulation results of the preceding sections establish that the geometry, the search and
> the coordinate conventions are mutually consistent, but they cannot establish that the
> forward model resembles the sky. This section reports what was obtained from the physical
> instrument.
>
> The acquisition chain was verified first. The camera is recognised under the operating
> system, captures at 1600 by 1200 pixels in the YUYV format with exposure, gain and white
> balance held at the fixed values recorded in Section 5.1, and stores frames named with their
> coordinated universal time so that each frame carries the information needed to label itself
> against the ephemeris. The illuminated disc fits a radius of 566 pixels, which corresponds
> to an angular scale of 0.159 degrees per pixel across the hemisphere.
>
> Exposure through the dome was then characterised, because the polarising film attenuates and
> the working exposure could not be assumed to follow the bare lens value. A bracket was taken
> through the optic at exposure times from 0.3 to 10 milliseconds. The behaviour is sharper
> than expected. At 1.2 milliseconds the sky region has a mean level of 189 out of 255 with
> 7.9 per cent of its pixels at or above 250, and at 1.0 milliseconds a mean of 157 with 3.0
> per cent, both of which preserve the intensity gradient the estimator reads. At 2 milliseconds
> and beyond the sky saturates, and at 10 milliseconds, close to the value that suited the bare
> lens, 68.5 per cent of the sky pixels stand at or above 250 and no pattern survives at all.
> The working exposure through the dome is therefore roughly a fifth of the bare lens value
> rather than a larger multiple of it, and the exposure that renders a frame pleasant to look
> at is not the exposure that preserves the measurement.
>
> Figure 6.6 shows a frame recorded through the dome on 31 July 2026 at 13:06 coordinated
> universal time, with the sun at azimuth 228.5 degrees and elevation 40.2 degrees. The eight
> gores and the seams between them are resolved, converging on the apex of the dome, which
> establishes directly that the analyser is imaged by the camera and that its structure is
> recoverable from a single frame. Binning the field into the eight gores and taking the mean
> level over sky pixels between 90 and 300 pixels of the apex gives a variation of a factor of
> 1.8 across the dome, from 121.9 in the darkest gore to 217.7 in the brightest. The two
> darkest gores are those whose centres lie at world azimuths 23 and 68 degrees, which straddle
> the antisolar azimuth of 48.5 degrees, and the two brightest are the diametrically opposite
> pair on the solar side. This is the ordering predicted in Section 3.3, where the degree of
> polarisation is small close to the sun and largest a quarter turn from it.
>
> Three qualifications must be attached to that agreement, and they are the reason this section
> reports a consistency rather than a measurement. The sky was broken to overcast at the time
> of capture, and forward scattering through cloud produces a comparable bright toward sun
> gradient with no polarising element present at all, so the ordering alone does not isolate
> the polarisation. No matching frame of the same sky was recorded through the bare lens, so
> the pattern has not been shown to appear and disappear with the optic and nothing else. The
> camera heading was recovered from the solar glare within the frame rather than from a compass
> bearing and carries an uncertainty of roughly twenty degrees, which is half the angular width
> of a gore, so the identification of the darkest pair could shift by one gore either way.
>
> What Section 6.4 therefore establishes is that the acquisition chain works, that the working
> exposure through the dome is far shorter than the bare lens value, that the analyser and its
> eight gores are resolved in a single frame, and that the azimuthal variation of the recorded
> intensity is consistent with the forward model of Section 3.3. What it does not yet establish
> is the fidelity of that model to the sky, which requires a clear sky, a control pair recorded
> with and without the optic, and a compass bearing taken at the mount. Those three
> measurements are the immediate next step and are described in Section 7.3.

Adjust the figure number to whatever the annotated frame becomes; the file is
`Doc images/NEW_fig_6_4_dome_frame_annotated.png` and its caption is in the session notes.
Delete "and, once it is built, through the radial dome" wherever it survives.

---

## 13. Chapter 8, a broken sentence and superseded numbers

**ANCHOR** lines 3178 to 3192, from "A preliminary development tool was synthetic" to "with
just 60% of the heavy-cloud estimates within 5."

The sentence "A preliminary development tool was synthetic data was considered" has two verbs,
and the three error figures are the superseded n = 60 means.

**REPLACE WITH**

> Synthetic data was used as a preliminary development tool. The estimator was found to produce
> very small errors for the clear sky and thin cloud simulations, but its performance decreased
> significantly in the heavy cloud simulation. Over 200 solar positions the median error was
> 0.075 degrees for the clear sky through the flat filter, 0.777 degrees under thin cloud and
> 4.103 degrees under heavy cloud, with 56.5 per cent of the heavy cloud estimates falling
> within five degrees. The radial dome matched the flat filter under a clear sky and fell
> behind it as the sky degraded, reaching a median error of 20.783 degrees under heavy cloud.

---

## 14. The Figure 6.3 caption and its List of Figures entry

**ANCHOR** lines 2554 to 2559 and, identically, lines 361 to 367.

Both still carry the unqualified claim that began the whole problem.

**REPLACE WITH**

> Figure 6.3: Synthetic frames rendered through the flat filter at the true solar positions for
> 21 June 2026 at Turku. The solar azimuth and elevation used to render each frame are given
> above it and the red circle marks the resulting sun position in the image. Because a
> photograph taken without a polarising element records no polarisation information, labelled
> frames for development and testing are produced in this manner from measured solar geometry
> rather than drawn from an archive of ordinary sky imagery.

The two must match word for word.

---

## 15. §4.2, the prototype geometry paragraph

**ANCHOR** lines 1726 to 1740, from "The prototype geometry uses R = 40mm" to "These accurate
measurements were taken in order to produce a prototype that is cost-effective as proposed."

The numbers are right. The English is not: "the number number of gores", "resulting the films
standing not far from the lens that it's rim intrudes on the horizon", "the gore length about
62.83mm".

**REPLACE WITH**

> The prototype geometry uses a radius of 40 mm and eight gores, the gore count being chosen to
> match the eight sampling directions of the model. A radius of 40 mm clears the PiCam360,
> whose half diagonal is 26.9 mm, by enough that the film stands away from the lens and its rim
> does not intrude on the horizon. The resulting gores are 62.83 mm long and 31.42 mm wide at
> the base. All eight were cut from a single sheet of 200 by 150 mm film, where an earlier
> estimate had required half such a sheet for each gore, which reduces the material cost of the
> prototype substantially.

---

## 16. The abstract reports no result

**ANCHOR** lines 58 to 63, from "Hence, this work demonstrates the feasibility" to the end of
the abstract.

The abstract states the problem and the design but gives the reader no number, and it is the
first thing an examiner reads.

**REPLACE WITH**

> On synthetic frames rendered at 200 real solar positions for Turku, the estimator recovers
> the solar azimuth with a median error of 0.075 degrees under a clear sky, 0.777 degrees under
> thin cloud and 4.103 degrees under heavy cloud, the errors in the degraded conditions being
> dominated by a minority of frames that fail through the solar and antisolar ambiguity. A
> physical dome of eight polarising film gores was built and imaged, and a frame recorded
> through it resolves the eight gores and shows an azimuthal intensity variation of a factor of
> 1.8 whose minimum falls at the antisolar azimuth, as the forward model predicts. This work
> therefore demonstrates the feasibility of representing skylight polarisation as a spatial
> intensity pattern using a passive fisheye camera architecture, and identifies the practical
> requirements and limitations involved in transferring the method from an idealised model to a
> physical sensor. Validation of the forward model against a clear sky, using a control pair
> recorded with and without the polarising optic, remains the immediate next step.

If the dome frame does not make it into the submitted version, delete the second sentence and
end the abstract at "physical sensor" followed by the existing closing sentence.

---

## Order of work, if time is short

Items 1, 2, 3 and 6 remove every internal contradiction and take under an hour between them.
Item 8 answers the supervisor. Items 12 and 10 are the two places where your own data says
something the thesis does not. Everything else is repair work that can wait.
