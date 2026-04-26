# Working Notes: How To Frame The Pressure-Strain Results

Date: 2026-04-25

These are working notes for writing the thesis. They are not polished chapter
text. The goal is to keep the story simple, honest, and mechanically clear.

Do not describe the model-resolved tensor work as an unquestionable truth standard. Use:

- model-resolved tensor work
- model-resolved internal work
- finite-element tensor work
- tensor-work reference

## The Main Story

The most principled result is the single-simulation regional ratio analysis.

It asks a clean mechanics question:

> In one fixed simulated heart, do pressure-strain proxies preserve how work is
> distributed between regions?

This does not require pretending that the pressure sweep is a real PAH disease
trajectory. It is just a controlled comparison inside one simulated state.

The answer is:

> Free walls behave like one-pressure walls. The adjacent-cavity pressure proxy
> works reasonably well there. The septum is different because it is shared
> tissue loaded from both sides. Septal magnitude is better described by a
> two-sided pressure scale than by transmural pressure alone.

The pressure sweep is still useful, but it should be framed as a sensitivity
experiment:

> The pressure sweep tests how proxy rankings change along one controlled
> loading path. It is not a clinical PAH progression and not a patient cohort.

## What We Should Not Say

Do not say:

- "We simulated PAH progression."
- "This identifies the best clinical pressure for septal work."
- "The tensor work is the true biological work."
- "Transmural pressure is wrong."
- "The pressure sweep proves what happens clinically."

Better:

- "We performed a controlled RV pressure-loading experiment."
- "The ranking of proxies depends on the loading path."
- "The model-resolved tensor work is used as a reference quantity."
- "Transmural pressure is meaningful for septal shape and pressure difference,
  but it is not a robust proxy for septal work magnitude."
- "Clinical interpretation requires caution because geometry, wall thickness,
  stiffness, activation, and loading covary in real disease."

## Two Different Questions

A lot of confusion came from mixing two questions.

Question 1:

> Does a proxy preserve regional work magnitudes inside one simulation?

This is a ratio question. Example:

```text
model-resolved LV/RV work-density ratio
versus
proxy LV/RV work-density ratio
```

Question 2:

> Does a proxy rank cases correctly across a pressure sweep?

This is a correlation question.

These are both useful, but they are not the same. A proxy can rank a sweep well
and still fail at preserving regional magnitudes. The septum shows this clearly.

## Result 1: Free Walls Are The Clean Case

When we compare only LV free wall and RV free wall, excluding the septum, the
adjacent-pressure proxy works well.

Single healthy free-wall case:

```text
model-resolved tensor work LV/RV: 3.97

longitudinal strain:
P_LV everywhere:      1.75
P_RV everywhere:      1.14
adjacent pressure:    4.79
waveform only:        1.16
P x geometry:         5.57
```

Corrected n=16 sweep, mean absolute LV/RV ratio error:

```text
longitudinal strain:
adjacent pressure:    0.21   best
P x geometry:         0.29
P_LV everywhere:      0.64
P_RV everywhere:      0.89
waveform only:        0.84
```

Interpretation:

> In the free walls, each region is mainly loaded by its adjacent cavity. The
> natural pressure choice is therefore P_LV for the LV free wall and P_RV for
> the RV free wall. This is the domain where the pressure-strain proxy makes
> the most mechanical sense.

Useful figure paths:

```text
/home/dtsteene/D1/cardiac-work/results/analysis/freewall_ratio/fig_freewall_single_case_ratio.pdf
/home/dtsteene/D1/cardiac-work/results/analysis/freewall_ratio/fig_freewall_ratio_spectrum.pdf
```

Script:

```text
/home/dtsteene/D1/cardiac-work/freewall_ratio_proxy_test.py
```

## Result 2: Including The Septum Breaks The Simple LV/RV Ratio

The earlier tau-split LV/RV ratio included septal tissue. That made the regional
comparison harder because the septum is not cleanly LV wall or RV wall.

Laplace tau split, single case:

