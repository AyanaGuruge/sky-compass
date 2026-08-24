Robot orientation by solar polarization
University of Turku
Department of Computing
Master of Science Thesis
Information and Communication Technology: Robotics and Autonomous Systems
July 2026
Ayana Kotuwegoda Guruge
Supervisors:
Paavo Nevalainen
Jukka Heikkonen
TheoriginalityofthisthesishasbeencheckedinaccordancewiththeUniversityofTurkuqualityassurance
systemusingtheTurnitinOriginalityCheckservice.

UNIVERSITY OF TURKU
Department of Computing
Ayana Kotuwegoda Guruge: Robot orientation by solar polarization
Master of Science Thesis, 49 p., 1 app. p.
Information and Communication Technology: Robotics and Autonomous Systems
July 2026
The main issue in navigating drones and mobile robotics is when there are discrep-
ancies in maintaining Global Navigation Satellite System (GNSS) which is mostly
in the method of Global Positioning Systems (GPS). This mostly happens when
the robots travel underground, in high signal interference areas, or even in dense
canopies such as under dense forests. Failing to provide GNSS will result in the
robots falling back to the inertial dead reckoning but this strategy works until it
gradually accumulates error readings. This will then follow up to dominate the po-
sition estimate. But it is worth mentioning that this inertial sensing is quite useful
for short-term orientation. Regardless this shows that robotic navigation strongly
require an independent absolute heading reference. There are certain animals like
bees and desert ants that have evolved to solve this obstacle by using the polariza-
tion pattern in the sky produced by the sunlight in a scattered skylight. Generally
meaning that they the sky as a celestial compass which means encoding the solar
direction even when the sun is covered in clouds. This thesis and research dives deep
whether the naturally evolved strategy can be replicated, tested and used in provid-
ing an absolute reference in an outdoor robot in a low-cost sky compass sensor that
is passive and accessible. The system is developed and evaluated for Turku, Fin-
land. The latitude of 60.45◦North, where the solar azimuth sweeps approximately
290◦ of the compass circle over a single summer day while the elevation of the sun
reaches only about 53◦. The difference was in the geographical location as the earlier
systems were tested in lower latitudes.
The proposed system was to make a sky-compass system that is bio-inspired. It
consists of images taken from a fisheye camera fixed underneath a passive hemi-
spherical dome which is made by linear polarizing films organized and connected in
a specific order. The arrangement of the transmission axes of the dome was done
radially to sample the light from the sky across the visible hemisphere with a single
exposure without any moving parts which is the closest to the replication of the
fan-like angular sampling of the insect dorsal rim area. Therefore, four models were
developed and used to relate the position of the sun and the pattern recorded by the
dome which was the solar position model, an equidistant fisheye projection model,
polariser transmission based on Malus’s Law and a Rayleigh sky polarisation model.
Hence, this work demonstrates the feasibility of representing skylight polarisation as
a spatial intensity pattern using a passive fisheye-camera architecture and identifies
the practical requirements and limitations involved in transferring this method from
an idealised model to a physical sensor. The results provide a foundation for fur-
ther outdoor validation and for future integration of the sky-compass heading with
inertial navigation in GNSS-denied robotic systems.

Keywords: sky compass, polarised skylight, celestial navigation, GNSS-denied nav-
igation, fisheye camera, bio-inspired robotics, dorsal rim area, high-latitude oper-
ation

——————————————-
i

Acknowledgements
I would like to express my heartfelt gratitude to my supervisor Dr. Paavo
Nevalainen for all the guidance, support, understanding and the motivation given
to make this thesis study possible with all the challenges that happened along the
way. The guidance to provide me with technical knowledge and with the ideas to
approach my problems are highly appreciated. Furthermore, I thank my parents,
friends and colleagues for the encouragement and the constant support that led me
to the success of my thesis and studies. Turku, July 2026
ii

| Declaration | of AI Usage | in the | Thesis |
| ----------- | ----------- | ------ | ------ |
During the preparation of this work, the author used Grammarly to check gram-
mar, spelling, and language fluency. After using this tool, the author reviewed and
edited the content as needed and takes full responsibility for the content of this
publication.
During the preparation of this work, the author used claude to assist with struc-
turing code snippets and brainstorming conceptual outlines. The author verified all
generated outputs, critically assessed the results, and takes full responsibility for the
| integrity of the | thesis. |     |     |
| ---------------- | ------- | --- | --- |
iii

Contents
| Acknowledgements |             |               | ii  |
| ---------------- | ----------- | ------------- | --- |
| Declaration      | of AI Usage | in the Thesis | iii |
| 1 Introduction   |             |               | 1   |
| 2 Literature     | Review      |               | 6   |
2.1 The insect sky compass . . . . . . . . . . . . . . . . . . . . . . . . . . 6
2.2 Computational models bridging biology and robotics . . . . . . . . . 8
2.3 Hardware implementations and their relationship to this thesis . . . . 9
2.4 Recent developments and open simulation tools . . . . . . . . . . . . 10
| 3 Theoretical | Background |     | 13  |
| ------------- | ---------- | --- | --- |
3.1 Solar position model for Turku . . . . . . . . . . . . . . . . . . . . . . 13
3.2 Fisheye lens projection model . . . . . . . . . . . . . . . . . . . . . . 17
3.3 Sky polarization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19
| 4 System | Design |     | 23  |
| -------- | ------ | --- | --- |
4.1 Optical architecture and build options . . . . . . . . . . . . . . . . . 23
4.2 Dome geometry and fabrication . . . . . . . . . . . . . . . . . . . . . 24
4.3 Camera and mount . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28
4.4 Processing pipeline . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28
iv

| 5 Methods |     |     |     | 29  |
| --------- | --- | --- | --- | --- |
5.1 Camera configuration . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
5.2 Sun detection and pixel to azimuth mapping . . . . . . . . . . . . . . 33
5.3 Orientation estimation . . . . . . . . . . . . . . . . . . . . . . . . . . 33
5.4 Synthetic data generation . . . . . . . . . . . . . . . . . . . . . . . . 34
| 6 Results |     |     |     | 37  |
| --------- | --- | --- | --- | --- |
6.1 Sun position coverage at Turku . . . . . . . . . . . . . . . . . . . . . 37
6.2 Dome band geometry . . . . . . . . . . . . . . . . . . . . . . . . . . . 39
6.3 Estimator accuracy in simulation . . . . . . . . . . . . . . . . . . . . 42
| 7 Discussion, | Limitations, | and Future | Work | 43  |
| ------------- | ------------ | ---------- | ---- | --- |
7.1 Limitations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 43
7.2 High latitude considerations . . . . . . . . . . . . . . . . . . . . . . . 44
7.3 Future work . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 45
| 8 Conclusion |     |     |     | 47  |
| ------------ | --- | --- | --- | --- |
| References   |     |     |     | 50  |
Appendices
| A Full Weekly | Results |     |     | A-1 |
| ------------- | ------- | --- | --- | --- |
v

List of Figures
3.1 Solar noon elevation across 2026 at Turku as computed by the inde-
pendent NOAA implementation, shown against the analytic solstice
values for latitude 60.45 degrees North. The modelled curve meets
bothreferencelines, withagreementwithin0.01degreesateachsolstice. 16
3.2 Geometry of the sky polarization pattern. (a) The observer at O, the
zenith Z, the sun at S, and a sky point P. The scattering angle gamma
is the angle at O between the line of sight to P and the direction to
the sun, and the shaded region is the scattering plane containing
both lines. The e-vector at P, shown in red, lies perpendicular to
the scattering plane. (b) The same pattern in the zenith-centred
projection used by the fisheye camera. Dashed curves are contours
of constant angular distance from the sun, red bars give the e-vector
direction with length scaled by the degree of polarisation, and the
solid ring marks the band 90 degrees from the sun where the degree
of polarisation reaches its maximum. . . . . . . . . . . . . . . . . . . 20
4.1 Constructionsequenceofthehemisphericalpolarising-filmdome,from
the preparation of individual gore sections and camera positioning to
the assembly of the eight gores into the completed dome around the
fisheye camera. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25
4.2 Image of final version of the constructed dome . . . . . . . . . . . . . 26
vi

4.3 Testing the polarizing film and confirming the polarity with respect
to the direction of the sun . . . . . . . . . . . . . . . . . . . . . . . . 26
4.4 goretemplate, sheetlayout, andassembledhemispherefromthedome
cutting guide. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27
4.5 Final Dome Construction Prototype . . . . . . . . . . . . . . . . . . . 27
5.1 A bench test capture through the bare fisheye lens, taken at Turku on
26July2026at15:17UTCataresolutionof1600by1200pixelsinthe
YUYV format, with exposure, gain and white balance fixed through
Video4Linux2. The polarising optic is not fitted and the optical axis
is not vertical, so the frame is a test of the capture chain and of the
lens geometry rather than a sky measurement. The illuminated disc
has a radius of approximately 565 pixels. . . . . . . . . . . . . . . . . 30
6.1 Daylight solar positions at Turku between 14 May and 14 July 2026,
sampled at ten minute intervals and coloured by day. Azimuth spans
approximately 35 to 325 degrees and elevation reaches 53.0 degrees,
which is the range of sun geometry the compass is required to handle
at latitude 60.45 degrees North. The right panel shows the same
positions projected onto the sky hemisphere, where the radius is the
zenith angle, so the centre of the plot is directly overhead. . . . . . . 38
6.2 Modelled sky radiance through the polarising optic for a sun azimuth
of 135 degrees and an elevation of 30 degrees, with image up corre-
sponding to North. The left panel is the single flat filter and the right
panel is the radial gore arrangement. The red circle marks the true
solar position in both. . . . . . . . . . . . . . . . . . . . . . . . . . . 40
vii

6.3 Synthetic frames rendered through the flat filter at the true solar
positions for 21 June 2026 at Turku. The solar azimuth and elevation
used to render each frame are given above it and the red circle marks
theresultingsunpositionintheimage. Becauseordinaryphotographs
record no polarisation information, labelled frames for development
and testing are produced in this manner from measured solar geometry. 40
viii

List of Tables
2.1 Comparison of camera-based and photodiode-based celestial compass
systems with the design presented in this thesis. Latitude is included
because the geometry of the daily solar arc, and therefore the range of
conditions a compass must handle, depends strongly on geographical
location. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
6.1 Absolute azimuth error in degrees over 60 solar positions drawn at
random from 5972 real daylight positions at Turku between 14 May
and 14 July 2026. The film axis was 35 degrees and the image up
heading 0 degrees throughout, with sensor noise of 0.020 in all four
runs. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 42
ix

1 Introduction
Navigation has always been a primary element for survival in any species on Earth
as it aids in the location of food, returning to their nesting sites, avoiding predators
and migration due to climate changes. This can be from few meters to thousands
of kilometres [1]. Animals use a variety of changes such as visually sited landmarks,
magnetic fields, celestial bodies and skylight [2]. Other factors like birds following
wind currents, fishes following different ocean currents, observing the position of the
sun during different seasons in the nature to navigate vast distances without any
external reliance of equipment. Humans too, have relied on environemental factors
in the past and have navigated from very small distances to a difference terrain for
hunting to exploring different lands thousands of kilometres away from their homes
or where they were based at to also exploring different continents across the seas [3].
In the present day, we are heavily relying on the concepts and learnings of navi-
gation to improve the manoeuvrability and the developments of robotics and drones.
The advancements in the field are becoming more progressive because of the poten-
tial of including Artificial Intelligence (AI) in the pipeline. However, Navigation
without a satellite fix is a persistent difficulty in mobile robotics [4]. When a robot
loses GPS coverage, whether underground, inside a building, beneath a dense for-
est canopy, or in an area where the signal has been jammed, it must fall back on
dead reckoning which enables the estimation of the robot’s current orientation from
previous states and in most systems this means relying on an Inertial Measurement

