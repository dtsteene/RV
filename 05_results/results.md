(chap-results)=
# Results

The results are easiest to understand if two questions are kept separate. First: does the pressure-strain proxy get the size of regional differences right? Second: when the circulation is changed while geometry is held fixed, does the proxy rank loading cases in the same order as the finite-element stress-strain work density? These are both useful questions, but they are not the same. A proxy can rank a pressure sweep well and still give the wrong regional balance in a single patient.

For that reason this chapter starts with the regional ratio analysis. This is the cleaner mechanics test. It does not require treating the pressure sweep as a real disease trajectory, and it does not depend on whether the hemodynamic axis chosen for the sweep is clinically typical. It asks only whether the pressure-strain construction preserves relative work-density magnitudes in a fixed model state. The pressure sweep is then used as a controlled loading experiment, asking whether the same proxies rank loading cases in the same order as the finite-element work reference.

Unless stated otherwise, the results below use the high-resolution capped-reference pressure-loading sweep described in {ref}`chap-calibration`. This sweep was run at 5 mm characteristic mesh length, all 16 cases completed canonical postprocessing, and all pressure and per-cell work arrays passed finite-value checks. In that sweep the biventricular geometry, material parameters, boundary conditions, activation waveform, and end-diastolic mesh target are held fixed, while the circulation parameters are changed to raise RV pressure over a controlled range. The RV end-diastolic pressure used only for inverse unloading is capped at 5 mmHg to avoid the severe RV reference collapse observed in the uncapped fixed-geometry pilot. Case names such as `sPAP55` are nominal calibration labels; pressure axes, correlations, and proxy calculations use the achieved pressures and volumes from the coupled finite-element/circulation simulations. All pressure-strain proxies use the solver cavity pressures returned by the volume-constrained mechanics problem, not the standalone 0D elastance pressures.

The chapter follows five steps. It first defines the density and ratio metrics, then asks what the finite-element stress-strain work contains. It next tests the free walls, where each wall has one adjacent pressure. It then turns to the septum, where pressure assignment and strain direction are both ambiguous. Finally, it summarizes the numerical checks that support the interpretation.

The comparisons should be read as tests of simplification. The finite-element stress-strain work is the model-side reference, not patient-level ground truth. The question is how much of that reference survives when regional mechanics are reduced first to a scalar pressure scale and then to one longitudinal strain component.

The ratio tests use simple formulas. For two regions $A$ and $B$, the finite-element work-density ratio is

$$
R_\text{FE}(A,B) = \frac{w_\text{int}(A)}{w_\text{int}(B)},
\qquad
w_\text{int}(A)=\frac{W_\text{int}[\Omega_A]}{|\Omega_{A,0}|},
$$

and the clinical-style proxy ratio is

$$
R_\text{proxy}(A,B) = \frac{w_\text{PS}(A)}{w_\text{PS}(B)}.
$$

Here $W_\text{int}[\Omega_A]$ is the volume-integrated stress-strain work over region $\Omega_A$, and $|\Omega_{A,0}|$ is that region's reference volume. Both $w_\text{int}$ and the pressure-strain loop area $w_\text{PS}$ are density-like quantities with units of pressure: J/m$^3$ = Pa, reported here in kPa. The pressure-strain proxy is already treated as a density-like index, so it has no additional regional volume factor.

Two ratio errors are used. For the free-wall LV/RV comparison, the reported error is the absolute difference $|R_\text{proxy}-R_\text{FE}|$. For the septum, two ratios are tested in each case, septum/LV-free-wall and septum/RV-free-wall, and the reported error is a mean absolute log ratio error,

$$
\eta_\text{ratio}
= \left\langle
\left|
\log \left(
\frac{R_\text{proxy}}{R_\text{FE}}
\right)
\right|
\right\rangle .
$$

This scale is multiplicative: $\eta_\text{ratio}=0$ is exact, while $\eta_\text{ratio}=0.18$ corresponds to a typical ratio error of about $\exp(0.18)-1 \approx 20\%$.

