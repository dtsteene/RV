# Results

The results are easiest to understand if two questions are kept separate. First: does the pressure-strain proxy get the size of regional differences right? Second: when the circulation is changed while geometry is held fixed, does the proxy rank loading cases in the same order as model-resolved tensor work density? These are both useful questions, but they are not the same. A proxy can rank a pressure sweep well and still give the wrong regional balance in a single patient.

For that reason this chapter starts with the regional ratio analysis. This is the cleaner mechanics test. It does not require treating the pressure sweep as a real disease trajectory, and it does not depend on whether the hemodynamic axis chosen for the sweep is clinically typical. It asks only whether the pressure-strain construction preserves relative work-density magnitudes in a fixed model state. The pressure sweep is then used as a controlled loading experiment, asking whether the same proxies rank loading cases in the same order as model-resolved tensor work.

Unless stated otherwise, the results below use the high-resolution corrected pressure-loading sweep described in the calibration chapter. This sweep was rerun at 5 mm characteristic mesh length, and all 16 cases completed canonical postprocessing. In that sweep the biventricular geometry, material parameters, boundary conditions, and activation waveform are held fixed, while the circulation parameters are changed to raise RV pressure over a controlled range. Case names such as `sPAP55` are nominal calibration labels; pressure axes, correlations, and proxy calculations use the achieved pressures and volumes from the coupled finite-element/circulation simulations. All pressure-strain proxies use the solver cavity pressures returned by the volume-constrained mechanics problem, not the standalone 0D elastance pressures.

The chapter follows five steps. It first defines the density and ratio metrics, then asks what the model-resolved tensor work contains. It next tests the free walls, where each wall has one adjacent pressure. It then turns to the septum, where pressure assignment and strain direction are both ambiguous. Finally, it summarizes the numerical checks that support the interpretation.

The ratio tests use simple formulas. For two regions $A$ and $B$, the model-resolved ratio is

$$
R_\text{tensor}(A,B) = \frac{w_\text{int}(A)}{w_\text{int}(B)},
\qquad
w_\text{int}(A)=\frac{W_\text{int}[\Omega_A]}{|\Omega_{A,0}|},
$$

and the clinical-style proxy ratio is

$$
R_\text{proxy}(A,B) = \frac{w_\text{PS}(A)}{w_\text{PS}(B)}.
$$

Here $W_\text{int}[\Omega_A]$ is the volume-integrated tensor work over region $\Omega_A$, and $|\Omega_{A,0}|$ is that region's reference volume. Both $w_\text{int}$ and the pressure-strain loop area $w_\text{PS}$ are density-like quantities with units of pressure: J/m$^3$ = Pa, reported here in kPa. The pressure-strain proxy is already treated as a density-like index, so it has no additional regional volume factor.

Two ratio errors are used. For the free-wall LV/RV comparison, the reported error is the absolute difference $|R_\text{proxy}-R_\text{tensor}|$. For the septum, two ratios are tested in each case, septum/LV-free-wall and septum/RV-free-wall, and the reported error is a mean absolute log ratio error,

$$
\eta_\text{ratio}
= \left\langle
\left|
\log \left(
\frac{R_\text{proxy}}{R_\text{tensor}}
\right)
\right|
\right\rangle .
$$

This scale is multiplicative: $\eta_\text{ratio}=0$ is exact, while $\eta_\text{ratio}=0.18$ corresponds to a typical ratio error of about $\exp(0.18)-1 \approx 20\%$.

Throughout the chapter, the longitudinal-strain proxy uses the clinical scalar longitudinal strain $\varepsilon_{ll}$. Fibre-aligned diagnostics use the model-side Green-Lagrange fibre strain $E_{ff}=\mathbf{E}:(\mathbf{f}_0\otimes\mathbf{f}_0)$ and are treated as mechanical checks rather than competing clinical proxies.

These ratios are tested first in the free walls, where pressure assignment is simple, and then in the septum, where it is not.

```{figure} ../figures/fig_5_0_freewall_vs_septum_schematic.png
:name: fig-freewall-septum-schematic
:width: 85%

The pressure assignment is mechanically simple for a free wall and ambiguous for the septum. A free wall has one adjacent cavity pressure. The septum is shared tissue with LV pressure on one face and RV pressure on the other, so pressure difference, mean pressure, and through-wall weighted pressure are all mechanically plausible but answer different questions.
```

