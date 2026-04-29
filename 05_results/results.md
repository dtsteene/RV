# Results

The results are easiest to understand if two questions are kept separate. First: does the pressure-strain proxy get the size of regional differences right? Second: when the circulation is changed while geometry is held fixed, does the proxy rank loading cases in the same order as model-resolved tensor work density? These are both useful questions, but they are not the same. A proxy can rank a pressure sweep well and still give the wrong regional balance in a single patient.

For that reason this chapter starts with the regional ratio analysis. This is the cleaner mechanics test. It does not require treating the pressure sweep as a real disease trajectory, and it does not depend on whether the hemodynamic axis chosen for the sweep is clinically typical. It asks only whether the pressure-strain construction preserves relative work-density magnitudes in a fixed model state. The pressure sweep is then used as a sensitivity experiment, showing how proxy rankings change when the loading path changes.

Unless stated otherwise, the results below use the corrected 16-case pressure-loading sweep described in the calibration chapter. In that sweep the biventricular geometry, material parameters, boundary conditions, and activation waveform are held fixed, while the circulation parameters are changed to raise RV pressure over a controlled range. The older handover sweep is used only in the section on why a correlation ranking changed.

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

Before comparing pressure-strain proxies with tensor work, it is useful to ask what the tensor work contains. In the local fibre-sheet-normal basis, the full contraction can be decomposed into fibre, sheet, sheet-normal, and cross terms. These are signed contributions relative to the net regional tensor work density: a negative component subtracts from the net work rather than representing a separate positive share. Across the corrected 16-case pressure-loading sweep, the free walls were strongly fibre dominated, with the fibre term accounting for about 89% of LV free-wall work density and 94% of RV free-wall work density on average.

The septum was less one-dimensional. Fibre work was still the largest component, about 75% of net septal work density on average, but sheet-normal work was much larger than in the free walls and cross-axis terms grew in several high-load cases. This matters for interpretation: a single strain direction can track part of the work trend because fibre work moves closely with total tensor work, but it does not contain the full septal mechanical accounting. The septum is therefore difficult not only because its pressure scale is ambiguous, but also because more of its work is carried outside one strain direction.

```{figure} ../figures/fig_5_0b_work_components_vs_rvsp.png
:name: fig-work-components
:width: 95%

Component breakdown of model-resolved tensor work density across the corrected 16-case pressure-loading sweep. Work density is decomposed in the local fibre-sheet-normal basis. Fibre work dominates the free-wall trends, while the septum has a larger sheet-normal and cross-axis contribution.
```

## Free Walls

The simplest case is the comparison between the LV free wall and the RV free wall. Each free wall faces one cavity, so the pressure assignment is mechanically natural: $p_\text{LV}$ for the LV free wall and $p_\text{RV}$ for the RV free wall. This is the cleanest setting for the pressure assignment; failure here would point to a more basic limitation than septal pressure ambiguity.

For the single healthy UKB baseline, the model-resolved tensor work density in the LV free wall was 3.97 times the RV free-wall value. The longitudinal-strain proxy using adjacent cavity pressure gave an LV/RV ratio of 4.79. This is not exact, but it is much closer than assigning the same pressure to both free walls. Using LV pressure everywhere gave a ratio of 1.75, and using RV pressure everywhere gave 1.14. Removing the pressure magnitude and keeping only the normalized waveform also lost the LV/RV balance, giving 1.16. The result is shown in {numref}`fig-freewall-single`.

```{figure} ../figures/fig_5_1_freewall_single_case_ratio.png
:name: fig-freewall-single
:width: 90%

Free-wall LV/RV work-density ratio in the single healthy UKB baseline. The black line is the model-resolved tensor-work-density ratio. For the longitudinal-strain proxy, adjacent cavity pressure gives the closest ratio; using one pressure everywhere or removing pressure magnitude loses the LV/RV work-density balance.
```

The same pattern holds across the corrected 16-case pressure-loading sweep. The mean absolute error in the free-wall LV/RV ratio was 0.21 for the adjacent-pressure longitudinal proxy, compared with 0.64 for LV pressure everywhere, 0.89 for RV pressure everywhere, and 0.84 for the pressure-normalized waveform-only index. A simple bulk geometry correction, $p \times \mathcal{V}_\text{cavity}/\mathcal{V}_\text{wall}$, was also tested. It reduced the error compared with using one pressure everywhere and came fairly close to the adjacent-pressure result, but it did not exceed it. The sweep result is shown in {numref}`fig-freewall-spectrum`.

