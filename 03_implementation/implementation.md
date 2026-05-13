(chap-implementation)=
# Validating the Mechanical Reference

The model in {ref}`chap-model` produces stress, strain, and regional work fields that {ref}`chap-results` uses as the reference for the pressure-strain proxy comparison. That comparison only means something if the simulation is correct at the field level, not just at the level of pressure-volume loops. A run can converge, eject a plausible volume, and trace a healthy pressure waveform while the stress and strain fields underneath are wrong. The failures described in this chapter all share that property: each one was invisible in the pressure-volume loop and only surfaced when the field-level reference was checked directly.

Two classes of failure show up in this work. The forward problem can produce stress magnitudes outside reported myocardial ranges, or an inferred unloaded reference that the forward inflation cannot recover. The postprocessing can disagree with the solver about what it integrated — wrong region tags, wrong work integrand, wrong boundary-term formulation, or the wrong pressure record. The chapter is organized in that order: forward-problem checks first, then postprocessing checks. Where a check did not initially close, the source was identified and the implementation corrected; the pipeline described below is what passes these checks.

## Reference Configuration

The image-derived mesh is the heart at end-diastole, already loaded by ventricular pressures of 5–10 mmHg. The constitutive law expects a stress-free reference, so using this mesh directly would bake the pre-load into every downstream stress and strain. We instead estimate the unloaded geometry by inverse unloading following Bols et al. {cite}`bols2013computational`: a candidate reference is repeatedly loaded with the target end-diastolic pressures, and the resulting displacement updates the reference coordinates until the loaded shape reproduces the imaged end-diastole. The same Dirichlet and Robin boundary conditions used in the cycle solve are applied here, so the reference and the cycle see identical supports.

The procedure has one weakness in the present sweep. The baseline mesh and the passive material parameters are held fixed across every pressure level, so the algorithm cannot absorb a high RV end-diastolic pressure by hypertrophy, septal flattening, or stiffening — its only remaining knob is the unloaded cavity volume. At high RV pressures it therefore shrinks the unloaded RV to unphysically small sizes. The production sweep avoids this by capping the RV end-diastolic pressure used during inverse unloading at 5 mmHg, within the typical resting right-heart filling-pressure range of 0–8 mmHg in healthy adults {cite}`humbert2022esc`. The value was chosen empirically: lower caps were unnecessary on the low-pressure cases, and higher caps reintroduced the small-cavity pathology on the high-pressure cases.

The cap is justified by round-trip consistency. The inverse problem's defining requirement is that forward-simulating from the inferred unloaded reference reproduces the imaged end-diastolic shape. In the most severe uncapped case (sPAP95) it does not: the forward-simulated end-diastole misses the imaged target by 9.4 mm whole-mesh mean and 13.9 mm at the septum, with a peak local discrepancy of 32 mm, even though cavity volume is recovered exactly through the Lagrange-multiplier coupling. With the cap the same case drops to 3.7 mm whole-mesh and 4.3 mm at the septum, below the in-plane CMR voxel size. The error is septum-localised — about 1.5 times the free-wall residuals — consistent with the septum being the region most sensitive to where the unloaded reference sits.

The cap is a fixed-geometry correction, not a model of remodelling, and it does not propagate into the proxy comparison: the pressure-strain bookkeeping is anchored at start-of-beat strain and accumulates increments, which are invariant to translation of the reference state. The sweep-wide cap activation pattern and the inferred unloaded volume fractions are reported in {ref}`sec-app-reference-remodeling-sensitivity`.

## Stress Magnitudes