Before comparing pressure-strain proxies with tensor work, it is useful to ask what the tensor work contains. In the local fibre-sheet-normal basis, the full contraction can be decomposed into fibre, sheet, sheet-normal, and cross terms. These are signed contributions relative to the net regional tensor work density: a negative component subtracts from the net work rather than representing a separate positive share. Across the high-resolution pressure-loading sweep, the free walls were strongly fibre dominated, with the fibre term accounting for about 89% of LV free-wall work density and 93% of RV free-wall work density on average.

The septum was less one-dimensional. Fibre work was still the largest component, about 72% of net septal work density on average, but sheet-normal work was much larger than in the free walls and cross-axis terms grew in several high-load cases. This matters for interpretation: a single strain direction can track part of the work trend because fibre work moves closely with total tensor work, but it does not contain the full septal mechanical accounting. The septum is therefore difficult not only because its pressure scale is ambiguous, but also because more of its work is carried outside one strain direction.

```{figure} ../figures/fig_5_0b_work_components_vs_rvsp.png
:name: fig-work-components
:width: 95%

Component breakdown of model-resolved tensor work density across the high-resolution pressure-loading sweep. Work density is decomposed in the local fibre-sheet-normal basis. Fibre work dominates the free-wall trends, while the septum has a larger sheet-normal and cross-axis contribution. This is the first warning that a one-direction pressure-strain proxy is mechanically cleaner in the free walls than in the septum.
```

## Free Walls

The simplest case is the comparison between the LV free wall and the RV free wall. Each free wall faces one cavity, so the pressure assignment is mechanically natural: $p_\text{LV}$ for the LV free wall and $p_\text{RV}$ for the RV free wall. This is the cleanest setting for the pressure assignment; failure here would point to a more basic limitation than septal pressure ambiguity.

For the single healthy UKB baseline, the model-resolved tensor work density in the LV free wall was 3.97 times the RV free-wall value. The longitudinal-strain proxy using adjacent cavity pressure gave an LV/RV ratio of 4.79. This is not exact, but it is much closer than assigning the same pressure to both free walls. Using LV pressure everywhere gave a ratio of 1.75, and using RV pressure everywhere gave 1.14. Removing the pressure magnitude and keeping only the normalized waveform also lost the LV/RV balance, giving 1.16. The result is shown in {numref}`fig-freewall-single`.

```{figure} ../figures/fig_5_1_freewall_single_case_ratio.png
:name: fig-freewall-single
:width: 90%

Free-wall LV/RV work-density ratio in the single healthy UKB baseline. The black line is the model-resolved tensor-work-density ratio. For the longitudinal-strain proxy, adjacent cavity pressure gives the closest ratio; using one pressure everywhere or removing pressure magnitude loses the LV/RV work-density balance.
```

The same pattern holds across the high-resolution pressure-loading sweep. The mean absolute error in the free-wall LV/RV ratio was 0.33 for the adjacent-pressure longitudinal proxy, compared with 0.58 for LV pressure everywhere, 0.82 for RV pressure everywhere, and 0.76 for the pressure-normalized waveform-only index. The sweep result is shown in {numref}`fig-freewall-spectrum`. Adjacent cavity pressure remains the best of the tested longitudinal pressure assignments for the free-wall ratio.

```{figure} ../figures/fig_5_2_freewall_ratio_spectrum.png
:name: fig-freewall-spectrum
:width: 95%

Free-wall LV/RV work-density ratio across the high-resolution pressure-loading sweep. The adjacent-pressure longitudinal proxy follows the model-resolved tensor-work-density ratio better than the alternatives. The pressure-normalized waveform-only index preserves timing information but not work-density magnitude.
```

A scatter view of the same comparison is shown in {numref}`fig-freewall-ratio-scatter`. This makes the difference between correlation and magnitude easier to see. Several pressure choices rank the cases in a similar order, but the adjacent-pressure points lie closest to the identity line.

```{figure} ../figures/fig_5_2c_freewall_ratio_scatter.png
:name: fig-freewall-ratio-scatter
:width: 95%

Scatter comparison between pressure-strain proxy LV/RV ratios and model-resolved tensor-work LV/RV ratios in the high-resolution sweep. Each panel shows one longitudinal pressure assignment. The solid line is a least-squares regression, the dashed line is the identity line, and colour denotes achieved RV systolic pressure. A high correlation alone is not enough; the useful proxy should also lie near the identity line.
```

