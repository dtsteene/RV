(chap-appendix-numerical)=
# Numerical Robustness Appendix

This appendix collects the numerical checks that support the main pressure-strain conclusions. The purpose is not to claim that the simulations are free of numerical uncertainty. The purpose is to show where that uncertainty was tested, which quantities were sensitive, and why the final production choices were retained.

## Production Configuration

The production simulations use the compressible biventricular mechanics formulation, second-order tetrahedral displacement elements, a characteristic mesh length of 5 mm, and six coupled beats. Regional stress-strain work density is computed offline from the saved displacement checkpoints over the final beat. The current stress is evaluated from the UFL constitutive expression at quadrature points, previous stress and strain states are stored in a degree-six quadrature space, and DG0 test functions are used only to extract cellwise integrals from the quadrature-level work density.

The basal support combines Robin springs on the epicardium and base with a partial basal Dirichlet condition that fixes only the base-normal/global-x displacement component. It is not a full basal clamp. The remaining two displacement components on the basal surface are free to slide.

The robustness checks are summarized in {numref}`tab-numerical-robustness-summary`. Direct production audits are separated from related numerical-method and historical sensitivity checks. Only the direct capped shared-L5 checks are used as evidence for the numerical values in {ref}`chap-results`; the older pre-cap and exploratory checks are retained to explain why the final interpretation became more conservative. The main pattern is consistent across the checks: hemodynamics and free-wall ratios are comparatively stable, while septal absolute work density is the quantity that most deserves caution.

```{table} Summary of numerical checks supporting the production configuration.
:name: tab-numerical-robustness-summary
:align: left

| Check | Evidence | Consequence for interpretation |
|---|---|---|
| Energy-consistent postprocessing | Quadrature-level stress-strain work closes the whole-heart boundary-work budget to about $10^{-5}$--$10^{-4}$ relative error | The regional work reference is computed from the same mechanics that drives the cavities |
| Primary capped sweep audit | All 16 capped shared-L5 cases completed strict canonical quadrature-level postprocessing on the same 8070-cell reference mesh, with finite pressure histories and per-cell work arrays | The primary figures and tables use a complete internally consistent regional result set with one-to-one cell correspondence |
| Capped septum envelope sweep | Epi-excluded and epi-inclusive relaxed septum envelopes were recomputed on the capped shared-L5 sweep | The geometric septum cutoff is unchanged; the far relaxed tail changes modestly, and transmural pressure remains a poor capped-sweep ranking proxy |
| Principal-strain replay | All 16 capped cases were replayed from displacement checkpoints; fibre direction was closer to septal principal shortening than longitudinal strain, while principal shortening itself did not remove the pressure-choice ambiguity | The strain-direction limitation is real, but full local 3D strain information would be needed to resolve it |
| Mesh convergence | h=5 differs from h=3.75 by less than 0.8% for hemodynamics and less than about 3% for free-wall ratios in the endpoint mesh study; severe septal work differs by about 5--7% | Free-wall conclusions are robust; high-pressure septal magnitudes are reported with mesh sensitivity in mind |
| Postprocessing space replay | DG1 stays within about 1.2% of Quadrature6 for integrated regional stress-strain work; DG0 underestimates high-pressure septal work | DG1 is adequate for integrated regional totals in this check; DG0 is too crude for septal work; Quadrature6 is retained as the conservative production path |
| Basal support audit | The production condition fixes only the base-normal/global-x component; tangential basal sliding remains | The model does not use a full basal clamp |
| No-Dirichlet variants | Endpoint cases failed during end-diastolic inflation after removing the basal displacement constraint | The partial constraint is a stabilizing modelling choice in this production setup |
| Robin work budget | Signed net Robin work is below about 0.2% of cavity boundary work in checked endpoint cases | Robin springs are part of the model definition but do not dominate the reported work-density results |
| 3D--0D coupling interface | Volume ratio sits within a few percent of unity in most production cases; a controlled pulmonary-compliance sweep shows the interface remains usable at right-ventricular ratios as low as 0.26 | Bounds the 0D-parameter range over which the volume-coupling design is reliable |
| Historical h=10/h=5 full-sweep rerun | In the 16 paired pre-cap cases, LV/RV pressures shifted by at most 1.8%/1.1% and free-wall ratios by a few percent | This supports the broad free-wall pressure-strain result as a resolution-robust finding, but is not a capped-sweep convergence proof |
| Pre-cap versus capped sweep comparison | The pre-cap and capped 16-case sweeps give different septal ranking correlations: transmural pressure was strongest in the pre-cap path, but not in the capped primary path | The old sweep is retained as a loading/reference-state sensitivity, not as the main septal result |
| Reference-state and remodelling sensitivity | Unloading-only regional stiffness variants, capped-RV-EDP production cases, acute fixed-reference pilots, and exploratory patient meshes were compared with the fixed-geometry production interpretation | Severe fixed-geometry RV and RV-side septal work-density magnitudes are reference-state sensitive; the pressure-proxy conclusions remain fixed-geometry tests |
```