```{figure} ../figures/fig_5_2_freewall_ratio_spectrum.png
:name: fig-freewall-spectrum
:width: 95%

Free-wall LV/RV work-density ratio across the corrected 16-case pressure-loading sweep. The adjacent-pressure longitudinal proxy follows the model-resolved tensor-work-density ratio better than the alternatives. The pressure-normalized waveform-only index preserves timing information but not work-density magnitude.
```

The free-wall ratio test asks whether the proxy preserves regional magnitudes. The next question is whether pressure-strain also ranks loading cases better than pressure or strain alone.

This RV free-wall ranking result connects the model to the recent clinical validation by Lakatos et al. {cite}`lakatos2024right`. Their endpoint was invasive RV contractility, whereas the endpoint here is model-resolved RV free-wall tensor work density, so the comparison is not a reproduction of their pressure-volume analysis. It is instead the finite-element analogue of the same pressure-correction idea.

Across the corrected 16-case sweep, the RV pressure-longitudinal-strain index correlated strongly with RV free-wall tensor work density ($r=0.993$). Peak RV longitudinal shortening alone did not: it correlated negatively with tensor work density ($r=-0.486$), and an RV ejection-fraction-like FEM volume metric also correlated negatively ($r=-0.390$). RV systolic pressure alone correlated less strongly ($r=0.838$), and using LV pressure with RV strain was weaker still ($r=0.750$). In this fixed-geometry sweep, pressure-strain tracks RV free-wall tensor work better than strain alone, pressure alone, or an arbitrary cavity-pressure pairing.

```{figure} ../figures/fig_5_2b_rv_lakatos_bridge.png
:name: fig-rv-lakatos-bridge
:width: 95%

RV free-wall bridge to the clinical pressure-strain result of Lakatos et al. In the corrected pressure-loading sweep, peak RV longitudinal shortening alone does not track model-resolved RV free-wall tensor work density, while the RV pressure-longitudinal-strain index does. Colour denotes RV systolic pressure.
```

This result is important because it prevents an over-broad conclusion. Cavity pressure still carries useful mechanical information as a work-density proxy. In the free walls, where the one-wall/one-pressure assumption is closest to valid, adjacent pressure preserves regional work-density magnitudes reasonably well. The difficulty appears when tissue is shared between the two cavities.

## The Septum

The septum is not a free wall. It is a shared internal wall with LV pressure on one side and RV pressure on the other. That makes the pressure assignment qualitatively different. A free wall has one comparatively unambiguous pressure scale; the septum has several plausible pressure scales. The LV pressure reflects the usual clinical convention. The RV pressure reflects the pressure on the opposite septal face. The transmural pressure, $p_\text{LV}-p_\text{RV}$, reflects the net pressure difference across the wall. The mean pressure, $(p_\text{LV}+p_\text{RV})/2$, reflects the fact that the septal tissue is loaded from both sides.

The distinction matters because pressure difference and tissue loading are not the same thing. The pressure difference is the natural quantity for net septal force, curvature, and the clinical D-sign. If RV pressure rises toward LV pressure, the septum flattens because the pressure difference across it is reduced. But myocardial work density is local stress times local strain. A septum compressed and constrained by two pressurized cavities can still carry substantial tissue work density even when the pressure difference is small. Transmural pressure is therefore mechanically meaningful, but it is not automatically the best scalar stress scale for septal work density.

To test this directly, the septal pressure choices for the longitudinal pressure-strain proxy were compared in two ways. First, their correlations with septal tensor work density were computed across the pressure sweep. Second, their ability to preserve septum/free-wall work-density ratios was measured. The ratio test is the more direct magnitude test: it asks whether the proxy gives the correct amount of septal work density relative to the LV and RV free walls in the same simulation.

In the corrected 16-case sweep, the longitudinal-strain proxy using LV pressure correlated most strongly with septal tensor work density, with $r=0.932$. The transmural proxy also correlated positively, with $r=0.819$, and the mean-pressure proxy gave $r=0.837$. If the only question is case ordering along this particular loading path, LV pressure is therefore the strongest longitudinal-strain proxy.

The magnitude result is different. The mean-pressure and through-wall-weighted proxies gave the lowest septum/free-wall ratio errors, both about 0.18 in mean absolute log error, while LV pressure gave 0.29 and transmural pressure gave 0.82. RV pressure alone had a poor correlation but a ratio error similar to LV pressure, which is a useful warning that correlation and magnitude preservation are different tests.