The free-wall ratio test asks whether the proxy preserves regional magnitudes. The next question is whether pressure-strain also ranks loading cases better than pressure or strain alone.

This RV free-wall ranking result connects the model to the recent clinical validation by Lakatos et al. {cite}`lakatos2024right`. Their endpoint was invasive RV contractility, whereas the endpoint here is model-resolved RV free-wall tensor work density, so the comparison is not a reproduction of their pressure-volume analysis. It is instead the finite-element analogue of the same pressure-correction idea.

Across the high-resolution sweep, the RV pressure-longitudinal-strain index correlated strongly with RV free-wall tensor work density ($r=0.986$). Peak RV longitudinal shortening alone did not: it correlated negatively with tensor work density ($r=-0.569$), and an RV ejection-fraction-like FEM volume metric also correlated negatively ($r=-0.331$). RV systolic pressure alone correlated less strongly ($r=0.832$), and using LV pressure with RV strain was weaker still ($r=0.629$). In this fixed-geometry sweep, pressure-strain tracks RV free-wall tensor work better than strain alone, pressure alone, or an arbitrary cavity-pressure pairing.

```{figure} ../figures/fig_5_2b_rv_lakatos_bridge.png
:name: fig-rv-lakatos-bridge
:width: 95%

RV free-wall bridge to the clinical pressure-strain result of Lakatos et al. In the high-resolution pressure-loading sweep, peak RV longitudinal shortening alone does not track model-resolved RV free-wall tensor work density, while the RV pressure-longitudinal-strain index does. Colour denotes RV systolic pressure.
```

This result is important because it prevents an over-broad conclusion. Cavity pressure still carries useful mechanical information as a work-density proxy. In the free walls, where the one-wall/one-pressure assumption is closest to valid, adjacent pressure preserves regional work-density magnitudes reasonably well. The difficulty appears when tissue is shared between the two cavities.

## The Septum

The septum is not a free wall. It is a shared internal wall with LV pressure on one side and RV pressure on the other. That makes the pressure assignment qualitatively different. A free wall has one comparatively unambiguous pressure scale; the septum has several plausible pressure scales. The LV pressure reflects the usual clinical convention. The RV pressure reflects the pressure on the opposite septal face. The transmural pressure, $p_\text{LV}-p_\text{RV}$, reflects the net pressure difference across the wall. The mean pressure, $(p_\text{LV}+p_\text{RV})/2$, reflects the fact that the septal tissue is loaded from both sides.

The distinction matters because pressure difference and tissue loading are not the same thing. The pressure difference is the natural quantity for net septal force, curvature, and the clinical D-sign in RV pressure overload {cite}`ryan1985echocardiographic,vonk2013right`. If RV pressure rises toward LV pressure, the septum flattens because the pressure difference across it is reduced. But myocardial work density is local stress times local strain. A septum compressed and constrained by two pressurized cavities can still carry substantial tissue work density even when the pressure difference is small. Transmural pressure is therefore mechanically meaningful, but it is not automatically the best scalar stress scale for septal work density.

To test this directly, the septal pressure choices for the longitudinal pressure-strain proxy were compared in two ways. First, their correlations with septal tensor work density were computed across the pressure sweep. Second, their ability to preserve septum/free-wall work-density ratios was measured. The ratio test is the more direct magnitude test: it asks whether the proxy gives the correct amount of septal work density relative to the LV and RV free walls in the same simulation.

In the high-resolution sweep, the longitudinal-strain proxy using transmural pressure correlated most strongly with septal tensor work density, with $r=0.964$. LV pressure was close behind, with $r=0.955$, while the mean-pressure proxy gave $r=0.779$. If the only question is case ordering along this particular loading path, the best scalar pressure is therefore not sharply identified: transmural and LV pressure both rank the high-resolution sweep well.

The magnitude result is different. The lowest septum/free-wall ratio errors were obtained by lower-pressure or two-sided choices: nearest-side pressure gave a mean absolute log error of 0.33, through-wall weighted pressure 0.34, mean pressure 0.34, and RV pressure 0.35. LV pressure gave 0.46 and transmural pressure gave 0.60. RV pressure alone had almost no correlation with septal tensor work, but one of the better magnitude errors, which is a useful warning that correlation and magnitude preservation are different tests.

