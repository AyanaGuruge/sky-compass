# Thesis revision plan — `thesis1.md`

> **The actual replacement prose is in `THESIS_REPLACEMENT_TEXT.md` (and `.docx`).**
> This plan tells you *what* is wrong and *why*. That file contains 19 blocks of finished thesis
> prose, about 5800 words, ready to paste, covering the abstract, §3.3, §4.1, §4.2, §5.1, §5.3,
> §5.4, §6.1, §6.2, §6.3, §7.1, §7.2, §7.3 and the whole of Chapter 8. Section 6.4 is in
> `SECTION_6_4_DRAFT.md`. Figures and their captions are in `THESIS_FIGURE_GUIDE.pdf`.
> Read this plan for the reasoning; paste from those.

Prepared 30 July 2026 against `thesis1.md` (2722 lines) and the full contents of
`polarizing_dome/`. Everything marked **verified** below was checked by running the code
or measuring the files, not inferred from the text.

Hard submission is 31 July 2026, so this is ordered by what an examiner sees first and
what costs least time, not by chapter order.

---

## 0. Answer to your direct question about Section 5.4

**Yes. Comfortably. Compute is not your constraint — writing is.**

Measured on this machine just now:

| operation | measured cost |
|---|---|
| render one synthetic frame at 128 px | **4.4 ms** |
| render one synthetic frame at 512 px | 79 ms |
| render **all 5972** real Turku sun positions at 128 px | **≈ 26 s** |
| generate a 2000-frame labelled dataset (`generate_dataset`) | **5.9 s** (verified — written to `outputs/dataset_flat/`) |
| estimate azimuth on one frame (2° sweep + 0.25° refine) | **≈ 0.56 s** |
| `evaluate.py --n 60` (one condition) | **34 s** (verified) |
| `evaluate.py --n 200` (one condition) | **≈ 108 s** (verified) |
| **the whole six-condition matrix at n = 200** | **10 min 54 s** (verified — run 30 July, results in §6.3) |

Even estimating every one of the 5972 positions is under an hour. Two hours is ample.

**Status: this has now been run.** `outputs/` contains the six `n200_*.txt` condition files,
a rebuilt `results_table.txt`, and three labelled datasets. Section 6.3 below carries the
final numbers, and §5.4 records a discrepancy the run exposed.

**So do not leave 5.4 as it stands, and do not enlarge it either.** It currently ends on
a placeholder note asking for numbers that take ten minutes to produce, and an unfilled
`NOTE, expand` block is the single most damaging thing in the draft. Fill it in with the
real counts. Concrete plan in §5.4 below.

**What is *not* achievable in the time left:** a trained learned regressor, a proper
multi-hour real capture campaign, or a calibrated real-frame error table. Section 5.3
currently promises the learned regressor ("A learned regressor trained on synthetic
images is also considered, both as an alternative estimator and as a point of
comparison"). Move that sentence to future work or an examiner will ask where the
results are.

---

## 1. Priority triage

### Tier 1 — factually wrong, must fix (≈ 90 minutes total)

1. **The dome geometry in §4.2 describes a dome you did not build.** R = 9 cm vs the
   built R = 40 mm. See §4.2 below. This is the most serious single error in the draft.
2. **The claim that the radial dome's dark band "points toward the sun" is wrong.**
   Verified numerically; it points at the *antisolar* azimuth. Appears three times
   (§3.3, §4.1, §6.2). See §6.2 below.
3. **Five citations point at the wrong reference** ([5], [3], [2], [6] used for Gkanias
   and Stürzl). See §References below.
4. **Keywords are from someone else's thesis** ("large language models, ChatGPT,
   computing education, learning analytics, object-oriented programming").
5. **Abstract is the literal string "Something here, maybe 3 paragraphs."**
6. **AI declaration still has `[Tool Name, e.g., Grammarly]` placeholders.**
7. **Chapter 8 Conclusion is empty. Appendix A is empty.**
8. **Table 2.1 says "Reported in Chapter ??"** — a broken cross-reference in the one
   table an examiner reads closely.
9. **Section 6.4 is referenced from Chapter 7 but does not exist.**

### Tier 2 — internally inconsistent, fix if time (≈ 60 minutes)

10. §6.1 quotes azimuth 35–325° and n = 5972 in the same passage; those are two different
    datasets (verified: the 5972 set spans 50–311°).
11. Figure numbering collides three ways in Chapter 4.
12. Duplicate paragraphs in Chapter 1 and §3.3.
13. §5.1 quantitative claims (mean 220, one third saturated) do not reproduce from the
    stored frames.
14. Table 6.1 has four of six cells; the missing two are already computed below.

### Tier 3 — improvements, only if Tiers 1 and 2 are done

15. Prose analysis under Table 6.1 (currently the table stands alone with no discussion).
16. Processing pipeline figure (§4.4 placeholder).
17. Exposure bracket table in §5.1 (data already exists in `captures/`).

---

## 2. Front matter

**Abstract (line 26).** Replace `Something here, maybe 3 paragraphs.` Suggested shape:
one paragraph on the problem (GNSS-denied heading, IMU drift, the insect sky compass),
one on what was built (fisheye camera under a passive radial polarising dome of eight
gores, R = 40 mm, validated against an NOAA solar model for Turku at 60.45° N), one on
results and their limits (simulation azimuth error below 0.1° clear sky rising to tens
of degrees under heavy cloud, hardware validated end to end but not yet calibrated
against a full outdoor campaign).

**Keywords (line 28).** Replace entirely. Suggested: *sky compass, polarised skylight,
celestial navigation, GNSS-denied navigation, fisheye camera, bio-inspired robotics,
dorsal rim area, high-latitude operation.*

**AI declaration (lines 56, 64).** Fill in the actual tools. You used Claude for code and
for structuring; say so. UTU's rule is disclosure, not abstinence, and a visible
`[Tool Name]` placeholder in a declaration of honesty reads badly.

**Page count (line 22).** "45 p., 1 app. p." — recount once the conclusion and appendix
are written.

---

## 3. Chapter 1, Introduction

**Delete the duplicated paragraph.** Lines 450–460 and 462–484 say the same thing twice:
"The sky compass reads the polarization pattern of scattered sunlight. This pattern is
predictable and geometrically consistent…" then "The sky compass is based on the
polarization pattern of scattered sunlight. This pattern is consistent and geometric
throughout the hemisphere…". Keep the second (it has the sunglasses analogy and the
distributed-sensing point), delete the first, and move the DRA citation [9] into the
survivor.