## Energy-Consistent Postprocessing

The model-side reference quantity is the stress-strain work density

$$
w_\mathrm{int}[\Omega_j] =
\frac{1}{|\Omega_{j,0}|}
\int_0^T\int_{\Omega_{j,0}}\mathbf{S}:\dot{\mathbf{E}}\,dV_0\,dt.
$$

Early postprocessing attempts projected stress and strain into discontinuous Galerkin spaces before integrating this quantity. During development, these projected-field replays were associated with large energy-budget discrepancies: smooth-looking stress and strain fields could still give work totals that were far too small compared with the boundary work. Later replay tests showed that this was not simply a DG1-versus-quadrature issue. Once the stress evaluation, pressure history, and boundary-work bookkeeping had been corrected, DG1 reproduced integrated regional work closely. DG0, however, still suppressed high-pressure septal work. The final pipeline therefore uses quadrature-level stress evaluation as the conservative production path rather than as proof that DG1 totals are unusable.

The final method avoids projecting the current stress before integration. The current stress is evaluated directly from the constitutive law at quadrature points, previous stress and strain are stored in a degree-six quadrature space for the trapezoidal time rule, and the DG0 space is used only as a cellwise partition of unity. As a hard implementation check, the sum of the DG0 per-cell work values is compared with an independent scalar domain integral of the same quadrature-level expression. In the checked runs, this agreement is at machine precision, confirming that the cellwise extraction is not changing the integrated work.

The external work terms were also matched to the solver formulation. Cavity work uses the actual solver cavity pressures, not the 0D elastance pressures, and the volume change is computed from the nonlinear cavity-volume expression rather than a linearized surface displacement. Robin work uses the same deformed-normal/Nanson formulation as the variational boundary condition. With these choices, the whole-heart stress-strain work and boundary-work budget close to the small residual shown in the main text.

(sec-app-mesh-convergence)=
## Mesh Convergence

The primary capped-reference sweep was also audited directly before being promoted to the main result set. All 16 cases in the capped shared-L5 sweep use a single 5 mm reference tetrahedralisation ($n=8070$ cells) and a single set of region tags, integrated under the reference-tag protocol of {ref}`sec-reference-tag-postprocessing`. The pressure histories have shape `(4800, 2)`, the per-cell arrays are finite, and the geometric septum is 1269 cells while the tag-3 septum is 1266 cells in every case (a 0.1% volume difference shared across the sweep). The capped sweep is therefore numerically usable as a complete regional production set with one-to-one cell correspondence across cases.

The separate mesh-convergence study repeated three representative pressure cases, sPAP22, sPAP60, and sPAP95, using characteristic lengths of 10, 7.5, 5, and 3.75 mm. The 3.75 mm runs were used as the finest available reference.

At the production 5 mm resolution, hemodynamic quantities differed from the 3.75 mm reference by less than 0.8%. Free-wall work-density ratios were also stable, with differences below about 3%. Septal quantities were more mesh-sensitive, especially at high RV pressure. At 5 mm, septal stress-strain work differed from the 3.75 mm reference by about 0.2% in sPAP22, 3.8% in sPAP60, and 5.7% in sPAP95; the largest septal longitudinal-proxy discrepancy was about 6.6%. The 10 mm mesh was clearly too coarse for septal quantities in the high-pressure case, with errors up to about 18%.