The Holzapfel-Ogden law depends on the finite-strain state through the full Green-Lagrange tensor $\mathbf{E}$. An early check compared peak fibre stress against reported myocardial ranges {cite}`delhaas1994regional,finsberg2017phd`, and the simulated values were systematically below the literature envelope. Tracing the source identified that the compressible-formulation code path of `fenicsx-pulse` was passing only the deviatoric part of the strain state to the stress evaluation, dropping the volumetric contribution that the constitutive law requires. After the library was patched to forward the full strain state, the production pipeline reports peak Cauchy fibre stress $|\sigma_{ff}|$ of 62, 50, and 41 kPa for the LV free wall, RV free wall, and septum on the lowest-pressure case of the production sweep, where the coupled simulation achieves peak LV pressure 105 mmHg and peak RV pressure 32 mmHg. {numref}`fig-stress-magnitudes` shows the post-fix per-region peaks against the cited literature envelope.

The check matters because it does not show up in the pressure-volume loops. With or without the volumetric contribution, runs converge, ejection fractions are plausible, and the loop shapes look qualitatively normal; a sanity check restricted to global hemodynamics would have missed it.

```{figure} ../figures/fig_stress_magnitudes.png
:name: fig-stress-magnitudes
:width: 75%

Post-fix peak Cauchy fibre stress $|\sigma_{ff}|$ per region in the lowest-pressure case of the production sweep (peak LV pressure 105 mmHg, peak RV pressure 32 mmHg, bars) against a reported myocardial fibre-stress envelope (band, 20–80 kPa) drawn to bracket the canine epicardial peaks reported by Delhaas et al. {cite}`delhaas1994regional` (mean 21–27 kPa across regions; up to 2–3× higher transmurally) and the human computational estimates of Finsberg {cite}`finsberg2017phd`. The simulated peaks fall inside this envelope, in contrast to the pre-fix simulations where the deviatoric-only stress evaluation depressed the magnitudes below it.
```

The remaining checks shift from the forward problem to postprocessing. Even when the solver returns the right stress and strain fields, the regional work-density numbers reported in {ref}`chap-results` come from a separate replay step that has to integrate those fields over the right cells, with the right integrand, against boundary terms that match the solver's variational form, using the pressure that the solver actually saw. Each of those choices is a place the field-level reference can quietly disagree with the solver, and each one was wrong at some point during development.

(sec-reference-tag-postprocessing)=
## Region Definitions

The regional integrals require a definition of each region $\Omega_j$, and that definition must be stable across the loading sweep. The cell tags for the LV free wall, RV free wall, and septum are computed once on the imaged end-diastolic mesh and reused for every simulation in the sweep, rather than recomputed from each simulation's deformed end-diastolic state. Outputs computed under this scheme are called **reference-tag postprocessing** in the rest of the thesis.

The choice keeps cross-case region definitions stable: an LV-side septal cell remains LV-side regardless of the RV pressure load, so the integration domains do not shift between simulations. Per-case re-tagging tracks the deformed geometry but is fragile to small differences in the geometric distance criteria — a near-boundary cell can flip between regions under modest deformation. An LDRB-style classification was also tested and consistently misclassified cells inside the geometric septum partition in the curved transition between septum and free wall. The reference-tag scheme is therefore the conservative choice for cross-case proxy comparisons, and the case-ranking effect of switching from per-case canonical tagging to the reference-tag scheme is documented in the appendix: the septal transmural-pressure ranking correlation moves from $r=+0.222$ to $r=-0.331$ once the case-to-case mask drift is removed ({ref}`tab-app-precap-capped-septum`). The production sweep used in {ref}`chap-results` integrates all 16 cases on the shared reference mesh under this convention ($n = 8070$ cells, 1269 geometric septum cells in every case).

## Energy Budget

Whole-heart internal stress-strain work equals cavity-pressure work plus Robin support work, accumulated through the cycle. {numref}`fig-energy-balance` shows this closure on the UKB baseline at a residual of order $10^{-5}$ relative.

Reaching that closure took diagnostic work. An earlier postprocessing path projected the stress and strain fields to a piecewise-linear DG1 space before integrating, and produced a much looser closure — the integrated regional stress-strain work came out about a third of the cavity work, a discrepancy initially mistaken for a fundamental modelling error. The source was the DG1 projection itself: at the thin septum, where the LV-RV transmural stress gradient is steep relative to the cell size, the nodal projection introduced spurious oscillations across cell interfaces, large enough to flip the sign of the work integrand locally. Moving integration back to quadrature-level evaluation, with DG0 used only as a cellwise partition for output, removed the oscillations and brought the residual to the order shown above.