```text
model-resolved tensor work LV/RV: 2.53

fiber strain:
P_LV everywhere:        1.78
P_RV everywhere:        1.28
adjacent pressure:      5.28
adjacent waveform only: 1.28

longitudinal strain:
P_LV everywhere:        1.69
P_RV everywhere:        1.15
adjacent pressure:      4.71
adjacent waveform only: 1.14
```

Interpretation:

> Once septal/shared-wall tissue is included, the simple "each side gets its
> adjacent pressure" rule over-amplifies the LV/RV work ratio. This is not
> because pressure is always useless. It is because the septum is not a
> one-pressure free wall.

Useful figure path:

```text
/home/dtsteene/D1/cardiac-work/results/analysis/cascade/fig_regional_ratio_waveform.pdf
```

Script:

```text
/home/dtsteene/D1/cardiac-work/regional_ratio_waveform_test.py
```

## Result 3: The Septum Is A Shared-Wall Problem

Engineering picture:

```text
free wall:
one cavity pressure pushes one wall

septum:
LV pressure pushes one side
RV pressure pushes the other side
the tissue is constrained by both ventricles
```

For the septum, the pressure difference:

```text
P_LV - P_RV
```

is important for net force, curvature, and bowing. But tissue work is local
stress times local strain. If both cavities press on the septum, the tissue can
be loaded even when the pressure difference is small.

Simple example:

```text
Case A: P_LV = 100, P_RV = 10, difference = 90
Case B: P_LV = 100, P_RV = 80, difference = 20
```

The septum may bow less in Case B because the pressure difference is smaller.
But that does not mean the septal tissue is unloaded. It is still compressed and
constrained by both ventricles.

Short sentence to use:

> Transmural pressure is a good candidate for septal displacement and curvature.
> It is not automatically the best scalar stress scale for septal tissue work.

## Result 4: Septal Magnitudes Prefer A Two-Sided Pressure

We tested fixed septal pressure choices:

```text
P_LV
P_RV
P_LV - P_RV
mean(P_LV, P_RV)
nearest-side pressure through the septum
tau-weighted pressure through the septum
```

The important part is that these are fixed formulas, not fitted formulas.

Corrected n=16, longitudinal strain:

```text
correlation with septum total tensor work:
P_LV:        r = 0.932
Mean:        r = 0.837
Transmural:  r = 0.819

septum/free-wall ratio error:
Mean:        0.182   best
TauWeighted: 0.182
NearestSide:0.183
P_LV:        0.289
Transmural:  0.818   bad
```

Corrected n=16, fibre strain:

```text
correlation with septum total tensor work:
Mean:        r = 0.984
TauWeighted: r = 0.982
P_LV:        r = 0.974
Transmural:  r = 0.877

septum/free-wall ratio error:
NearestSide: 0.115   best
TauWeighted: 0.121
Mean:        0.123
Transmural:  0.782   bad
```

Interpretation:

> For septal work magnitudes, a two-sided pressure scale is more stable than
> transmural pressure. Mean pressure and through-wall weighted pressure are both
> mechanically defensible because the septum is loaded from both sides.

Useful figure paths:

```text
/home/dtsteene/D1/cardiac-work/results/analysis/septum_mechanics/fig_septum_lambda_scan.pdf
/home/dtsteene/D1/cardiac-work/results/analysis/septum_mechanics/fig_septum_layer_work.pdf
```

Scripts:

```text
/home/dtsteene/D1/cardiac-work/septum_mechanics_proxy_test.py
/home/dtsteene/D1/cardiac-work/septum_proxy_robustness_old_new.py
```

## Result 5: Old Data Versus Corrected Data

The old handover data had an unrealistic LV pressure drop. In that dataset,
transmural pressure looked best for septal correlations.

But that does not make transmural pressure a robust septal work proxy.

Old handover n=7, longitudinal strain:

```text
correlation with septum total tensor work:
Transmural:  r = 0.982
P_LV:        r = 0.874
Mean:        r = 0.496

septum/free-wall ratio error:
Transmural:  0.757   bad
P_LV:        0.391
Mean:        0.257
TauWeighted: 0.255   best-ish
```