CHAPTER 1. INTRODUCTION 2
Unit (IMU). The accumulated error in the measurement of the acceleration and
angle-rate values is initially small, so that an IMU does a good job of performance
over short distances and short intervals. After some distance however, a robot needs
to navigate itself through a kilometre of open area, and then this drift can start to
be fast. Dead reckoning [5] uses a known position to determine the current position
by continuously monitoring the distance and direction the robot has moved. If you
walk across a dark room without any outside reference point (just counting steps
and remembering each turn), the distance you take between steps and the angle you
turn by will gradually cause the distance you think you have walked to be off by a
little each time.
The same basic issue exists for an IMU. The accelerometers and gyroscopes do
not sense position or heading, but rather sense changes in motion and orientation.
These measurements are then summed over time, adding up small biases, noise and
measurement errors [6]. This small error in heading direction can then result in a
large error in the lateral position; over a long distance, it could therefore produce
an inaccurate estimation of the robot’s own position. It can be reduced by using an
independentabsoluteheadingreferencethatperiodicallycorrectstheorientationap-
plied to dead reckoning. It is this gap that the sky-compass approach developed here
aims to fill: an external reference of a heading (north-seeking direction) independent
of satellite availability.
A number of alternative approaches address this problem in part. Visual odome-
try, wheel encoders, magnetometers, barometric altimeters, and LiDAR-based local-
isation each contribute something useful under the right conditions. Each also has
a characteristic weakness, however, since these methods variously depend on known
infrastructure, failinfeaturelesssurroundings, oraresusceptibletoaparticularform
of interference. What would be useful is a heading reference that is passive, draws
very little power, works anywhere beneath open sky irrespective of terrain, and de-

CHAPTER 1. INTRODUCTION 3
pends on no external network at all. A sensor of this kind has existed in nature for
a very long time, even though it has been slow to appear in engineering.
Desert ants of the genus Cataglyphis provide one of the most striking examples
of autonomous navigation succeeding without any of these aids [7]. These small
insects forage across almost featureless North African salt pans, travelling hundreds
of meters from the nest in search of food and returning to it with remarkable ac-
curacy. They make little meaningful use of landmarks. Instead, they maintain a
continuously updated internal estimate of heading and distance from two sources,
using step integration to measure distance and a sky compass to fix direction [8].
The sky compass reads the polarization pattern of scattered sunlight. This pat-
tern is predictable and geometrically consistent across the whole hemisphere, and
it encodes the position of the sun even when the sun itself is obscured by cloud.
The eye structure responsible for reading it, the dorsal rim area, is a narrow band
of photoreceptors along the top margin of each compound eye, arranged so that it
samples the angle of polarisation from several sky regions at once.
The sky compass is based on the polarization pattern of scattered sunlight. This
pattern is consistent and geometric throughout the hemisphere, and also describes
the Sun’s position when the Sun is hidden by clouds. A narrow band of specialised
photoreceptors along the top of each compound eye called its dorsal rim area [9] that
isnecessaryforreadingit. Thisregioncanbeconsideredasanarrowbandofbuilt-in
polarisingsensors, likeathinbandofpolarisingsunglasses, butspecialisedinsensing
polarised light instead of creating traditional images. The dorsal rim area samples
polarization information from a number of regions at once rather than from just
one direction in the sky This distributed sensing approach will enhance the solution
robustness, as long as one portion of the sky is obstructed by clouds, vegetation or
neighbouring objects, the rest of the sky still provides enough polarization cues to
get the right orientation.

CHAPTER 1. INTRODUCTION 4
The biological mechanism is worth replicating for its tolerance rather than only
for its appearance and elegance. Partial cloud cover, haze, and occlusion of the
sun degrade a GPS receiver or a magnetometer-based compass well before they
meaningfully affect a compass based on sky polarization. This tolerance leads to
the central question of the thesis, which is whether a low-cost fisheye camera paired
with a dome of polarizing film, built to follow the geometry of the insect dorsal rim
area, can produce reliable heading estimates for a robot operating outdoors at high
latitude.
This thesis proposes, designs, and evaluates such a system. A fisheye camera
is mounted underneath a hemispherical dome of polarizing film, which is cut and
assembled from gores whose transmission axes are arranged radially, so that the axis
at each azimuth points away from the zenith and the sky polarization is sampled
across many directions at once. An image taken through the dome records the sky
polarizationasaspatialpatternofintensity, andfromthispatternthesolarazimuth,
and with it the robot’s absolute heading, can be recovered. The system is validated
against a solar position model developed for Turku, Finland, which computes the
ground-frame azimuth and elevation of the sun for any date and time of day from
astronomical parameters.
The work also has a practical motivation beyond the academic one. Autonomous
outdoorplatformsinFinlandexperienceGPSdegradationduringgeomagneticstorms,
within certain urban building geometries, in the thick forest with heavy canopy
growth, under intentional or accidental GPS signal denial, and in the indoor to out-
door transition zones that are common in many logistics settings. A passive sky
compass adds an independent heading channel that complements the existing sen-
sors rather than duplicating them, and it supplies an absolute directional reference
that does not drift over time. The site itself gives a further reason to study the
problem locally, since at the high latitude of Turku the summer sun sweeps through

| CHAPTER | 1. INTRODUCTION |     |     | 5   |
| ------- | --------------- | --- | --- | --- |
a very wide range of azimuths over the course of a day and climbs to only about 53
degreesatnoon, sothesungeometrythatacompassmustreadherediffersmarkedly
from that at the lower latitudes where most earlier systems were tested.
The remainder of the thesis is organised as follows. Chapter 2 reviews the rele-
vant biological and engineering literature. Chapter 3 sets out the theoretical foun-
dations, covering the solar position model, the fisheye projection, and the physics of
sky polarization. Chapter 4 describes the system design. Chapters 5 and 6 cover the
implementation, the experiments, and the results. Chapter 7 discusses the findings,
| their limitations, | and directions | for future | work. |     |
| ------------------ | -------------- | ---------- | ----- | --- |

2 Literature Review
In this chapter the existing research that is available and serves as the basis for this
thesiswillbereviewed. Itstartswithalookatthebiologyofthisinsectskycompass,
with particular emphasis on the polarization vision system of desert ants and other
insectsthat make useofthe celestialcompassfor navigation. The chapter thenlooks
at the way these biological processes have been implemented in a computational
model that connects biology and robotics, especially the algorithms used to estimate
heading from polarized skylight. This is followed by a description of the various
ways in which an artificial sky compass has been implemented, both optically and
in terms of sensors, and a comparison of the proposed system and previous systems.
Finally, the chapter reviews recent advances in the area of simulation environments
and open-source tools, which facilitate the design, evaluation, and comparison of
the different types of polarization-based navigation systems. These studies together
define the state of the art, the shortcomings of existing approaches, and inspire the
design choices proposed in the following chapters.
2.1 The insect sky compass
Theideathatinsectsusethepositionofthesuntonavigatepredatesmodernrobotics
by several decades, and the mechanism behind it has come into sharper focus over
time. Wehner [8] provides a thorough account of what studies of the desert ant
Cataglyphis had established by that point. The ant relies on a navigational strat-

2.1 THE INSECT SKY COMPASS 7
egy built around path integration, meaning a continuously updated estimate of its
position relative to the nest, computed from the direction and distance of every step
taken since it set out. Direction is supplied by the sky compass, and distance by
step counting. The sky compass is of particular interest because it does not read the
position of the sun directly. What it reads is the polarization pattern of the sky, that
is, the distribution of electric-field vector orientations across the hemisphere, which
is related geometrically to the position of the sun through the physics of atmospheric
scattering.
The structure responsible for this reading is the dorsal rim area (DRA) of the
compound eye, a specialised band of photoreceptors along the eye’s dorsal margin.
The rest of the compound eye is optimised for spatial vision and colour discrimina-
tion, but in the DRA the light-sensitive microvilli are arranged in orthogonal pairs
at a range of orientations. This arrangement turns each receptor pair into a polar-
ization analyser tuned to a specific sky azimuth. The output of the DRA passes
to the central complex, a brain region that has since been identified as a heading-
integration circuit common to a wide range of insect species. Wehner’s broader
point is that Cataglyphis navigates by following a procedural routine rather than
by building a map, in the sense that it maintains a heading, counts its steps, and
computes the vector back to the nest. The sky compass is the anchor that keeps
this heading reliable over long distances.
One detail that is easy to overlook, yet matters a great deal for an engineering
implementation, is how well this strategy holds up under partial cloud cover. An
insect does not require an unobstructed view of the whole sky. The polarization
angle at any single point of clear sky already encodes the position of the sun, so
even a small break in the clouds supplies a usable directional reference. Because
the DRA integrates across space, combining many sky samples into a single heading
estimate, the loss or attenuation of any individual sample does not destroy the

2.2 COMPUTATIONAL MODELS BRIDGING BIOLOGY AND ROBOTICS 8
estimate as a whole.
2.2 Computational models bridging biology and robotics
Turning the biological mechanism into a working algorithm took time, and the link
between the neural circuit and the engineering solution is less direct than it first
appears. The work in Gkanias et al. (2019) [10] presents a computational model
that follows the known signal pathway from sky polarization input to directional
output, tracing the processing stages that correspond to identified neural structures
in the insect brain. The model takes the angle of polarisation measured at a set
of sky azimuths and combines these values with a circular-mean algorithm that
mirrors the integration carried out in the central complex. One of its more useful
results is that a fairly small number of polarization samples, spread across different
sky directions, is enough to recover the solar azimuth with reasonable accuracy.
The practical consequence is that neither a camera with millions of pixels nor a
dense array of sensors is required. A modest set of well-distributed polarization
measurements suffices, and the redundancy among those measurements gives the
system a natural tolerance to occlusion.
On the engineering side, Stürzl [11] presents a single-camera polarization com-
pass with a careful treatment of measurement uncertainty. Rather than moving any
component, the system images the sky through three fixed polarizers set at different
orientations on one sensor, across a field of view of roughly 56 degrees, and recovers
the sky polarization from these simultaneous channels. From this it computes the
solar azimuth directly. Beyond the heading estimate itself, its notable feature is
an explicit covariance, since the algorithm reports a quantified heading uncertainty
alongside each estimate. This matters for sensor fusion. A heading measurement
whose covariance is known can be weighted correctly within a Kalman filter or a
comparable estimator when it is fused with IMU data, whereas without an uncer-

2.3 HARDWARE IMPLEMENTATIONS AND THEIR RELATIONSHIP TO
THIS THESIS 9
tainty model the fusion depends on ad hoc tuning that may not transfer from one
sky condition to another. Stürzl’s work was among the first to treat the polarization
compass as a true probabilistic sensor rather than a simple angle readout.
2.3 Hardware implementations and their relation-
ship to this thesis
Moving from algorithm to physical sensor, Stürzl and Carey [12] showed that a
fisheye camera system could perform polarization detection reliably enough to be
carried on a UAV. The fisheye lens is a natural choice here, since a single wide-
angle image captures most of the sky hemisphere, and the spatial distribution of
polarization across that image carries considerably more information than any single
narrow-field measurement. Their experiments showed that the solar azimuth could
still be estimated reliably when the sun itself lay outside the camera’s field of view,
for example when the aircraft was flying with the sun behind it. This is the form of
occlusion tolerance that makes the approach attractive for mobile robotics, where
the orientation of the robot relative to the sun changes constantly.
The most recent and most directly relevant hardware work is that of Gkanias et
al. [13], who present a physical prototype of the DRA-inspired compass. Instead of
a camera, the sensor uses a ring of eight photodiode pairs, with each pair measuring
two orthogonal polarization orientations. This circular layout imitates the fan-like
structure of the DRA, and a circular-mean model turns the eight measurements
into a solar azimuth estimate. The sensor was tested across a range of weather
conditions, includingheavycloudandpartialocclusion, andthespatiallyintegrating
design outperformed more computationally complex algorithms when the sky was
poor. This behaviour is consistent with the biological mechanism, in that the very
simplicity of the spatial averaging is what gives the system its tolerance to local