Here "through-wall weighted" means that each septal cell receives a pressure between $p_\text{LV}$ and $p_\text{RV}$ according to its transventricular position, with LV-side cells closer to $p_\text{LV}$ and RV-side cells closer to $p_\text{RV}$. A related "nearest-side" diagnostic assigns each septal cell the pressure of the closest cavity side.

These results are summarized in {numref}`tab-septum-proxies`. The table is restricted to the longitudinal-strain proxy, because this is the clinical pressure-strain quantity tested by the thesis. A fibre-aligned diagnostic was also computed as a model-side check. It gave the same qualitative conclusion for septal magnitude: transmural pressure was not the best scalar for regional work-density ratios, while lower-pressure or two-sided pressure choices were closer. That diagnostic is useful for interpreting the mechanics, but it is not treated as a competing clinical proxy.

```{table} Septal longitudinal pressure-strain proxy performance in the high-resolution pressure-loading sweep. Correlation tests case ranking across the sweep; ratio error tests preservation of septum/free-wall magnitude within each case. The two metrics do not select the same pressure choice.
:name: tab-septum-proxies
:align: left

| Pressure choice | Ranking correlation $r$ | Magnitude ratio error |
|---|---:|---:|
| $p_\text{LV}$ | 0.955 | 0.462 |
| $p_\text{RV}$ | 0.034 | 0.353 |
| $p_\text{LV}-p_\text{RV}$ | 0.964 | 0.605 |
| Mean pressure | 0.779 | 0.344 |
| Nearest-side pressure | 0.639 | 0.332 |
| Through-wall weighted pressure | 0.772 | 0.338 |
```

The correlation part of the table is shown as scatter plots in {numref}`fig-septum-correlation-scatter`. The plot makes two points visible. First, the transmural and LV-pressure proxies both rank the high-resolution cases well. Second, the lower-correlation pressure choices are not simply noisy copies of the same relationship; they follow different trends because they weight the RV-pressure contribution differently.

```{figure} ../figures/fig_5_3a_septum_proxy_correlation_scatter.png
:name: fig-septum-correlation-scatter
:width: 95%

Septal pressure-choice correlations in the high-resolution sweep. Each panel compares a longitudinal pressure-strain proxy with model-resolved septal tensor work density. The solid line is a least-squares regression and colour denotes achieved RV systolic pressure. These panels show why a high correlation should be read as good case ranking, not necessarily good regional magnitude preservation.
```

The table shows the central septal result of the thesis in its most useful form. There is no single septal pressure that is best for every task. Transmural and LV pressure order the high-resolution longitudinal-strain sweep well, but neither preserves septal density magnitudes as well as the lower-pressure or two-sided diagnostics. Transmural pressure captures a real mechanical idea, the pressure difference across the septum, but it remains a poor proxy for septal work-density magnitude in these data. The high-resolution rerun therefore strengthens, rather than weakens, the central conclusion: the septum is shared tissue, and "best pressure" depends on the metric.

The fibre-aligned diagnostic helps separate pressure-choice error from strain-direction error. When the same pressure choices were combined with the model-side fibre strain $E_{ff}$, correlations with septal tensor work became high for a wider set of pressure choices: $r=0.999$ for LV pressure, $r=0.991$ for mean pressure, $r=0.976$ for nearest-side pressure, and $r=0.990$ for through-wall weighted pressure. The magnitude test improved too: for mean pressure, the septum/free-wall mean absolute log-ratio error fell from 0.344 with longitudinal strain to 0.102 with fibre strain; nearest-side and through-wall weighted pressure showed similar improvements. Transmural pressure remained a poor magnitude proxy even with fibre strain. This suggests that part of the septal difficulty is a strain-direction limitation of longitudinal strain, not only a pressure-assignment limitation.

```{figure} ../figures/fig_5_3b_septum_strain_direction_diagnostic.png
:name: fig-septum-strain-direction-diagnostic
:width: 95%

Model-side septal fibre diagnostic in the high-resolution sweep. Left: correlations with model-resolved septal tensor work density. Right: septum/free-wall magnitude preservation. Fibre-aligned strain improves several two-sided pressure choices, but transmural pressure still performs poorly for magnitude preservation.
```

