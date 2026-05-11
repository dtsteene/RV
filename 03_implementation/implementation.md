(chap-implementation)=
# Implementation and Checks

The model in {ref}`chap-model` produces stress, strain, and regional work fields that {ref}`chap-results` uses as the reference for the pressure-strain proxy comparison. That comparison only means something if the simulation is correct at the field level, not just at the level of pressure-volume loops. A run can eject a plausible volume while stress magnitudes sit outside reported myocardial ranges, the work integration is inconsistent across the cycle, or the pressure history used in boundary work has drifted from the pressure that actually loaded the mechanics solve.

This chapter records the field-level checks that establish the simulation as a credible reference: a stress-free configuration consistent with the imaged end-diastolic geometry, region definitions that are stable across the loading sweep, stress magnitudes consistent with reported myocardial ranges, a closed energy budget at the cell and domain level, postprocessing boundary terms that match the solver's variational form, and a single record of the pressure that actually loaded the mechanics solve. Where a check did not initially close, the source was identified and the implementation corrected; the pipeline described below is what passes these checks.

## Reference Configuration

The image-derived mesh represents the heart at end-diastole, already loaded by ventricular pressures of order 5–10 mmHg. The constitutive law expects a stress-free reference. Using the loaded mesh directly as the reference would treat an already pressurised geometry as unloaded, biasing every downstream stress and strain.

The unloaded reference is therefore estimated by inverse unloading following Bols et al. {cite}`bols2013computational`. The mesh is repeatedly loaded with the target end-diastolic pressures, the resulting displacement updates the reference coordinates, and the iteration continues until the loaded configuration reproduces the imaged end-diastolic geometry. The same basal Dirichlet condition and Robin support used in the main mechanics solve are applied during this step so that the reference and the cycle solve see identical boundary conditions. The cardiac cycle then starts from the inferred unloaded reference, inflates to the imaged end-diastolic state, and proceeds through systole and relaxation.

A sensitivity check identified one limitation of using the same UKB baseline geometry and the same passive material parameters at every loading level of the sweep. At high RV end-diastolic pressures the unloading algorithm has to explain the added load with neither RV hypertrophy, curvature change, nor passive remodelling, and an uncapped pilot consequently inferred unphysically small RV unloaded cavities for the high-RV-pressure cases. The production sweep therefore caps the RV end-diastolic pressure used during inverse unloading at 5 mmHg, within the typical resting RV end-diastolic range of about 0–8 mmHg in healthy adults. The value was chosen empirically: lower caps were unnecessary because the low-RV-pressure cases converge to physical references on their own, while higher caps reopened the unphysical-reference problem on the high-RV-pressure cases. With the cap applied, the inferred unloaded cavity reductions across the 16 production sweep cases fall in the range 20–26% for the LV and 32–39% for the RV; the raw uncapped RV end-diastolic pressures targeted by these cases ranged from 4.8 to 16.3 mmHg, so the cap activated only for the higher-pressure cases and left the low-pressure cases unchanged. The cap is a bounded fixed-geometry correction, not a model of remodelling, and it does not propagate into the proxy comparison: the pressure-strain bookkeeping is anchored at start-of-beat strain and accumulates increments, which are invariant to translation of the reference state.

(sec-reference-tag-postprocessing)=
## Region Definitions

The regional integrals require a definition of each region $\Omega_j$, and that definition must be stable across the loading sweep. The cell tags for the LV free wall, RV free wall, and septum are computed once on the imaged end-diastolic mesh and reused for every simulation in the sweep, rather than recomputed from each simulation's deformed end-diastolic state. Outputs computed under this scheme are called **reference-tag postprocessing** in the rest of the thesis.

The choice keeps cross-case region definitions stable: an LV-side septal cell remains LV-side regardless of the RV pressure load, so the integration domains do not shift between simulations. Per-case re-tagging tracks the deformed geometry but is fragile to small differences in the geometric distance criteria — a near-boundary cell can flip between regions under modest deformation. An LDRB-style classification was also tested and consistently misclassified cells inside the geometric septum partition in the curved transition between septum and free wall. The reference-tag scheme is therefore the conservative choice for cross-case proxy comparisons. The production sweep used in {ref}`chap-results` integrates all 16 cases on the shared reference mesh under this convention, with a common tetrahedralisation ($n = 8070$ cells, 1269 geometric septum cells across every case).

## Stress Magnitudes

The Holzapfel-Ogden law depends on the finite-strain state through the full Green-Lagrange tensor $\mathbf{E}$. An early check compared peak fibre stress $|S_{ff}|$ against reported myocardial ranges {cite}`delhaas1994regional,finsberg2017phd`, and the simulated values were systematically below the literature envelope. Tracing the source identified that the compressible material path of `fenicsx-pulse` was passing only the deviatoric part of the strain state to the stress evaluation, dropping the volumetric contribution that the constitutive law requires. After the library was patched to forward the full strain state, the production pipeline reports peak $|S_{ff}|$ of 71, 60, and 49 kPa for the LV free wall, RV free wall, and septum on the lowest-pressure case of the production sweep, where the coupled simulation achieves peak LV pressure 105 mmHg and peak RV pressure 32 mmHg. {numref}`fig-stress-magnitudes` shows the post-fix per-region peaks against the cited literature envelope.

