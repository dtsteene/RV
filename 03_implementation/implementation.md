(chap-implementation)=
# Validating the Mechanical Reference

The model in {ref}`chap-model` produces stress, strain, and regional work fields that {ref}`chap-results` uses as the reference for the pressure-strain proxy comparison. That comparison only means something if the simulation is correct at the field level, not just at the level of pressure-volume loops. A run can converge, eject a plausible volume, and trace a healthy pressure waveform while the stress and strain fields underneath are wrong. The failures described in this chapter all share that property: each one was invisible in the pressure-volume loop and only surfaced when the field-level reference was checked directly.

Two classes of failure show up in this work. The forward problem can produce stress magnitudes outside reported myocardial ranges, or an inferred unloaded reference that the forward inflation cannot recover. The postprocessing can disagree with the solver about what it integrated — wrong region tags, wrong work integrand, wrong boundary-term formulation, or the wrong pressure record. The chapter is organized in that order: forward-problem checks first, then postprocessing checks. Where a check did not initially close, the source was identified and the implementation corrected; the pipeline described below is what passes these checks.

## Reference Configuration

The image-derived mesh is the heart at end-diastole, already loaded by ventricular pressures of 5–10 mmHg. The constitutive law expects a stress-free reference, so using this mesh directly would bake the pre-load into every downstream stress and strain. The inverse-elastic prestressing formulation used to infer that reference is defined in {ref}`sec-inverse-unloaded-reference`: it solves on the loaded end-diastolic mesh for an inverse displacement $\mathbf{u}_\text{pre}$ whose coordinates $\mathbf{X}=\mathbf{x}+\mathbf{u}_\text{pre}(\mathbf{x})$ define the stress-free reference. The same Dirichlet and Robin boundary conditions used in the cycle solve are applied during this step, so the reference and the cycle see identical supports. This section checks whether that inferred reference is mechanically usable.

A pilot sweep without intervention exposed the failure mode that drove the production setup. {numref}`fig-unloaded-cap-grid` shows the inferred unloaded reference at three representative sweep cases, with the production capped runs on top and the matching uncapped pilots underneath. In the uncapped pilot, the inferred unloaded RV cavity becomes implausibly small as RV end-diastolic pressure rises, collapsing visibly in the severe case (bottom right). The cause is structural: the baseline mesh and the passive material parameters are held fixed across every pressure level, so the algorithm cannot absorb a high RV end-diastolic pressure by hypertrophy, septal flattening, or stiffening, and the unloaded cavity volume is the only knob it has. The production sweep prevents this by capping the RV end-diastolic pressure used during inverse unloading at 5 mmHg — within the typical resting right-heart filling-pressure range of 0–8 mmHg in healthy adults {cite}`humbert2022esc` — and the top row of the figure is the result: an unloaded RV that stays plausibly shaped across the sweep. The cap acts only on the unloading step; the cycle solve still inflates to each case's full ED-pressure target.

```{figure} ../figures/fig_unloaded_cap_grid_nocbar.png
:name: fig-unloaded-cap-grid
:width: 95%

Inferred unloaded reference geometry at three representative sweep cases with peak RV systolic pressures of 32, 67, and 100 mmHg (left to right): production capped runs on top, uncapped pilots underneath. Colour is the cell-wise displacement magnitude $|u_\text{ED}|$ needed to inflate this geometry to the imaged end-diastolic mesh, on a 0–2 cm saturating scale (some uncapped-severe cells reach about 3 cm).
```

The quantitative side matches the visual one. The formal check on inverse unloading is round-trip consistency: forward-simulating from the inferred unloaded reference should reproduce the imaged end-diastolic shape, since that is what the inverse problem is defined to solve. The uncapped severe case fails this check by 9.4 mm whole-mesh mean and 13.9 mm at the septum (peak local discrepancy 32 mm), even though cavity volume is recovered exactly through the Lagrange-multiplier coupling — a failure that leaves the pressure-volume loop looking normal. With the cap applied, the same case closes to 3.7 mm whole-mesh and 4.3 mm at the septum, below the in-plane CMR voxel size, and the residual is septum-localised at about 1.5 times the free-wall means. The 5 mmHg value was chosen empirically: lower caps were unnecessary on the low-pressure cases, and higher caps reintroduced the small-cavity pathology on the high-pressure cases. The end-diastolic visual companion to {numref}`fig-unloaded-cap-grid` is {numref}`fig-app-ed-cap-grid`.