A through-wall layer diagnostic gives a complementary view of the same issue. The geometric septum was split into LV-side, middle, and RV-side thirds using the LV-to-RV scalar used for the through-wall pressure diagnostics. This is not a fully resolved transmural stress measurement, but it shows that septal work and component balance are not uniform through the wall. The RV-side third generally carries larger tensor work density than the other two thirds, while the fibre fraction and sheet-normal fraction change differently across layers as RV pressure rises. This supports the conservative interpretation: a single scalar septal pressure-strain loop compresses a spatially heterogeneous tissue response into one number.

```{figure} ../figures/fig_5_3c_septum_layer_mechanics.png
:name: fig-septum-layer-mechanics
:width: 95%

Diagnostic through-wall septal layer summary in the high-resolution sweep. Layers are defined by the LV-to-RV scalar and should be read as coarse LV-side, middle, and RV-side summaries. The septum does not behave as a uniform one-pressure wall: tensor work density and the relative fibre and sheet-normal contributions vary across the wall and across loading cases.
```

## Pressure Mixtures As A Diagnostic

To make the septal pressure ambiguity more explicit, a one-parameter pressure family was tested:

$$
p_\lambda = \lambda p_\text{LV} + (1-\lambda)p_\text{RV}.
$$

This family is useful because the parameter has a direct interpretation. $\lambda=0$ gives RV pressure, $\lambda=0.5$ gives mean pressure, $\lambda=1$ gives LV pressure, and values above one behave like LV pressure with some RV pressure subtracted. It is not proposed as a fitted clinical proxy. It is a diagnostic tool for asking where the data place the septum on the scale between RV-like, mean-like, LV-like, and transmural-like pressure.

For the longitudinal-strain proxy in the high-resolution sweep, the best correlation with septal tensor work density occurred at a strongly LV-weighted extrapolation, near $\lambda=2.2$. The best septum/free-wall ratio preservation occurred near $\lambda=0.08$, much closer to RV pressure than to LV pressure. These numerical optima should not be interpreted as a proposed clinical pressure formula. They are a diagnostic: the optimum moves dramatically depending on whether the target is sweep ranking or magnitude preservation, so fitting one septal pressure scalar would hide the ambiguity rather than solve it. This split is shown in {numref}`fig-septum-lambda`.

```{figure} ../figures/fig_5_4_septum_lambda_scan.png
:name: fig-septum-lambda
:width: 95%

Diagnostic scan of the septal pressure mixture $p_\lambda=\lambda p_\text{LV}+(1-\lambda)p_\text{RV}$ in the high-resolution sweep. The best value of $\lambda$ depends on whether the target is correlation across the pressure sweep or preservation of septum/free-wall work-density ratios. This is why a single fitted septal pressure would be misleading.
```

The mixture scan supports the same conclusion as the fixed candidates. If the goal is to rank one specific pressure sweep, the best pressure can move toward LV pressure or even beyond it. If the goal is to preserve work-density magnitudes inside the heart, the best pressure scale can move toward the lower-pressure/RV side. The scan is useful because it shows that this is not just one unlucky choice among the fixed candidates. It is the signature of the septum behaving as shared tissue rather than as a free wall.

## Numerical Robustness Checks

Several numerical checks were performed to test whether the main conclusions depended on mesh resolution, postprocessing space, or the basal support condition. The detailed checks are collected in the numerical-robustness appendix; only the implications for the results are summarized here.

```{table} Numerical checks used to defend the high-resolution result interpretation. The purpose is not to remove all numerical uncertainty, but to identify which conclusions are stable and which quantities should be read with caution.
:name: tab-results-numerical-defence
:align: left

| Check | What was tested | Main observation | Interpretation |
|---|---|---|---|
| h=10 to h=5 sweep rerun | 16 paired corrected-sweep cases | Pressures shifted by at most 1.8%; free-wall ratios shifted by a few percent | Free-wall conclusions are not a coarse-mesh artifact |
| h=5 to h=3.75 endpoint convergence | sPAP22, sPAP60, sPAP95 | Hemodynamics and free-wall ratios were stable; severe-case septal values shifted about 5--7% | Septal magnitudes are the most mesh-sensitive quantities |
| Postprocessing space | Quadrature6, DG1, DG0 replay | DG1 stayed close to Quadrature6; DG0 suppressed high-pressure septal work | DG1 is adequate for integrated regional totals in this check; DG0 is too crude for septal work; Quadrature6 remains the conservative production path |
| Basal support | x-only basal constraint versus no-Dirichlet variants | Production runs use only a partial constraint; no-Dirichlet variants did not converge | The retained constraint is a stabilizing modelling choice, not a full basal clamp |
| Robin work | Boundary work budget in checked cases | Net Robin work was below 0.2% of cavity boundary work | Robin springs are not driving the work-density results |
```