Throughout the chapter, the longitudinal-strain proxy uses the tangent-longitudinal definition from {ref}`sec-work-definitions`. The raw apico-basal direction is projected into the local wall tangent plane before evaluating $\varepsilon_{ll}$, so the proxy does not count the through-wall component of the LDRB apex-gradient field as longitudinal strain. Fibre-aligned diagnostics use the model-side Green-Lagrange fibre strain $E_{ff}=\mathbf{E}:(\mathbf{f}_0\otimes\mathbf{f}_0)$ and are treated as mechanical checks rather than competing clinical proxies.

These ratios are tested first in the free walls, where pressure assignment is simple, and then in the septum, where it is not.

```{figure} ../figures/fig_5_0_freewall_vs_septum_schematic.png
:name: fig-freewall-septum-schematic
:width: 85%

The pressure assignment is mechanically simple for a free wall and ambiguous for the septum. A free wall has one adjacent cavity pressure. The septum is shared tissue with LV pressure on one face and RV pressure on the other, so pressure difference, mean pressure, and through-wall weighted pressure are all mechanically plausible but answer different questions.
```

Before comparing pressure-strain proxies with the finite-element work reference, it is useful to ask what the stress-strain contraction contains. In the local fibre-sheet-normal basis, the full contraction can be decomposed into fibre, sheet, sheet-normal, and cross terms. These are signed contributions relative to the net regional work density: a negative component subtracts from the net work rather than representing a separate positive share. Across the primary pressure-loading sweep, the free walls were strongly fibre dominated, with the fibre term accounting for about 89% of LV free-wall work density and 94% of RV free-wall work density on average.

The septum was less one-dimensional. Fibre work was still the largest component, about 80% of net septal work density on average, but sheet-normal work was much larger than in the free walls and cross-axis terms changed in several high-load cases. This matters for interpretation: a single strain direction can track part of the work trend because fibre work moves closely with total stress-strain work, but it does not contain the full septal mechanical accounting. The septum is therefore difficult not only because its pressure scale is ambiguous, but also because more of its work is carried outside one strain direction.

```{figure} ../figures/fig_5_0b_work_components_vs_rvsp.png
:name: fig-work-components
:width: 95%

Component breakdown of finite-element stress-strain work density across the primary capped-reference pressure-loading sweep. Work density is decomposed in the local fibre-sheet-normal basis. Fibre work dominates the free-wall trends, while the septum has a larger sheet-normal and cross-axis contribution. This is the first warning that a one-direction pressure-strain proxy is mechanically cleaner in the free walls than in the septum.
```

(sec-results-freewalls)=
## Free Walls

The simplest case is the comparison between the LV free wall and the RV free wall. Each free wall faces one cavity, so the pressure assignment is mechanically natural: $p_\text{LV}$ for the LV free wall and $p_\text{RV}$ for the RV free wall. This is the cleanest setting for the pressure assignment; failure here would point to a more basic limitation than septal pressure ambiguity.

For the lowest-pressure UKB baseline case in the primary sweep, the finite-element stress-strain work density in the LV free wall was 3.77 times the RV free-wall value. The tangent-longitudinal proxy using adjacent cavity pressure gave an LV/RV ratio of 4.24. This is not exact, but it is much closer than assigning the same pressure to both free walls. Using LV pressure everywhere gave a ratio of 2.01, and using RV pressure everywhere gave 1.19. Removing the pressure magnitude and keeping only the normalized waveform also lost the LV/RV balance, giving 1.29. The result is shown in {numref}`fig-freewall-single`.

```{figure} ../figures/fig_5_1_freewall_single_case_ratio.png
:name: fig-freewall-single
:width: 90%

Free-wall LV/RV work-density ratio in the lowest-pressure UKB baseline case. The dashed line is the finite-element stress-strain work-density ratio. For the longitudinal-strain proxy, adjacent cavity pressure gives the closest ratio; using one pressure everywhere or removing pressure magnitude loses the LV/RV work-density balance.
```