The cap is a fixed-geometry correction, not a model of remodelling. Passive stress at end-diastole does depend on the unloaded reference, but the proxy comparison is anchored on strain: the pressure-strain bookkeeping starts from start-of-beat strain and accumulates increments, which are invariant to translation of the reference state. The sweep-wide cap activation pattern and the inferred unloaded volume fractions are reported in {ref}`sec-app-reference-remodeling-sensitivity`.

## Stress Magnitudes

Pre-fix, peak fibre stresses sat systematically below the reported myocardial envelope {cite}`delhaas1994regional,finsberg2017phd`. The active strain energy was evaluated on the full right Cauchy-Green tensor $\mathbf{C}$, which couples volumetric response into the active fibre stress and depresses peak magnitudes during contraction. The production code evaluates the active strain energy on the isochoric part $\bar{\mathbf{C}}=J^{-2/3}\mathbf{C}$, the same deviatoric-volumetric split that the Holzapfel-Ogden passive law uses in {ref}`sec-holzapfel-ogden`; volumetric response is then carried entirely by the compressibility penalty rather than mixing through the fibre invariants. With the active law evaluated on $\bar{\mathbf{C}}$, peak Cauchy fibre stress $|\sigma_{ff}|$ on the lowest-pressure case is 62, 50, and 41 kPa for the LV free wall, RV free wall, and septum — inside the reported envelope ({numref}`fig-stress-magnitudes`). A magnitudes check is necessary but not sufficient: a stress field can sit in the right band and still be wrong in its spatial distribution. The directional and regional checks that follow give the spatial side.

```{figure} ../figures/fig_stress_magnitudes.png
:name: fig-stress-magnitudes
:width: 75%

Post-fix peak Cauchy fibre stress $|\sigma_{ff}|$ per region in the lowest-pressure case of the production sweep (peak LV pressure 105 mmHg, peak RV pressure 32 mmHg, bars) against a reported myocardial fibre-stress envelope (band, 20–80 kPa) drawn to bracket the canine epicardial peaks reported by Delhaas et al. {cite}`delhaas1994regional` (mean 21–27 kPa across regions; up to 2–3× higher transmurally) and the human computational estimates of Finsberg {cite}`finsberg2017phd`. The simulated peaks fall inside this envelope, in contrast to the pre-fix simulations where the active stress evaluated on the full right Cauchy-Green tensor $\mathbf{C}$ depressed the magnitudes below it.
```

The remaining checks shift from the forward problem to postprocessing. The regional work-density numbers reported in {ref}`chap-results` come from an offline replay of the saved stress and strain fields, and three choices in that replay must agree with what the solver assembled: which cells define each region, how the boundary-work terms are formulated, and which cavity pressure record is read. Each was wrong at some point during development. The whole-heart energy-consistency audit at the end of this chapter shows how the three fixes together close the budget.

(sec-shared-mask-tagging)=
## Region Definitions

The regional integrals require a definition of each region $\Omega_j$, and that definition must be stable across the loading sweep. The cell tags for the LV free wall, RV free wall, and septum are computed once on the imaged end-diastolic mesh and reused for every simulation in the sweep, rather than recomputed from each simulation's deformed end-diastolic state. This convention is called **shared-mask tagging** in the rest of the thesis.

The septum on that mesh is defined by the geometric distance rule in {ref}`sec-geometry-anatomical-model` rather than by a threshold on the LV-to-RV Laplace scalar. That choice and the choice to tag once rather than per case are linked, and each has a cost.

The clinically natural alternative to a shared reference mask would have been to re-tag each case on its own end-diastolic geometry. The geometric distance rule, however, is sensitive enough to the deformed shape that small case-to-case differences flip near-boundary cells between regions, and the integration domains would drift between simulations rather than tracking the same myocardium. A Laplace-scalar region label would avoid that drift. The LV-to-RV Laplace solution is smooth and stable under the small end-diastolic deformations the sweep produces, and the same property makes it a useful coordinate for blending fibre rules and weighting LV against RV pressure across the septum elsewhere in this work. Its weakness as a *region label*, however, is one of parameterization. Narrowing the scalar band does not produce a transparently smaller anatomical septum, especially near the basal RV/LV junction, and the Laplace partition we tested consistently misclassified cells in the curved transition between septum and free wall. That error is consistent across cases rather than case-dependent: the Laplace label would not have driven the cross-case mask drift the shared-mask scheme is meant to remove, but it would have made the envelope sweep in {ref}`sec-app-septum-epi-envelope` hard to control.