Here "through-wall weighted" means that each septal cell receives a pressure between $p_\text{LV}$ and $p_\text{RV}$ according to its transventricular position, with LV-side cells closer to $p_\text{LV}$ and RV-side cells closer to $p_\text{RV}$. A related "nearest-side" diagnostic assigns each septal cell the pressure of the closest cavity side.

These results are summarized in {numref}`tab-septum-proxies`. The table is restricted to the longitudinal-strain proxy, because this is the clinical pressure-strain quantity tested by the thesis. A fibre-aligned diagnostic was also computed as a model-side check. It gave the same qualitative conclusion for septal magnitude: transmural pressure was not the best scalar for regional work-density ratios, while nearest-side, mean, and through-wall pressure choices were much closer. That diagnostic is useful for interpreting the mechanics, but it is not treated as a competing clinical proxy.

```{table} Septal longitudinal pressure-strain proxy performance in the corrected 16-case pressure-loading sweep. Correlations are Pearson correlations with model-resolved septal tensor work density. Ratio error is the mean absolute log error in septum/free-wall work-density ratios.
:name: tab-septum-proxies
:align: left

| Pressure choice | Correlation | Ratio error |
|---|---:|---:|
| $p_\text{LV}$ | 0.932 | 0.289 |
| $p_\text{RV}$ | 0.384 | 0.261 |
| $p_\text{LV}-p_\text{RV}$ | 0.819 | 0.818 |
| Mean pressure | 0.837 | 0.182 |
| Nearest-side pressure | 0.751 | 0.183 |
| Through-wall weighted pressure | 0.825 | 0.182 |
```

The table shows the central septal result of the thesis in its most useful form. There is no single septal pressure that is best for every task. LV pressure orders the corrected longitudinal-strain sweep well, but it does not preserve septal density magnitudes as well as a two-sided pressure. Transmural pressure captures a real mechanical idea, the pressure difference across the septum, but it is a poor proxy for septal work-density magnitude in these data. Mean pressure and through-wall weighted pressure are more stable for the magnitude question because they reflect the two-sided loading of the shared wall.

## Why The Old Sweep Flipped

This section explains a discrepancy with the earlier analysis; it is not a second physiological result. The earlier simulations suggested that the transmural longitudinal-strain proxy correlated best with septal work density. That old result was not simply random. It came from the loading path. In the old handover data, LV pressure fell systematically as RV pressure rose. Under that path, subtracting the RV-pressure proxy removed a component that was anti-correlated with septal work density, so the transmural proxy won the correlation table.

The corrected simulations changed the LV pressure calibration. LV pressure is now much more stable across the RV pressure sweep. Under this preserved-systemic-pressure path, the RV-pressure contribution no longer has the same sign effect, and the LV-pressure longitudinal proxy gives the highest correlation with septal tensor work density. The sign flip is therefore a warning about the sweep, not a reason to distrust the mechanics: correlation rankings depend on the hemodynamic path used to generate the cases.

```{figure} ../figures/fig_5_3b_old_new_pressure_path.png
:name: fig-old-new-pressure-path
:width: 95%

Achieved pressure paths in the old handover sweep and the corrected sweep. In the old data, LV peak pressure drifted downward at high RV pressure. In the corrected data, LV peak pressure is much more stable while RV pressure rises. This difference in the loading path explains why a correlation ranking can flip even when the same model and proxy definitions are used.
```

The ratio analysis is more stable. In both the old and corrected data, transmural pressure was poor at preserving septum/free-wall work-density magnitudes, while mean or through-wall weighted pressure was better. For longitudinal strain, the old handover data gave ratio errors of 0.76 for transmural pressure and 0.26 for mean or through-wall weighted pressure. The corrected data gave 0.82 for transmural pressure and 0.18 for mean or through-wall weighted pressure. {numref}`fig-septum-old-new` shows this old-versus-corrected comparison.

```{figure} ../figures/fig_5_3_septum_old_new_ratio_error.png
:name: fig-septum-old-new
:width: 95%

Septum/free-wall ratio error for fixed longitudinal-strain septal pressure choices in the old handover data and the corrected 16-case sweep. The transmural proxy won the old correlation table, but it did not preserve regional work-density magnitudes in either dataset. Mean and through-wall weighted pressure were more stable for the magnitude question.
```

This is the clearest way to use the old data. It should not be presented as an additional physiological result. It is a sensitivity experiment showing that correlation-based rankings can flip when the pressure path changes. The robust finding is not that transmural pressure always wins or always loses. The robust finding is that the septum is not a one-pressure free wall, and that the question being asked matters.

## Pressure Mixtures As A Diagnostic