2.4 RECENT DEVELOPMENTS AND OPEN SIMULATION TOOLS 10
disturbances in the sky.
This thesis builds on both the camera-based approach of Stürzl and Carey [12]
and the bio-inspired principle of spatial integration in Gkanias et al. [13]. A fisheye
camera is used in place of discrete photodiodes, which yields richer spatial informa-
tion and allows the implementation to be validated against a full sky polarization
model. In place of the several fixed polarizers used by those earlier camera sys-
tems, a single static dome of polarizing film is used, whose transmission axes are
arranged radially, so that the whole sky polarization pattern is captured in one
exposure through a single lens. What sets this design apart is not the absence of
moving parts, which several of these earlier systems already achieve, but the par-
ticular combination of a single low-cost fisheye covering the whole sky hemisphere,
a passive radially arranged polarizing dome, and validation at the high latitude of
Turku. This distinguishes it from the narrow-field three-polarizer camera of Stürzl,
the four-camera system of Stürzl and Carey, and the discrete eight-photodiode ring
of Gkanias et al. The geometric design of this dome, a hemisphere assembled from
gores of polarizing film, is described in detail in Chapter 4. The table 2.3 shows the
previous work and the work related to this research.
2.4 Recent developments and open simulation tools
Work on the insect celestial compass has continued since the studies above. Gkanias
and Webb [14] extend the compass model to the problem of time compensation,
showing how a circuit of clock and compass neurons could hold a stable geocentric
heading as the sun moves through the day, with the correction depending on the
time of year and on the observer’s latitude. The dependence on latitude is of direct
interest here, since the system in this thesis is validated at a high latitude where the
sun stays low and moves through a wide azimuth range. Two further studies, both
in preparation at the time of writing, continue this line. Kolyfetis and colleagues [15]

| 2.4 RECENT | DEVELOPMENTS |     | AND OPEN | SIMULATION | TOOLS | 11  |
| ---------- | ------------ | --- | -------- | ---------- | ----- | --- |
System Sensor and polarisation Sky coverage Test site and Reported accuracy
|     | sampling |     |     | latitude |     |     |
| --- | -------- | --- | --- | -------- | --- | --- |
Stürzland Foursynchronisedcameraswith Wholesky Notstated Recoverssolar
| Carey[12] | fisheyelensesanddifferently |     | hemisphere |     | azimuthand           |     |
| --------- | --------------------------- | --- | ---------- | --- | -------------------- | --- |
|           | orientedfixedpolarisers     |     |            |     | elevation;tolerantof |     |
cloudandUAVpitch
androll
Approx.56◦
| Stürzl[11] | Singlecamerawiththreefixed |     |     | Notstated | Sundirection  |     |
| ---------- | -------------------------- | --- | --- | --------- | ------------- | --- |
|            | polarisersononesensor      |     |     |           | estimatedwith |     |
explicitcovariance
Gkaniasetal. SimulatedDRA-likepolarisation Simulationonly Notapplicable Proofofprinciple
| [10] | array;modelonly |     |     |     | demonstratedin |     |
| ---- | --------------- | --- | --- | --- | -------------- | --- |
simulation
Gkaniasetal. Ringofeightpolarisation Discrete Sardinia,Italy RMSE:5.89◦ global
[13] analysers,eachcontainingfour sampling; (39.3◦N);Vryburg, and2.77◦ localfor
|     | UVphotodiodesat0◦,45◦,90◦,  |     | approx.45◦ |                    |                      |     |
| --- | --------------------------- | --- | ---------- | ------------------ | -------------------- | --- |
|     |                             |     |            | SouthAfrica        | solarelevationsabove |     |
|     | and135◦;analysersinclinedat |     |            | (26.4◦S);BelaBela, | 10◦                  |     |
acceptance
|     | 45◦ |     | angleper | SouthAfrica |     |     |
| --- | --- | --- | -------- | ----------- | --- | --- |
|     |     |     | analyser | (24.7◦S)    |     |     |
Current Singlefisheyecamerabeneatha Wholesky Turku,Finland Reportedin
Thesis work passivehemispherical hemisphere (60.45◦N) Chapter??
polarising-filmdomewith
radiallyarrangedtransmission
axes
Table 2.1: Comparison of camera-based and photodiode-based celestial compass
systems with the design presented in this thesis. Latitude is included because the
geometry of the daily solar arc, and therefore the range of conditions a compass
| must handle, | depends | strongly on | geographical | location. |     |     |
| ------------ | ------- | ----------- | ------------ | --------- | --- | --- |
build a biologically accurate model of the polarisation vision of bees that runs from
eye anatomy through to navigation, and Gkanias and colleagues [16] examine how
little skylight the insect compass needs, reporting that a single ray can be enough
to locate the sun. These last two are cited as directions in the field rather than
as settled results, and their bibliographic details should be confirmed against the
| published | versions before | final submission. |     |     |     |     |
| --------- | --------------- | ----------------- | --- | --- | --- | --- |
A number of open tools now make it practical to simulate polarized skylight
and to test a compass against a modelled sky rather than against measurements
alone. The Prague Sky Model of Vévoda and colleagues [17] provides precomputed
sky radiance across a wide spectral range and includes polarisation, and an open
Python implementation of it, alongside simpler analytic sky models, is available in
the sky package released by Gkanias [18]. On the measurement side, the open source
OpenSky simulator of Moutenet and colleagues [19] reproduces sky polarization

2.4 RECENT DEVELOPMENTS AND OPEN SIMULATION TOOLS 12
measurements made with a fisheye camera and compares them against outdoor
captures, which is close in spirit to the validation carried out in this thesis. The
present work draws on tools of this kind to render the expected polarization pattern
for a given sun position and to compare the rendered pattern against captured
images.

3 Theoretical Background
3.1 Solar position model for Turku
Any sky-compass system needs a way to determine where the sun should be for
a given time and location [20]. Here, that calculation has two roles. It provides a
ground-truthheadingduringthevalidationexperiments, anditactsasapriorforthe
sky polarization model used in heading estimation. The solar position is computed
in local ground-level coordinates at Turku, Finland, at a latitude of 60.45◦ N and a
longitude of approximately 22.3◦ E.
The choice of Turku also provides a demanding test environment for a sky-
compasssystem. Atalatitudeofapproximately60.45◦ N,theSunremainsrelatively
lowabovethehorizonformuchoftheyear, daylightdurationvariessubstantiallybe-
tween seasons, and atmospheric conditions frequently include cloud cover and haze.
In addition, satellite-based positioning can become less reliable at high latitudes
because the geometry of visible satellites is often less favourable, reducing posi-
tioning accuracy and increasing susceptibility to signal degradation in challenging
environments. These factors make it valuable to investigate an independent heading
reference that does not rely on satellite signals but extract information from spatial
polarization patterns [21]. A sky compass derived from the polarization pattern of
scattered sunlight therefore, offers a complementary navigation cue that can con-
tinue to provide orientation information even when GNSS performance is degraded

| 3.1 SOLAR      | POSITION | MODEL | FOR TURKU |     | 14  |
| -------------- | -------- | ----- | --------- | --- | --- |
| or unavailable | [22].    |       |           |     |     |
The starting point is the Earth’s annual orbit, parameterised by the fractional-
| year angle | gamma | (γ) which is denoted | by: |     |     |
| ---------- | ----- | -------------------- | --- | --- | --- |
2π(d−1)
|     |     |     | γ = | ,   |     |
| --- | --- | --- | --- | --- | --- |
365
where is the day of the year counted from 1 January. From γ, the equation of
d
time accounts for the uneven orbital speed of the Earth, which arises from the
E(γ)
ellipticity of its orbit, together with the tilt of the rotation axis. The equation gives
the difference in minutes between true solar time and mean solar time, and over the
course of a year it shifts true solar noon by up to about sixteen minutes relative to
clock time. At Turku the mean solar noon falls at roughly 12:39 local time, and true
noon departs from this by an amount that depends on the day of the year.
Thesolardeclinationδ istheanglebetweentheequatorialplaneandthedirection
to the Sun, and it follows the seasonal cycle set by the Earth’s axial tilt of 23.44◦. At
the summer solstice, the Sun stands north of the equator, while at the winter
23.44◦
solstice, it stands 23.44◦ south of the equator. For a given declination and hour
δ
angle α, where α is measured from local solar noon at 15◦ per hour, the direction
to the Sun can be written as a unit vector in the equatorial coordinate frame, with
| the z-axis | pointing | toward the celestial | north | pole. |     |
| ---------- | -------- | -------------------- | ----- | ----- | --- |
Converting this vector to local ground-level coordinates at Turku requires a ro-
tation matrix R built from the site latitude. In the local frame the x-axis points
West, the y-axis points South, and the z-axis points vertically upward. The matrix
| R rotates | the equatorial | frame into | this local | frame:    |     |
| --------- | -------------- | ---------- | ---------- | --------- | --- |
|           |                |            | ⎡          | ⎤         |     |
|           |                |            | 1 0        | 0         |     |
|           |                |            | ⎢          | ⎥         |     |
|           |                |            | ⎢          | ⎥         |     |
|           |                | R =        | ⎢0 sin(θ)  | −cos(θ)⎥, |     |
|           |                |            | ⎢          | ⎥         |     |
|           |                |            | ⎣          | ⎦         |     |
|           |                |            | 0 cos(θ)   | sin(θ)    |     |

| 3.1 SOLAR | POSITION | MODEL | FOR | TURKU | 15  |
| --------- | -------- | ----- | --- | ----- | --- |
where is the latitude of Turku. The resulting local Sun vector gives the
| θ   | = 60.45◦ |     |     |     |     |
| --- | -------- | --- | --- | --- | --- |
azimuth [23], measured from South toward West, and the elevation directly. The
model was implemented in Python and checked against two analytical reference
values. At solar noon on the winter solstice, the elevation at Turku should equal
|              |         | 90◦ −60.45◦ | −23.44◦   | = 6.11◦,        |     |
| ------------ | ------- | ----------- | --------- | --------------- | --- |
| and at solar | noon on | the summer  | solstice, | it should equal |     |
|              |         | 90◦ −60.45◦ | +23.44◦   | = 52.99◦.       |     |
The implementation returns 6.11◦ and 52.97◦, respectively, which confirms its cor-
| rectness | to within the | precision | of the input | constants. |     |
| -------- | ------------- | --------- | ------------ | ---------- | --- |
The same solar geometry was implemented a second time from an independent
source, using the NOAA solar position equations after Meeus, in order to guard
against a hidden error in the derivation or in its port to Python. This second model
agrees with the one above to a fraction of a degree across the range of dates and
timesofinterest, whichraisesconfidencethatthegroundtruthusedinthevalidation
| experiments | is correct. |     |     |     |     |
| ----------- | ----------- | --- | --- | --- | --- |
A second independent implementation was carried out from the same solar ge-
ometry using the NOAA solar position equations (Meeus) and the algorithms [24],
with the result providing an independent check of both the algorithm and implemen-
tation in Python. The solar elevation at local solar noon for each day of 2026 for the
NOAA implementation is plotted in Figure 3.1. Solar elevation is given by a contin-
uous curve, which follows the normal variation according to the seasons, and by the
two horizontal dashed lines representing the analytical solstice elevations (52.99◦ in
summer, in winter) calculated directly from the latitude of Turku and the tilt
6.11◦
of the earth’s axis without the use of any numerical model. The computed curve