Corrected n=16, longitudinal strain:

```text
correlation with septum total tensor work:
P_LV:        r = 0.932
Transmural:  r = 0.819
Mean:        r = 0.837

septum/free-wall ratio error:
Transmural:  0.818   bad
P_LV:        0.289
Mean:        0.182
TauWeighted: 0.182   best-ish
```

This gives a very useful interpretation:

> Transmural pressure can win a correlation in one particular pressure sweep,
> especially when the LV pressure path changes. But it does not preserve septal
> magnitude ratios in either old or corrected data. Mean/two-sided pressure is
> more robust for the magnitude question.

Useful figure path:

```text
/home/dtsteene/D1/cardiac-work/results/analysis/septum_proxy_robustness/fig_septum_proxy_old_new_ratio_error.pdf
```

## Result 6: Waveform-Only Is A Diagnostic, Not Work

Pressure-strain work can be factored as:

```text
integral P(t) dε = P_peak * integral [P(t) / P_peak] dε
```

The second term is the pressure-normalized loop area. It keeps timing and shape,
but removes pressure magnitude.

This is useful diagnostically:

> It tells us whether strain happens during high-pressure or low-pressure parts
> of the beat.

But it is not a work proxy by itself, because stress magnitude has been removed.

In the free-wall ratio test, waveform-only performed poorly:

```text
corrected n=16 free-wall LV/RV ratio error, longitudinal strain:
adjacent pressure: 0.21
waveform only:     0.84
```

Interpretation:

> Pressure magnitude is needed for free-wall work ratios. Removing pressure
> magnitude destroys the work interpretation. Waveform-only is useful for
> decomposing the proxy, not for replacing it.

## Result 7: Bulk Geometry Scaling Did Not Rescue The Proxy

We tested a simple clinically measurable geometry correction:

```text
proxy = P * (cavity volume / wall volume) * strain loop
```

This was motivated by a bulk Laplace-style idea.

For the tau-split single case, it made the LV/RV ratio worse:

```text
model-resolved tensor work LV/RV: 2.53

fiber strain:
adjacent pressure:      5.28
waveform only:          1.28
P x geometry:           6.81
geometry x waveform:    1.65
```

For the free-wall corrected n=16 ratio, it was close but not better than
adjacent pressure:

```text
longitudinal strain mean abs LV/RV ratio error:
adjacent pressure: 0.21
P x geometry:      0.29
```

Interpretation:

> A simple global cavity-volume/wall-volume correction is not enough. If a
> geometry-corrected stress proxy is needed, it likely needs local wall
> thickness, curvature, and the septal two-sided loading condition.

Script:

```text
/home/dtsteene/D1/cardiac-work/geometry_scaled_proxy_test.py
```

## How To Talk About Laplace

Do not say Laplace's law is wrong.

Better:

> Laplace's law applied to the septum gives a relation between pressure
> difference, curvature, wall thickness, and net force balance. That is relevant
> for septal shape. But myocardial work depends on the local stress state inside
> the tissue, and in a shared wall that stress state is influenced by both
> cavity pressures.

Shorter:

> Transmural pressure helps explain where the septum moves. It does not by
> itself give the best stress scale for how much work septal tissue does.

## How To Frame The Pressure Sweep

The pressure sweep is not the main proof. It is a sensitivity experiment.

Good framing:

> The sweep varies circulation while keeping anatomy and material properties
> fixed. This isolates one loading path. It is useful for testing sensitivity of
> proxy rankings, but it should not be interpreted as PAH progression.

Why this matters:

Real PAH changes many things together:

- RV pressure
- RV volume
- RV wall thickness
- septal curvature
- myocardial stiffness
- activation and contractility
- fibrosis/remodelling
- valve flow
- ventricular interaction

Our fixed-geometry pressure sweep changes only part of this system. It samples
one artificial line through a high-dimensional space.

So the pressure sweep supports this claim:

> Correlation-based proxy rankings are loading-path sensitive.

It should not support this stronger claim:

> This is the best proxy for clinical PAH patients.

## Suggested Thesis Structure