The interpretation is therefore targeted: the 5 mm production mesh is sufficient for the qualitative free-wall conclusions tested here, while absolute high-pressure septal values should be read with the observed 5-7% difference between the 5 mm and 3.75 mm meshes in mind. This is a practical finest-mesh comparison, not a formal mesh-uncertainty estimate.

The historical pre-cap corrected pressure sweep was also rerun at 5 mm resolution. Across the 16 h=10/h=5 paired pre-cap cases, achieved LV and RV end-systolic pressures changed by at most 1.8% and 1.1%, respectively. The free-wall finite-element LV/RV stress-strain work ratio changed by at most 5.4%, and the adjacent-pressure longitudinal proxy ratio by at most 11.9%. This supports the free-wall pressure-strain result as a robust regional finding rather than a consequence of the coarse 10 mm sweep. It is retained as numerical-method support for the broad free-wall result, not as a direct convergence proof for the capped reference-state choice.

The distinction is important because an h=10-to-capped-h=5 comparison would mix three changes at once: mesh resolution, the RV-EDP cap during inverse unloading, and the achieved pressure path. That mixed comparison is not used as a mesh-convergence estimate. The capped sweep is evaluated directly as the primary 5 mm production set, while the pre-cap h=10/h=5 rerun is kept only as resolution support for the broad free-wall conclusion.

The septum required a different interpretation. The 10 mm corrected sweep used a case-specific geometric septum mask that covered only part of the tag-3/canonical septum in several cases. In the completed capped shared-L5 sweep, the geometric septum volume matches the tag-3 septum volume to within about 0.1% in every case. For that reason, h=10-to-h=5 septal differences are not reported as simple mesh errors. The high-resolution capped septal results replace the earlier septal tables rather than merely perturbing them. This is the conservative choice: it avoids treating a change in septal definition as a change in mesh resolution.

(sec-app-coupling-robustness)=
## 3D--0D Coupling Interface

The fixed mesh-to-circulation volume ratio defined in {ref}`sec-3d-0d-coupling` is the only point at which 0D and 3D end-diastolic volumes are reconciled. Whether this scalar correction is small or large depends on how close the 0D end-diastolic volume sits to the mesh end-diastolic volume after calibration. The optimizer in {ref}`chap-calibration` includes the mesh end-diastolic volumes as targets, but the cost function balances them against pressure, flow, ejection-fraction, and stroke-volume balance, so an exact match is not enforced and a residual ratio offset is accepted. Across the sixteen primary production cases the left-ventricular ratio sits within three percent of unity in twelve cases, while three intermediate-pressure cases (sPAP60 to sPAP70) require left-ventricular scalings of seventeen, twenty-one, and forty-seven percent. The right-ventricular ratio is more uniformly off-unity, with magnitudes between near zero and sixteen percent and a tendency toward larger corrections in the lower-pressure cases. The interface ratio is therefore not decorative in the production sweep: it absorbs a small-to-moderate residual mismatch that the joint pressure-and-volume optimization leaves behind, including one outlier in which the left-ventricular correction is large.

A separate sensitivity sweep tested how far the interface can be pushed before the coupled simulation breaks. The same UKB mean mesh was coupled to five 0D parameter sets in which pulmonary arterial compliance was reduced by factors $f \in \{1.00, 0.75, 0.50, 0.25, 0.10\}$ and pulmonary arterial resistance was raised by the inverse factor, while the rest of the circulation was held fixed and not re-tuned for the perturbed pulmonary load. Under these unbalanced parameter sets the 0D model itself responds strongly: the right-ventricular end-diastolic volume in the standalone 0D pre-run grows from about 180 mL at $f=1.00$ to about 285 mL at $f=0.10$, well outside any physiological range. The volume ratio absorbed this drift transparently, with $s_\text{RV}$ falling from 0.42 to 0.26 across the sweep. All five coupled simulations completed six beats and reached periodic cavity volumes by the third beat, with no solver failures or evident strain artefacts. The interface therefore remains usable at right-ventricular ratios roughly an order of magnitude further from unity than the production runs ever encounter, which is the relevant numerical-robustness statement for the volume-coupling design.