3.1 SOLAR POSITION MODEL FOR TURKU 16
Figure 3.1: Solar noon elevation across 2026 at Turku as computed by the indepen-
dent NOAA implementation, shown against the analytic solstice values for latitude
60.45 degrees North. The modelled curve meets both reference lines, with agreement
within 0.01 degrees at each solstice.
crossesboththereferencevaluesontheanticipateddaysandtheagreementiswithin
around 0.01° around each solstice. This close agreement is much stronger evidence of
correctness than a single implementation doing so because two independent deriva-
tions yield essentially identical results. Thus, there is greater confidence that the
solar positions used as ground truth during the following validation experiments are
accurate. This also shows an important aspect of high latitude operation, that the
sunrise elevation at local noon at the latitude changes by only about 47◦, from about
6◦ in winter to 53◦ in summer; and that the sun does not get near the zenith. The
small number of solar elevations is a key feature of northern environments, and will
be discussed in relation to high-latitude operation in Section 7.2.
One point of convention should be recorded here so that the later chapters do
not silently mix frames. The derivation above measures azimuth from South toward
West, following the supervisor’s original formulation for Turku, and that frame is
keptunchanged. TheheadingestimatesreportedfromChapter4onwardinsteaduse

| 3.2 FISHEYE |     | LENS | PROJECTION |     | MODEL |     | 17  |
| ----------- | --- | ---- | ---------- | --- | ----- | --- | --- |
the standard robot convention, in which azimuth is measured clockwise from North.
The two are related by a fixed rotation of 180 degrees, with the North referenced
azimuth equal to the South referenced azimuth plus 180 degrees reduced into the
range from 0 to 360 degrees, and this relation is applied wherever a solar azimuth
| from this | model   | is  | compared | against    | an estimated | heading. |     |
| --------- | ------- | --- | -------- | ---------- | ------------ | -------- | --- |
| 3.2       | Fisheye |     | lens     | projection |              | model    |     |
The fisheye camera in this system follows the equidistant projection model, in which
the pixel radius from the image centre scales linearly with the angle from the optical
| axis [25], | [26]. | This | is written | as  |     |     |     |
| ---------- | ----- | ---- | ---------- | --- | --- | --- | --- |
ρ = aθ,
where ρ is the pixel distance from the centre and θ is the angle from the optical
axis, which corresponds to the zenith when the camera points straight up. The
| scale factor |     | is given | by  |     |     |     |     |
| ------------ | --- | -------- | --- | --- | --- | --- | --- |
a
r
|     |     |     |     |     | a = | .   |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
θ
max
With the camera parameters used in the supervisor’s MATLAB script,
r = 470
| pixels | corresponds |     | to θ | = 90◦, | which gives |     |     |
| ------ | ----------- | --- | ---- | ------ | ----------- | --- | --- |
max
470
|     |     |     | a   | =   | ≈ 5.22 pixels | per degree, |     |
| --- | --- | --- | --- | --- | ------------- | ----------- | --- |
90◦
or equivalently,
1
|     |     |     |     |     | 0.19◦ | per pixel. |     |
| --- | --- | --- | --- | --- | ----- | ---------- | --- |
≈
a
This angular resolution has a direct consequence for Sun detection. Seen from
Earth, the solar disk has an angular diameter of approximately 0.53◦, which, at an

3.2 FISHEYE LENS PROJECTION MODEL 18
angular resolution of 0.19◦ per pixel, corresponds to a diameter of approximately
0.53◦
≈ 2.8 pixels
0.19◦/pixel
in the fisheye image. An object only about three pixels across, set within a sky
image that is subject to lens vignetting, cloud, and bloom around bright sources,
is not a reliable detection target on its own. This is the reason for adopting the
polarization dome. Instead of locating a small bright disk, the system reads a broad
spatial pattern that spans the whole sky image, so that the position of the sun is
encoded in the structure of the pattern rather than in the location of a bright spot.
The projection model also governs the relationship between positions on the
dome and directions in the sky. Each pixel in the image corresponds to a particular
sky direction, and each point on the inner surface of the dome corresponds to a
particular region of pixels. This mapping is used in two places. It guides the
dome design, so that the polarization axes are distributed correctly across the sky
azimuths,anditenterstheimageprocessing,wherepixel-levelpolarizationestimates
must be referred back to sky coordinates before the solar azimuth can be computed.
The inverse of this projection is the mapping actually used when a captured
image is processed. For a pixel measured from the image centre, the radial distance
rho gives the angle from the optical axis as theta equal to rho divided by the scale
factor a, while the direction of the pixel around the centre gives the azimuthal angle
of the sky point. Together, these two angles define a unit vector pointing from the
camera toward the corresponding point on the sky hemisphere. This is the same
mapping the synthetic image generator uses in reverse, assigning a sky direction to
every pixel so that a modelled polarization pattern can be written into the image.

3.3 SKY POLARIZATION 19
3.3 Sky polarization
Beforethepolarizationpatternisdescribedindetail, ithelpstofixageometricframe
[27]. Consider an observer at the origin O, with the zenith Z directly overhead and
the sun at a position S in the sky. A viewing direction toward any point P on the
sky hemisphere then makes a scattering angle gamma with the direction to the sun,
where gamma is the angle at O between the line of sight to P and the line to the
sun. The plane that contains both of these lines is the scattering plane for that
point. The two quantities that describe the sky polarization, namely the angle of
polarisation and the degree of polarisation, are both functions of this geometry, and
in particular of the scattering angle gamma, so the whole pattern can be treated as
a field defined over the hemisphere relative to the fixed points Z and S.
The regular polarization of skylight arises from Rayleigh scattering of direct
sunlight by molecules in the atmosphere [28]. When an electromagnetic wave meets
a scattering centre much smaller than its wavelength, such as a nitrogen or oxygen
molecule, the scattered wave becomes partially linearly polarized. The electric field
of the scattered light lies in the plane perpendicular to the scattering plane, the
latter being the plane defined by the incoming ray, the scattering centre, and the
observer. Across the sky this produces a polarization pattern that is symmetric
about the solar meridian, the great circle that passes through the sun, the zenith,
and the anti-solar point.
At any point in the sky, the Angle of Polarisation (AoP) lies perpendicular to the
great circle that that joins that point to the sun. The iso-AoP contours therefore
form concentric rings around the solar position, and the whole pattern rotates as
a rigid body as the sun moves across the sky [29]. The Degree of Polarisation
(DoP) reaches its maximum at an angular distance of 90◦ from the Sun, in the
plane containing the Sun and the zenith, and decreases toward zero at the solar and
anti-solar points. Under clear-sky conditions, the maximum DoP is typically in the

3.3 SKY POLARIZATION 20
Figure 3.2: Geometry of the sky polarization pattern. (a) The observer at O, the
zenith Z, the sun at S, and a sky point P. The scattering angle gamma is the angle at
O between the line of sight to P and the direction to the sun, and the shaded region
is the scattering plane containing both lines. The e-vector at P, shown in red, lies
perpendicular to the scattering plane. (b) The same pattern in the zenith-centred
projection used by the fisheye camera. Dashed curves are contours of constant
angular distance from the sun, red bars give the e-vector direction with length
scaled by the degree of polarisation, and the solid ring marks the band 90 degrees
from the sun where the degree of polarisation reaches its maximum.
range of 70% to 80%.
The geometry of the angle of polarisation of the sky is shown in figure 3.2 The
electricfieldvibratesatalltimesatrightanglestothescatteringplane, andcontours
of constant angle of polarisation are seen as concentric rings centered on the position
of the sun. The whole pattern rotates as a rigid body but maintains the same shape
as the Sun travels through the sky. This predictable geometric relationship is the
property that is exploited by a sky compass, with the direction of the polarisation
pattern being the direction of the Sun even if the solar disk is obscured. Polarisation
is also an everyday phenomenon. The atmosphere causes light from the Sun to be
slightly polarised and polarising sunglasses can block glare from some parts of the
sky and enhance visual contrast. The same principle is used in a sky compass that
measures the orientation of the polarized light to determine heading (not reduce
glare).
The degree of polarisation varies with the scattering angle in a way that Rayleigh

3.3 SKY POLARIZATION 21
theory makes explicit. To a good approximation, the degree of polarisation is given
by
sin2(γ)
DoP(γ) = d ,
max 1+cos2(γ)
where γ is the scattering angle. The DoP falls to zero toward the Sun and the
anti-solar point, where γ = 0◦ or 180◦, respectively, and rises to its maximum value,
d , at a scattering angle of γ = 90◦, along the band of sky that lies a quarter turn
max
from the Sun.
The peak value d is determined by atmospheric conditions and typically lies
max
between 0.7 and 0.8 under clear-sky conditions, decreasing as haze or thin cloud
introduces additional unpolarised light. Since the electric field of singly scattered
light lies perpendicular to the scattering plane, the angle of polarisation at each
point is determined by the same geometry. This makes the polarisation pattern a
rigid function of the Sun’s position rather than of the local sky brightness.
ThepropertythatmattersfornavigationisthattheAoPpatterndependsmainly
on the position of the sun and is far less sensitive to atmospheric turbidity, haze, or
thin cloud than the sky radiance itself. The geometric relationship between the AoP
and the solar position holds across a wide range of conditions. This is presumably
why insects evolved a compass based on polarization rather than on intensity, since
polarization carries the more reliable directional information. Gkanias et al. [5] note
that the degree of polarisation and the intensity of skylight carry complementary
information, and that using both signals together improves compass performance in
adverse conditions.
In the dome and camera system used in this thesis, the polarizing film at each
position transmits the incoming skylight according to Malus’s law [30]. If the local
sky has an angle of polarisation AoP and a degree of polarisation DoP, and the film
transmission axis at that position makes an angle α with the reference direction,

| 3.3 SKY  | POLARIZATION |           |                            |     | 22  |
| -------- | ------------ | --------- | -------------------------- | --- | --- |
| then the | transmitted  | intensity | is given by                |     |     |
|          |              | I = I     | [0.5+0.5DoPcos(2(AoP−α))], |     |     |
out in
where I is the incident intensity. The transmitted intensity is highest where the
in
sky polarisation aligns with the film transmission axis and lowest where the two are
a quarter turn apart. Consequently, the recorded image becomes a map of how the
sky angle of polarisation is oriented relative to the film transmission axis across the
entire visible hemisphere. This is the model implemented in the synthetic image
| generator, | and it is | the model | the heading estimator | inverts. |     |
| ---------- | --------- | --------- | --------------------- | -------- | --- |
The way the film axes are arranged across the dome therefore fixes where the
low transmission band falls in the image. If a single flat filter with one fixed axis
is used, the band of low transmission is set by that fixed axis and sits across the
sky without regard to the sun, so it cuts across the solar position. If instead the
dome is built from gores whose axes are arranged radially, so that the transmission
axis at every azimuth points away from the zenith, the band of low transmission is
placed so that it points toward the sun. This is the reason the radial dome is the
target design rather than the flat filter, since it ties the most visible feature of the
image, the dark band, directly to the quantity the system exists to estimate. The
behaviour was checked by rendering the two cases with the polarization model, and
the earlier description of the dome as carrying a distributed set of polarization axes
should be read specifically as this radial arrangement. The intensity pattern that
suits the circular mean algorithm developed from the biological model of Gkanias et
| al. [2] is | the one produced | by  | this radial dome. |     |     |
| ---------- | ---------------- | --- | ----------------- | --- | --- |

4 System Design
This chapter describes the physical design of the sky compass and the flow of data
through it. The account begins with the optical arrangement of the camera and the
polarizing material, moves to the geometry of the polarizing dome and the way it is
fabricated, then covers the camera and its mounting, and closes with an overview of
the processing pipeline that turns a captured image into a heading estimate. The
detailed methods for each processing stage are given in Chapter 5.
4.1 Optical architecture and build options
A fisheye camera points at the zenith and images the sky hemisphere through a layer
of linear polarizing film. Because a single linear polarizer transmits light according
to Malus’s law, the intensity that reaches each pixel depends on the angle between
the local sky polarisation and the transmission axis of the film in front of that part
of the sky. The spatial pattern of transmitted intensity across the image therefore
carries the sky polarization pattern, and with it the position of the sun.
Two build options were considered, and both are kept in the work because they
trade fidelity against ease of construction. The first is a flat sheet of polarizing
film held above the lens with a single fixed transmission axis across the whole field.
It is simple to build and to reason about, and it serves as the first prototype for
checking the capture chain and the estimation code. The second and target design
is a hemispherical dome assembled from petal shaped sections of film, called gores,