The same pattern holds across the primary pressure-loading sweep. The mean absolute error in the free-wall LV/RV ratio was 0.23 for the adjacent-pressure tangent-longitudinal proxy, compared with 0.59 for LV pressure everywhere, 0.81 for RV pressure everywhere, and 0.77 for the pressure-normalized waveform-only index. The sweep result is shown in {numref}`fig-freewall-spectrum`. Adjacent cavity pressure remains the best of the tested longitudinal pressure assignments for the free-wall ratio.

```{figure} ../figures/fig_5_2_freewall_ratio_spectrum.png
:name: fig-freewall-spectrum
:width: 95%

Free-wall LV/RV work-density ratio across the primary capped-reference pressure-loading sweep. The adjacent-pressure longitudinal proxy follows the finite-element stress-strain work-density ratio better than the alternatives. The pressure-normalized waveform-only index preserves timing information but not work-density magnitude.
```

A scatter view of the same comparison is shown in {numref}`fig-freewall-ratio-scatter`. This makes the difference between correlation and magnitude easier to see. Several pressure choices rank the cases in a similar order, but the adjacent-pressure points lie closest to the identity line.

```{figure} ../figures/fig_5_2c_freewall_ratio_scatter.png
:name: fig-freewall-ratio-scatter
:width: 95%

Scatter comparison between pressure-strain proxy LV/RV ratios and finite-element stress-strain LV/RV ratios in the primary capped-reference sweep. Each panel shows one longitudinal pressure assignment. The solid line is a least-squares regression, the dashed line is the identity line, and colour denotes achieved RV systolic pressure. A high correlation alone is not enough; the useful proxy should also lie near the identity line.
```

The free-wall ratio test asks whether the proxy preserves regional magnitudes. The next question is whether pressure-strain also ranks loading cases better than pressure or strain alone.

This RV free-wall ranking result connects the model to the recent clinical validation by Lakatos et al. {cite}`lakatos2024right`. Their endpoint was invasive RV contractility, whereas the endpoint here is finite-element RV free-wall stress-strain work density, so the comparison is not a reproduction of their pressure-volume analysis. It is instead the finite-element analogue of the same pressure-correction idea.

Across the primary sweep, the RV pressure-longitudinal-strain index correlated strongly with RV free-wall stress-strain work density ($r=0.965$). Peak RV longitudinal shortening alone did not ($r=0.090$), and an RV ejection-fraction-like FEM volume metric correlated negatively ($r=-0.716$). RV systolic pressure alone also correlated strongly ($r=0.908$), reflecting the fact that the sweep is deliberately pressure-loaded. Using LV pressure with RV strain was similarly high ($r=0.974$), because achieved LV and RV pressures are not independent along this capped-reference path. The important result is therefore not that RV pressure is uniquely identified by this correlation test. It is that adding a pressure scale to RV longitudinal strain recovers the RV free-wall work trend far better than strain alone.

```{figure} ../figures/fig_5_2b_rv_lakatos_bridge.png
:name: fig-rv-lakatos-bridge
:width: 95%

RV free-wall bridge to the clinical pressure-strain result of Lakatos et al. In the primary capped-reference sweep, peak RV longitudinal shortening alone does not track finite-element RV free-wall stress-strain work density, while a pressure-longitudinal-strain index does. Colour denotes RV systolic pressure.
```

This result is important because it prevents an over-broad conclusion. Cavity pressure still carries useful mechanical information as a work-density proxy. In the free walls, where the one-wall/one-pressure assumption is closest to valid, adjacent pressure preserves regional work-density magnitudes reasonably well. The difficulty appears when tissue is shared between the two cavities.

(sec-results-septum)=
## The Septum