The trace in {numref}`fig-energy-balance` is produced by this final pipeline — replay from the displacement checkpoint, regional integration over reference tags, and reconstruction of cavity and Robin work using the kinematic conventions the solver uses — so the closure validates the full pipeline behind every regional work-density number in this work, not only the continuum identity. Full debug-postprocessing reruns on two production cases confirm the same tolerance: the lowest-pressure case closes at $8.0\times10^{-6}$ and the sPAP70 high-RV case at $3.2\times10^{-5}$.

The discrete form integrated by the postprocessor is

$$
W_\mathrm{int}[\Omega_j] = \sum_i \int_{\Omega_j} \bar{\mathbf{S}}_i : \Delta \mathbf{E}_i \, dV_0 ,
$$

with $\bar{\mathbf{S}}_i$ the timestep-average second Piola-Kirchhoff stress and $\Delta\mathbf{E}_i$ the Green-Lagrange strain increment. The integration is evaluated at the quadrature points where the constitutive law is assembled during the Newton solve, so postprocessing consumes the same integrand the solver wrote.

The current stress comes directly from the UFL constitutive expression; previous stress and strain states are stored in a degree-six quadrature space matching the integration order of the solve. DG0 is used only as a cellwise partition for extracting per-cell integrals once the quadrature integrand has been formed, so regional cell sums equal the scalar domain assembly to numerical precision. Function-space sensitivity comparing DG0, DG1, and Quadrature6, together with the active/passive/compressible decomposition that confirms the passive elastic contribution returns to zero over the cycle, are reported in the numerical-robustness appendix.

## Boundary Terms

The energy closure above only holds if the postprocessing reproduces the boundary work the solver actually computed. Even after the integrand and projection space were fixed, the cycle-end residual sat at several percent until two boundary terms were corrected. Each used an obvious-looking formula that turned out to be variationally inconsistent with what the solver assembled.

The Robin spring support is applied in the current configuration and only along the deformed normal, so the postprocessing uses the same deformed-normal projection and Nanson surface mapping as the variational form. A reference-configuration formula using the full displacement vector — the natural first attempt — instead overestimates the spring work, because it penalises tangential sliding that the solver does not penalise.

Cavity-pressure work uses the nonlinear cavity-volume functional rather than the small-displacement approximation $\int \mathbf{N}\cdot\Delta\mathbf{u}\,dS_0$, because at finite deformation the linearised volume change underestimates the volume swing during ejection and filling, the phases that dominate work. The cavity contribution is

$$
W_\mathrm{cav} = \sum_i \bar p_i \, \Delta \mathcal{V}_i ,
$$

with $\Delta\mathcal{V}_i$ taken from the same cavity-volume functional used by the coupled solve. With these conventions, the postprocessor reproduces the boundary work the solver computes.

## Pressure Records

The coupled simulation produces two pressure-like quantities: the 0D elastance pressure that defines the loading path, and the cavity-pressure Lagrange multiplier that the 3D solve uses to enforce the cavity-volume constraint. The multiplier is what acts on the variational boundary, so it is the correct pressure for boundary work. Using the 0D pressure instead gives a cycle-end cavity work 2.8% off — about 28 mJ on a 1000 mJ total in the production sPAP-70 case — even though the two pressure traces agree within 5.76 mmHg over the beat. The solver multiplier is saved at every checkpoint alongside the displacement field, and all stress-strain and proxy work calculations use it. The 0D model still supplies the coupled loading path but no longer enters the work bookkeeping.

The 5.76 mmHg gap is structural rather than numerical. The 0D elastance and the FEM Holzapfel-Ogden material with prescribed active tension are two independently calibrated mechanical descriptions of the same chamber; {ref}`sec-app-coupling-residual` unpacks the calibration architecture that produces the gap.