| 4.2 DOME | GEOMETRY |     |     | AND FABRICATION |     |     | 24  |
| -------- | -------- | --- | --- | --------------- | --- | --- | --- |
whose transmission axes follow a radial pattern so that the axis at each azimuth
points away from the zenith. The radial dome matches the fan like sampling of the
insect dorsal rim area more closely than a single flat filter, and as shown in Chapter
6 it places the low transmission band of the image in a more useful relationship to
the sun.
| 4.2 | Dome | geometry |     |     | and fabrication |     |     |
| --- | ---- | -------- | --- | --- | --------------- | --- | --- |
The dome is modelled as a hemisphere of radius R covered by N identical gores.
Each gore is a petal whose length from the base ring to the apex at the zenith equals
a quarter of the circumference of a great circle derived by standard circle geometry
| [31] and | is therefore |     | given | by: |     |     |     |
| -------- | ------------ | --- | ----- | --- | --- | --- | --- |
πR
|     |     |     |     |     | L = . |     |     |
| --- | --- | --- | --- | --- | ----- | --- | --- |
2
The width of each gore at the base is obtained by dividing the circumference of
| the hemispherical |     | base | by the | number | of gores: |     |     |
| ----------------- | --- | ---- | ------ | ------ | --------- | --- | --- |
2πR
|     |     |     |     |     | W = | ,   |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
N
where L is the gore length, W is the gore width at the base, R is the radius of
| the dome, | and | N is the | total | number | of identical | gores. |     |
| --------- | --- | -------- | ----- | ------ | ------------ | ------ | --- |
The width of a gore at a height corresponding to the polar angle phi measured
up from the base follows the same rule scaled by the cosine of phi, so each section
is widest at the base and tapers to a point at the apex where all N gores meet. The
prototype geometry uses R = 40mm and N equal to 8 since the number number of
gores would be equal to the 8 directions. It cleared the PiCAM360 where the half
diagonal is 26.9mm resulting the films standing not far from the lens that it’s rim
intrudes on the horizon. As a result, the gore length about 62.83mm and a width
of about 31.42mm wide at the base. These accurate measurements were taken in

4.2 DOME GEOMETRY AND FABRICATION 25
Figure 4.1: Construction sequence of the hemispherical polarising-film dome, from
the preparation of individual gore sections and camera positioning to the assembly
of the eight gores into the completed dome around the fisheye camera.
order to produce a prototype that is cost-effective as proposed. Therefore, resulting
in saving the cost of films quite substantially as previous estimations required half a
filmintherangeof200mmby150mmforasinglegore. Thefigure4.1showsthesteps
taken for the construction of the dome according to the predefined measurements
calculated above. The figure 4.2 shows the final prototype of the dome.
NOTE, expand in your own words (then delete this note): • Once
the dome is built, record its actual measured radius and gore count here,
and note any difference from the design figures. • This is where the
outside photo of the finished dome should go, as Paavo asked, once you
have taken it. [ Figure 4.1: gore template, sheet layout, and assem-
bled hemisphere from the dome cutting guide. Insert the diagrams from
dome_cutting_guide.html, or add the guide as an appendix.]
Fabrication follows a printable cutting guide that provides the petal template,
the sheet layout, and the assembly order. Before any film is cut, the transmission
axis of the film is found with a simple crossed polarizer test and marked on each
blank, because the optical function of the dome depends entirely on the axis of each

| 4.2 DOME | GEOMETRY    | AND FABRICATION |         |                    |      | 26  |
| -------- | ----------- | --------------- | ------- | ------------------ | ---- | --- |
|          | Figure 4.2: | Image of final  | version | of the constructed | dome |     |
gore being placed at the intended angle. The testing of the polarizing film is shown
| in figure | 4.3 |     |     |     |     |     |
| --------- | --- | --- | --- | --- | --- | --- |
Figure 4.3: Testing the polarizing film and confirming the polarity with respect to
| the direction | of the sun |     |     |     |     |     |
| ------------- | ---------- | --- | --- | --- | --- | --- |
The gores are then cut, their axes are checked once more against the template,
the sections are joined edge to edge with a small overlap, and the apex tips are
gathered and fixed at the zenith. A flat ring holds the base circle open and gives
| the dome | a stable surface | for mounting | over the | lens. |     |     |
| -------- | ---------------- | ------------ | -------- | ----- | --- | --- |

| 4.2 DOME | GEOMETRY | AND FABRICATION |     |     | 27  |
| -------- | -------- | --------------- | --- | --- | --- |
Figure 4.4: gore template, sheet layout, and assembled hemisphere from the dome
| cutting guide. |        |                 |              |           |     |
| -------------- | ------ | --------------- | ------------ | --------- | --- |
|                | Figure | 4.5: Final Dome | Construction | Prototype |     |

4.4 PROCESSING PIPELINE 28
4.3 Camera and mount
The camera is a PiCam 360 fisheye unit [32], chosen for its wide omnidirectional
field with a single camera system and its support under Linux. This device is used in
robotics, environmental monitoring, teleoperation, surveillance and computer vison
based research [33], [34], [35]. It is mounted with its optical axis vertical so that
the zenith falls at the image centre and the horizon falls on the circle at the edge
of the fisheye field. The mount records the heading of a fixed reference mark on
the camera body relative to the base, since the heading estimate produced by the
system is expressed relative to that mark and must be tied to a known direction
before it can be compared against the solar azimuth. The base is levelled so that
the assumed correspondence between image radius and sky angle holds without a
separate tilt correction. The radiometric settings on the camera are fixed rather
than automatic, for reasons set out in the next chapter.
4.4 Processing pipeline
The path from a raw image to a heading estimate has four stages. In capture,
a frame is acquired through the dome with fixed exposure and white balance. In
preprocessing, the sky region is isolated from the surrounding frame and each re-
tained pixel is associated with a sky direction through the fisheye calibration. In
estimation, the observed intensity pattern is compared against a family of modelled
patterns, one for each candidate heading, and the best match is selected together
with a measure of confidence. In validation, the estimated azimuth is compared
against the solar azimuth computed by the position model of Chapter 3 for the time
and place of capture. Each stage is described in detail in Chapter 5.
[ Figure 4.2: processing pipeline, from capture through preprocessing
and estimation to validation. ]

5 Methods
Thischaptersetsoutthemethodsusedateachstageofthepipeline,fromconfiguring
the camera to producing a heading estimate with an associated confidence, and it
explains how labelled data are generated for development and testing.
5.1 Camera configuration
ThecamerarunsonUbuntu,whereitscontrolsareexposedthroughtheVideo4Linux2
interface [36]. Exposure, gain, and white balance are set to fixed values rather than
being left under automatic control. This matters more here than in ordinary pho-
tography, because polarization imaging depends on the relative intensities recorded
across the frame, and any automatic adjustment that changes exposure or colour
balance between frames, or across regions within a frame, would alter those relative
intensitiesandcorruptthemeasuredpattern. Automaticwhitebalanceinparticular
is disabled, since it would otherwise shift the colour channels in response to the very
intensity variations that carry the signal.
NOTE, expand in your own words (then delete this note): • Record
the exact V4L2 values you fixed, exposure, gain, and white balance, so
the capture is reproducible.
Calibration ties image coordinates to sky angles. Under the equidistant model of
Chapter 3, a pixel at radius rho from the image centre corresponds to an angle theta
equal to rho divided by the scale factor a, and the direction of the pixel around the

| 5.1 CAMERA | CONFIGURATION |     |     | 30  |
| ---------- | ------------- | --- | --- | --- |
Figure 5.1: A bench test capture through the bare fisheye lens, taken at Turku on
26 July 2026 at 15:17 UTC at a resolution of 1600 by 1200 pixels in the YUYV
format, with exposure, gain and white balance fixed through Video4Linux2. The
polarising optic is not fitted and the optical axis is not vertical, so the frame is a
test of the capture chain and of the lens geometry rather than a sky measurement.
| The illuminated | disc has | a radius of approximately | 565 pixels. |     |
| --------------- | -------- | ------------------------- | ----------- | --- |
centre gives the azimuthal angle of the sky point. The centre of the fisheye circle
and the scale factor are found from a reference image in which the horizon ring is
visible at the edge of the field, so that the mapping from pixel to sky direction is
| fixed before | any polarization | measurement | is made. |     |
| ------------ | ---------------- | ----------- | -------- | --- |
The image in Figure 5.1 is a preliminary image captured with the bare fisheye
lens. At this point, the polarising optic had not yet been installed, and the optical
axis of the camera wasn’t aligned with zenith. It is therefore not to be seen as a
polarisation measurement, nor as the outcome of the sky-compass estimator. The

| 5.1 CAMERA | CONFIGURATION |     | 31  |
| ---------- | ------------- | --- | --- |
intent of this test, however, was to confirm the entire image-acquisition chain and to
look at whether the geometry of the real lens was consistent with the fisheye model
| used in | Section 3.2. |     |     |
| ------- | ------------ | --- | --- |
The test results showed that the camera was recognised correctly under Ubuntu,
andthatphotographscouldbetakenatthedesiredresolutionof1600×1200pixelsin
YUYV format[37]. Manual exposure, gain and white-balance could also be done via
Video4Linux2, andtheimagescouldbesavedandopenedupagainbytheprocessing
software. The test thus confirmed the full end-to-end acquisition pathway between
the physical image sensor, via the operating system camera interface, to an image
| that could | then be processed | further. |     |
| ---------- | ----------------- | -------- | --- |
The captured frame also gives a good test of the assumed fisheye geometry. The
usable image is an approximately circular area that is surrounded by a dark framed
area, where the horizon is close to the edge of the fisheye image. The straighter the
lines in the scene, the stronger the bend towards the image border (as in the balcony
rails). These are typical of the strong radial distortion likely to be found in a fisheye
lens and are consistent with employing the equidistant projection model described
| in Section | 3.2. |     |     |
| ---------- | ---- | --- | --- |
Perhaps more importantly, the physical image offers an immediate estimate of
the sampling angle of the camera employed in the experiments. The radius of the
lighted portion of the disc measured is about pixels. This radius represents
565
the angle (90◦) between the optical axis and the horizon, and results in an angular
| resolution | of about |     |     |
| ---------- | -------- | --- | --- |
90◦
0.159◦/pixel.
≈
565
Since the apparent angular diameter of the Sun is approximately 0.53◦, the solar
| disc would | occupy only |     |     |
| ---------- | ----------- | --- | --- |

5.1 CAMERA CONFIGURATION 32
0.53◦
≈ 3.3 pixels
0.159◦/pixel
across the captured image. A measurement on the same order of magnitude as
the 0.19◦ per pixel and around 2.8-pixel solar diameter calculated in Section 3.2
using the parameters of the previous lens built by the supervisor. This is why the
previous estimation is still representative, and the present estimation is based on
the physical camera that was employed during the experiments.
The bench test also showed that only successful image acquisition is not enough
for gaining polarisation measurement. The sky portion of Figure 5.1 is heavily
saturated, with an average intensity of 220 and about 1/3 of the sky pixels being
250 or higher. If a pixel is saturated, the differences in intensity of the incident
photons above the limit of the photon detector are lost and will not be recovered
during further processing. Such a frame might look good for the viewer, but will
not maintain the intensity variation needed for polarisation analysis. Selection of
the exposure was thus considered as a calibration step in itself. The exposure time
was bracketed experimentally and the longest exposure time that resulted in not
saturating the relevant part of the sky was chosen for the further measurements.
The inclusion of the polarising optic also affects the correct exposure. Ideal
linear polariser, by definition, will also decrease the amount of light that reaches the
sensor, and in reality, any polarising film will add additional losses and may affect
the colours recorded. Therefore, the exposure with the bare fisheye lens was not just
scaled and used again for the finished system. Instead, the final working exposure
was made with the polarising film in place so that the calibration would correspond
to the optical set-up for the actual sky-compass exposures.
Another practical problem was noted when using the manual camera controls.
When images were taken immediately after opening the imaging device, the bright-
ness of the same frame can vary significantly, even if the same exposure time was