The septum is not a free wall. It is a shared internal wall with LV pressure on one side and RV pressure on the other. That makes the pressure assignment qualitatively different. A free wall has one comparatively unambiguous pressure scale; the septum has several plausible pressure scales. The LV pressure reflects the usual clinical convention. The RV pressure reflects the pressure on the opposite septal face. The transmural pressure, $p_\text{LV}-p_\text{RV}$, reflects the net pressure difference across the wall. The mean pressure, $(p_\text{LV}+p_\text{RV})/2$, reflects the fact that the septal tissue is loaded from both sides.

The distinction matters because pressure difference and tissue loading are not the same thing. The pressure difference is the natural quantity for net septal force, curvature, and the clinical D-sign in RV pressure overload {cite}`ryan1985echocardiographic,vonk2013right`. If RV pressure rises toward LV pressure, the septum flattens because the pressure difference across it is reduced. Myocardial work density, however, is local stress times local strain. A septum compressed and constrained by two pressurized cavities can still carry substantial tissue work density even when the pressure difference is small. Transmural pressure is therefore mechanically meaningful, but it is not automatically the best scalar stress scale for septal work density.

To test this directly, the septal pressure choices for the longitudinal pressure-strain proxy were compared in two ways. First, their correlations with septal stress-strain work density were computed across the pressure sweep. Second, their ability to preserve septum/free-wall work-density ratios was measured. The ratio test is the more direct magnitude test: it asks whether the proxy gives the correct amount of septal work density relative to the LV and RV free walls in the same simulation.

In the primary capped-reference sweep, transmural pressure was not the best ranking pressure for septal stress-strain work density. The tangent-longitudinal proxy using LV pressure gave $r=0.783$, mean pressure gave $r=0.779$, through-wall weighted pressure gave $r=0.771$, and nearest-side pressure gave $r=0.760$. RV pressure also ranked the cases reasonably well ($r=0.745$). Transmural pressure was much weaker, with $r=0.222$. If the only question is case ordering along this loading path, the useful pressure scale is therefore closer to the two-sided or LV-like loading of the septum than to the net pressure difference across it.

The magnitude result points in the same conservative direction. The lowest septum/free-wall ratio error for the tangent-longitudinal clinical proxy was obtained with LV pressure, with a mean absolute log error of 0.352. Through-wall weighted pressure gave 0.528, mean pressure 0.535, nearest-side pressure 0.569, and RV pressure 0.770. Transmural pressure was the worst fixed candidate, with a mean absolute log error of 1.532. This is the main septal warning: the pressure difference across the septum is not the same as the scalar stress scale needed to preserve septal tissue-work density.

Here "through-wall weighted" means that each septal cell receives a pressure between $p_\text{LV}$ and $p_\text{RV}$ according to its transventricular position, with LV-side cells closer to $p_\text{LV}$ and RV-side cells closer to $p_\text{RV}$. A related "nearest-side" diagnostic assigns each septal cell the pressure of the closest cavity side.

These results are summarized in {numref}`tab-septum-proxies`. The table is restricted to the longitudinal-strain proxy, because this is the clinical pressure-strain quantity tested by the thesis. A fibre-aligned diagnostic was also computed as a model-side check. It made the two-sided interpretation stronger: transmural pressure still performed poorly, while mean, nearest-side, and through-wall weighted pressure became the closest choices. That diagnostic is useful for interpreting the mechanics, but it is not treated as a competing clinical proxy.

```{table} Septal longitudinal pressure-strain proxy performance in the primary capped-reference pressure-loading sweep. Correlation tests case ranking across the sweep; ratio error tests preservation of septum/free-wall magnitude within each case.
:name: tab-septum-proxies
:align: left

| Pressure choice | Ranking correlation $r$ | Magnitude ratio error |
|---|---:|---:|
| $p_\text{LV}$ | 0.783 | 0.352 |
| $p_\text{RV}$ | 0.745 | 0.770 |
| $p_\text{LV}-p_\text{RV}$ | 0.222 | 1.532 |
| Mean pressure | 0.779 | 0.535 |
| Nearest-side pressure | 0.760 | 0.569 |
| Through-wall weighted pressure | 0.771 | 0.528 |
```

