(chap-appendix-reference-state)=
# Reference-State and Remodelling Sensitivity

The inverse-unloading workflow treats the image-derived mesh as a loaded end-diastolic target, so the unloaded reference depends on the end-diastolic pressures, the passive material parameters, and the anatomy used during unloading. In the pressure sweep, the anatomy and passive material law are held fixed while RV pressure is raised. This isolates the pressure-proxy question but removes the RV hypertrophy, curvature changes, and regional passive remodelling that would normally accompany severe PAH. This appendix records the reference-state checks that justify the capped-RV-EDP production choice. None of these are corrected PAH models; they are bounded sensitivity tests.

(sec-app-reference-remodeling-sensitivity)=
## Regional Passive Stiffness Sensitivity

In the uncapped fixed-geometry pilot, the inferred RV unloaded cavity became much smaller as RV end-diastolic pressure increased. A late unloading-only sensitivity sweep tested whether regional passive stiffening could reduce that collapse. The LV material scale was held at 1.0, while RV and septal scales were varied; the stiffest tested point used RV scale 16 and septum scale 8. Only the unloading stage was repeated.

```{table} Unloaded-volume fraction in the baseline unloading and in the stiffest tested RV/septum regional material variant. Fractions are unloaded volume divided by the fixed end-diastolic target volume.
:name: tab-app-reference-stiffness
:align: left

| Case | Baseline LV | Stiffened LV | Baseline RV | Stiffened RV |
|---|---:|---:|---:|---:|
| sPAP22 | 80.5% | 82.4% | 55.6% | 80.2% |
| sPAP60 | 74.9% | 78.7% | 34.3% | 63.3% |
| sPAP95 | 72.2% | 77.4% | 20.9% | 48.6% |
```

Regional RV and septal stiffening makes the low-pressure case much more plausible and improves the intermediate case substantially. It does not fully rescue the severe case: even at RV scale 16 and septum scale 8, the sPAP95 RV unloaded cavity remains only 48.6% of the end-diastolic target volume. Uniform passive material properties exaggerate the deformation needed to inflate the RV from its unloaded state to end diastole.

## Capped-RV-EDP Unloading

A more targeted correction keeps the end-diastolic mesh target but caps the RV end-diastolic pressure used during inverse unloading at 5 mmHg. Wall thickness, curvature, activation, and passive material parameters remain fixed. The cap changes only the most questionable input to the unloading problem.

```{table} Effect of capping RV end-diastolic pressure at 5 mmHg during inverse unloading in completed capped cases. Fractions are unloaded volume divided by the fixed end-diastolic target volume.
:name: tab-app-rvedp-capped-unloading
:align: left

| Case | Baseline LV | Capped LV | Baseline RV | Capped RV |
|---|---:|---:|---:|---:|
| sPAP22 | 80.5% | 78.3% | 55.6% | 62.7% |
| sPAP55 | 80.3% | 80.1% | 31.1% | 60.7% |
| sPAP65 | 75.1% | 74.0% | 33.7% | 67.2% |
| sPAP95 | 72.2% | 75.8% | 20.9% | 65.3% |
```

Across the 16 production sweep cases, the inferred unloaded cavity reductions under the cap fall in the range 20–26% for the LV and 32–39% for the RV. The raw uncapped RV end-diastolic pressures targeted by these cases ranged from 4.8 to 16.3 mmHg, so the cap was inactive in three cases whose raw targets sat just below 5 mmHg and brought the targets from up to about 16 mmHg down to 5 mmHg in the higher-pressure cases.

## Round-Trip Check

Forward-simulating from the inferred unloaded reference back to end diastole should reproduce the imaged ED, since that is what the inverse problem is defined to solve. In the most severe uncapped case (sPAP95) this round-trip fails: the forward-simulated ED differs from the imaged ED by 9.4 mm whole-mesh mean and 13.9 mm at the septum (maximum local discrepancy 32 mm), while cavity volume is recovered exactly through the Lagrange-multiplier coupling. With the cap applied to the same case the residual drops to 3.7 mm whole-mesh mean and 4.3 mm at the septum, below typical CMR in-plane voxel resolution.

The discrepancy is septum-localised in the uncapped case: the septum residual is roughly 1.5 times the LV free-wall (9.0 mm) and RV free-wall (8.2 mm) means, consistent with the septum being the region whose deformation mode is most sensitive to the unloaded reference. Without the cap, the two solvers honour the cavity volume but disagree on the end-diastolic shape, particularly at the septum.

The qualitative picture is in {numref}`fig-app-unloaded-cap-grid` and {numref}`fig-app-ed-cap-grid`. Each figure shows three representative sweep cases (sPAP22, sPAP60, sPAP95 left to right) with the production capped run in the top row and the matching uncapped pilot in the bottom row. {numref}`fig-app-unloaded-cap-grid` shows the inferred unloaded reference itself: with the cap in place the unloaded geometry stays plausibly shaped across the sweep, while the uncapped severe case (bottom right) shows a markedly collapsed RV and septum. {numref}`fig-app-ed-cap-grid` shows the forward-simulated end-diastolic state for the same six runs. The capped severe case (top right) reproduces the imaged end-diastolic geometry with septal flattening visible — the characteristic D-sign of RV pressure overload {cite}`ryan1985echocardiographic` — while the uncapped severe case (bottom right) deviates grossly from the imaged target.

