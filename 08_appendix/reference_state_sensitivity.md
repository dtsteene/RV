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

The unloaded-reference visual is in {numref}`fig-unloaded-cap-grid` in chapter 3, where the qualitative collapse of the uncapped severe-case RV motivates the capped setup directly. The end-diastolic companion to that figure is {numref}`fig-app-ed-cap-grid`: it shows the forward-simulated end-diastolic state for the same six runs — three representative sweep cases (sPAP22, sPAP60, sPAP95 left to right), production capped run on top and matching uncapped pilot underneath. The capped severe case (top right) reproduces the imaged end-diastolic geometry with septal flattening visible — the characteristic D-sign of RV pressure overload {cite}`ryan1985echocardiographic` — while the uncapped severe case (bottom right) deviates grossly from the imaged target.

```{figure} ../figures/fig_ed_cap_grid_nocbar.png
:name: fig-app-ed-cap-grid
:width: 95%

Forward-simulated end-diastolic geometry from the same three sweep cases and the same six runs as {numref}`fig-unloaded-cap-grid`. Colour is the same displacement magnitude $|u_\text{ED}|$ from the inferred unloaded reference to the imaged end-diastolic target, on the same 0–2 cm saturating scale. The capped severe case (top right) shows the septum flattened toward the LV — the D-sign of RV pressure overload — at moderate displacement, consistent with the imaged geometry. The uncapped severe case (bottom right) does not reproduce that morphology: the forward-inflated shape disagrees with the imaged end-diastolic mesh across the wall, with the largest residual at the septum. This is the visual companion to the 3.7 mm / 4.3 mm capped versus 9.4 mm / 13.9 mm uncapped whole-mesh / septum residuals reported above.
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

The shift from a weakly positive transmural ranking ($r=0.222$ when each case was tagged on its own end-diastolic geometry) to a negative one ($r=-0.331$ once the cell tags were fixed on the reference mesh) had a specific methodological cause, not a change in the underlying simulations. In the per-case analysis the geometric septum varied from 1203 to 1278 cells across the sixteen cases, and that case-to-case mask drift was enough to inject a spurious positive correlation. Fixing the tags once on the reference mesh ({ref}`sec-shared-mask-tagging`) holds the geometric septum at 1269 cells in every case and removes the drift. An independent check confirms the negative correlation is not an artefact of the proxy construction either: the Pearson correlation between achieved peak transmural pressure $p_\text{LV,ES}-p_\text{RV,ES}$ and the FE septal stress-strain work density across the sweep is $r=-0.56$, more negative than the proxy's $-0.331$.

Despite the sign flip between sweeps, the qualitative magnitude story is preserved: in both pre-cap and capped sweeps, transmural pressure is the worst single-pressure magnitude candidate and LV pressure the best. The cap choice is load-bearing only for case-ranking correlations and severe-case absolute work magnitudes, not for the central LV-best / transmural-worst septum/free-wall magnitude conclusion.

## Robustness Across Sweep Designs

The capping decision can be isolated by holding it constant and varying the rest of the sweep design. Five independently calibrated alternative sweep architectures were therefore compared with the production capped sweep on the same proxy and reference questions. The shared-unloaded sweep uses the same Optuna circulation calibration and Klotz EDPVR as production but replaces per-case inverse unloading with a shared reference inferred from one production case (sPAP30, the case with the lowest final RV end-diastolic pressure). The pre-cap sweep is the Optuna/Klotz production architecture before the cap was introduced, retaining per-case uncapped unloading. The linear-reference sweep is an eight-case Optuna calibration with a linear chamber EDPVR and per-case uncapped unloading. The single-knob sweep is the minimal-engineering alternative — Regazzoni defaults with the pulmonary arterial compliance and resistance scaled by a single factor $f\in\{1.00,0.75,0.50,0.25,0.10\}$, no Optuna, no chamber EA scaling, linear EDPVR — uncapped. The single-knob capped sweep applies the same 5 mmHg RV-EDP cap to the simple-calibration architecture, isolating the cap from the calibration choice. Taken together, the six designs vary the optimizer, the chamber EDPVR form, the calibration target set, and the reference-state strategy, so any feature shared across them is independent of those design choices.

The comparison is laid out in three tables. Free-wall correlations and the LV/RV magnitude ratio appear in {numref}`tab-app-cross-sweep-freewall`. Septum cross-case correlations under four pressure choices appear in {numref}`tab-app-cross-sweep-septum-r`. Septum/free-wall magnitude errors $\eta$ under the same four pressure choices appear in {numref}`tab-app-cross-sweep-septum-eta`. Free-wall correlations are cross-case Pearson $r$ between the volume-weighted adjacent-pressure proxy and the volume-weighted FE work density; LV/RV ratio mean is $\langle|R_\text{proxy}-R_\text{FE}|\rangle$ across cases for the LV/RV free-wall ratio. Septum correlations are cross-case Pearson $r$ between proxy and FE septum work. Septum $\eta$ values are the mean absolute log-ratio errors of septum/free-wall work-density ratios (averaged over the septum/LV and septum/RV pairs). Production capped values are reproduced from the main-text septum proxy table.

```{table} Cross-sweep free-wall correlations and LV/RV magnitude ratio fidelity.
:name: tab-app-cross-sweep-freewall
:align: left