The corrected sweep was first generated at 10 mm resolution and then rerun at 5 mm resolution. Across the 16 paired cases, achieved pressures changed little: the maximum h=10-to-h=5 difference was 1.8% for LV end-systolic pressure and 1.1% for RV end-systolic pressure. Free-wall ratios shifted more, but not enough to change the qualitative result: the model-resolved LV/RV tensor ratio changed by at most 5.4%, and the adjacent-pressure longitudinal proxy ratio by at most 8.3%. These shifts are summarized in {numref}`fig-h10-h5-shift`.

```{figure} ../figures/fig_5_5_h10_to_h5_nonseptal_shift.png
:name: fig-h10-h5-shift
:width: 88%

Observed shift from the 10 mm corrected sweep to the 5 mm rerun for quantities that can be compared directly. Hemodynamic pressures changed by about 1-2% or less, while free-wall LV/RV ratios changed by a few percent. Septal h=10-to-h=5 differences are not shown here because the 10 mm corrected sweep used a non-canonical geometric septum mask.
```

The mesh-convergence endpoints give the finer-resolution reference. Against the 3.75 mm mesh, peak pressures and end-diastolic volumes differed by less than 0.8% at 5 mm, and free-wall work-density ratios differed by less than about 3%. Septal quantities were more sensitive, especially at high RV pressure: the observed difference between the 5 mm and 3.75 mm meshes was about 5-7% for severe-case septal tensor work and septal longitudinal-proxy quantities. The 10 mm septal comparison is not used as a direct mesh-error estimate for the final sweep because that earlier geometric septum mask covered only part of the canonical/tagged septum in several cases. The 5 mm rerun fixes this: the completed 5 mm cases have geometric septum volumes matching the tag-3 septum.

In postprocessing-only replay tests, DG1 state storage changed integrated regional tensor work by at most about 1.2% relative to Quadrature6, whereas DG0 suppressed high-pressure septal work. The basal support should be read as a stabilizing modelling choice: the production setup fixes only the base-normal/global-x displacement component, tangential sliding remains, and the no-Dirichlet variants did not converge during end-diastolic inflation. Net Robin work was below 0.2% of cavity boundary work in the checked endpoint cases. These checks support the main regional conclusions, with the septum appropriately treated as the numerically more sensitive region.

## What This Establishes

The results support three claims. First, for the LV and RV free walls, adjacent cavity pressure is a reasonable regional stress scale for preserving work-density ratios and tracking the sweep trend. Second, the septum cannot be treated as either LV free wall or RV free wall. It is a shared wall, and the "best" septal pressure depends on the metric: transmural and LV pressure rank the high-resolution longitudinal-strain sweep well, while lower-pressure or two-sided choices better preserve septal work-density magnitudes. The fibre diagnostic adds that part of the septal difficulty is also a strain-direction issue: fibre-aligned strain makes several two-sided pressure choices much more faithful, but this remains a model-side diagnostic rather than a clinical replacement. Third, pressure-sweep correlations are conditional on the achieved hemodynamic path, the chosen metric, and the numerical definition of the septal region. They are useful for sensitivity testing, but they should not be interpreted as universal clinical rankings.

The fixed-geometry pressure sweep should therefore be read carefully. It is not a simulation of PAH progression in a patient. Real PAH changes pressure, volume, wall thickness, curvature, stiffness, activation, and contractility together. The sweep isolates one part of that system by changing the circulation while holding the anatomy and material model fixed. That isolation is useful, because it exposes how pressure choices for the longitudinal proxy respond to loading changes. It is not the same as a clinical cohort.

This distinction gives the thesis a more conservative and more useful result. The model does not prove that one septal pressure formula is clinically best. It shows where the pressure-strain idea is mechanically reasonable, where it becomes ambiguous, and why the septum is the difficult case.