5.3 ORIENTATION ESTIMATION 33
used; in one test, the difference in intensity between frames taken 3 seconds apart
was about 2.6. This was because the automatic camera settings were allowed to
continue for a short period of time until the manual settings were applied. The
acquisition process then discards a fixed number of initial frames of image data
following application of the camera controls and only stores an image for analysis.
5.2 Sun detection and pixel to azimuth mapping
The sun is not found by looking for its disk. As shown in Chapter 3, the solar
disk spans only about 2.8 pixels on this lens corresponding to an angular diameter
of approximately 0.53◦ [38], which is too small and too easily confused with cloud
edges and lens bloom to serve as a reliable target. The position of the sun is instead
recovered from the polarization pattern that fills the whole sky image, so that the
estimate draws on the entire hemisphere rather than on one small and fragile feature
[29].
Once a candidate solar azimuth has been produced in the image frame, it is con-
verted to a heading in the world frame using the fisheye calibration and the recorded
camera heading. Headings are expressed in the standard robot convention [39], mea-
sured clockwise from North, which differs by a fixed rotation of 180 degrees from
the South referenced azimuth used in the solar derivation of Section 3.1. The two
conventions are related by setting the North referenced azimuth equal to the South
referenced azimuth plus 180 degrees, reduced into the range from 0 to 360 degrees,
and every heading reported in this and later chapters uses the North convention.
5.3 Orientation estimation
Headingisestimatedwithamodelbasedsearch. Foreachcandidateazimutharound
the full circle, the expected intensity pattern that the dome would produce is ren-

5.4 SYNTHETIC DATA GENERATION 34
dered with the sky polarization model of Chapter 3, using the known sun elevation
for the time of capture. Each rendered pattern is compared against the observed
image by correlation, and the candidate whose rendered pattern correlates most
strongly with the observation is taken as the estimate. The sharpness of the correla-
tion peak provides a measure of confidence, since a sharp and isolated peak indicates
a well constrained estimate while a broad or multiple peak indicates an ambiguous
one [40]. A single fixed offset between the image reference mark and true North
is fitted once from calibration data and applied to every subsequent estimate. The
elevation of the sun is not estimated from the image but taken directly from the
ephemeris, since it is already known for the time and place of capture and does not
need to be recovered.
This estimator is related to the circular mean method of Gkanias et al, in that
both integrate polarization information across many sky directions into a single
azimuth rather than relying on any one measurement. The difference is that the
method here compares the whole observed image against a rendered model of the
dome, which allows the specific optical behaviour of the film and the geometry of
the dome to be built into the comparison. A learned regressor trained on synthetic
images is also considered, both as an alternative estimator and as a point of compar-
ison. It maps an image directly to an azimuth without the explicit search, and its
accuracy can be measured against the model based estimator on the same synthetic
data.
5.4 Synthetic data generation
Labelled data are useful for developing and testing the estimator before a sufficiently
large set of controlled real-world captures is available. However, ordinary intensity
images do not directly provide the polarisation information required to reproduce
the characteristic pattern produced by the polarising optic. For this reason, syn-

5.4 SYNTHETIC DATA GENERATION 35
thetic data were investigated during the development of the system. A numerical
generator was implemented using the sky-polarisation model and the polarising-film
transmission law described in the preceding sections. For a specified solar position,
the generator could render the theoretical intensity pattern expected from either
the flat polarising filter or the radial polarising dome. Since the solar position was
supplied directly to the generator, the corresponding solar azimuth and elevation
were known exactly within the simulation.
The solar positions considered by the generator were based on the calculated
solar trajectory over Turku during the period leading up to the capture campaign.
This allowed the simulation to consider solar geometries representative of the study
location rather than relying only on arbitrarily selected Sun positions. In particular,
the calculations included the range of azimuths and elevations produced by the high-
latitude solar trajectory described earlier in this thesis. The historical information
was therefore used to provide realistic solar geometry; it was not used as a source
of measured polarisation data.
The synthetic-data approach was useful for investigating how the proposed po-
larisation model and heading estimator behaved under controlled conditions. How-
ever, it was not adopted as the final route for experimental validation. Producing a
synthetic image that accurately represents a physical sky-compass capture requires
substantially more information than the position of the Sun. The observed pattern
depends on the orientation of the camera relative to the Sun and horizon, including
its heading, pitch, and roll, as well as the calibration and projection characteristics
of the fisheye lens. The orientation, placement, and transmission properties of the
polarising material also influence the intensity reaching the camera. In addition,
camera settings and characteristics such as exposure, gain, white balance, sensor
response, and saturation affect the resulting image.
Atmosphericconditionsintroducefurthervariablesthataredifficulttoreproduce

5.4 SYNTHETIC DATA GENERATION 36
accurately. The implemented model provides an idealised representation of skylight
polarisation, whereasrealobservationsmaybeaffectedbycloud, haze, aerosols, mul-
tiple scattering, reflections, and spatial variations in sky brightness. Simplifying or
incorrectly estimating any of these variables can therefore produce a synthetic image
that is consistent with the mathematical model but does not accurately represent
what is observed by the physical camera.
This limitation is particularly relevant when the synthetic images and the es-
timator are based on related geometric and physical assumptions. In such a case,
a small estimation error can demonstrate that the implementation behaves consis-
tently under the assumptions of the model, but it does not by itself demonstrate
equivalent accuracy in real outdoor conditions. The synthetic route was therefore
used only as a preliminary investigation of the proposed method. The final experi-
mental approach instead focused on images acquired using the physical camera and
optical system, where the estimator is exposed to the combined effects of the real
optics, camera response, alignment, and environmental conditions.

6 Results
This chapter reports the results. The sun geometry that the method must handle at
this latitude is described first, followed by the geometric justification for the radial
dome, and then the accuracy of the estimator in simulation and against captured
images. The experimental subsections are laid out here and will be completed as
the capture campaign proceeds.
6.1 Sun position coverage at Turku
Therangeofsunpositionsthemethodmusthandlewastakenfromthesolarposition
model for the two months leading up to the capture campaign. Across this period
the azimuth of the sun spans a very wide arc, and its elevation reaches only about
53 degrees at local noon around midsummer, which is a direct consequence of the
high latitude of Turku. The coverage is shown in figure 6.1.
The range of solar positions taken into account for the evaluation period are
described in figure 6.1 The left-hand side displays all the sun’s positions during the
day for each of these dates, for example, 14 May to 14 July 2026, sampled every
10 minutes. The horizontal axis is solar azimuth (clockwise from North) and the
vertical axis is solar elevation. During this time the solar azimuth ranges from about
35◦ to 325◦, that is about 290◦ of the entire compass circle. The evaluation therefore
tests the estimator with a wide range of headings that it could potentially see in its
out-of-doors operation, and not just a small sample of solar directions.

6.1 SUN POSITION COVERAGE AT TURKU 38
Figure 6.1: Daylight solar positions at Turku between 14 May and 14 July 2026,
sampled at ten minute intervals and coloured by day. Azimuth spans approximately
35 to 325 degrees and elevation reaches 53.0 degrees, which is the range of sun
geometry the compass is required to handle at latitude 60.45 degrees North. The
right panel shows the same positions projected onto the sky hemisphere, where the
radius is the zenith angle, so the centre of the plot is directly overhead.
The highest point that the sun ascends during the time interval is about 53.0◦.
The Sun’s elevation angle is thus, as a direct consequence of the latitude of Turku
60.45◦N, more than 37◦ away from the zenith even at the summer solstice. The
colour scale indicates the number of days since 14 May, and the seasonal evolution
can be seen. As the summer solstice nears the solar arcs grow further and further
out, and the peak days of high elevation occur during the solstice itself, after which
they start to recede and the solar arcs gradually shrink. The figure thus not only
reflects the various directions of the sun during the course of a day, but also the
different solar geometries over the two-month period under consideration.
The right side shows the same solar positions displayed as a hemispherical sky.
The projections in this projection display the zenith angle on the radial coordinate;
the centre of the chart is the zenith and the further out, the closer to the horizon.
The resulting solar trajectories form a broad band away from the centre of the
hemisphere. This gives a direct visualization of the high-latitude solar geometry;
the Sun is well off the zenith and its elevation angle stays mostly in the fringe of the
visible hemisphere of the sky in the course of the whole evaluation period.

6.2 DOME BAND GEOMETRY 39
The total number of daylight solar positions calculated over the evaluation win-
dow is 5972. The test set for evaluating the estimator in Section 6.3 was a random
sample of 60 of this population. Such samples of all daylight positions enable an
evaluation to be conducted for a variety of azimuths, elevations, times of day and
dates, and not just for a few hand picked solar positions.
Therelativelylowsolarelevationalsohadsomepracticalimplicationsforoutdoor
image capture. A maximum elevation of some 53◦ indicates that the Sun never rises
highabovethehorizoninthesummertime,eveninthemostclearandsunnysummer
days in Finland. In reality, this results in longer shadows than at lower latitudes and
makes the brightest part of the sky further away from the centre point of the image
and closer to the horizon in a zenith facing fisheye shot. This is especially the case
for exposure and dynamic range, as the bright areas near the horizon can compete
with much darker areas of the sky. This experience showed that it is important to
testthesky-compasssystemintherealsolargeometryoftheoperatingenvironment,
rather than by making assumptions for lower latitudes.
6.2 Dome band geometry
The geometric argument for the radial dome is shown by rendering the intensity
pattern that each build option produces. A single flat filter with a fixed transmission
axisplacesabandoflowtransmissionacrossthesky,orientedbythefixedaxisrather
than by the sun, so the band sits across the solar position. A radial dome, whose
transmission axis points away from the zenith at every azimuth, instead places the
band so that it points toward the sun, which ties the most visible feature of the
image directly to the quantity being estimated. The two geometries are compared
in figure 6.2, and a single captured time rendered as a synthetic frame is shown in
figure 6.3.
NEW. Points on the content of Figures 6.2 and 6.3, to expand into the

6.2 DOME BAND GEOMETRY 40
Figure 6.2: Modelled sky radiance through the polarising optic for a sun azimuth
of 135 degrees and an elevation of 30 degrees, with image up corresponding to
North. The left panel is the single flat filter and the right panel is the radial gore
arrangement. The red circle marks the true solar position in both.
Figure 6.3: Synthetic frames rendered through the flat filter at the true solar posi-
tions for 21 June 2026 at Turku. The solar azimuth and elevation used to render
each frame are given above it and the red circle marks the resulting sun position
in the image. Because ordinary photographs record no polarisation information,
labelled frames for development and testing are produced in this manner from mea-
sured solar geometry.