| Sweep | Reference state | $n$ | FW $r$ LV | FW $r$ RV | LV/RV ratio mean |
|---|---|---:|---:|---:|---:|
| production capped | per-case capped 5 mmHg | 16 | +0.99 | +0.97 | 0.16 |
| shared-unloaded | shared sPAP30 prestress | 16 | +1.00 | +0.98 | 0.13 |
| pre-cap | per-case uncapped | 16 | — | — | — |
| linear-reference | per-case uncapped, linear EDPVR | 8 | +0.98 | +0.99 | 0.27 |
| single-knob | per-case uncapped, simple cal | 5 | +0.90 | +0.98 | 1.00 |
| single-knob capped | per-case capped 5 mmHg, simple cal | 5 | +0.43 | +0.84 | 1.07 |
```

```{table} Cross-sweep septum cross-case correlations under four pressure choices.
:name: tab-app-cross-sweep-septum-r
:align: left

| Sweep | Sep $r$ PLV | Sep $r$ PRV | Sep $r$ Trans | Sep $r$ Mean |
|---|---:|---:|---:|---:|
| production capped | +0.54 | +0.53 | −0.33 | +0.54 |
| shared-unloaded | +0.78 | +0.68 | +0.01 | +0.73 |
| pre-cap | +0.89 | −0.19 | +0.95 | +0.53 |
| linear-reference | +0.83 | −0.02 | +0.94 | +0.57 |
| single-knob | +0.47 | −0.21 | +0.34 | +0.23 |
| single-knob capped | −0.19 | −0.65 | +0.07 | −0.33 |
```

```{table} Cross-sweep septum/free-wall magnitude errors $\eta$ under four pressure choices.
:name: tab-app-cross-sweep-septum-eta
:align: left