**Typos and grammar, line by line:**

| line | current | fix |
|---|---|---|
| 336 | "Animals use a variety of changes such as visually sited landmarks" | "a variety of cues such as visual landmarks" |
| 344 | "environemental" | "environmental" |
| 346 | "navigated from very small distances to a difference terrain" | rewrite: "navigated over distances ranging from a short walk across unfamiliar terrain to journeys of thousands of kilometres" |
| 358 | "However, Navigation without a satellite fix" | lowercase "navigation" |
| 476–478 | "from just one direction in the sky This distributed sensing" | missing full stop |
| 478 | "This distributed sensing approach will enhance" | "enhances" |

**Unsupported claim (line 528).** "Autonomous outdoor platforms in Finland experience GPS
degradation during geomagnetic storms, within certain urban building geometries, and in
the indoor to outdoor transition zones" is stated flatly with no citation. Either cite it
or soften to "are reported to experience". At 60° N the geomagnetic point is defensible
and worth keeping, but it needs a source.

---

## 4. Chapter 2, Literature Review

**Line 807:** "The table 2.3 shows the previous work" → "Table 2.1 compares the previous
work". There is no Table 2.3.

**Table 2.1, your own row (line 926):** "Reported in Chapter ??" must go. But be careful
how you fill it. Every other row in that table reports a **field-measured** accuracy;
yours would report a **simulation** figure. Putting 0.08° next to Gkanias's 5.89° RMSE
without qualification invites the obvious objection. Suggested cell text:

> Simulation only at time of writing: median absolute azimuth error 0.08° clear sky, 0.78°
> thin cloud, 4.10° heavy cloud (Table 6.1). Not directly comparable with the field results
> in the rows above.

That sentence converts a weakness into evidence that you understand your own experiment.

**References [7] and [8] are the same paper** (Wehner, *Desert ant navigation*, J. Comp.
Physiol. A 189(8), 2003). Merge them and renumber. [7] is cited at line 438 and [8] at
line 600.

**Section 2.4, lines 827–943.** You already flag that [15] and [16] are "in preparation"
and that "their bibliographic details should be confirmed against the published versions
before final submission." Do that confirmation now or drop them. Leaving a
self-acknowledged unverified citation in the final version is worse than omitting it.

---

## 5. Chapter 3, Theoretical Background

### 3.1 Solar position model

**Line 1169, garbled sentence.** "the sunrise elevation at local noon at the latitude
changes by only about 47◦" — "sunrise elevation at local noon" is not a thing. Intended
meaning: *the solar elevation at local noon varies by only about 47 degrees over the
year, from roughly 6 degrees at the winter solstice to 53 degrees at the summer
solstice.*

**Numerical inconsistency.** Line 1114 says the implementation returns "6.11◦ and 52.97◦".
`README.md` and the handoff both say 6.110 and 52.986 against analytic values of 6.108
and 52.988. The 52.97 figure appears nowhere in the code output. Re-run `python3
turku_sun.py`, quote what it actually prints, and use the same numbers in the Figure 3.1
caption (which claims agreement "within 0.01 degrees" — that holds for 52.986 vs 52.988,
but not for 52.97 vs 52.99).

**Rotation matrix (lines 1066–1094).** The extracted text shows a malformed matrix with a
first row of `1 0 0` and only two further rows. Check this renders correctly in the LaTeX
source; as extracted it is a 3×3 with a missing entry.

### 3.2 Fisheye projection

This section is sound. One optional tightening: you derive 5.22 px/deg from the
supervisor's 470 px lens, then measure 6.28 px/deg (565 px) on your own camera in §5.1,
and reconcile them as "the same order of magnitude". They differ by 20%. Consider using
the measured value as the primary figure throughout and citing 470 px only as the
historical parameter, since every number downstream depends on your lens, not the old one.

### 3.3 Sky polarization

**Wrong statement about iso-AoP contours (line 1342).** "The iso-AoP contours therefore
form concentric rings around the solar position" is incorrect. Contours of constant
*scattering angle* (and therefore of constant *degree* of polarisation) form rings around
the sun. The angle of polarisation is perpendicular to the great circle joining the point
to the sun, and its contours are not concentric rings. Your own Figure 3.2 caption gets
this right ("Dashed curves are contours of constant angular distance from the sun"), so
the text contradicts the figure. Fix to:

> Contours of constant scattering angle, and with them contours of constant degree of
> polarisation, form rings centred on the solar position, while the angle of polarisation
> at each point lies perpendicular to the great circle that joins that point to the sun.
> The whole pattern rotates rigidly as the sun moves across the sky.

**Duplicated content.** Lines 1340–1350 and 1370–1378 both explain that the e-vector is
perpendicular to the scattering plane and that the pattern rotates rigidly. Merge.

**Wrong citations.**
- Line 1441: "Gkanias et al. [5] note that the degree of polarisation and the intensity
  of skylight carry complementary information" — [5] is Steinhoff and Schiele on dead
  reckoning. Should be **[13]**.
- Line 1501: "the circular mean algorithm developed from the biological model of Gkanias
  et al. [2]" — [2] is Muheim et al. on migratory birds. Should be **[10]**.

**The band claim (lines 1486–1494).** See §6.2 below. Same correction needed here.

---

## 6. Chapter 4, System Design — the dome section

### 4.1 Optical architecture

Line 1554: "as shown in Chapter 6 it places the low transmission band of the image in a
more useful relationship to the sun." Keep the sentence but change what it claims; see
§6.2.

### 4.2 Dome geometry and fabrication — **rewrite this section**