6.2 DOME BAND GEOMETRY 41
paragraphs above (then delete this note): • Figure 6.2: both panels are
rendered for the same sun, azimuth 135 degrees and elevation 30 degrees,
so any difference between them comes from the optic alone and not from
the sky. • Figure 6.2: the four lobed pinwheel structure in both panels
comes from the factor cos(2(AoP minus alpha)) in Malus’s law, since the
transmitted intensity completes two full cycles as the analyser angle turns
once through the circle. • Figure 6.2: the flat filter produces markedly
higher contrast between its light and dark lobes, while the radial arrange-
ment produces a smoother and flatter field. • CHECK BEFORE YOU
WRITE: the existing prose in 6.2 states that the radial dome places the
dark band so that it points toward the sun. Look carefully at the right
panel against the red circle and confirm that the rendering actually shows
this. If what the figure shows is a difference of phase and contrast rather
than a band that points at the sun, the sentence must be softened to
match the figure. Do not leave a claim in the text that the reader can see
is not in the picture. • Figure 6.3: the four frames are 03:00, 07:00, 11:00
and 15:00 UTC on 21 June 2026, with the sun at azimuth 59, 111, 190
and 262 degrees and elevation 10, 38, 53 and 32 degrees respectively. •
Figure 6.3: the red circle moves clockwise around the image and inward
toward the centre as the elevation rises, reaching its closest approach at
11:00 when the sun is at 53 degrees, then moving outward again. This
is the equidistant projection of Section 3.2 doing exactly what it should.
• Figure 6.3: the whole intensity pattern rotates rigidly with the sun
rather than changing shape, and that rigidity is the property the estima-
tor exploits when it searches over candidate azimuths. • Figure 6.3: the
11:00 frame is visibly flatter than the others. Note that pattern contrast
falls as the sun climbs, which is one reason the elevation is supplied from

| 6.3 ESTIMATOR |           | ACCURACY    | IN        | SIMULATION    |        | 42  |
| ------------- | --------- | ----------- | --------- | ------------- | ------ | --- |
| the ephemeris |           | rather than | estimated | from the      | image. |     |
| 6.3           | Estimator | accuracy    |           | in simulation |        |     |
This section reports the azimuth error of the estimator on synthetic frames across
the full range of sun positions covered in Section 6.1. Because the synthetic frames
carry an exact ground truth, the error here isolates the behaviour of the estimator
| itself from | any error | in capture | or calibration. |     |     |     |
| ----------- | --------- | ---------- | --------------- | --- | --- | --- |
The estimator was evaluated on 60 solar positions drawn at random from the
5972realdaylightpositionsofSection6.1, underfourconditions: aclearskythrough
the flat filter, thin cloud, heavy cloud, and a clear sky through the radial gore dome.
| The results | are collected | in  | Table 6.1. |     |     |     |
| ----------- | ------------- | --- | ---------- | --- | --- | --- |
Table6.1: Absoluteazimutherrorindegreesover60solarpositionsdrawnatrandom
from 5972 real daylight positions at Turku between 14 May and 14 July 2026. The
film axis was 35 degrees and the image up heading 0 degrees throughout, with sensor
| noise of | 0.020 in | all four runs. |     |     |     |     |
| -------- | -------- | -------------- | --- | --- | --- | --- |
Condition Optic d Clutter Mean Median P90 Max. err. Within 5◦ Conf.
max
Clear Flatfilter 0.75 0.00 0.075 0.073 0.144 0.206 100.0% 1.78
Thincloud Flatfilter 0.45 0.30 0.984 0.671 2.252 4.125 100.0% 1.78
Heavycloud Flatfilter 0.20 0.60 16.259 3.254 14.519 179.657 60.0% 1.74
Clear Radialdome 0.75 0.00 0.075 0.074 0.130 0.224 100.0% 1.76

7 Discussion, Limitations, and
Future Work
This chapter reflects on what the design achieves, the conditions under which it is
expected to work, and the directions in which it could be extended.
7.1 Limitations
Several limitations follow directly from the design and should be stated plainly. The
first concerns the use of synthetic data. Because an ordinary photograph records
no polarization, historical real imagery cannot show the band that the dome pro-
duces, and synthetic frames rendered at real sun positions are used in its place for
development and for the simulation results. This is a reasonable substitute, but it
means that the simulation accuracy reflects the fidelity of the model rather than the
behaviour of the physical dome, and only the captured image validation of Section
6.4 tests the latter.
A single polarizing film also leaves a solar and antisolar ambiguity, because the
transmission pattern is symmetric under a rotation that exchanges the sun with
the point opposite it in the sky, and the estimator must resolve this ambiguity
rather than assume it away. The method further depends on a reasonably clear
view of some part of the sky, since it needs polarized skylight to read, and although
it tolerates broken cloud far better than a sun tracker would, a fully overcast sky

7.2 HIGH LATITUDE CONSIDERATIONS 44
with no polarization structure leaves it without a signal. Finally, any error in the
recorded camera heading maps directly onto the reported azimuth, so registration
of the camera to a known direction is as important as the estimation itself, and the
flat filter prototype, being lower in fidelity than the radial dome, is expected to give
correspondingly weaker estimates.
NEW. Two limitations to add to the paragraph above, in your own
words (then delete this note): • The confidence metric does not discrimi-
nate. The mean confidence reported in Table 6.1 varies by less than three
percent across conditions whose mean error differs by more than two or-
ders of magnitude, so the sharpness of the correlation peak, as currently
defined, does not distinguish a reliable estimate from a failed one. This
matters because the intended use of the confidence value was to weight
the heading within a fusion filter and to reject the solar and antisolar
failures, and neither is possible until the metric is redefined. Frame this
as a known and identified weakness with a clear route forward, since an
examiner will respect that far more than silence. • The synthetic and the
captured validations answer different questions, and this thesis answers
the first thoroughly and the second partially. The simulation establishes
internal consistency of the geometry, the search and the coordinate con-
ventions; only captured frames test whether the forward model resembles
the real sky. Frame the gap as scheduled rather than overlooked.
7.2 High latitude considerations
The site places particular demands on the method. At the latitude of Turku the
summer sun reaches only about 53 degrees above the horizon at noon and sweeps
through a very wide range of azimuths over the course of a day, so the estimator
is exercised across almost the whole azimuth circle but never sees a sun near the

7.3 FUTURE WORK 45
zenith. This differs from the middle and lower latitude conditions under which much
of the earlier work was carried out, and it is one reason the local sun geometry is
worth validating against directly. A useful extension would repeat the experiments
in October, when the sun is lower and follows a shorter and differently shaped daily
arc, so that the behaviour of the method can be checked under a second and quite
different sun geometry at the same site.
NOTE, expand in your own words (then delete this note): • Explain
in a sentence why October changes the arc, since the sun rises lower,
travels a shorter path, and sets sooner than at midsummer. • Note how
you plan to capture the sun then, for example the snapshots and the
annual movement video.
7.3 Future work
Several extensions follow from this work. The capture campaign could be repeated
in October as noted above, and extended to collect data during rain, so that the
effect of rain on the polarization pattern can be observed rather than assumed.
On the application side, a passive heading reference of this kind is of interest for
environmental monitoring and for other outdoor observation tasks where a robot
must hold a heading without a satellite fix.
On the method side, a tilt correction would remove the requirement for a level
base and could follow the approach taken in the hardware compass of Gkanias et al.
[5],andfusionwithaninertialmeasurementunitwouldlettheabsoluteheadingfrom
the sky compass bound the drift of the inertial estimate, using the covariance idea of
Stürzl[3]toweightthetwosourcescorrectly. Alearnedestimatortrainedonalarger
syntheticandrealdatasetcouldbecomparedagainstthemodelbasedestimator,and
the whole system could be cross checked against measured sky polarization datasets
and against the recent insect compass model of Gkanias and Webb [6] together with

| 7.3 FUTURE  | WORK     |                 | 46  |
| ----------- | -------- | --------------- | --- |
| the related | work now | in preparation. |     |
NOTE, expand in your own words (then delete this note): • Explain
briefly why rain interferes, since water on the film and droplets in the
air scatter and depolarise the light, and frame this as making the dome
| more versatile | for | poor weather. |     |
| -------------- | --- | ------------- | --- |

8 Conclusion
The goal of this thesis was to explore the possibility of providing an autonomous
heading reference for outdoor robot navigation using the polarisation pattern of
scattered skylight. The motivation was to provide absolute orientation information
as GNSS may not work when required and also insects like desert ants use polarised
skylight to keep their direction when moving. The goal was to develop a system that
was relatively simple and inexpensive to translate this biological principle into the
field of optics, using a fisheye camera and passive polarising material. A polarising
dome of radius 40 millimetres was designed, cut and assembled from eight gores
whose transmission axes were fixed by three independent observations and which
fan radially outward from the apex. A whole geometric structure was created to
link the position of the Sun with the picture captured by the camera. This involved
development of a solar-position model for Turku, an equidistant fisheye projection,
an equidistant model of sky polarisation (Rayleigh sky) and a model of the trans-
mission of polarized light through the polarizing optic. It was seen that both a flat
polarisingfilterandahemisphericaldomemadeofpolarising-filmgoreswithradially
oriented transmission axes could be considered. A prototype was built and tested
in camera to establish the image-acquisition chain and to obtain a realistic measure
of the angular sampling of the lens. A preliminary development tool was synthetic
data was considered. The estimator was found to produce very small errors for the
clear-sky and thin-cloud simulations, but its performance decreased significantly in

CHAPTER 8. CONCLUSION 48
the heavy-cloud simulation. The mean errors reported were 0.075◦ for the clear flat-
filter case, 0.984◦ for thin cloud, and 16.259◦ for heavy cloud, with just 60% of the
heavy-cloud estimates within 5. These are results obtained according to the assump-
tions of the forward model, and should not be interpreted as the accuracy of the
physical compass that will be completed. The thesis also acknowledges that the ac-
tual observations are also influenced by the alignment of the camera, response of the
camera’s sensor, optical properties, atmospheric scattering, clouds, haze etc. which
cannot be completely simulated. Additional significant limitations were also iden-
tified. Ambiguity in the polarisation pattern, the necessity of using some polarised
skylight, and the direct relation between the camera’s heading and the azimuth in
the method all lead to ambiguity in the reported azimuth. Furthermore, the present
confidence measure, which is derived from the sharpness of the peak of the correla-
tion, is not consistently different for successful estimates and failed estimates, and
thus is not effective for rejection of the measurement or weighting in sensor fusion.
It is noteworthy that the evaluation takes place in a high-latitude setting, which
offers a unique evaluation context for Turku. The Sun elevation is only around 53°
in the summer season used in this thesis and the Sun is seen almost over the entire
compass circle, so the system should perform throughout a large part of the compass
circle without a close passage of the Sun to the Zenith. This further emphasizes the
need to test celestial-navigation devices in the solar geometry of the site on which
they will be used, not on lower latitude conditions. Overall, the thesis provides the
theoretical, computational and physical basis for a bio-inspired sky compass, instead
of showing a fully validated replacement for any existing navigation sensors. It also
illustrates the possibility of integrating solar geometry, skylight polarisation, fisheye
imaging and a passive polarising optic into a single heading-estimation system and
provides insight into the challenges of transitioning from simulation to a physical
outdoor system. For future work, the extended outdoor test should be made, im-

| CHAPTER | 8. CONCLUSION |     |     |     | 49  |
| ------- | ------------- | --- | --- | --- | --- |
provement of the ambiguity and confidence estimation of the sky compass, camera
tilt correction and fusion of the sky compass and IMU so that the sky compass can
give an absolute heading reference to constrain the inertial drift. These directions
| are already | present | in the future | work section | of the thesis. |     |
| ----------- | ------- | ------------- | ------------ | -------------- | --- |