(sec-app-reference-remodeling-sensitivity)=
## Reference-State and Remodelling Sensitivity

The inverse-unloading workflow treats the image-derived mesh as a loaded end-diastolic target. That is the appropriate target for a single end-diastolic image-derived mesh, but it also means that the unloaded reference depends on the end-diastolic pressures, the passive material parameters, and the anatomy used during unloading. In the pressure sweep, the anatomy and passive material law are held fixed while RV pressure is raised. This is useful for isolating the pressure-proxy question, but it removes the RV hypertrophy, curvature changes, and regional passive remodelling that would normally accompany severe PAH.

This matters most for the RV. In the uncapped fixed-geometry pilot, the inferred RV unloaded cavity became much smaller as RV end-diastolic pressure increased. A late unloading-only sensitivity sweep tested whether regional passive stiffening could reduce that collapse. The LV material scale was held at 1.0, while RV and septal scales were varied; the stiffest tested point used RV scale 16 and septum scale 8. This was not a full corrected production rerun, because only the unloading stage was repeated. It is therefore a reference-state sensitivity check, not a replacement result set.

```{table} Unloaded-volume fraction in the baseline unloading and in the stiffest tested RV/septum regional material variant. Fractions are unloaded volume divided by the fixed end-diastolic target volume.
:name: tab-app-reference-stiffness
:align: left

| Case | Baseline LV | Stiffened LV | Baseline RV | Stiffened RV |
|---|---:|---:|---:|---:|
| sPAP22 | 80.5% | 82.4% | 55.6% | 80.2% |
| sPAP60 | 74.9% | 78.7% | 34.3% | 63.3% |
| sPAP95 | 72.2% | 77.4% | 20.9% | 48.6% |
```

The pattern is clear. Regional RV and septal stiffening makes the low-pressure case much more plausible and improves the intermediate case substantially. It does not fully rescue the severe case: even at RV scale 16 and septum scale 8, the sPAP95 RV unloaded cavity remains only 48.6% of the end-diastolic target volume. The conclusion is therefore not that the stiffened run is the correct model. The conclusion is that the severe fixed-geometry production sweep is reference-state sensitive, and that uniform passive material properties likely exaggerate the deformation needed to inflate the RV from its unloaded state to end diastole.

A more targeted correction was then tested by keeping the same end-diastolic mesh target but capping the RV end-diastolic pressure used during inverse unloading at 5 mmHg. This is not a complete PAH remodelling model: wall thickness, curvature, activation, and passive material parameters remain fixed. Its value is that it changes the most questionable input to the unloading problem directly, rather than using regional stiffness as an uncalibrated tuning parameter. In the completed capped cases, the RV unloaded/ED fraction moved substantially upward while the LV unloaded/ED fraction stayed in the same range as before.

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

This capped-unloading result is the most defensible fixed-geometry path among the tested options, and it is therefore used as the primary sweep in the thesis. It preserves the logic of inverse unloading from an end-diastolic image mesh, avoids treating passive stiffness as a free post-hoc target, and removes much of the severe RV reference collapse. The effect on work density was not a simple downward correction: in the severe sPAP80--92 block, mean RV stress-strain work density increased from 4.68 to 6.20 kPa and mean septal stress-strain work density from 2.26 to 5.53 kPa. The important conclusion is therefore reference-state sensitivity, not a guaranteed direction of bias. Acute fixed-reference loading was also tested as the opposite limit, by reusing the low-pressure reference configuration while increasing RV pressure, but high-pressure cases produced non-finite stress-strain work values even with circulation preconditioning and pressure/volume ramping. That failure is informative: the model needs a compatible pre-stressed reference state, but the original high-RV-EDP unloading target was too aggressive. The capped-RV-EDP sweep is therefore a bounded sensitivity model, not a claim that the fixed UKB anatomy has become a remodeled PAH heart.

The changed reference-state path also changed the septal proxy ranking, which is why the capped sweep replaces the pre-cap sweep in the main results. {numref}`tab-app-precap-capped-septum` keeps the older sweep visible as a sensitivity result, while making clear that the rightmost capped columns are the production result used in {ref}`chap-results`.

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