**The geometry in the draft is not the dome you built.** The draft (lines 1596–1601)
specifies R = 9 cm, N = 8, gores 14.1 cm long and 7.1 cm wide, two gores per 20 × 15 cm
sheet. That is the old `dome_cutting_guide.html`. The dome you actually built follows
`dome_build_guide_R40_picam360.html` and `dome_cutting_guide_FINAL_CONFIRMED.pdf`:

| quantity | draft says | **built dome** |
|---|---|---|
| dome radius R | 9 cm | **40.0 mm** |
| gore count N | 8 | 8 (unchanged) |
| gore length L = πR/2 | 14.1 cm | **62.83 mm** |
| gore base width W = 2πR/N | 7.1 cm | **31.42 mm** |
| base circumference | — | **251.3 mm** |
| sheets of film needed | 4 (2 gores each) | **1 of 4** (all eight gores from one 200 × 150 mm sheet, three spare) |
| mount | "a flat ring holds the base circle open" | **octagonal box-lid mount, circumradius 40.0 mm, edge 30.61 mm, inradius 36.96 mm, eight edge slits, 8 × 28 mm tuck tabs folded 90°** |

The formulas L = πR/2 and W = 2πR/N in the draft are correct and stay. What changes is
every numerical value derived from them, plus the sheet layout and the mount description.

**The half-width taper formula should match the guide you cut from.** The draft says the
width "follows the same rule scaled by the cosine of phi". The template you actually
traced uses half-width(s) = (πR/N)·sin(s/R) with s measured from the apex, giving 15.71 ×
sin(s/40) mm. State the formula in that form and reproduce the eight-row table from the
guide (0 cm → 0.0 mm, 1 cm → 3.9 mm, 2 cm → 7.5 mm, 3 cm → 10.7 mm, 4 cm → 13.2 mm,
5 cm → 14.9 mm, 6 cm → 15.7 mm, 6.28 cm → 15.7 mm). It is a good concrete table and it
makes the fabrication reproducible, which is what a methods chapter is for.

**The axis determination paragraph is wrong and undersells what you did.** The draft says
"the transmission axis of the film is found with a simple crossed polarizer test". What
actually happened, per `dome_cutting_guide_FINAL_CONFIRMED.pdf` and the photographs, is
better and should be written up properly:

> The transmission axis of the film cannot be identified from a crossed polariser test
> alone, because that test locates the axis but leaves a ninety degree ambiguity between
> the pass axis and the block axis, and a dome built on the wrong branch of that ambiguity
> would be optically inverted. The axis was therefore fixed by three independent
> observations that agree with one another. Glare reflected from a horizontal surface at a
> shallow angle was viewed through the film and the film rotated until the glare was
> dimmest, the film was held against an LCD display whose own polarisation is known, and a
> pair of polarising sunglasses with a known vertical axis was used as a cross check. All
> three go dark with the sheet in landscape orientation, which places the transmission
> axis parallel to the long two hundred millimetre edge of the sheet. Each gore was then
> cut with its long dimension, apex to base, lying along that edge, so that in the
> assembled dome the transmission axes fan outward from the apex.

You have photographs of all three tests (`Doc images/WhatsApp Image 2026-07-29 at
12.37.23.jpeg` outdoor sky, `19.36.46.jpeg` laptop display, `Other images/WhatsApp Image
2026-07-28 at 20.46.01.jpeg` and `20.46.02.jpeg` the crossed pair). One of these should
become a figure; the crossed-pair photo showing one half bright and one half dark is the
clearest.

**Fill in the measured values.** The `NOTE, expand` at lines 1603–1617 asks for the
as-built measurements, and the confirmed cutting guide has explicit blanks for them:

- measured dome radius after the gores were cut and joined: ______ mm (design 40.0 mm)
- measured octagon lid circumradius after cutting: ______ mm (design 40.0 mm)
- date and time of the sunglasses confirmation test: ______

Measure the physical dome with a ruler and write the two numbers in. Then add one sentence
of the form *the assembled dome measured X mm in radius against a design value of 40.0 mm,
a difference of Y mm, which corresponds to an angular error of Z degrees at the horizon.*
That single sentence is what turns a craft project into an experiment.

**Be honest about the mount.** It is a shipping box lid with slits cut in it. Say that.
The draft's "a flat ring holds the base circle open and gives the dome a stable surface for
mounting over the lens" describes a machined part you do not have. A cardboard lid, levelled
with a phone level and marked for North with a compass, is a legitimate prototype mount and
saying so plainly is stronger than an aspirational description an examiner might see through
in the photograph.

**Figure numbering collision.** Three figures currently compete for two numbers:

- Caption at line 1611 is "Figure 4.1: Image of constructed dome"
- Inline placeholder at line 1619 says "[ Figure 4.1: gore template, sheet layout, and assembled hemisphere ]"
- Caption at line 1647 is "Figure 4.2: gore template, sheet layout, and assembled hemisphere"
- Caption at line 1650 is "Figure 4.3: Final Dome Construction Prototype"
- Inline placeholder at line 1706 says "[ Figure 4.2: processing pipeline ]"

Proposed clean set: **4.1** gore template and sheet layout from the cutting guide, **4.2**
the film axis confirmation photograph, **4.3** the assembled dome on its octagonal mount,
**4.4** the mounted rig outdoors, **4.5** the processing pipeline diagram. Renumber the
in-text references accordingly.

### 4.3 Camera and mount

- Line 1658: "PiCam 360" → "PiCam360" (consistent with reference [31]).
- Line 1662: "computer vison" → "computer vision".
- Add the concrete device facts you have: `/dev/video4`, 1600 × 1200, YUYV 4:2:2 packed.
- Reference [31] is a bare URL with no title. Give it one.

### 4.4 Processing pipeline

The four-stage prose description is good. The figure is still a placeholder. A four-box
diagram (capture → preprocessing → estimation → validation) with the inputs and outputs
labelled takes ten minutes in any drawing tool and fills a visible hole.

---

## 7. Chapter 5, Methods

### 5.1 Camera configuration — fill the NOTE with real values

You have them in `captures/*/session.json` (verified):