The check matters because it does not show up in the pressure-volume loops. With or without the volumetric contribution, runs converge, ejection fractions are plausible, and the loop shapes look qualitatively normal; a sanity check restricted to global hemodynamics would have missed it.

```{figure} ../figures/fig_stress_magnitudes.png
:name: fig-stress-magnitudes
:width: 75%

Post-fix peak fibre stress $|S_{ff}|$ per region in the lowest-pressure case of the production sweep (peak LV pressure 105 mmHg, peak RV pressure 32 mmHg, bars) against a reported myocardial fibre-stress envelope (band, 20–80 kPa) drawn to bracket the canine epicardial peaks reported by Delhaas et al. {cite}`delhaas1994regional` (mean 21–27 kPa across regions; up to 2–3× higher transmurally) and the human computational estimates of Finsberg {cite}`finsberg2017phd`. The simulated peaks fall inside this envelope, in contrast to the pre-fix simulations where the deviatoric-only stress evaluation depressed the magnitudes below it.
```

## Energy Budget

Whole-heart internal stress-strain work equals cavity-pressure work plus Robin support work, accumulated through the cycle. {numref}`fig-energy-balance` already showed this closure on the UKB baseline, with a residual of order $10^{-5}$ relative. The trace there is produced by the postprocessing path used throughout the thesis — replay from the displacement checkpoint, regional integration over reference tags, and reconstruction of cavity and Robin work with the kinematic conventions the solver uses — so the closure validates the full pipeline that produces every other regional work-density number in this work, not only the continuum identity. A full debug-postprocessing rerun on the sPAP70 production case confirms the same tolerance under elevated RV loading, with a cycle-end residual of $3.2\times10^{-5}$ relative.

The discrete form integrated by the postprocessor is

$$
W_\mathrm{int}[\Omega_j] = \sum_i \int_{\Omega_j} \bar{\mathbf{S}}_i : \Delta \mathbf{E}_i \, dV_0 ,
$$

with $\bar{\mathbf{S}}_i$ the timestep-average second Piola-Kirchhoff stress and $\Delta\mathbf{E}_i$ the Green-Lagrange strain increment. The integration is evaluated at the quadrature points where the constitutive law is assembled during the Newton solve, so postprocessing consumes the same integrand the solver wrote.

The current stress comes directly from the UFL constitutive expression; previous stress and strain states are stored in a degree-six quadrature space matching the integration order of the solve. DG0 is used only as a cellwise partition for extracting per-cell integrals once the quadrature integrand has been formed, so regional cell sums equal the scalar domain assembly to numerical precision. Function-space sensitivity comparing DG0, DG1, and Quadrature6, together with the active/passive/compressible decomposition that confirms the passive elastic contribution returns to zero over the cycle, are reported in the numerical-robustness appendix.

## Boundary Terms

The energy closure above only holds if the postprocessing reproduces the boundary work the solver actually computed. Two terms required attention.

The Robin spring support is applied in the current configuration and only along the deformed normal, so the postprocessing uses the same deformed-normal projection and Nanson surface mapping as the variational form. A reference-configuration formula using the full displacement vector would instead overestimate the spring work by penalising tangential sliding that the solver does not penalise.

Cavity-pressure work uses the nonlinear cavity-volume functional rather than the small-displacement approximation $\int \mathbf{N}\cdot\Delta\mathbf{u}\,dS_0$, because at finite deformation the linearised volume change underestimates the volume swing during ejection and filling, the phases that dominate work. The cavity contribution is

$$
W_\mathrm{cav} = \sum_i \bar p_i \, \Delta \mathcal{V}_i ,
$$

with $\Delta\mathcal{V}_i$ taken from the same cavity-volume functional used by the coupled solve. With these conventions, the postprocessor reproduces the boundary work the solver computes.

## Pressure Records

The coupled simulation produces two pressure-like quantities: the 0D elastance pressure that defines the loading path, and the cavity-pressure Lagrange multiplier that the 3D solve uses to enforce the finite-element cavity-volume constraint. The multiplier is what acts on the variational boundary and is therefore the correct pressure for boundary work; integrating cumulative cavity work with the 0D pressure instead of the multiplier gives a cycle-end value 2.8% off, about 28 mJ on a 1000 mJ total in the production sPAP-70 case, even though the two pressure traces agree within 5.76 mmHg over the beat. The solver multiplier is saved at every checkpoint alongside the displacement field, and all stress-strain and proxy work calculations use it. The 0D model still supplies the coupled loading path but no longer enters the work bookkeeping. The 5.76 mmHg gap is structural rather than numerical — the 0D elastance and the FEM Holzapfel-Ogden material with prescribed active tension are two independently calibrated mechanical descriptions of the same chamber — and {ref}`sec-app-coupling-residual` unpacks the calibration architecture that produces it.