The correlation part of the table is shown as scatter plots in {numref}`fig-septum-correlation-scatter`. The plot makes two points visible. First, transmural pressure is visually the wrong trend for this primary sweep: high RV-pressure cases do not have low septal tensor work simply because the LV-RV pressure difference has fallen. Second, the LV, mean, nearest-side, and through-wall weighted choices are not identical, but they all keep the septum inside the two-cavity loading picture rather than treating it as a pure pressure-difference wall.

```{figure} ../figures/fig_5_3a_septum_proxy_correlation_scatter.png
:name: fig-septum-correlation-scatter
:width: 95%

Septal pressure-choice correlations in the primary capped-reference sweep. Each panel compares a longitudinal pressure-strain proxy with finite-element septal stress-strain work density. The solid line is a least-squares regression and colour denotes achieved RV systolic pressure. Transmural pressure is mechanically meaningful for net septal pressure difference, but it is not a good scalar work-density pressure in this analysis.
```

The table shows the central septal result of the thesis in its most useful form. Transmural pressure is a poor work-density proxy in the primary capped-reference analysis, both for case ranking and for preserving septal density magnitudes. LV pressure gives the best fixed-candidate longitudinal magnitude result, while mean, nearest-side, and through-wall weighted pressure express the more physical idea that the septum is loaded by both cavities. The high-resolution capped-reference sweep therefore strengthens the central conclusion: the septum is shared tissue, and reducing it to one pressure-strain loop is a modelling choice with measurable consequences.

The geometric septum mask itself was also checked with a boundary-relaxation sweep. The mask is parametrized by an in/out displacement $t$: at $t=0$ it is the baseline geometric septum, $t<0$ erodes it, and $t>0$ grows it outward into the free-wall junction. {numref}`fig-septum-sweep` shows the seven sweep frames used in the sensitivity analysis, from $t=-5$ mm to $t=+10$ mm. In the primary capped-reference sweep, the canonical geometric septum volume matched the tag-3 septum volume case by case, so the reported septal region is not a moving postprocessing artifact. The relaxed-mask comparison is kept as a definition sensitivity rather than as an alternative result set; the detailed comparison is given in {ref}`sec-app-septum-epi-envelope`.

```{figure} ../figures/fig_5_6_septum_sweep.png
:name: fig-septum-sweep
:width: 95%

Septum-definition sweep used for the boundary-relaxation sensitivity. Each panel shows the geometric septum mask (red) embedded in a translucent cut-away of the biventricular mesh (gray), parametrized by the in/out displacement $t$. Negative $t$ erodes the baseline mask; positive $t$ grows it outward into the LV-RV junction. The $t=+10$ mm extreme corresponds to an envelope-style septal definition that includes most cells with both LV and RV pressure influence on either side.
```

The fibre-aligned diagnostic helps separate pressure-choice error from strain-direction error. When the same pressure choices were combined with the model-side fibre strain $E_{ff}$, correlations with septal stress-strain work became strongest for two-sided pressure choices: $r=0.975$ for mean pressure, $r=0.943$ for nearest-side pressure, and $r=0.978$ for through-wall weighted pressure. LV pressure also remained good ($r=0.840$), while transmural pressure became negative ($r=-0.262$). The magnitude test improved sharply for the two-sided choices: mean absolute log-ratio error was 0.072 for mean pressure, 0.075 for nearest-side pressure, and 0.069 for through-wall weighted pressure, compared with 0.886 for transmural pressure. This suggests that part of the septal difficulty is a strain-direction limitation of longitudinal strain, not only a pressure-assignment limitation.

The structural reason for this behaviour is shown in {numref}`tab-principal-strain-alignment`. The saved displacement checkpoints from the primary capped-reference sweep were replayed, the cell-centred Green--Lagrange strain tensor was diagonalized at each septal cell, and the most compressive eigenvector was compared with the model fibre, longitudinal, radial, and circumferential directions. The fibre direction was not identical to principal shortening, but it was substantially closer than the longitudinal direction and was the best aligned of the four candidates in more than half of the septal volume. The fibre-strain diagnostic above is therefore not only a rhetorical alternative to longitudinal strain; it follows from the deformation geometry of the septum in this sweep.