| control | value used |
|---|---|
| device | `/dev/video4` |
| resolution | 1600 × 1200 |
| pixel format | YUYV |
| `exposure_time_absolute` | 100 for the bench test, 300 for the 30 July session, bracketed at 1, 5, 20 and 50 |
| `gain` | 0 |
| `white_balance_temperature` | 5000 K, automatic white balance off |
| `gamma` | 100 |
| auto exposure | disabled, with a fixed number of initial frames discarded |

**State which exposure you settled on and why.** This matters because the answer from your
own data is uncomfortable: at 300 the frames saturate badly.

**Add the exposure bracket as a table — you already have the data and it is a real
result.** Measured from the stored frames (verified):

| `exposure_time_absolute` | mean level | fraction ≥ 250 |
|---|---|---|
| 1 | 174.7 | 56.4 % |
| 5 | 24.8 | 0.0 % |
| 20 | 24.8 | 0.0 % |
| 50 | 55.8 | 9.9 % |
| 300 | 187.7 | 59.6 % |

Two things to note in the prose. First, 5 and 20 give identical levels, which means the
driver quantises or clamps the control at the short end rather than honouring every value,
and that is worth one sentence because it constrains how finely exposure can be tuned.
Second, the value 1 gives a *brighter* frame than 5 or 20, which is the first-frame
artefact you already describe: that bracket ran as a separate short session and the frame
was captured before the manual settings took effect. It is the same effect, and pointing at
it with numbers is much stronger than describing it in words.

**Quantitative claims that do not reproduce (lines 1854–1858).** The draft states the sky
region of Figure 5.1 has "an average intensity of 220 and about 1/3 of the sky pixels being
250 or higher". Measuring the frame at 26 July 15:17 UTC inside the illuminated disc I get a
mean of 158.5 and 27.6 % of pixels at 250 or above. The one-third figure is close; the mean
is not. Either state exactly which region you measured (the whole disc, the upper half, a
manually drawn sky mask) or re-measure and quote the new numbers. An examiner who tries to
reproduce a number and cannot will doubt the ones they cannot check.

**Line 1900, ambiguous number.** "the difference in intensity between frames taken 3 seconds
apart was about 2.6" — 2.6 what? Say "a factor of about 2.6". From your files the clearest
instance is the 26 July bench pair, where the mean level fell from 152.0 to 68.3 across two
seconds, a factor of 2.2. Quote both means rather than the ratio alone.

**Disc radius.** The caption claims "approximately 565 pixels". My crude threshold estimate
on the same frame gives roughly 600. Since the whole angular scale of §5.1 hangs on this
number, measure it once carefully (fit a circle to the disc edge rather than thresholding)
and state the method in one clause.

### 5.2 Retitle this section

It is called "Sun detection and pixel to azimuth mapping" and its first sentence is "The sun
is not found by looking for its disk." Retitle to **"Pixel to sky direction mapping and
heading convention"**. The content is right; the title contradicts it.

### 5.3 Orientation estimation

**Define the confidence metric explicitly.** The draft says only "the sharpness of the
correlation peak provides a measure of confidence". The implementation is precise and should
be stated: the confidence is the height of the correlation peak above the mean of the
correlation curve, expressed in units of the standard deviation of that curve. This matters
because Chapter 7 then criticises this metric, and you cannot criticise a quantity you never
defined.

**State the search resolution.** Coarse sweep at 2° over the full circle, then a local
refinement at 0.25° within ±2° of the coarse peak.

**Move the "true by construction" caveat here.** It currently lives only in Chapter 7 and in
`README.md`. The estimator inverts the same forward model that renders the synthetic frames.
Saying this in the methods, where the reader first meets the estimator, is what makes the
Chapter 6 numbers credible rather than suspicious. Suggested placement, after the
correlation description:

> Because the estimator renders its candidate patterns with the same forward model that
> generates the synthetic test frames, the accuracy reported on clean synthetic data is in
> part true by construction. What that accuracy establishes is that the search, the
> projection geometry and the coordinate conventions are mutually consistent, which is a
> necessary condition and not a sufficient one. The degraded conditions, in which the
> assumed maximum degree of polarisation no longer matches the value used to render the
> frame, and the captured frames of Section 6.4 are what test the model against something
> other than itself.

**Drop or defer the learned regressor.** Lines 1984–1992 promise a learned regressor as an
alternative estimator and a point of comparison. There is no time to train one and no results
section for it. Move the sentence to §7.3 future work.

### 5.4 Synthetic data generation — what to write

The physics and the justification in this section are already good and should stay. What is
missing is the paragraph the `NOTE` at line 2032 asks for. **The datasets have now been
generated**, but generating them exposed a problem with the section as written.

### The claim in 5.4 does not match what `generate_dataset()` does — verified

Lines 2016–2030 state:

> The sun positions used to drive the generator are not chosen arbitrarily. They are taken
> from the real record of the sun over Turku across the two months leading up to the capture
> campaign, sampled at ten minute steps through the daylight hours…

That is true of `evaluate.py`, which draws its test positions from `generate_history()`. It is
**not** true of `generate_dataset()` in `synthetic_sky_polarizer.py`, which samples azimuth and
elevation independently and uniformly from `az_range=(0.0, 360.0)` and `el_range`. Running it
confirms this: the resulting labels span azimuth 0.1° to 359.8°, which includes roughly a
hundred degrees of azimuth the sun never occupies at Turku in that window.

So a dataset built the way the section describes was generated instead, drawing 2000 positions
without replacement from the 5972 real daylight records and keeping the UTC timestamp as a
label column:

| dataset in `outputs/` | n | azimuth range | elevation | supports the §5.4 claim? |
|---|---|---|---|---|
| `dataset_flat/` | 2000 | 0.1° – 359.8° | 5.0° – 53.0° | **no**, uniform sampling |
| `dataset_turku_flat/` | 2000 | **50.2° – 310.7°** | 5.0° – 53.0° | **yes** |
| `dataset_turku_radial/` | 2000 | **50.2° – 310.7°** | 5.0° – 53.0° | **yes**, radial optic |

Each is a `(2000, 128, 128)` float32 `images.npy` plus a `labels.csv` carrying index, UTC
timestamp, sun azimuth and sun elevation. Generation took 6.8 s per dataset.