The geometric distance rule has the opposite profile. The size of the geometric septum is one of the things {ref}`chap-results` is sensitive to, so the parameterization advantage of the distance rule is what motivated picking it over the Laplace label. The shared-mask scheme then neutralizes its per-case drift by computing the partition once. An LV-side septal cell remains LV-side regardless of the RV pressure load, and the case-ranking effect of switching from per-case tagging to shared-mask tagging is documented in the appendix: the septal transmural-pressure ranking correlation moves from $r=+0.222$ to $r=-0.331$ once the case-to-case mask drift is removed ({ref}`tab-app-precap-capped-septum`). The production sweep used in {ref}`chap-results` integrates all 16 cases on the shared reference mesh under this convention ($n = 8070$ cells, 1269 geometric septum cells in every case).

(sec-implementation-boundary-terms)=
## Boundary Terms

The postprocessor reconstructs the boundary work — Robin support and cavity pressure work — separately from the solver, and each term needs to match the solver's variational form exactly to be meaningful. Two natural-looking formulas, one for each term, turned out to be variationally inconsistent with what the solver actually assembled and had to be corrected.

The Robin spring support is applied in the current configuration and only along the deformed normal, so the work integral pulls back to the reference configuration through the Nanson surface mapping {cite}`holzapfel2000nonlinear` (derived in {ref}`chap-appendix-energy-identity`),

$$
W_\text{Robin}(t)
= -\int_0^t \int_{\Gamma_\text{epi}\cup\Gamma_\text{base}}
\alpha\,(\mathbf{u}\cdot\mathbf{n})\,(\dot{\mathbf{u}}\cdot\mathbf{n})\,
\|\operatorname{cof}\mathbf{F}\,\mathbf{N}\|\,dS_0\,d\tau,
$$

with $\mathbf{n}=\operatorname{cof}\mathbf{F}\,\mathbf{N}/\|\operatorname{cof}\mathbf{F}\,\mathbf{N}\|$ the deformed unit normal and $\alpha\in\{k_\text{epi},k_\text{base}\}$ the spring stiffness on each patch. An earlier reference-configuration form, $-\int \alpha\,\mathbf{u}\cdot\dot{\mathbf{u}}\,dS_0$ — the natural first attempt — drops the Nanson area mapping and the deformed-normal projection. It overestimates the spring work because it penalises tangential sliding that the solver does not penalise.

Cavity-pressure work uses the nonlinear cavity-volume functional rather than the small-displacement approximation $\int \mathbf{N}\cdot\Delta\mathbf{u}\,dS_0$, because at finite deformation the linearised volume change underestimates the volume swing during ejection and filling, the phases that dominate work. The cavity contribution is

$$
W_\text{cav}(t)
= \int_0^t \bigl( p_\text{LV}\,\dot{\mathcal{V}}_\text{LV} + p_\text{RV}\,\dot{\mathcal{V}}_\text{RV} \bigr)\,d\tau
\;\approx\; \sum_{i\le n(t)}
\bigl( \bar p_{\text{LV},i}\,\Delta\mathcal{V}_{\text{LV},i}
+ \bar p_{\text{RV},i}\,\Delta\mathcal{V}_{\text{RV},i} \bigr),
$$

with $\Delta\mathcal{V}_i$ taken from the same cavity-volume functional used by the coupled solve and $\bar p_i$ the timestep-average solver Lagrange multiplier. With these conventions, the postprocessor reproduces the boundary work the solver computes.

## Pressure Records

The coupled simulation produces two pressure-like quantities: the 0D elastance pressure that defines the loading path, and the cavity-pressure Lagrange multiplier that the 3D solve uses to enforce the cavity-volume constraint. The multiplier is what acts on the variational boundary, so it is the correct pressure for boundary work. The structural origin of the gap between the two — and its magnitude on the production sweep — is documented in {ref}`sec-coupling-residual` and {ref}`sec-app-coupling-residual`; in a mid-pressure case (peak RV systolic about 86 mmHg), using the 0D pressure instead of the solver multiplier gives a 2.8% cycle-end cavity work error. The solver multiplier is saved at every checkpoint alongside the displacement field, and all stress-strain and proxy work calculations use it; the 0D model still supplies the coupled loading path but no longer enters the work bookkeeping.