```{table} Alignment of candidate directions with principal shortening in the geometric septum, primary capped-reference sweep. Values are volume-weighted within each case and averaged across the 16 capped cases.
:name: tab-principal-strain-alignment
:align: left

| Candidate direction | Mean angle to principal shortening | Mean $\lvert\cos\theta\rvert$ | Best-aligned septal volume fraction |
|---|---:|---:|---:|
| Fibre | 32.3 deg | 0.788 | 0.56 |
| Longitudinal | 50.3 deg | 0.595 | 0.22 |
| Radial | 58.5 deg | 0.485 | 0.14 |
| Circumferential | 62.9 deg | 0.431 | 0.09 |
```

A deliberately non-clinical upper-bound scalar was also tested by using principal shortening itself in the pressure-strain loops. This did not make the septal pressure problem disappear. The best septal ranking used the through-wall weighted pressure ($r=0.767$), and the best magnitude preservation used nearest-side pressure with a mean absolute log-ratio error of 0.141. The magnitude result is better than the longitudinal proxy, but the ranking is not better than the longitudinal fixed-candidate result in {numref}`tab-septum-proxies` and remains well below the fibre-aligned diagnostic. Because principal shortening requires the full local strain tensor and varies cell by cell, it is best read as supporting evidence for the need for three-dimensional strain information rather than as a practical scalar replacement.

```{figure} ../figures/fig_5_3b_septum_strain_direction_diagnostic.png
:name: fig-septum-strain-direction-diagnostic
:width: 95%

Model-side septal fibre diagnostic in the primary capped-reference sweep. Left: correlations with finite-element septal stress-strain work density. Right: septum/free-wall magnitude preservation. Fibre-aligned strain strongly favours two-sided pressure choices, while transmural pressure still performs poorly.
```

A through-wall layer diagnostic gives a complementary view of the same issue. The geometric septum was split into LV-side, middle, and RV-side thirds using the LV-to-RV scalar used for the through-wall pressure diagnostics. This is not a fully resolved transmural stress measurement, but it shows that septal work and component balance are not uniform through the wall. The RV-side third generally carries larger stress-strain work density than the other two thirds, while the fibre fraction and sheet-normal fraction change differently across layers as RV pressure rises. This supports the conservative interpretation: a single scalar septal pressure-strain loop compresses a spatially heterogeneous tissue response into one number.

```{figure} ../figures/fig_5_3c_septum_layer_mechanics.png
:name: fig-septum-layer-mechanics
:width: 95%

Diagnostic through-wall septal layer summary in the primary capped-reference sweep. Layers are defined by the LV-to-RV scalar and should be read as coarse LV-side, middle, and RV-side summaries. The septum does not behave as a uniform one-pressure wall: stress-strain work density and the relative fibre and sheet-normal contributions vary across the wall and across loading cases.
```

(sec-results-pressure-mixtures)=
## Pressure Mixtures As A Diagnostic

To make the septal pressure ambiguity more explicit, a one-parameter pressure family was tested:

$$
p_\lambda = \lambda p_\text{LV} + (1-\lambda)p_\text{RV}.
$$

This family is useful because the parameter has a direct interpretation. $\lambda=0$ gives RV pressure, $\lambda=0.5$ gives mean pressure, $\lambda=1$ gives LV pressure, and values above one behave like LV pressure with some RV pressure subtracted. It is not proposed as a fitted clinical proxy. It is a diagnostic tool for asking where the data place the septum on the scale between RV-like, mean-like, LV-like, and transmural-like pressure.