**Use the `dataset_turku_*` pair and delete `dataset_flat`**, otherwise the claim quoted above
is unsupported. A useful consistency to point at in the prose: the 50.2° to 310.7° span of
these datasets is the same range as the 5972-position set in the corrected §6.1, because it is
drawn from exactly that set.

Optionally also fix `generate_dataset()` itself to accept a list of positions rather than
ranges, but with the deadline where it is, the standalone script that produced
`dataset_turku_*` is sufficient and the thesis need only describe what was done.

**Then state, in prose:** how many frames the dataset contains, at what pixel size, drawn
from how many real daylight sun positions over which window, the azimuth and elevation range
those positions cover, the film axis angle assumed, the maximum degree of polarisation
assumed for each sky condition, and the noise model (zero-mean Gaussian sensor noise at
σ = 0.02 plus a smooth large-scale brightness gradient standing in for cloud). Draft text:

> The generator was used to produce a labelled set of two thousand frames at a resolution of
> one hundred and twenty eight pixels square, rendered at sun positions drawn without
> replacement from the five thousand nine hundred and seventy two real daylight positions
> computed for Turku over the two month window, which span solar azimuths from fifty point two
> to three hundred and ten point seven degrees and elevations from five to fifty three degrees.
> Each frame is labelled with the coordinated universal time of the position that produced it
> together with the corresponding azimuth and elevation, so the ground truth is exact rather
> than estimated. Three sky
> conditions were rendered by varying the maximum degree of polarisation, taking zero point
> seven five for a clear sky, zero point four five for thin cloud and zero point two zero for
> heavy cloud, and each frame was then degraded with zero mean Gaussian sensor noise at a
> standard deviation of two percent of the base intensity together with a smooth large scale
> brightness gradient that stands in for the uneven illumination an overcast sky produces.
> Both optical arrangements, the single flat filter and the radial gore dome, were rendered
> under each condition, which gives the six cell design reported in Section 6.3.

Adjust the numbers to whatever you actually run. If you keep n = 60 rather than 200, say 60.

---

## 8. Chapter 6, Results

### 6.1 Sun position coverage

**Internal inconsistency, verified.** The section quotes "the solar azimuth ranges from about
35◦ to 325◦" (line 2070) and "The total number of daylight solar positions calculated over the
evaluation window is 5972" (line 2126). These describe two different sets:

| set | count | azimuth range | max elevation |
|---|---|---|---|
| elevation ≥ 0° (used for Figure 6.1) | 6740 | 35° to 325° | 53.0° |
| elevation ≥ 5° (used by `evaluate.py`, the 5972) | **5972** | **50° to 311°** | 53.0° |

Fix by stating both explicitly: the figure plots all 6740 daylight positions spanning 35° to
325°, and the estimator was tested on a random sample drawn from the 5972 positions above five
degrees elevation, which span 50° to 311°. The five degree floor is a deliberate choice (the
Rayleigh model and the horizon mask both degrade near the horizon) and saying so is better than
letting the two numbers sit side by side unexplained.

**Window mismatch.** Line 2054 calls 14 May to 14 July "the two months leading up to the capture
campaign", but the campaign ran 26 to 30 July. Either reword to "a two month window spanning
midsummer" or shift the window to 31 May – 31 July. I checked the second option: it gives
n = 5965 with identical azimuth and elevation ranges, so re-running with the corrected window
costs nothing and removes the objection. Your CSV already covers 14 May to 31 August.

### 6.2 Dome band geometry — **the claim here is wrong, verified**

The draft states in three places that the radial dome "places the band so that it points toward
the sun" (§3.3 line 1488, §4.1 line 1556, §6.2 line 2167). The `CHECK BEFORE YOU WRITE` note at
line 2215 asks you to verify this against the figure before writing. **I verified it numerically
and it is false.**

Method: render the radial dome for a given sun position, bin the image into ten degree azimuth
wedges between 0.25 and 0.95 of the disc radius, and find the darkest wedge.

| sun azimuth | antisolar azimuth | **darkest wedge, radial dome** |
|---|---|---|
| 0° | 180° | **180°** |
| 90° | 270° | **270°** |
| 135° | 315° | **310°** |
| 225° | 45° | **40°** |

Consistent across sun elevations of 10°, 30° and 50°. Mean intensity in a forty degree wedge
toward the sun versus toward the antisolar point, at elevation 30°: **0.489 solar side, 0.293
antisolar side.** The dark lobe is on the *antisolar* side.

This is physically correct and there is a clean explanation. Along the solar meridian the
scattering plane is the meridian plane, so the sky e-vector there is tangential in the image
while the radial analyser axis is radial. The two are a quarter turn apart, so transmission is
minimised along the *whole* meridian, on both the solar and the antisolar side. The two ends
differ because the degree of polarisation is low close to the sun and high a quarter turn from
it, which makes the antisolar end of the dark axis the deeper of the two.

**Suggested replacement prose for §6.2:**

> The radial arrangement does not place a dark band on the sun, and the rendering makes this
> plain. What it does is align the dark axis of the image with the solar meridian, because
> along that meridian the sky electric field vector is tangential while the transmission axis
> of the dome is radial, so the two stand a quarter turn apart and transmission is minimised
> along the whole great circle that runs from the sun through the zenith to the antisolar
> point. The two ends of that axis are not equally dark. For a sun at an azimuth of one hundred
> and thirty five degrees and an elevation of thirty degrees, the darkest ten degree azimuth
> wedge lies at three hundred and ten degrees, close to the antisolar direction, and the mean
> transmitted intensity in a wedge toward the sun is zero point four nine against zero point
> two nine in the wedge away from it. The dark axis therefore fixes the solar meridian, and it
> is the brightness asymmetry between its two ends, rather than the position of the darkest
> point, that identifies which end of the meridian holds the sun. This asymmetry is what the
> estimator uses to resolve the solar and antisolar ambiguity, and it is why that ambiguity
> reappears as a failure mode in Section 6.3 once cloud has flattened the pattern.