References
[1] H. Mouritsen, “Long-distance navigation and magnetoreception in migratory
| animals”, | Nature, | vol. | 558, | no. 7708, | pp. | 50–59, | 2018. |     |
| --------- | ------- | ---- | ---- | --------- | --- | ------ | ----- | --- |
[2] R. Muheim, F. R. Moore, and J. B. Phillips, “Calibration of magnetic and
celestialcompasscuesinmigratorybirds-areviewofcue-conflictexperiments”,
|         |                 |     |     | Biology, | vol. | 209, no. | 1, pp. 2–17, | 2006. |
| ------- | --------------- | --- | --- | -------- | ---- | -------- | ------------ | ----- |
| Journal | of Experimental |     |     |          |      |          |              |       |
[3] D. Sobel, Longitude: The true story of a lone genius who solved the greatest
scientific problem of his time. Bloomsbury Publishing USA, 2007.
[4] L.dePaulaVeronese,C.Badue,F.A.Cheein,J.Guivant,andA.F.DeSouza,
“A single sensor system for mapping in gnss-denied environments”,
Cognitive
| Systems | Research, |     | vol. 56, | pp. 246–261, |     | 2019. |     |     |
| ------- | --------- | --- | -------- | ------------ | --- | ----- | --- | --- |
[5] U. Steinhoff and B. Schiele, “Dead reckoning from the pocket-an experimental
study”, in 2010 IEEE international conference on pervasive computing and
|     |     | (PerCom), |     | IEEE, | 2010, | pp. | 162–170. |     |
| --- | --- | --------- | --- | ----- | ----- | --- | -------- | --- |
communications
[6] S. Thrun, “Probabilistic algorithms in robotics”, Magazine, vol. 21, no. 4,
Ai
| pp. 93–93, | 2000. |     |     |     |     |     |     |     |
| ---------- | ----- | --- | --- | --- | --- | --- | --- | --- |
[7] R.Wehner,“Desertantnavigation:Howminiaturebrainssolvecomplextasks”,
|         |                |     |            |     | A,  | vol. 189, | no. 8, pp. | 579–588, 2003. |
| ------- | -------------- | --- | ---------- | --- | --- | --------- | ---------- | -------------- |
| Journal | of Comparative |     | Physiology |     |     |           |            |                |
[8] R.Wehner,“Desertantnavigation:Howminiaturebrainssolvecomplextasks”,
Journal of Comparative Physiology A: Sensory, Neural, and Behavioral Phys-

REFERENCES 51
| iology, vol. | 189, | no. 8, | pp. 579–588, | Aug. | 2003. doi: |     |     |     |
| ------------ | ---- | ------ | ------------ | ---- | ---------- | --- | --- | --- |
10.1007/s00359-003-
0431-1.
[9] T. Labhart, “Specialized photoreceptors at the dorsal rim of the honeybee’s
compound eye: Polarizational and angular sensitivity”, Journal of comparative
| physiology, | vol. | 141, | no. 1, pp. 19–30, | 1980. |     |     |     |     |
| ----------- | ---- | ---- | ----------------- | ----- | --- | --- | --- | --- |
[10] E. Gkanias, B. Risse, M. Mangan, and B. Webb, “From skylight input to
behavioural output: A computational model of the insect polarised light com-
pass”, PLOS Computational Biology, vol. 15, no. 7, J. Ayers, Ed., e1007123,
| Jul. 2019. | doi: | 10.1371/journal.pcbi.1007123. |     |     |     |     |     |     |
| ---------- | ---- | ----------------------------- | --- | --- | --- | --- | --- | --- |
[11] W. Sturzl, “A lightweight single-camera polarization compass with covariance
estimation”,inProceedings
|         |           |            | of the | IEEE International |     | Conference |     | on Computer |
| ------- | --------- | ---------- | ------ | ------------------ | --- | ---------- | --- | ----------- |
| Vision, | 2017, pp. | 5353–5361. |        |                    |     |            |     |             |
[12] W.StürzlandN.Carey,“Afisheyecamerasystemforpolarisationdetectionon
uavs”, in European Conference on Computer Vision, Springer, 2012, pp. 431–
440.
[13] E. Gkanias, R. Mitchell, J. Stankiewicz, S. R. Khan, S. Mitra, and B. Webb,
“Celestial compass sensor mimics the insect eye for navigation under cloudy
and occluded skies”, Communications Engineering, vol. 2, no. 1, p. 82, 2023.
[14] E. Gkanias and B. Webb, “Spatiotemporal computations in the insect celestial
| compass”, |     | Communications, |     | vol. 16, | no. 1, | p. 2832, | 2025. |     |
| --------- | --- | --------------- | --- | -------- | ------ | -------- | ----- | --- |
Nature
[15] G.E.Kolyfetisetal.,“Fromeyeanatomytonavigation:Abiologicallyaccurate
| model of | bees’ | polarisation | vision”, | bioRxiv, | pp. 2026–06, |     | 2026. |     |
| -------- | ----- | ------------ | -------- | -------- | ------------ | --- | ----- | --- |
[16] E. Gkanias, G. Kolyfetis, M. Dacke, J. Foster, and B. Webb, “The celestial
compass of insects needs a single ray of skylight to find the sun”, Manuscript
| in preparation, |     | 2026. |     |     |     |     |     |     |
| --------------- | --- | ----- | --- | --- | --- | --- | --- | --- |

| REFERENCES |     |     |     |     | 52  |
| ---------- | --- | --- | --- | --- | --- |
[17] P. Vévoda, T. Bashford-Rogers, M. Kolářová, and A. Wilkie, “A wide spec-
| tral     | range sky radiance | model”,      | in       | Forum, Wiley | Online |
| -------- | ------------------ | ------------ | -------- | ------------ | ------ |
|          |                    |              | Computer | Graphics     |        |
| Library, | vol. 41, 2022,     | pp. 291–298. |          |              |        |
[18] evgkanias, Github - evgkanias/sky: Python package that implements models
|     |                       | 2022. | [Online]. Available: |                     |     |
| --- | --------------------- | ----- | -------------------- | ------------------- | --- |
| for | skylight information. |       |                      | https://github.com/ |     |
evgkanias/sky.
[19] A. Moutenet, L. Poughon, B. Toulon, J. R. Serres, and S. Viollet, “Opensky: A
modular and open-source simulator of sky polarization measurements”, IEEE
Transactions on Instrumentation and Measurement, vol. 73, pp. 1–16, 2024.
[20] I. Reda and A. Andreas, “Solar position algorithm for solar radiation applica-
| tions”, | energy, | vol. 76, no. | 5, pp. 577–589, | 2004. |     |
| ------- | ------- | ------------ | --------------- | ----- | --- |
Solar
[21] K. Fang, G. Yingjing, F. Xiaojing, G. Xiaohan, et al., “Review on bio-inspired
polarized skylight navigation”, Chinese Journal of Aeronautics, vol. 36, no. 9,
| pp. | 14–37, 2023. |     |     |     |     |
| --- | ------------ | --- | --- | --- | --- |
[22] S. B. Karman, S. Z. M. Diah, and I. C. Gebeshuber, “Bio-inspired polar-
ized skylight-based navigation sensors: A review”, Sensors, vol. 12, no. 11,
| pp.     | 14232–14261, 2012.  |          |               |     |     |
| ------- | ------------------- | -------- | ------------- | --- | --- |
| [23] G. | L. Hosmer, Azimuth. | J. Wiley | & sons, 1909. |     |     |
[24] J. H. Meeus, algorithms. Willmann-Bell, Incorporated, 1991.
Astronomical
[25] J. Kannala and S. S. Brandt, “A generic camera model and calibration method
forconventional,wide-angle,andfish-eyelenses”,IEEE transactions on pattern
analysis and machine intelligence, vol. 28, no. 8, pp. 1335–1340, 2006.
[26] S. Sun, J. Gao, D. Wang, T. Yang, and X. Wang, “Improved models of imaging
ofskylightpolarizationthroughafisheyelens”,Sensors,vol.19,no.22,p.4844,
2019.

| REFERENCES |     |     |     |     |     |     |     | 53  |
| ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
[27] B.Siciliano,O.Khatib,andT.Kröger,Springer robotics.Springer,
|            |      |     |     |     |     | handbook | of  |     |
| ---------- | ---- | --- | --- | --- | --- | -------- | --- | --- |
| 2008, vol. | 200. |     |     |     |     |          |     |     |
[28] C. F. Bohren and D. R. Huffman, Absorption and scattering of light by small
| particles. | John | Wiley | & Sons, | 2008. |     |     |     |     |
| ---------- | ---- | ----- | ------- | ----- | --- | --- | --- | --- |
[29] G.HorváthandD.Varjú,Polarized
|         |          |     |         |            | light in | animal vision: | polarization | patterns |
| ------- | -------- | --- | ------- | ---------- | -------- | -------------- | ------------ | -------- |
| nature. | Springer |     | Science | & Business | Media,   | 2004.          |              |          |
in
[30] P. Li, X. Lei, H. Cui, and L. Zhao, “Malus’s law and a dynamic three-polarizer
system”, The Physics Teacher, vol. 62, no. 4, pp. 302–304, 2024.
[31] D. Pedoe, Circles: a mathematical view. Cambridge University Press, 1995.
[32] 2017. [Online]. Available: https://www.picam360.com/equipment/list.
[33] W. Gao, K. Wang, W. Ding, F. Gao, T. Qin, and S. Shen, “Autonomous
aerial robot using dual-fisheye cameras”, Journal of Field Robotics, vol. 37,
| no. 4, | pp. 497–514, |     | 2020. |     |     |     |     |     |
| ------ | ------------ | --- | ----- | --- | --- | --- | --- | --- |
[34] Y.-W. Choi, K.-K. Kwon, S.-I. Lee, J.-W. Choi, and S.-G. Lee, “Multi-robot
mapping using omnidirectional-vision slam based on fisheye images”,
ETRI
| Journal, | vol. | 36, no. | 6, pp. | 913–923, | 2014. |     |     |     |
| -------- | ---- | ------- | ------ | -------- | ----- | --- | --- | --- |
[35] Y. Dong, M. Pei, L. Zhang, B. Xu, Y. Wu, and Y. Jia, “Stitching videos from
a fisheye lens camera and a wide-angle lens camera for telepresence robots”,
|               |     |         |           |     | Robotics, vol. | 14, no. | 3, pp. 733–745, | 2022. |
| ------------- | --- | ------- | --------- | --- | -------------- | ------- | --------------- | ----- |
| International |     | Journal | of Social |     |                |         |                 |       |
[36] M. H. Schimek, B. Dirks, H. Verkuil, and M. Rubli, “Video for linux two api
| specification”, |     | History, | vol. | 6, p. | 11, 1999. |     |     |     |
| --------------- | --- | -------- | ---- | ----- | --------- | --- | --- | --- |
[37] LinuxKernelDevelopers,V4L2_PIX_FMT_YUYV (’YUYV’),LinuxKernel
Documentation, Video4Linux2 API, YUV 4:2:2 packed pixel format, 2026.
| Accessed: | Jul. | 29, 2026. | [Online]. |     | Available: |     |     |     |
| --------- | ---- | --------- | --------- | --- | ---------- | --- | --- | --- |
https://www.kernel.org/doc/
html/latest/userspace-api/media/v4l/pixfmt-packed-yuv.html.

| REFERENCES |     |     |     |     | 54  |
| ---------- | --- | --- | --- | --- | --- |
[38] J. P. Rozelot, A. G. Kosovichev, and A. Kilcik, “A brief history of the solar
diameter measurements: A critical quality assessment of the existing data”,
| arXiv preprint | arXiv:1609.02710, | 2016. |     |     |     |
| -------------- | ----------------- | ----- | --- | --- | --- |
[39] A. Budiyono, “Principles of gnss, inertial, and multi-sensor integrated navi-
| gation systems”, |            |           |               | Journal, vol. | 39, no. 3, |
| ---------------- | ---------- | --------- | ------------- | ------------- | ---------- |
|                  | Industrial | Robot: An | International |               |            |
2012.
[40] J. Tonry and M. Davis, “A survey of galaxy redshifts. i-data reduction tech-
niques”, Astronomical Journal, vol. 84, Oct. 1979, p. 1511-1525., vol. 84,
| pp. 1511–1525, | 1979. |     |     |     |     |
| -------------- | ----- | --- | --- | --- | --- |

| Appendix | A Full | Weekly | Results |
| -------- | ------ | ------ | ------- |