For the tangent-longitudinal proxy in the primary capped-reference sweep, the best correlation with septal stress-strain work density occurred near $\lambda=0.83$, between mean and LV pressure. The best septum/free-wall ratio preservation occurred near $\lambda=2.13$, an LV-weighted extrapolation outside the physical LV--RV pressure interval. These numerical optima should not be interpreted as proposed clinical pressure formulas. They are diagnostics: the optimum depends on whether the target is sweep ranking or magnitude preservation, and the magnitude optimum being outside the physical interval is a warning against fitting a single septal pressure scalar too literally. This split is shown in {numref}`fig-septum-lambda`.

```{figure} ../figures/fig_5_4_septum_lambda_scan.png
:name: fig-septum-lambda
:width: 95%

Diagnostic scan of the septal pressure mixture $p_\lambda=\lambda p_\text{LV}+(1-\lambda)p_\text{RV}$ in the primary capped-reference sweep. The best value of $\lambda$ depends on whether the target is correlation across the pressure sweep or preservation of septum/free-wall work-density ratios. This is why a single fitted septal pressure would be misleading.
```

The mixture scan supports the same conclusion as the fixed candidates. If the goal is to rank one specific pressure sweep, the best pressure can sit between mean and LV pressure. If the goal is to preserve work-density magnitudes, the fitted optimum can even move beyond LV pressure. That does not make the extrapolated pressure physiological; it shows that the single-pressure reduction is being asked to absorb geometry, stress redistribution, and strain-direction error. The scan is useful because it shows that this is not just one unlucky choice among the fixed candidates. It is the signature of the septum behaving as shared tissue rather than as a free wall.

(sec-results-numerical)=
## Numerical Robustness Checks

Several numerical checks were performed to test whether the main conclusions depended on mesh resolution, postprocessing space, basal support, or reference-state construction. The detailed checks are collected in {ref}`chap-appendix-numerical`; only the implications for the results are summarized here.

```{table} Numerical checks used to defend the high-resolution result interpretation. The purpose is not to remove all numerical uncertainty, but to identify which conclusions are stable and which quantities should be read with caution.
:name: tab-results-numerical-defence
:align: left

| Check | What was tested | Main observation | Interpretation |
|---|---|---|---|
| Primary capped sweep audit | 16 capped-reference cases | All cases completed canonical quadrature-level postprocessing with finite pressure and per-cell work arrays | The primary figures and tables use a complete internally consistent result set |
| h=5 to h=3.75 endpoint convergence | sPAP22, sPAP60, sPAP95 | Hemodynamics and free-wall ratios were stable; severe-case septal values shifted about 5--7% | Septal magnitudes are the most mesh-sensitive quantities |
| Septum sweep envelope | Epi-excluded versus epi-inclusive relaxed septum masks | The geometric cutoff was unchanged; only the far relaxed sweep tail shifted | Main geometric-septum result is stable; wide sweep tails are definition sensitivity |
| Postprocessing space | Quadrature6, DG1, DG0 replay | DG1 stayed close to Quadrature6; DG0 suppressed high-pressure septal work | DG1 is adequate for integrated regional totals in this check; DG0 is too crude for septal work; Quadrature6 remains the conservative production path |
| Basal support | x-only basal constraint versus no-Dirichlet variants | Production runs use only a partial constraint; no-Dirichlet variants did not converge | The retained constraint is a stabilizing modelling choice, not a full basal clamp |
| Robin work | Boundary work budget in checked cases | Net Robin work was below 0.2% of cavity boundary work | Robin springs are not driving the work-density results |
| Reference-state and remodelling sensitivity | RV-EDP-capped unloading, regional stiffness checks, fixed-reference acute-loading pilots, and exploratory patient geometries | Capping RV end-diastolic pressure during unloading directly reduced RV reference collapse; stiffness and patient-geometry checks supported the same reference-state concern | High-pressure RV and RV-side septal absolute work-density magnitudes are reference-state sensitive; the capped-unloading sweep is the preferred bounded fixed-geometry sensitivity model |
```