Note that this reads *better* than the original claim, because it explains the 180° failures in
Table 6.1 instead of leaving them unmotivated. Also correct §3.3 and §4.1 to match, and change
the docstring in `synthetic_sky_polarizer.py` line 64 and `make_figures.py` line 11, which both
still assert the old claim.

**One more measured quantity worth stating.** Pattern contrast, defined as (max − min)/mean over
the azimuth profile, is **1.18 for the flat filter and 0.79 for the radial dome**. The radial
arrangement produces a visibly flatter field, which the `NEW` note at line 2211 already observes
qualitatively. Giving the number turns an observation into evidence, and it sets up the Section
6.3 result below.

**Expand the remaining `NEW` notes** (lines 2197–2257) into prose. They are all correct: the four
lobed pinwheel comes from the factor cos(2(AoP − α)) completing two cycles per turn of the
analyser; the red marker in Figure 6.3 moves inward as elevation rises because the equidistant
projection maps zenith angle linearly to radius; the pattern rotates rigidly rather than changing
shape, which is the property the search exploits; and contrast falls as the sun climbs, which is
one reason elevation is taken from the ephemeris rather than estimated from the image.

### 6.3 Estimator accuracy — **full six-condition matrix, run at n = 200**

Table 6.1 in the draft has four of six cells at n = 60. The complete matrix has now been run at
**n = 200**, which is the version to put in the thesis. Source files: `outputs/n200_*.txt`,
summarised in `outputs/results_table.txt`.

| condition | optic | d_max | clutter | mean | median | p90 | max | within 5° | conf | gross |
|---|---|---|---|---|---|---|---|---|---|---|
| clear | flat filter | 0.75 | 0.00 | 0.078 | 0.075 | 0.138 | 0.272 | 100.0 % | 1.80 | 0 |
| thin cloud | flat filter | 0.45 | 0.30 | 1.020 | 0.777 | 2.188 | 4.224 | 100.0 % | 1.80 | 0 |
| heavy cloud | flat filter | 0.20 | 0.60 | 17.972 | 4.103 | 15.639 | 179.951 | 56.5 % | 1.75 | 15 / 200 |
| clear | radial dome | 0.75 | 0.00 | 0.079 | 0.075 | 0.142 | 0.269 | 100.0 % | 1.78 | 0 |
| thin cloud | radial dome | 0.45 | 0.30 | 5.687 | 2.120 | 8.432 | 179.911 | 75.0 % | 1.74 | 3 / 200 |
| heavy cloud | radial dome | 0.20 | 0.60 | 65.634 | 20.783 | 177.324 | 179.839 | 18.5 % | 1.53 | 75 / 200 |

n = 200 sun positions per condition, drawn from the 5972 real Turku daylight positions.
Sensor noise 0.020, film axis 35°, image up heading 0°. "Gross" counts errors above 45°.

**What changed from n = 60 to n = 200.** Five of the six cells barely moved. One moved a lot:

| condition | n = 60 mean | n = 200 mean | n = 60 median | n = 200 median |
|---|---|---|---|---|
| flat, clear | 0.075 | 0.078 | 0.073 | 0.075 |
| flat, thin | 0.984 | 1.020 | 0.671 | 0.777 |
| flat, heavy | 16.259 | 17.972 | 3.254 | 4.103 |
| radial, clear | 0.075 | 0.079 | 0.074 | 0.075 |
| **radial, thin** | **11.588** | **5.687** | 2.116 | 2.120 |
| radial, heavy | 65.395 | 65.634 | 17.232 | 20.783 |

The radial thin cloud mean halved while its median did not move at all (2.116 → 2.120). The
reason is that at n = 60 the draw happened to contain three near-180° failures, or five percent
of the sample, whereas at n = 200 there are still only three, or one and a half percent. The
mean is hostage to a handful of outliers close to 180°, so it is not a stable statistic for this
experiment at small n.

**Report the median and the gross-failure count as the primary figures, with the mean
secondary.** That is a defensible methodological choice and it is worth one sentence in §6.3,
because it also explains the otherwise baffling rows where the 90th percentile is smaller than
the mean.

**The design argument still needs addressing, though less dramatically than the n = 60 run
suggested.** Under clear sky the two optics are indistinguishable (0.078° and 0.079°). Under
cloud the radial dome is consistently worse: 5.69° against 1.02° for thin cloud, and 65.63°
against 17.97° for heavy cloud, with 75 gross failures out of 200 against the flat filter's 15.
The explanation follows from the contrast measurement in §6.2. The radial arrangement varies its
analyser orientation across the field and produces a lower contrast pattern (0.79 against 1.18),
so when cloud depolarises the sky and adds a brightness gradient, the radial dome's signal falls
below the clutter sooner and the solar and antisolar ends of the dark axis become confusable.

This is a genuinely interesting finding and it is much better to report it than to bury it. It
does not invalidate the dome: the dome samples the whole hemisphere the way the dorsal rim area
does, it needs no assumption about a single fixed film orientation, and under clear sky it
matches the flat filter exactly. But the claim that it is *robustly better* is not supported by
your own simulation, and the honest version is that the radial arrangement trades pattern
contrast for geometric fidelity to the biological design, and that under this particular cloud
model the trade goes the wrong way. Suggested closing sentence for §6.3:

> The comparison between the two optics under cloud was not the expected one. Under a clear sky
> the flat filter and the radial dome are indistinguishable, both recovering the azimuth to
> within a tenth of a degree, but as the sky degrades the radial dome loses accuracy faster,
> reaching a median error of two point one two degrees under thin cloud against zero point seven
> eight for the flat filter, and failing outright on three quarters of the frames under heavy
> cloud where the flat filter fails on rather more than half. The cause is visible in the
> renderings of Section 6.2, where the radial arrangement produces a pattern whose contrast is
> zero point seven nine against one point one eight for the flat filter. A lower contrast
> pattern carries less signal above the same clutter, so the solar and antisolar ends of the
> dark axis become confusable sooner, which is what the seventy five gross failures in the heavy
> cloud row represent against fifteen for the flat filter. This result qualifies rather than
> overturns the case for the radial dome, since the dome samples the full hemisphere without
> committing to a single film orientation and matches the flat filter exactly under a clear sky,
> but it does mean the advantage claimed for it on geometric grounds is not borne out under the
> cloud model used here.