## Energy Budget

The three preceding sections each removed a different postprocessing or stress-evaluation error. The diagnostic that made them visible is whole-heart energy consistency: internal stress-strain work, accumulated through the cycle, equals cavity-pressure work plus Robin support work, by the divergence-theorem identity quoted in {ref}`sec-energy-identity` and derived in {ref}`chap-appendix-energy-identity`. The internal stress-strain work is accumulated to time $t$ as

$$
W_\text{int}(t)
= \sum_{i\le n(t)} \int_\Omega \bar{\mathbf{S}}_i:\Delta\mathbf{E}_i\,dV_0,
$$

with $\bar{\mathbf{S}}_i$ the timestep-average second Piola-Kirchhoff stress and $\Delta\mathbf{E}_i$ the Green-Lagrange strain increment over step $i$; the cavity work $W_\text{cav}(t)$ and the Robin work $W_\text{Robin}(t)$ are the time-cumulative versions of the boundary integrals introduced in {ref}`sec-implementation-boundary-terms`. The closure residual is

$$
R(t) = W_\text{int}(t) - W_\text{cav}(t) - W_\text{Robin}(t),
$$

and energy consistency requires $|R(T)|/|W_\text{cav}(T)| \ll 1$ at the cycle end $T$. Chapter 1 confirmed that this implementation achieves $\sim 10^{-5}$ on the UKB baseline ({numref}`fig-energy-balance`).

That closure was the end of a longer debugging arc. During development $|R(T)|/|W_\text{cav}(T)|$ sat near $0.33$, and the first-pass diagnosis blamed DG1 projection oscillations in the thin septum. That diagnosis was wrong: replay tests after the surrounding pipeline was corrected showed DG1 reproduces the Quadrature6 integrated regional stress-strain work to within 1.2%, so the projection space was never the load-bearing issue. The real causes were the three errors corrected above: the deviatoric-strain stress evaluation (Stress Magnitudes), the Robin support-work formulation (Boundary Terms), and the cavity pressure record (Pressure Records). {numref}`fig-three-bugs-audit` isolates each fix's contribution to closure on the lowest-pressure sweep case (peak RV systolic 32 mmHg), by replaying the saved production displacement under successive postprocessing variants.

```{figure} ../figures/fig_three_bugs_audit.png
:name: fig-three-bugs-audit
:width: 80%

Cycle-end closure residual $|R(T)|$ on the lowest-pressure sweep case (peak RV systolic 32 mmHg) as the three fixes are applied successively, log scale. Each bar replays the saved production displacement under one postprocessing variant. The relative residual $|R(T)|/|W_\text{cav}(T)|$ is shown in parentheses below each value; reduction factors between adjacent bars sit above the arrows.
```

The figure makes three points. The deviatoric-strain fix has no measurable effect on closure (21.33 mJ → 21.32 mJ): the compressibility-stress contribution to cycle-integrated $\int \mathbf{S}:\dot{\mathbf{E}}\,dV\,dt$ is near zero at near-incompressibility, so the bug mattered for instantaneous stress magnitudes (Stress Magnitudes, above), not for whole-heart energy conservation. The cavity-pressure record fix is the largest single-step improvement, cutting the residual by 28× from 21 mJ to 0.75 mJ — the 0D-vs-Lagrange-multiplier pressure gap accumulates over the volume-changing phases of the cycle. The Robin-formulation fix cuts a further 126×, from 0.75 mJ to 6 µJ, by removing the spurious tangential-sliding contribution the buggy reference-configuration form had counted.

Two production cases, full debug-postprocessing rerun, confirm the post-fix tolerance: the lowest-pressure case closes at $|R(T)|/|W_\text{cav}(T)|=8.0\times10^{-6}$ and a high-RV case (peak RV systolic about 86 mmHg) at $3.2\times10^{-5}$. The current stress comes directly from the UFL constitutive expression; previous stress and strain states are stored in a degree-six quadrature space matching the integration order of the solve, and DG0 is used only as a cellwise partition for extracting per-cell integrals once the quadrature integrand has been formed, so regional cell sums equal the scalar domain assembly to numerical precision. The active/passive/compressible decomposition that confirms the passive elastic contribution returns to zero over the cycle, and the full DG0/DG1/Quadrature6 sensitivity including the residual septal underestimate that DG0 still produces at high pressure, are in {ref}`chap-appendix-numerical`.