```{figure} ../figures/fig_unloaded_cap_grid_nocbar.png
:name: fig-app-unloaded-cap-grid
:width: 95%

Inferred unloaded reference geometry at three representative sweep cases — sPAP22, sPAP60, sPAP95 from left to right — with the production capped runs in the top row and the matching uncapped pilots in the bottom row. The same short-axis cut and the same colour scale are used in every panel: colour encodes the cell-wise displacement magnitude $|u_\text{ED}|$ that the forward inflation has to deliver to take this geometry back to the imaged end-diastolic mesh, with deep blue at zero and warm colours up to about 2 cm (the scale saturates above that; localised residuals in the uncapped severe case reach roughly 3 cm). With the cap in place the displacement field remains moderate across the sweep and the unloaded RV keeps a plausible shape. Without the cap, the inferred unloaded RV in the severe case (bottom right) is much smaller and demands very large displacements to be inflated back to end diastole, concentrated in the septum.
```

```{figure} ../figures/fig_ed_cap_grid_nocbar.png
:name: fig-app-ed-cap-grid
:width: 95%

Forward-simulated end-diastolic geometry from the same three sweep cases and the same six runs as {numref}`fig-app-unloaded-cap-grid`. Colour is the same displacement magnitude $|u_\text{ED}|$ from the inferred unloaded reference to the imaged end-diastolic target, on the same 0–2 cm saturating scale. The capped severe case (top right) shows the septum flattened toward the LV — the D-sign of RV pressure overload — at moderate displacement, consistent with the imaged geometry. The uncapped severe case (bottom right) does not reproduce that morphology: the forward-inflated shape disagrees with the imaged end-diastolic mesh across the wall, with the largest residual at the septum. This is the visual companion to the 3.7 mm / 4.3 mm capped versus 9.4 mm / 13.9 mm uncapped whole-mesh / septum residuals reported above.
```

The capped-unloading result is the most defensible fixed-geometry path among the tested options. It preserves the logic of inverse unloading from an end-diastolic image mesh, avoids treating passive stiffness as a free post-hoc target, and removes much of the severe RV reference collapse. The effect on work density is not a simple downward correction: in the severe sPAP80–92 block, mean RV stress-strain work density rose from 4.68 to 6.20 kPa and mean septal stress-strain work density from 2.26 to 5.53 kPa — reference-state sensitivity, not a guaranteed direction of bias.

Acute fixed-reference loading was tested as the opposite limit by reusing the low-pressure reference configuration while increasing RV pressure. The high-pressure cases produced non-finite stress-strain work values even with circulation preconditioning and pressure/volume ramping. That failure is informative: the model needs a compatible pre-stressed reference state, and the original high-RV-EDP unloading target was too aggressive.

## Work-Component Decomposition Under the Cap

A complementary observation comes from the regional work-component decomposition. In the uncapped pre-cap sweep the septum's fibre share drifts from about 78% at low RV pressure down to 67% at high RV pressure, with the sheet-normal share rising from 31% to 40% and the cross-axis share climbing from about $-2\%$ to $+10\%$. The capped sweep keeps these proportions flat — fibre near 80%, sheet-normal near 32%, cross near zero across all sixteen cases. The free walls show no such drift in either sweep.

The septum is the only region where the decomposition is sensitive to the reference-state choice, because it is the only region whose deformation mode is strongly dictated by how the unloaded shape is inferred. The capped sweep brings every case to a similar unloaded reference, so case-to-case variation reduces to differences in cycle loading. The uncapped sweep lets each case re-infer its own unloaded shape from its own end-diastolic-pressure target, and the very small unloaded RV that this produces in the severe cases drives transmural stretch on the septum that shifts work out of fibre. Which sweep represents physiology better is not directly decidable from the data alone; both are different calibration choices against the same image-derived mesh.

## Cap-Value Sensitivity

The cap value itself was tested for sensitivity. {numref}`fig-app-cap-sensitivity-unloading` shows the per-case unloaded RV fraction at four cap values (3, 5, 8, 10 mmHg) across the sweep. Above 5 mmHg the inferred unloaded RV collapses toward the same regime as the uncapped pilot — at 10 mmHg severe cases unload to 33–37% of ED, and at 8 mmHg to 41–47%. Below 5 mmHg the unloading is mild and uniform across the sweep (80–84%). The 5 mmHg production cap sits at the boundary where severe cases just begin to enter the small-unloaded-reference regime.