**Also add, as prose under the table:**

- Why the 90th percentile (15.6°) is smaller than the mean (17.97°) for flat heavy cloud: the
  error distribution is bimodal, with most frames accurate and a minority failing by close to
  180°, so the mean is dragged up by outliers the percentile does not see. This is worth one
  sentence because the table looks like an arithmetic error otherwise.
- The sample-size point above: at n = 60 the radial thin cloud mean was 11.59° and at n = 200 it
  is 5.69°, while the median held at 2.12° in both. Quote the median as the primary statistic
  and say why.
- What "within 5 degrees" means and why 5° was chosen as the threshold.
- The "true by construction" caveat, cross-referenced to §5.3.

### 6.4 — this section is referenced but does not exist

Chapter 7 says "only the captured image validation of Section 6.4 tests the latter" (line 2353).
There is no Section 6.4. You have two options and I would take the first.

**Written. See `SECTION_6_4_DRAFT.md`** (1344 words, about three thesis pages, eight paragraphs,
checked against the style rules). Read the covering note in that file before pasting, because
measuring all 32 frames changed what the section could claim.

**Correction to what this plan said earlier.** I first described the stored frames as saturated
and near-simultaneous. That was true but understated. Measuring every frame shows that **none of
them is a sky-compass measurement at all**: the polarising optic is not fitted in any stored
session, the optical axis is not vertical, and the camera was hand held. The estimator output on
these frames therefore has no meaning as a heading, and §6.4 cannot be the "captured image
validation" that Chapter 7 currently promises.

What the section reports instead, all measured:

- the acquisition chain works end to end, including self-labelling from the UTC timestamp
- the fitted disc radius is **exposure dependent**: 563–580 px correctly exposed, 378–466 px
  underexposed, up to 967 px when bloom inflates it. Median across all 32 frames is 566 px,
  agreeing with the 565 px of §5.1. Calibrating on the worst frame would give 0.093 deg/px
  instead of 0.159, an error of a factor of 1.7
- **not one of the 31 outdoor frames** is both geometrically complete and unclipped; clipping
  runs 11.6 % to 68.9 % of the disc. The one frame meeting both conditions is an out-of-focus
  indoor shot with no sky in it
- estimator spread of **14.0° and 14.8°** on frame pairs 10 and 11 s apart, against true solar
  motion of 0.04°
- calibration cannot run: the frames fall into two tight clusters, were taken without the optic,
  and the mount moved

**Two things to confirm before submitting**, both flagged at the top of the draft: that the optic
really was absent from every session (I read this off the images, since no session recorded it),
and whether `image_up_heading_deg_from_north: 0.0` in the 30 July session is a compass reading or
the script default. The draft treats it as a default.

**Consequential edit in Chapter 7.** Line 2353 says "only the captured image validation of
Section 6.4 tests the latter". Since 6.4 no longer validates anything against the sky, reword to
something like: *the captured frames of Section 6.4 establish the acquisition chain and identify
the radiometric conditions a measurement requires, but the question of whether the forward model
describes the real sky remains open.*

---

## 9. Chapter 7, Discussion

**Expand the two `NEW` notes at lines 2383–2413.** Both are correct and both are now better
supported than when they were written.

**On the confidence metric:** with six conditions the case is stronger than the note claims.
Mean confidence runs **1.80, 1.80, 1.75, 1.78, 1.74, 1.53** across conditions whose mean error
runs from **0.078° to 65.6°**, a spread of nearly three orders of magnitude in error against a
fifteen percent spread in confidence. Worse for the intended purpose, the two clear-sky
conditions and the flat filter's thin cloud condition, which are perfect, share a confidence of
1.80 with nothing to separate them from heavy cloud at 1.75, where more than four frames in ten
fall outside five degrees. State the metric's definition (peak height above curve mean, in
curve standard deviations), state that it fails to separate a good estimate from a failed one,
and give a route forward: the ratio of the primary peak to the second highest local maximum
would directly measure the solar and antisolar ambiguity, which is the failure mode that
actually occurs, whereas peak height above the mean does not.

**Add the radial dome result as a limitation.** The design argument for the radial dome was
partly geometric and partly biological, and the simulation does not support the robustness claim
under cloud. Say so here as well as in §6.3.

**Wrong citations in §7.3:**
- Line 2467: "the hardware compass of Gkanias et al. [5]" — [5] is Steinhoff and Schiele. Should
  be **[13]**.
- Line 2473: "the covariance idea of Stürzl [3]" — [3] is Sobel, *Longitude*. Should be **[11]**.
- Line 2479: "the recent insect compass model of Gkanias and Webb [6]" — [6] is Thrun. Should be
  **[14]**.

**§7.2, expand the October note (line 2441).** One sentence on why the arc changes: in October
the solar declination is negative rather than near its maximum, so at Turku the sun rises later
and further south, reaches a noon elevation of roughly twenty degrees rather than fifty three,
travels a much shorter arc, and sets earlier, which compresses the azimuth range the compass
sees and pushes the whole polarisation pattern toward the horizon where the mask discards it.
Then say how you would capture it, which is the snapshot sequence plus the annual movement video
you already have in `whereIsTheSun/`.

**§7.3, expand the rain note (line 2487).** Water on the film and droplets in the air both
scatter light through many events rather than one, and multiple scattering destroys the linear
polarisation that single Rayleigh scattering produces, so rain does not merely dim the signal but
removes the quantity being measured. Frame it as the boundary of the method's operating envelope.

**Add the learned regressor here** if you remove it from §5.3.

---

## 10. Chapter 8, Conclusion — empty, must be written

Roughly one page. Structure that works: restate the question (can a low-cost fisheye under a
passive polarising dome give a usable heading at high latitude), state what was built and
validated, state the three or four headline numbers, state plainly what was not achieved
(calibrated outdoor validation, the confidence metric, the radial dome's expected robustness
advantage), and close on what the work establishes for someone continuing it.

## 11. Appendix A "Full Weekly Results" — empty