To make the septal pressure ambiguity more explicit, a one-parameter pressure family was tested:

$$
p_\lambda = \lambda p_\text{LV} + (1-\lambda)p_\text{RV}.
$$

This family is useful because the parameter has a direct interpretation. $\lambda=0$ gives RV pressure, $\lambda=0.5$ gives mean pressure, $\lambda=1$ gives LV pressure, and values above one behave like LV pressure with some RV pressure subtracted. It is not proposed as a fitted clinical proxy. It is a diagnostic tool for asking where the data place the septum on the scale between RV-like, mean-like, LV-like, and transmural-like pressure.

For the longitudinal-strain proxy, the best correlation with septal tensor work density occurred near $\lambda=1.23$, which is slightly beyond LV pressure in the direction of subtracting RV pressure. The best septum/free-wall ratio preservation occurred near $\lambda=0.52$, essentially mean pressure. The fibre-aligned diagnostic was less conflicted, with the optimal values closer to the two-sided range. The optimum moves depending on the metric, so fitting one septal pressure scalar would hide the ambiguity rather than solve it. This split is shown in {numref}`fig-septum-lambda`.

```{figure} ../figures/fig_5_4_septum_lambda_scan.png
:name: fig-septum-lambda
:width: 95%

Diagnostic scan of the septal pressure mixture $p_\lambda=\lambda p_\text{LV}+(1-\lambda)p_\text{RV}$. The best value of $\lambda$ depends on whether the target is correlation across the pressure sweep or preservation of septum/free-wall work-density ratios. This is why a single fitted septal pressure would be misleading.
```

The mixture scan supports the same conclusion as the fixed candidates. If the goal is to rank one specific pressure sweep, the best pressure can move toward LV pressure or even toward a transmural-like combination. If the goal is to preserve work-density magnitudes inside the heart, a two-sided pressure scale is preferred. The scan is useful because it shows that this is not just one unlucky choice among the fixed candidates. It is the signature of the septum behaving as shared tissue rather than as a free wall.

## Numerical Robustness Checks

Three numerical checks were performed to test whether the main conclusions depended on mesh resolution, postprocessing space, or the basal support condition. The detailed checks are collected in the numerical-robustness appendix; only the implications for the results are summarized here.

The production mesh used a 5 mm characteristic length. Against the 3.75 mm reference mesh, peak pressures and end-diastolic volumes differed by less than 0.8%, and free-wall work-density ratios differed by less than about 3%. Septal quantities were more sensitive, especially at high RV pressure: the observed difference between the 5 mm and 3.75 mm meshes was about 5-7% for severe-case septal tensor work and septal longitudinal-proxy quantities. These differences are smaller than the main separation between pressure-choice conclusions, but absolute high-pressure septal magnitudes remain the most mesh-sensitive results.

In postprocessing-only replay tests, DG1 state storage changed integrated regional tensor work by at most about 1.2% relative to Quadrature6, whereas DG0 suppressed high-pressure septal work. The basal support should be read as a stabilizing modelling choice: the production setup fixes only the base-normal/global-x displacement component, tangential sliding remains, and the no-Dirichlet variants did not converge during end-diastolic inflation. Net Robin work was below 0.2% of cavity boundary work in the checked endpoint cases. These checks support the main regional conclusions, with the septum appropriately treated as the numerically more sensitive region.

## What This Establishes

The results support three claims. First, for the LV and RV free walls, adjacent cavity pressure is a reasonable regional stress scale for preserving work-density ratios and tracking the sweep trend. Second, the septum cannot be treated as either LV free wall or RV free wall. It is a shared wall, and the "best" septal pressure depends on the metric: LV pressure gives the strongest longitudinal-strain correlation in the corrected sweep, while mean, nearest-side, and through-wall pressure choices better preserve septal work-density magnitudes. Third, pressure-sweep correlations are conditional on the chosen loading path. They are useful for sensitivity testing, but they should not be interpreted as universal clinical rankings.

The fixed-geometry pressure sweep should therefore be read carefully. It is not a simulation of PAH progression in a patient. Real PAH changes pressure, volume, wall thickness, curvature, stiffness, activation, and contractility together. The sweep isolates one part of that system by changing the circulation while holding the anatomy and material model fixed. That isolation is useful, because it exposes how pressure choices for the longitudinal proxy respond to loading changes. It is not the same as a clinical cohort.

This distinction gives the thesis a more conservative and more useful result. The model does not prove that one septal pressure formula is clinically best. It shows where the pressure-strain idea is mechanically reasonable, where it becomes ambiguous, and why the septum is the difficult case.
