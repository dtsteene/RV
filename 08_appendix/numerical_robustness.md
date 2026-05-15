(chap-appendix-numerical)=
# Numerical Robustness

This appendix collects the numerical checks that support the main pressure-strain conclusions. Hemodynamics and free-wall ratios are stable across the tested resolutions, postprocessing spaces, and supports; septal absolute work density is the quantity that most deserves caution. Reference-state and geometry sensitivities are documented separately in {ref}`chap-appendix-reference-state` and {ref}`chap-appendix-patient-geometry`.

## Production Configuration

The production simulations use the nearly-incompressible penalty formulation ($\kappa = 1000$ kPa; pulse's `Compressible2`), second-order tetrahedral displacement elements, a characteristic mesh length $h=5$ mm, and six coupled beats. Regional stress-strain work density is computed offline from the saved displacement checkpoints over the final beat. The current stress is evaluated from the UFL constitutive expression at quadrature points, previous stress and strain states are stored in a degree-six quadrature space (Quadrature6 — values held at the integration points of a sixth-order Gauss rule, not projected to a polynomial basis), and DG0 test functions (piecewise-constant per cell, discontinuous across cell faces) are used only to extract cellwise integrals from the quadrature-level work density. The corresponding piecewise-linear discontinuous space, DG1, appears below as an alternative postprocessing storage.

The basal support combines Robin springs on the epicardium and base with a partial basal Dirichlet condition that fixes only the base-normal/global-x displacement component. It is not a full basal clamp.

Production results are reported on a single 16-case sweep, referred to throughout this appendix as the **capped shared-L5 sweep**: sixteen hemodynamic cases run on a single shared 5 mm reference mesh (L5 = characteristic length $h=5$ mm, 8070 cells), with right-ventricular end-diastolic pressure capped at 5 mmHg during the inverse-unloading reference-configuration step. Individual cases are labelled `sPAP##`, where `##` is the targeted peak systolic pulmonary arterial pressure in mmHg (so sPAP22 is the lowest-pressure case in the sweep and sPAP95 the highest). An earlier **pre-cap** sweep used the same cases without that 5 mmHg cap and is invoked only where explicitly noted.

```{table} Direct production audits.
:name: tab-numerical-robustness-summary
:align: left

| Check | Evidence |
|---|---|
| Energy-consistent postprocessing | Quadrature-level stress-strain work closes the whole-heart boundary-work budget to about $10^{-5}$–$10^{-4}$ relative error |
| Primary capped sweep audit | All 16 capped shared-L5 cases completed strict canonical quadrature-level postprocessing on the same 8070-cell reference mesh, with finite pressure histories and per-cell work arrays |
| Capped septum envelope sweep | Epi-excluded and epi-inclusive septum envelopes (two alternative outer boundaries for the relaxed septal mask, defined in {ref}`sec-app-septum-epi-envelope`) were recomputed from $t=-10$ to $+20$ mm on the capped shared-L5 sweep; the geometric septum cutoff is unchanged, and tight-core transmural ranking does not translate into magnitude preservation |
| Principal-strain replay | All 16 capped cases were replayed from displacement checkpoints; fibre direction was closer to septal principal shortening than longitudinal strain, while principal shortening itself did not remove the pressure-choice ambiguity |
| Mesh convergence | h=5 differs from h=3.75 by less than 0.8% for hemodynamics and less than about 3% for free-wall ratios in the endpoint mesh study; severe septal work differs by about 5–7% |
| Periodic convergence | Beat-to-beat relative change between beats 5 and 6: mean 0.4% on peak pressures and 0.4% on end-diastolic volumes across the 16 production cases; worst-case 1.5% peak pressure and 1.8% stroke volume in sPAP70 |
| Postprocessing space replay | DG1 stays within about 1.2% of Quadrature6 for integrated regional stress-strain work; DG0 underestimates high-pressure septal work |
| Basal support audit | The production condition fixes only the base-normal/global-x component; tangential basal sliding remains |
```

```{table} Numerical-method sensitivity checks.
:name: tab-numerical-robustness-sensitivity
:align: left

| Check | Evidence |
|---|---|
| No-Dirichlet variants | Endpoint cases failed during end-diastolic inflation after removing the basal displacement constraint |
| Robin work budget | Signed net Robin work is below about 0.2% of cavity boundary work in checked endpoint cases |
| 3D--0D coupling interface | The 0D-to-mesh volume ratio (the coupling factor that reconciles 0D-model and FEM end-diastolic volumes) sits within a few percent of unity in most production cases; a controlled pulmonary-compliance sweep shows the interface remains usable at right-ventricular ratios as low as 0.26 |
| Historical h=10/h=5 full-sweep rerun | In the 16 paired pre-cap cases, LV/RV pressures shifted by at most 1.8%/1.1% and free-wall ratios by a few percent |
```

## Energy-Consistent Postprocessing

This check asks whether the volume-integrated stress-strain work used as the model-side reference actually closes the boundary-work budget — if it does not, the postprocessing fields cannot be trusted as a faithful image of the simulated state, and any proxy comparison built on top of them is suspect. The model-side reference quantity is the stress-strain work density

$$
w_\mathrm{int}[\Omega_j] =
\frac{1}{|\Omega_{j,0}|}
\int_0^T\int_{\Omega_{j,0}}\mathbf{S}:\dot{\mathbf{E}}\,dV_0\,dt.
$$

Early postprocessing attempts projected stress and strain into discontinuous Galerkin spaces before integrating this quantity. During development, these projected-field replays were associated with large energy-budget discrepancies: smooth-looking stress and strain fields could still give work totals far too small compared with the boundary work. Later replay tests showed this was not simply a DG1-versus-quadrature issue. Once the pressure history and boundary-work bookkeeping had been corrected, DG1 reproduced integrated regional work closely. DG0, however, still suppressed high-pressure septal work. The final pipeline uses quadrature-level stress evaluation as the conservative production path.

The final method avoids projecting the current stress before integration. The current stress is evaluated directly from the constitutive law at quadrature points, previous stress and strain are stored in a degree-six quadrature space for the trapezoidal time rule, and the DG0 space is used only as a cellwise partition of unity. As a hard implementation check, the sum of the DG0 per-cell work values is compared with an independent scalar domain integral of the same quadrature-level expression. In the checked runs, this agreement is at machine precision, confirming that the cellwise extraction is not changing the integrated work.

The external work terms were also matched to the solver formulation. Cavity work uses the actual solver cavity pressures, not the 0D elastance pressures, and the volume change is computed from the nonlinear cavity-volume expression rather than a linearized surface displacement. Robin work uses the same deformed-normal/Nanson formulation as the variational boundary condition. With these choices, the whole-heart stress-strain work and boundary-work budget close to the small residual shown in the main text.

(sec-app-mesh-convergence)=
## Mesh Convergence

The aim of this section is to bound how much of the reported regional work could be a mesh-resolution artefact rather than a property of the simulated tissue — particularly for the septum, where the wall is thinnest and a coarse mesh has the fewest cells through-thickness.

All 16 cases in the capped shared-L5 sweep use the same 5 mm reference mesh ($n=8070$ cells) and the same region tag set (see {ref}`sec-shared-mask-tagging`). The pressure histories have shape `(4800, 2)`, the per-cell arrays are finite, and the geometric septum (cells satisfying the transventricular distance criterion in {ref}`sec-shared-mask-tagging`) is 1269 cells while the tag-3 septum (cells carrying LDRB region marker 3) is 1266 cells in every case (a 0.1% volume difference shared across the sweep).

A separate mesh-convergence study repeated three representative pressure cases — sPAP22, sPAP60, and sPAP95 — using characteristic lengths of 10, 7.5, 5, and 3.75 mm. The 3.75 mm runs were used as the finest available reference.

At the production 5 mm resolution, hemodynamic quantities differed from the 3.75 mm reference by less than 0.8%. Free-wall work-density ratios were also stable, with differences below about 3%. Septal quantities were more mesh-sensitive, especially at high RV pressure. At 5 mm, septal stress-strain work differed from the 3.75 mm reference by about 0.2% in sPAP22, 3.8% in sPAP60, and 5.7% in sPAP95; the largest septal longitudinal-proxy discrepancy was about 6.6%. The 10 mm mesh was clearly too coarse for septal quantities in the high-pressure case, with errors up to about 18%.

The 5 mm production mesh is sufficient for the qualitative free-wall conclusions tested here, while absolute high-pressure septal values should be read with the observed 5–7% difference between the 5 mm and 3.75 mm meshes in mind.

The historical pre-cap corrected pressure sweep was also rerun at 5 mm resolution. Across the 16 h=10/h=5 paired pre-cap cases, achieved LV and RV end-systolic pressures changed by at most 1.8% and 1.1%, respectively. The free-wall finite-element LV/RV stress-strain work ratio changed by at most 5.4%, and the adjacent-pressure longitudinal proxy ratio by at most 11.9%. This supports the free-wall pressure-strain result as a robust regional finding rather than a consequence of the coarse 10 mm sweep. It is retained as numerical-method support for the broad free-wall result, not as a direct convergence proof for the capped reference-state choice.

The septum required a different interpretation. The 10 mm corrected sweep used a case-specific geometric septum mask that covered only part of the tag-3/canonical septum in several cases. In the completed capped shared-L5 sweep, the geometric septum volume matches the tag-3 septum volume to within about 0.1% in every case. For that reason, h=10-to-h=5 septal differences are not reported as simple mesh errors. The high-resolution capped septal results replace the earlier septal tables rather than merely perturbing them.

(sec-app-periodic-convergence)=
## Periodic Convergence Across the Coupled Beats

The results in {ref}`chap-results` use the final beat of a six-beat coupled simulation, so the analysis assumes that this last beat is essentially periodic. The standalone zero-dimensional pre-run is already periodic to about $3\times10^{-5}$ relative cycle change before being handed to the coupled solve ({ref}`chap-calibration`), but the operating-point shift between the standalone and coupled steady states ({ref}`sec-app-coupling-residual`) means the coupled run starts away from its own periodic state and has to converge again under the full mechanics.

The metric used is the cycle-to-cycle relative change between beats five and six, computed for each of the sixteen production cases on six quantities that span the cycle: peak LV and RV cavity pressures (from the solver Lagrange multiplier), end-diastolic LV and RV volumes (from the coupled 0D state), and LV and RV stroke volumes.

```{list-table} Beat-to-beat relative change between the fifth and sixth coupled beats across the sixteen capped production cases.
:name: tab-app-periodic-convergence
:header-rows: 1

* - Metric (beat 5 → beat 6 relative change)
  - Mean across 16 cases
  - Worst case
* - Peak LV cavity pressure
  - 0.39%
  - 1.47% (sPAP70)
* - Peak RV cavity pressure
  - 0.23%
  - 0.60% (sPAP45)
* - LV end-diastolic volume
  - 0.39%
  - 1.32% (sPAP70)
* - RV end-diastolic volume
  - 0.28%
  - 0.85% (sPAP70)
* - LV stroke volume
  - 0.56%
  - 1.80% (sPAP70)
* - RV stroke volume
  - 0.57%
  - 1.82% (sPAP70)
```

Across the sweep the analysed beat is within about 1.5% of the preceding beat on peak cavity pressures, within 1.4% on cavity volumes, and within 1.8% on stroke volumes in the worst case. Median changes are 0.16–0.36% on pressures and 0.21–0.60% on volumes. The worst-case case (sPAP70) is the same intermediate-pressure case that already requires the largest mesh-to-circulation volume ratio in {ref}`sec-app-coupling-robustness`. The six-beat coupled simulation has settled enough that further beats would not move the proxy and reference values used in the proxy comparison.

The decay trend across the six beats is shown in {numref}`fig-app-periodic-convergence` for three representative cases. The largest beat-to-beat changes occur in the first beat, where the coupled solve readjusts the operating point away from the standalone pre-run state, and decay rapidly thereafter.

```{figure} ../figures/fig_app_periodic_convergence.png
:name: fig-app-periodic-convergence
:width: 95%

Beat-by-beat trace of peak cavity pressures (left), end-diastolic volumes (middle), and stroke volumes (right) across the six coupled beats for three representative cases: sPAP22 (low RV pressure, blue), sPAP70 (worst-converging, red), and sPAP95 (highest RV pressure, green). Solid lines with circles are the LV; dashed lines with squares are the RV. The largest beat-to-beat changes occur between beats one and two as the coupled solve readjusts away from the standalone pre-run state, and the curves have flattened to the residuals reported in {numref}`tab-app-periodic-convergence` by the analysed beat.
```

(sec-app-coupling-robustness)=
## 3D--0D Coupling Interface

The point of this check is to verify that the 0D-to-mesh volume coupling is operating in a stable region of parameter space across the sweep, rather than being pushed close to a regime in which the coupled solve would stall or distort the cavity volumes used in the proxy comparison. The fixed mesh-to-circulation volume ratio in {ref}`sec-3d-0d-coupling` is the only point at which 0D and 3D end-diastolic volumes are reconciled. The optimizer in {ref}`chap-calibration` includes the mesh end-diastolic volumes as targets, but the cost balances them against pressure, flow, ejection-fraction, and stroke-volume balance, so the optimizer accepts a residual offset rather than enforcing an exact match.

Across the sixteen production cases the LV ratio sits within 3% of unity in twelve cases; three intermediate-pressure cases (sPAP60 to sPAP70) require LV scalings of 17%, 21%, and 47%. The RV ratio is more uniformly off-unity, with magnitudes between near zero and 16% and a tendency toward larger corrections in the lower-pressure cases. The interface ratio absorbs the small-to-moderate residual mismatch that the joint pressure-and-volume optimization leaves behind.

A separate sensitivity sweep tested how far the interface can be pushed before the coupled simulation breaks. The same UKB mean mesh was coupled to five 0D parameter sets in which pulmonary arterial compliance was reduced by factors $f \in \{1.00, 0.75, 0.50, 0.25, 0.10\}$ and resistance raised by the inverse factor, while the rest of the circulation was held fixed. The 0D model responds strongly under these unbalanced parameters: the RV end-diastolic volume in the standalone pre-run grows from about 180 mL at $f=1.00$ to about 285 mL at $f=0.10$, well outside any physiological range.

The volume ratio absorbed this drift transparently, with $s_\text{RV}$ falling from 0.42 to 0.26 across the sweep. All five coupled simulations completed six beats and reached periodic cavity volumes by the third beat, with no solver failures or strain artefacts. The interface remains usable at RV ratios roughly an order of magnitude further from unity than the production runs ever encounter.

(sec-app-septum-epi-envelope)=
## Septum Envelope Sensitivity

This check asks whether the reported septal proxy correlations depend on the precise boundary between the septum and the free walls, since the location of that boundary is partly conventional and a marginally different mask could in principle move the proxy result. The boundary-relaxation sweep defines a family of septal masks,

$$
\Omega_\mathrm{sep}(t)
= \{c : \mathrm{entry}_t(c) < t\}\cap\Omega_\mathrm{env},
$$

where $\mathrm{entry}_t=\max(d_\mathrm{LV},d_\mathrm{RV})-d_\mathrm{epi}$, so that $t=0$ recovers the geometric septum. The envelope $\Omega_\mathrm{env}$ prevents the relaxed mask from growing indefinitely into the free walls. The production sweep used the stricter envelope

$$
\Omega_\mathrm{env}
= \{d_\mathrm{LV}+d_\mathrm{RV}\leq 22~\mathrm{mm}\}\cap\{\mathrm{not\ touching\ epicardium}\}.
$$

The topological epicardial exclusion removes cells on the outer boundary of the ventricular wall. Near the LV/RV junction the free wall becomes thin, and an epicardial boundary cell can satisfy the relaxed distance criterion even though it is still part of the outer wall surface. Excluding epicardial-touching cells makes the relaxed sweep a conservative interior-septum envelope.

The opposite convention was tested by using only $d_\mathrm{LV}+d_\mathrm{RV}\leq 22$ mm. This epi-inclusive envelope is anatomically defensible if the goal is to let the geometric parametrization grow the septal mask all the way to the outer wall. The two definitions are identical at the actual geometric septum cutoff and first diverge only at about $t=+4.5$ mm. The difference is therefore not a change to the reported primary septum; it is a sensitivity of the far relaxed sweep tail.

{numref}`fig-app-septum-mask-sweep` shows the geometric picture of the mask as $t$ varies; the quantitative effect on proxy correlations is in {numref}`fig-app-septum-epi-envelope` and {numref}`tab-app-septum-epi-envelope`. The sweep was recomputed over $t=-10$ to $+20$ mm so that negative thresholds test a genuinely smaller, deeper septal core rather than only relaxed masks.

```{figure} ../figures/fig_app_septum_mask_sweep.png
:name: fig-app-septum-mask-sweep
:width: 95%

Geometric septum mask under the boundary-relaxation sweep. Each panel shows the cells assigned to the septum (red) at threshold $t \in \{-5, -3, -1, 0, +1, +3, +5, +10\}$ mm on the biventricular mesh. At $t<0$ the mask is shrunk away from the LV/RV junction; at $t>0$ it grows into adjacent free-wall tissue.
```

```{figure} ../figures/fig_app_septum_epi_envelope_comparison.png
:name: fig-app-septum-epi-envelope
:width: 95%

Effect of allowing epicardial-touching cells into the relaxed septum sweep in the capped shared-L5 production set. Solid lines use the production epi-excluded envelope; dashed lines use the epi-inclusive envelope. The lower panel shows the inclusive-minus-excluded correlation change. The definitions coincide through the geometric cutoff and separate only when the relaxed mask reaches the outer wall.
```

The table also reports $\eta$, the mean absolute log error in the septum/free-wall work-density ratio, for the epi-excluded production envelope. This separates case ranking from magnitude preservation.

```{table} Selected thresholds from the capped shared-L5 epi-excluded and epi-inclusive septum sweep comparison. Correlations are Pearson correlations between volume-integrated septal stress-strain work and longitudinal pressure-strain proxies across the 16 capped production cases. The $\eta$ columns use the epi-excluded production envelope.
:name: tab-app-septum-epi-envelope
:align: left

| $t$ (mm) | Cells excl. -> incl. | $r(p_\mathrm{LV})$ | $r(p_\mathrm{RV})$ | $r(p_\mathrm{LV}-p_\mathrm{RV})$ | $r(p_\mathrm{mean})$ | $\eta(p_\mathrm{LV})$ | $\eta(p_\mathrm{LV}-p_\mathrm{RV})$ | $\eta(p_\mathrm{mean})$ |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| -10 | 733 -> 733 | 0.567 -> 0.567 | 0.556 -> 0.556 | 0.533 -> 0.533 | 0.563 -> 0.563 | 1.581 | 3.338 | 1.675 |
| -5 | 1008 -> 1008 | 0.514 -> 0.514 | 0.524 -> 0.524 | 0.071 -> 0.071 | 0.520 -> 0.520 | 1.222 | 2.621 | 1.359 |
| 0 | 1269 -> 1269 | 0.540 -> 0.540 | 0.528 -> 0.528 | -0.333 -> -0.333 | 0.535 -> 0.535 | 0.805 | 2.075 | 0.969 |
| +5 | 1555 -> 1558 | 0.600 -> 0.602 | 0.542 -> 0.543 | -0.358 -> -0.358 | 0.568 -> 0.569 | 0.507 | 1.683 | 0.691 |
| +10 | 1955 -> 2140 | 0.714 -> 0.723 | 0.578 -> 0.585 | -0.333 -> -0.349 | 0.635 -> 0.642 | 0.298 | 1.436 | 0.492 |
| +20 | 2592 -> 3112 | 0.865 -> 0.889 | 0.667 -> 0.641 | -0.351 -> -0.292 | 0.752 -> 0.745 | 0.171 | 1.286 | 0.369 |
```

Two cautions follow. First, a very tight central-septum mask can make transmural pressure rank the cases positively: at $t=-10$ mm, $r(p_\mathrm{LV}-p_\mathrm{RV})=0.533$. That ranking is not a good work-density proxy, because the same threshold gives the largest magnitude error in the table ($\eta=3.338$). The true septum/free-wall ratio is close to one in that tight core, while the transmural-pressure ratio is much smaller because the pressure difference cancels when both cavities are pressurised.

Second, positive thresholds increasingly mix the septum with junctional free-wall tissue. At $t=+20$ mm, the inclusive sweep adds 520 cells per case, increasing the region from 2592 to 3112 cells; $r(p_\mathrm{LV})$ changes from 0.865 to 0.889, while $r(p_\mathrm{LV}-p_\mathrm{RV})$ changes only from -0.351 to -0.292. This tail behaviour is useful as a mask-sensitivity check, but it is not the primary septum definition. The geometric septum used in the main result remains $t=0$, where the epi-excluded and epi-inclusive definitions coincide and transmural pressure is poor by both ranking and magnitude.

## Basal Boundary Condition

This check asks whether the partial basal Dirichlet constraint used in production is essential to obtaining a converged solution, or only one of several acceptable supports that could be replaced with the Robin springs alone without changing the reported result. The production basal condition fixes only the base-normal/global-x displacement component. In the completed pressure-sweep cases, the saved displacement fields confirm that the constrained component is zero to saved precision at the checked time points, while the other two basal displacement components retain millimetre-scale sliding motion.

A no-Dirichlet variant was tested by removing the basal displacement constraint while keeping the same Robin springs and the 5 mm production mesh. The sPAP22, sPAP60, and sPAP95 variants all reached the reference-configuration step (the inverse-unloading stage that recovers the unloaded geometry from the imaged configuration) but failed during the subsequent end-diastolic forward inflation (the first forward pressurisation, from the unloaded state up to end-diastole) with linear solver non-convergence. A previous coarse one-beat Robin-only test had converged, but that result did not carry over to the production mesh and pressure cases. The retained basal condition is a stabilizing constraint needed in this production setup, not a physiological claim about the base being fixed in space.

The energetic effect of the Robin support was small compared with the cavity work in the cycle-integrated balance. In the checked endpoint cases, the signed net Robin work was below about 0.2% of the cavity boundary work.

## Postprocessing Space Sensitivity

This check asks whether the reported regional work is a property of the simulated stress and strain fields, or an artefact of the particular discrete space chosen to store them during postprocessing — a coarser storage space could in principle smear or suppress sharp septal structure even when the solver itself is converged. The final method uses degree-six quadrature storage because it most directly matches the quadrature-level constitutive evaluation and gave the tightest energy closure during development. A defence-oriented check recomputed sPAP22, sPAP60, and sPAP95 at the production 5 mm mesh with DG0 and DG1 state storage, while keeping the same degree-six integration rule. The current stress expression was still evaluated directly from the constitutive law; only the stored previous stress and strain state used the degraded space.

DG1 reproduced the Quadrature6 integrated regional stress-strain work closely. Across the three representative cases, the largest regional work-density difference was 1.2%, occurring in the septum. DG0 was less reliable: whole-heart and free-wall totals stayed within a few percent, but septal stress-strain work was underestimated by 7.7% in sPAP60 and 15.4% in sPAP95. The energy-budget residual was also smallest for Quadrature6, at about $10^{-5}$ to $10^{-4}$ relative error, compared with up to $2.7\times10^{-3}$ for DG1 and $1.5\times10^{-2}$ for DG0.

The main integrated regional conclusions are not a fragile artifact of Quadrature6: DG1 gives essentially the same total regional stress-strain work. However, DG0 is not adequate for the high-pressure septal quantities, and the directional component decomposition is more sensitive than total work. Quadrature6 is retained as the production postprocessing space because it gives the best energy closure and avoids suppressing septal stress-strain structure.