Either fill it with the per-condition output files from `outputs/acc_*.txt` and the per-frame
tables, or remove it from the contents and from the "1 app. p." on the title page. An empty
appendix listed in the table of contents is worse than no appendix.

---

## 12. References

| ref | problem | fix |
|---|---|---|
| [7] and [8] | identical paper (Wehner 2003) listed twice | merge, renumber |
| [11] | "W. Sturzl" | "W. Stürzl", and check the venue (ICCV vs an ICCV workshop) |
| [15], [16] | "in preparation" / bioRxiv, flagged as unverified in your own text | confirm against published versions or drop |
| [18] | author given as "evgkanias", GitHub handle not a name | "E. Gkanias" |
| [31] | bare URL, no title or author | give it a title, e.g. "PiCam360 equipment list" |
| in-text [2] line 1501 | should be [10] | Gkanias et al. 2019 |
| in-text [5] line 1441 | should be [13] | Gkanias et al. 2023 |
| in-text [5] line 2467 | should be [13] | Gkanias et al. 2023 |
| in-text [3] line 2473 | should be [11] | Stürzl 2017 |
| in-text [6] line 2479 | should be [14] | Gkanias and Webb 2025 |

---

## 13. Suggested order of work for the time remaining

| # | task | time | why now |
|---|---|---|---|
| 1 | Front matter: abstract, keywords, AI declaration | 40 min | first thing read, currently placeholders |
| 2 | §4.2 dome geometry rewrite with the R = 40 mm numbers | 45 min | most serious factual error |
| 3 | Fix the five wrong citations, merge [7]/[8], fix "table 2.3" and "Chapter ??" | 25 min | cheap, highly visible |
| 4 | Correct the band claim in §3.3, §4.1, §6.2 (text above is drafted) | 40 min | the draft asserts something the figure contradicts |
| 5 | ~~Run the six-condition matrix~~ **(done)**; fill Table 6.1 from the n=200 table, write the §6.3 prose | 40 min | compute is finished, only writing remains |
| 6 | Fill the §5.1 and §5.4 `NOTE` blocks with the real numbers above | 45 min | removes every remaining placeholder |
| 7 | Write §6.4 from the real captures (Option A) | 40 min | turns a simulation-only thesis into one with hardware |
| 8 | Chapter 8 conclusion | 60 min | required |
| 9 | Chapter 7 expansions, figure renumbering, appendix decision | 45 min | polish |

Items 1 to 4 are the ones that change an examiner's impression most per minute spent. If time
runs out, item 8 is not optional but items 7 and 9 are.

---

## 14. What is on disk in `outputs/` after the 30 July run

| file or directory | contents |
|---|---|
| `n200_flat_clear.txt`, `n200_flat_thin.txt`, `n200_flat_heavy.txt` | flat filter, n = 200, three sky conditions |
| `n200_radial_clear.txt`, `n200_radial_thin.txt`, `n200_radial_heavy.txt` | radial dome, n = 200, three sky conditions |
| `results_table.txt` | all six rows with mean, median, p90, max, within-5°, confidence and gross-failure count |
| `dataset_turku_flat/` | 2000 labelled frames, flat filter, real Turku positions — **use this one** |
| `dataset_turku_radial/` | 2000 labelled frames, radial dome, same positions |
| `dataset_flat/` | uniform-azimuth dataset from `generate_dataset()` — **delete, see §5.4** |
| `acc_radial_thin.txt`, `acc_radial_heavy.txt` | the earlier n = 60 radial runs, superseded by the n200 files |
| `acc_clear.txt`, `acc_thin.txt`, `acc_heavy.txt`, `acc_radial.txt` | the original 26 July n = 60 runs, superseded |

The `acc_*.txt` files are kept only because §6.3 discusses the n = 60 against n = 200 sample-size
effect. If you drop that discussion, delete them so there is one unambiguous set of numbers.

### Figures, regenerated 30 July

`make_figures.py` has been corrected and re-run. All four PNGs in `outputs/` are current:
`turku_sun_coverage.png`, `polarizer_band_demo.png`, `matched_synthetic_example.png`,
`sun_position_validation.png`. **Re-insert `polarizer_band_demo.png` into the thesis**, since the
version currently in the draft carries the false caption described below.

Three places asserted that the radial dome makes the dark band point at the sun. All three are
now fixed:

| location | was | now |
|---|---|---|
| `synthetic_sky_polarizer.py`, `radial_axis` docstring | "darkens the whole solar meridian, so the dark band always points toward the sun" | full corrected explanation, naming the antisolar end as the darker one |
| `make_figures.py`, module docstring | "showing that the radial axis makes the dark band point at the sun" | "aligns the dark axis of the image with the solar meridian… darker of its two ends is the antisolar one" |
| `make_figures.py`, **text drawn inside the figure** | "the dark band points at the sun" | "dark axis follows the solar meridian, darker at the antisolar end" |

The third was the most damaging, because the false claim was rendered into the PNG itself and is
printed in the current draft where an examiner reads it directly off the figure.

**The figure now also annotates the solar meridian.** A cyan diameter is drawn through the image
centre, solid toward the solar azimuth and dashed toward the antisolar azimuth, with the flat
filter panel carrying the legend. This was added because the corrected caption asserts that the
antisolar end is darker, and without the annotation a reader has no way to check that against the
picture, which is the same failure the draft's own `CHECK BEFORE YOU WRITE` note warned about. In
the regenerated figure the dashed antisolar line runs straight along the dark lobe of the radial
panel while the solid solar line passes through mid grey with the sun circle on it, so the claim
is now visible rather than merely stated.

Note the antisolar *point* for a sun at thirty degrees elevation sits thirty degrees below the
horizon and is therefore not in the fisheye image at all. What the dashed line marks is the
antisolar *azimuth* at the disc edge. Say that in the figure caption in the thesis; it is the
kind of distinction an examiner will test.

One incidental confirmation: `make_figures.py` prints "6740 daylight positions, azimuth 35 to
325 deg" for the coverage figure, which independently confirms the §6.1 finding that the figure
and the 5972-position evaluation set are two different populations.