```{figure} ../figures/fig_app_cap_sensitivity_unloading.png
:name: fig-app-cap-sensitivity-unloading
:width: 80%

Sensitivity of the inferred unloaded RV fraction to the cap value, across the sixteen capped-reference sweep cases. Each line is one case, coloured by achieved RV systolic pressure. Above 5 mmHg the severe cases enter the small-unloaded-reference regime; below 5 mmHg the unloading is mild and uniform. The 5 mmHg production cap sits at the boundary.
```

To check that the central septum result does not depend on the exact cap value, six representative cases (sPAP22, sPAP45, sPAP65, sPAP80, sPAP92, sPAP95) were re-run with a 3 mmHg cap and compared to the matching cap=5 cases. The transmural pressure-strain proxy correlation stays negative at both cap values, and the septum magnitude ranking is preserved — LV pressure remains the best single-pressure choice and transmural pressure remains the worst.

```{table} Cycle-level cap sensitivity for the six-case subset (sPAP22, sPAP45, sPAP65, sPAP80, sPAP92, sPAP95). Septum $\eta$ values are mean absolute log-ratio errors for the septum/free-wall ratio under the tangent-longitudinal pressure-strain proxy.
:name: tab-app-cap-sensitivity-cycle
:align: left

| Cap (mmHg) | $r$ (transmural proxy, septum FE work) | Septum $\eta$ pLV | Septum $\eta$ pRV | Septum $\eta$ trans | Septum $\eta$ mean |
|---:|---:|---:|---:|---:|---:|
| 3 | -0.074 | 0.751 | 1.095 | 2.105 | 0.905 |
| 5 (six-case subset) | -0.468 | 0.798 | 1.144 | 2.159 | 0.952 |
| 5 (full 16-case, reference) | -0.331 | 0.805 | 1.171 | 2.075 | 0.969 |
```

The unloading bracket and the cycle robustness together justify the 5 mmHg choice: it cannot move much higher without re-entering the small-unloaded-reference regime, and it does not need to move lower because the central septum conclusion holds at cap=3.

## Pre-cap versus Capped Septum Comparison

The changed reference-state path also changed the septal proxy ranking. {numref}`tab-app-precap-capped-septum` keeps the older sweep visible as a sensitivity result, while making clear that the rightmost capped columns are the production result used in {ref}`chap-results`.

```{table} Pre-cap versus capped septal proxy performance. Correlations are Pearson correlations with septal finite-element stress-strain work density across the 16-case sweep. Magnitude error is the mean absolute log error in the septum/free-wall work-density ratio, using tangent-longitudinal pressure-strain density.
:name: tab-app-precap-capped-septum
:align: left

| Pressure choice | Pre-cap ranking $r$ | Capped ranking $r$ | Pre-cap magnitude error | Capped magnitude error |
|---|---:|---:|---:|---:|
| $p_\text{LV}$ | 0.892 | 0.540 | 0.254 | 0.805 |
| $p_\text{RV}$ | -0.191 | 0.527 | 0.420 | 1.171 |
| $p_\text{LV}-p_\text{RV}$ | 0.946 | -0.331 | 0.952 | 2.075 |
| Mean pressure | 0.532 | 0.535 | 0.290 | 0.969 |
| Nearest-side pressure | 0.279 | 0.547 | 0.309 | 0.999 |
| Through-wall weighted pressure | 0.484 | 0.540 | 0.290 | 0.970 |
```

In the pre-cap path, transmural pressure ranked the sweep well, but it already preserved magnitudes poorly. After the capped unloading correction, transmural pressure is poor by both tests, while LV, mean, nearest-side, and through-wall weighted pressure choices preserve a moderate positive ranking signal of $r \approx 0.53$–$0.55$. The common result across both sweeps is therefore not a universal best septal pressure but the weaker and more defensible claim used in the thesis: septal pressure-strain work is sensitive to loading and reference-state choices, and magnitude preservation is a safer diagnostic than sweep ranking alone.

The shift from a weakly positive transmural ranking ($r=0.222$ under per-case canonical tagging) to a negative one ($r=-0.331$ under reference-tag postprocessing) had a specific methodological cause, not a change in the underlying simulations. In the per-case canonical analysis the geometric septum varied from 1203 to 1278 cells across the sixteen cases, and that case-to-case mask drift was enough to inject a spurious positive correlation. The reference-tag postprocessing of {ref}`sec-reference-tag-postprocessing` fixes the geometric septum at 1269 cells in every case and removes the drift. An independent check confirms the negative correlation is not an artefact of the proxy construction either: the Pearson correlation between achieved peak transmural pressure $p_\text{LV,ES}-p_\text{RV,ES}$ and the FE septal stress-strain work density across the sweep is $r=-0.56$, more negative than the proxy's $-0.331$.

Despite the sign flip between sweeps, the qualitative magnitude story is preserved: in both pre-cap and capped sweeps, transmural pressure is the worst single-pressure magnitude candidate and LV pressure the best. The cap choice is load-bearing only for case-ranking correlations and severe-case absolute work magnitudes, not for the central LV-best / transmural-worst septum/free-wall magnitude conclusion.