The table shows why the old pre-cap ranking should not be carried into the main thesis narrative. In that path, transmural pressure ranked the sweep well, but it already preserved magnitudes poorly. After the capped unloading correction, transmural pressure is poor by both tests, while LV, mean, nearest-side, and through-wall weighted pressure choices preserve a moderate positive ranking signal of $r \approx 0.53$--$0.55$. The common result across both sweeps is therefore not a universal best septal pressure. It is the weaker and more defensible claim used in the thesis: septal pressure-strain work is sensitive to loading and reference-state choices, and magnitude preservation is a safer diagnostic than sweep ranking alone.

The shift from a weakly positive transmural ranking ($r=0.222$ under per-case canonical tagging) to a negative one ($r=-0.331$ under shared-tag postprocessing) had a specific methodological cause rather than a change in the underlying simulations. In the per-case-canonical analysis the geometric septum varied from 1203 to 1278 cells across the sixteen cases, and that case-to-case drift was sufficient to inject a spurious positive correlation that the shared-tag protocol of {ref}`sec-reference-tag-postprocessing` — which fixes the geometric septum at 1269 cells in every case — removes. An independent check confirms the negative correlation is not an artefact of the proxy construction either: the Pearson correlation between the achieved peak transmural pressure $p_\text{LV,ES}-p_\text{RV,ES}$ and the finite-element septal stress-strain work density across the sweep is $r=-0.56$, more negative than the proxy's $-0.331$.

Despite the sign flip of the case-ranking correlation between sweeps, the qualitative magnitude story is preserved: in both pre-cap and capped sweeps, transmural pressure is the worst single-pressure magnitude candidate and LV pressure the best. The cap choice is load-bearing only for case-ranking correlations and severe-case absolute work magnitudes, not for the central LV-best / transmural-worst septum/free-wall magnitude conclusion.

The exploratory patient meshes give a second, independent direction check. The PAH mesh is not merely the healthy mesh under a different pressure load. It has smaller cavities and more wall volume: RV EDV is 74.2 mL rather than 94.4 mL, while total wall volume is 165.7 mL rather than 129.1 mL. In the selected same-label comparisons, the thicker PAH geometry tended to carry lower RV and septal stress-strain work density than the healthy geometry at similar or even higher RV systolic pressure. The pressure-strain proxy did not always attenuate with the stress-strain work density, especially in the RV free wall.

```{table} Exploratory same-label healthy/PAH geometry comparisons. Work densities are reported as healthy/PAH pairs. Finite-element values use stress-strain work density. Proxy values use tangent-longitudinal pressure-strain density; the RV proxy uses adjacent RV pressure, and the septal proxy uses mean LV/RV pressure.
:name: tab-app-patient-geometry-direction
:align: left

| Case | RVSP (mmHg) | RV FE (kPa) | RV proxy (kPa) | Septum FE (kPa) | Septum proxy (kPa) |
|---|---:|---:|---:|---:|---:|
| sPAP22 | 31.7 / 31.7 | 3.69 / 1.51 | 0.35 / 0.30 | 6.54 / 2.90 | 0.71 / 0.46 |
| sPAP30 | 40.5 / 34.9 | 5.05 / 1.78 | 0.48 / 0.34 | 7.01 / 3.00 | 0.83 / 0.52 |
| sPAP45 | 41.7 / 49.8 | 4.90 / 3.02 | 0.46 / 0.56 | 6.55 / 3.72 | 0.78 / 0.72 |
| sPAP55 | 57.6 / 57.8 | 5.77 / 3.19 | 0.55 / 0.63 | 5.20 / 3.48 | 0.75 / 0.66 |
| sPAP65 | 61.5 / 72.8 | 4.75 / 4.08 | 0.54 / 0.79 | 5.08 / 3.73 | 0.74 / 0.74 |
```