The primary capped-reference sweep is complete: all 16 cases have solver pressure histories, metrics files, canonical per-cell work data, and finite numeric arrays. The capped production set was not rerun at 10 mm, so the earlier h=10-to-h=5 comparison is treated as numerical-method support rather than as a direct convergence proof for the capped reference-state choice. Against the 3.75 mm mesh-convergence endpoints in the related production setup, peak pressures and end-diastolic volumes differed by less than 0.8% at 5 mm, and free-wall work-density ratios differed by less than about 3%. Septal quantities were more sensitive, especially at high RV pressure: the observed difference between the 5 mm and 3.75 mm meshes was about 5-7% for severe-case septal stress-strain work and septal longitudinal-proxy quantities. The completed capped cases also have geometric septum volumes matching the tag-3 septum, so the primary septal region is not a non-canonical mask artifact.

In postprocessing-only replay tests, DG1 state storage changed integrated regional stress-strain work by at most about 1.2% relative to Quadrature6, whereas DG0 suppressed high-pressure septal work. The basal support should be read as a stabilizing modelling choice: the production setup fixes only the base-normal/global-x displacement component, tangential sliding remains, and the no-Dirichlet variants did not converge during end-diastolic inflation. Net Robin work was below 0.2% of cavity boundary work in the checked endpoint cases. These checks support the main regional conclusions, with the septum appropriately treated as the numerically more sensitive region.

A final robustness issue is not numerical resolution but the reference configuration. The inverse-unloading step uses the same fixed UKB geometry for all pressure cases. In severe RV loading, this can make the inferred unloaded RV reference too small because the model has no RV hypertrophy, curvature remodelling, or regional material adaptation with which to carry the higher end-diastolic pressure. The primary capped-reference sweep keeps the end-diastolic mesh target unchanged but caps the RV end-diastolic pressure used during inverse unloading at 5 mmHg. This is more constrained than arbitrary passive-stiffness tuning, because it changes only the questionable RV prestress target while keeping the circulation, anatomy, and material law otherwise comparable. Regional stiffness checks, fixed-reference acute-loading pilots, and an exploratory healthy/PAH patient-geometry comparison all supported the same central concern: RV and RV-side septal absolute work-density magnitudes are reference-state sensitive, and the direction of the bias is not captured by a simple one-sided correction. The detailed values are given in {ref}`sec-app-reference-remodeling-sensitivity`. The pressure-proxy comparisons remain useful as controlled fixed-geometry tests, but severe-case RV and RV-side septal magnitudes should not be treated as corrected PAH tissue-work estimates.

## What This Establishes

The results support three claims. First, for the LV and RV free walls, adjacent cavity pressure is a reasonable regional stress scale for preserving work-density ratios and tracking the sweep trend. Second, the septum cannot be treated as either LV free wall or RV free wall. It is a shared wall, and transmural pressure is not a sufficient work-density pressure: in the primary capped-reference sweep it was the weakest ranking candidate and the worst magnitude candidate. LV pressure gave the best fixed-candidate longitudinal magnitude result, while fibre-aligned diagnostics made mean and through-wall weighted pressure most faithful. This remains a model-side interpretation rather than a clinical replacement, because routine scalar strain components do not reconstruct the full strain tensor. Third, pressure-sweep correlations are conditional on the achieved hemodynamic path, the chosen metric, and the numerical definition of the septal region. They are useful for sensitivity testing, but they should not be interpreted as universal clinical rankings.

The fixed-geometry pressure sweep should therefore be read carefully. It is not a simulation of PAH progression in a patient. Real PAH changes pressure, volume, wall thickness, curvature, stiffness, activation, and contractility together. The sweep isolates one part of that system by changing the circulation while holding the anatomy and material model fixed. That isolation is useful, because it exposes how pressure choices for the longitudinal proxy respond to loading changes. It is not the same as a clinical cohort, and its severe RV and RV-side septal density magnitudes should not be treated as corrected PAH tissue-work estimates.

This distinction gives the thesis a more conservative and more useful result. The model does not prove that one septal pressure formula is clinically best. It shows where the pressure-strain idea is mechanically reasonable, where it becomes ambiguous, and why the septum is the difficult case.