### 1. Start With The Mechanics Question

Pressure-strain methods replace regional stress with a pressure signal. This is
simple and clinically attractive, but it assumes cavity pressure is a good
regional stress scale.

The model lets us test that assumption.

### 2. First Test: Single-Simulation Regional Ratios

This is the cleanest result.

Ask:

> Does the proxy preserve the distribution of work between regions?

Find:

> Free walls are tracked reasonably well by adjacent pressure. The septum is
> not, unless it is treated as shared-wall tissue.

### 3. Explain Free Wall Versus Septum

Free wall:

```text
one pressure boundary
one adjacent cavity
adjacent pressure makes mechanical sense
```

Septum:

```text
two pressure boundaries
shared tissue
pressure difference affects shape
two-sided pressure better preserves work magnitude
```

### 4. Then Use The Pressure Sweep As A Sensitivity Study

Ask:

> If we change the loading path, do correlation rankings remain stable?

Find:

> No. The old and corrected sweeps give different ranking behaviour. This is a
> warning that correlation results are conditional on the chosen hemodynamic
> path.

### 5. Clinical Discussion

Make the limitation explicit:

> The fixed-geometry pressure sweep is not a clinical PAH cohort. It is a
> controlled loading experiment.

Then say why it still matters:

> It reveals which assumptions in pressure-strain proxies are mechanically
> safe, and where they break.

## Claims We Can Make With Confidence

Strong claims:

- The free-wall LV/RV work-density ratio is much better preserved by adjacent
  pressure than by using LV pressure everywhere or RV pressure everywhere.
- The septum should not be treated as either an LV free wall or an RV free wall.
- Transmural pressure is not robust for preserving septum/free-wall work
  magnitudes.
- Mean/two-sided septal pressure is more stable for magnitude preservation.
- Correlation-based rankings across pressure sweeps are sensitive to the chosen
  hemodynamic path.

Moderate claims:

- The pressure sweep is useful as a controlled loading-path sensitivity test.
- A better septal proxy likely needs to include both cavity pressures.
- Fibre strain plus a two-sided pressure scale gives a strong septal result in
  this model.

Claims to avoid or soften:

- Any claim that the pressure sweep represents real PAH progression.
- Any claim that one septal pressure formula is clinically best.
- Any claim that the current mesh resolves transmural septal structure
  perfectly.
- Any claim that the bulk geometry proxy solves regional stress estimation.

## Open Follow-Up Ideas

Patient/thickness mesh test:

```text
healthy mesh + healthy pressure
healthy mesh + PAH pressure
PAH/thicker mesh + healthy pressure
PAH/thicker mesh + PAH pressure
```

Questions:

- Does adjacent pressure still track free-wall work?
- Does RV wall thickening reduce model-resolved RV work relative to pressure?
- Does strain already capture that reduction?
- Does geometry correction help or hurt?

Septum resolution test:

- A higher-resolution septal mesh would make the through-wall pressure/layer
  analysis more trustworthy.
- Current LV-side/middle/RV-side septal layers are useful diagnostics, but they
  should not be over-sold.

Possible future septal proxy:

```text
P_septum = mean(P_LV, P_RV)
```

or:

```text
P_septum(x) = tau(x) weighted pressure through the wall
```

But this should be presented as a mechanistic candidate, not a final clinical
method.

## One Paragraph Version

The model results suggest that pressure-strain proxies work best in the setting
they implicitly assume: a free wall loaded by one adjacent cavity. In the LV and
RV free walls, adjacent-cavity pressure preserves the LV/RV work-density ratio
reasonably well. The septum is different because it is shared tissue loaded from
both sides. There, transmural pressure is meaningful for net force and septal
shape, but it does not preserve septal work magnitudes. A two-sided pressure
scale, such as mean or through-wall weighted pressure, is more stable for
septum/free-wall magnitude ratios. Correlation rankings across a pressure sweep
are more fragile: they changed when the LV pressure path was corrected. The
pressure sweep should therefore be interpreted as a controlled loading-path
sensitivity study, not as PAH progression.