These patient-geometry runs are deliberately not promoted to main results. The healthy high-pressure sequence did not fully complete, the selected cases used end-diastolic region tagging, and the comparison changes anatomy, loading, and numerical robustness together. Their purpose here is narrower: they show that the fixed UKB pressure sweep should not be read as a patient-specific PAH remodelling model. In a thicker/remodelled geometry, RV and septal stress-strain work density can be lower at comparable RV pressure, while the pressure-strain proxy may attenuate less or even increase because it does not explicitly include wall volume, curvature, passive remodelling, or reference-state changes. Together with the capped-unloading production sweep, this means the severe fixed-geometry RV and RV-side septal magnitudes are best read as reference-state and geometry sensitive rather than as corrected PAH tissue-work estimates. The geometry-dependent relationship between the clinical-style pressure-strain proxy and finite-element stress-strain work density should be treated as a high-priority future-work question.

This caveat does not invalidate the main pressure-proxy comparisons. The free-wall adjacent-pressure result and the failure of transmural pressure as a septum/free-wall work-density proxy are comparisons made within the same fixed-geometry simulations. The sensitivity checks change the interpretation of absolute severe-case work-density magnitudes, not the central conclusion that the septum is a shared-wall pressure-assignment problem.

(sec-app-septum-epi-envelope)=
## Septum Envelope Sensitivity

The boundary-relaxation sweep defines a family of septal masks,

$$
\Omega_\mathrm{sep}(t)
= \{c : \mathrm{entry}_t(c) < t\}\cap\Omega_\mathrm{env},
$$

where $\mathrm{entry}_t=\max(d_\mathrm{LV},d_\mathrm{RV})-d_\mathrm{epi}$, so that $t=0$ recovers the geometric septum. The envelope $\Omega_\mathrm{env}$ prevents the relaxed mask from growing indefinitely into the free walls. The production sweep used the stricter envelope

$$
\Omega_\mathrm{env}
= \{d_\mathrm{LV}+d_\mathrm{RV}\leq 22~\mathrm{mm}\}\cap\{\mathrm{not\ touching\ epicardium}\}.
$$

This topological epicardial exclusion removes cells on the outer boundary of the ventricular wall. The reason for keeping it in the production definition is practical: near the LV/RV junction, the free wall becomes thin and an epicardial boundary cell can satisfy the relaxed distance criterion even though it is still part of the outer wall surface. Excluding epicardial-touching cells makes the relaxed sweep a conservative interior-septum envelope.

The opposite convention was tested by using only $d_\mathrm{LV}+d_\mathrm{RV}\leq 22$ mm. This epi-inclusive envelope is anatomically defensible if the goal is to let the geometric parametrization grow the septal mask all the way to the outer wall. The earlier pre-cap version of this check gave a high transmural-pressure ranking correlation, but that was a reference-state and loading-path result rather than a production robustness result. The sweep below was therefore recomputed from the capped shared-L5 per-cell arrays. The two definitions are identical at the actual geometric septum cutoff and first diverge only at about $t=+4.5$ mm. The difference is therefore not a change to the reported primary septum; it is a sensitivity of the far relaxed sweep tail.

```{figure} ../figures/fig_app_septum_epi_envelope_comparison.png
:name: fig-app-septum-epi-envelope
:width: 95%

Effect of allowing epicardial-touching cells into the relaxed septum sweep in the capped shared-L5 production set. Solid lines use the production epi-excluded envelope; dashed lines use the epi-inclusive envelope. The lower panel shows the inclusive-minus-excluded correlation change. The definitions coincide through the geometric cutoff and separate only when the relaxed mask reaches the outer wall.
```

```{table} Selected thresholds from the capped shared-L5 epi-excluded and epi-inclusive septum sweep comparison. Correlations are Pearson correlations between volume-integrated septal stress-strain work and longitudinal pressure-strain proxies across the 16 capped production cases.
:name: tab-app-septum-epi-envelope
:align: left

| $t$ (mm) | Cells excl. -> incl. | $r(p_\mathrm{LV})$ | $r(p_\mathrm{RV})$ | $r(p_\mathrm{LV}-p_\mathrm{RV})$ | $r(p_\mathrm{mean})$ |
|---:|---:|---:|---:|---:|---:|
| 0 | 1269 -> 1269 | 0.540 -> 0.540 | 0.528 -> 0.528 | -0.333 -> -0.333 | 0.535 -> 0.535 |
| +5 | 1555 -> 1558 | 0.600 -> 0.602 | 0.542 -> 0.543 | -0.358 -> -0.358 | 0.568 -> 0.569 |
| +10 | 1955 -> 2140 | 0.714 -> 0.723 | 0.578 -> 0.585 | -0.333 -> -0.349 | 0.635 -> 0.642 |
| +20 | 2592 -> 3112 | 0.865 -> 0.889 | 0.667 -> 0.641 | -0.351 -> -0.292 | 0.752 -> 0.745 |
```