| Sweep | Sep $\eta$ PLV | Sep $\eta$ PRV | Sep $\eta$ Trans | Sep $\eta$ Mean |
|---|---:|---:|---:|---:|
| production capped | 0.81 | 1.17 | 2.08 | 0.97 |
| shared-unloaded | 0.80 | 1.19 | 2.03 | 0.97 |
| pre-cap | 0.25 | 0.42 | 0.95 | 0.29 |
| linear-reference | 0.29 | 0.35 | 0.68 | 0.23 |
| single-knob | 0.05 | 1.08 | 0.47 | 0.42 |
| single-knob capped | 0.39 | 1.45 | 0.83 | 0.78 |
```

One caveat applies to cross-sweep reading. The two single-knob rows were built with per-case `tag_at_ed` LDRB tagging, which gives a geometric-septum mask covering roughly 40–57% of the LDRB tag-3 region; the other four rows fix the cell tags once on the reference mesh, holding the geometric septum at $\sim$1269 cells. The headline claims below survive because they rest on within-sweep comparisons (cap-induced collapse, magnitude-error growth) rather than on absolute cross-sweep magnitude matching between the per-case and fixed-reference groups.

Two sweep-design-independent patterns emerge from this comparison. The free-wall RV-side adjacent-pressure correlation sits at $r \geq 0.84$ across every design and the LV side at $r \geq 0.90$ in all designs except the single-knob capped sweep, where the imposed cap holds LV ESP nearly constant ($112.6$–$129.2$ mmHg, range $16.6$ mmHg) and the LV correlation drops to $r = +0.43$ on a range too narrow to support a useful cross-case ranking. The LV/RV magnitude ratio precision varies from a few percent in the multi-target Optuna designs to one full unit in both the uncapped and capped single-knob designs, but the qualitative finding — that adjacent cavity pressure preserves the regional ratio better than any of the tested alternatives — does not change. The free-wall pressure-strain result is therefore robust to the optimizer, the EDPVR form, the calibration targets, and the reference-state strategy.

The septum/free-wall magnitude pattern is also sweep-design-independent in its qualitative ordering. LV pressure delivers the smallest single-pressure log-ratio error in every design; transmural pressure is among the two worst single-pressure choices in every design, and is the worst in four of the six (the single-knob capped sweep has $\eta_\text{PRV} = 1.45 > \eta_\text{Trans} = 0.83$ because the narrow simple-calibration pressure range puts adjacent-RV pressure very far from cycle-averaged LV-side loading). The absolute magnitudes of the errors differ between sweeps: production capped and shared-unloaded sit at $\eta_\text{PLV} \approx 0.80$ and $\eta_\text{Trans} \approx 2.05$, while the per-case uncapped sweeps sit lower because their reference-state collapse depresses the absolute work-density values that the ratio is built from. The single-knob capped sweep falls between the two regimes ($\eta_\text{PLV} = 0.39$, $\eta_\text{Trans} = 0.83$), exactly where the cap-only change would place it on the magnitude axis.

The septum cross-case correlation does depend on sweep design, and the dependence has a clean mechanical explanation. The three sweeps with a non-collapsed per-case RV reference (production capped, shared-unloaded, and single-knob capped) give transmural-pressure correlations of $-0.33$, $+0.01$, and $+0.07$ respectively. The two Optuna sweeps with per-case uncapped unloading (pre-cap and linear-reference) give transmural correlations of $+0.95$ and $+0.94$. The uncapped single-knob sweep, whose narrow pressure range only mildly enters the regime where per-case unloading collapses, gives a weakly positive $+0.34$. The strongly positive transmural correlation in the uncapped per-case designs has a single mechanical cause. Inverse unloading at high RV end-diastolic pressure with a non-remodelled UKB anatomy infers an implausibly small unloaded RV cavity, which means the septum begins the cycle pre-bulged toward the RV side of the unloaded geometry. Inflating that reference back to the imaged end-diastolic shape requires a large transmural stretch of the septum, which enters the exponential stiffening regime of the Holzapfel-Ogden law. The septum then deforms much less than it otherwise would during the beat, the work it generates falls, and the deformation that does occur is dominated by the transmural direction — exactly the regime visible in the work-component decomposition where the septum's fibre share drifts from about 78% at low RV pressure down to 67% at high RV pressure in the uncapped sweep while the sheet-normal share rises correspondingly. In the severe-RV cases this produces simultaneously a low transmural pressure (because RV pressure has approached LV pressure) and a low septal stress-strain work density (because the septum has effectively frozen in its pre-bulged shape). These two quantities therefore co-vary across the loading sweep and produce the apparent positive transmural correlation. Removing the per-case reference collapse — either by capping the RV end-diastolic pressure during unloading or by sharing one well-behaved reference across all cases — eliminates the artefact, and the apparent transmural signal collapses to noise.

The conclusion is therefore stronger than the simpler statement that the cap inverts a real positive correlation. The cleanest experiment, the shared-unloaded sweep with no per-case reference-state variation, gives a transmural-pressure correlation indistinguishable from zero ($r = +0.006$) while LV pressure, mean pressure, nearest-side pressure, and through-wall weighted pressure retain positive correlations of 0.68 to 0.78. The qualitative septum result — that transmural pressure has no useful ranking signal for septal stress-strain work density, while two-sided pressure choices do — is not a feature of the capping decision. It is a feature of the proxy itself when applied to a shared wall whose deformation is not dominated by transmural displacement. The capped variant of the single-knob sweep closes the calibration × reference-state factorial. Applying the same 5 mmHg RV-EDP cap to the simple-calibration sweep collapses the transmural-pressure correlation from $r = +0.34$ in the uncapped run to $r = +0.07$, and moves every septum magnitude error partway toward the production-capped scale ($\eta_\text{PLV}$ from $0.05$ to $0.39$ against production $0.81$; $\eta_\text{Trans}$ from $0.47$ to $0.83$ against production $2.08$). The headline prediction therefore holds: the capping decision, not the Optuna calibration architecture, is the operative variable for the transmural-correlation collapse and the magnitude-error growth. The simple-calibration sweep does not reproduce the production-capped sign of the PLV and PRV correlations — both go more negative under the cap on the simple sweep than they do under the cap on Optuna, which is consistent with the small ($n=5$) sweep size and the very narrow LV-pressure range that the simple calibration produces. The cross-sweep central finding survives anyway: across all six designs LV pressure preserves the septum/free-wall magnitude ratio better than any other single-pressure choice, and transmural pressure remains among the two worst across every design.