The effect is now aligned with the primary capped result. Adding the epicardial-touching cells lets the relaxed septal region grow farther toward the outer LV/RV junction, but it does not restore transmural pressure as a work-density pressure scale. At $t=+20$ mm, the inclusive sweep adds 520 cells per case, increasing the region from 2592 to 3112 cells; $r(p_\mathrm{LV})$ changes from 0.865 to 0.889, while $r(p_\mathrm{LV}-p_\mathrm{RV})$ changes only from -0.351 to -0.292. The older pre-cap envelope sweep is therefore best understood as a loading/reference-state sensitivity, not as a production mask-robustness result.

This sensitivity check supports two conclusions. First, the geometric septum used in the primary result is not affected by the epicardial-envelope convention. Second, the far relaxed tail of the septum sweep should not be overinterpreted as a unique anatomical septum. It is better read as a controlled definition sensitivity: the strict envelope asks what happens when only interior septal cells are admitted, while the epi-inclusive envelope asks what happens when the geometric parametrization is allowed to grow to the outer wall.

## Basal Boundary Condition

The production basal condition fixes only the base-normal/global-x displacement component. This choice was checked in two ways.

First, the saved displacement fields were audited directly. In the completed pressure-sweep cases, the constrained basal displacement component was zero to saved precision at the checked time points, while the other two basal displacement components retained millimetre-scale sliding motion. This confirms that the final results used the intended partial constraint rather than a full basal clamp. The audit should be treated as a kinematic implementation check rather than a separate boundary-condition sensitivity study.

Second, the no-Dirichlet variant was tested by removing the basal displacement constraint while keeping the same Robin springs and the 5 mm production mesh. The sPAP22, sPAP60, and sPAP95 variants all reached the reference-configuration step but failed during end-diastolic inflation with linear solver non-convergence. A previous coarse one-beat Robin-only test had converged, but that result did not carry over to the production mesh and pressure cases. The retained basal condition is therefore best interpreted as a stabilizing constraint needed in this production setup, not as a physiological claim about the base being fixed in space.

The energetic effect of the Robin support was small compared with the cavity work in the cycle-integrated balance. In the checked endpoint cases, the signed net Robin work was below about 0.2% of the cavity boundary work.

## Postprocessing Space Sensitivity

The main postprocessing sensitivity is the choice of state/storage space used when reconstructing stress and strain histories. The final method uses degree-six quadrature storage because it most directly matches the quadrature-level constitutive evaluation and gave the tightest energy closure during development. A defence-oriented check recomputed sPAP22, sPAP60, and sPAP95 at the production 5 mm mesh with DG0 and DG1 state storage, while keeping the same degree-six integration rule. The current stress expression was still evaluated directly from the constitutive law; only the stored previous stress and strain state used the degraded space.

DG1 reproduced the Quadrature6 integrated regional stress-strain work closely. Across the three representative cases, the largest regional work-density difference was 1.2%, occurring in the septum. DG0 was less reliable: whole-heart and free-wall totals stayed within a few percent, but septal stress-strain work was underestimated by 7.7% in sPAP60 and 15.4% in sPAP95. The energy-budget residual was also smallest for Quadrature6, at about $10^{-5}$ to $10^{-4}$ relative error, compared with up to $2.7\times10^{-3}$ for DG1 and $1.5\times10^{-2}$ for DG0.

The interpretation is that the main integrated regional conclusions are not a fragile artifact of Quadrature6: DG1 gives essentially the same total regional stress-strain work. However, DG0 is not adequate for the high-pressure septal quantities, and the directional component decomposition is more sensitive than total work. Quadrature6 is therefore retained as the production postprocessing space because it gives the best energy closure and avoids suppressing septal stress-strain structure.
