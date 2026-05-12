(chap-appendix-circulation-calibration)=
# Circulation Calibration Details

This appendix documents the calibration details behind the pressure-loading sweep defined in {ref}`chap-calibration`. The main text keeps only the information needed to interpret the results: what was held fixed, what varied, and what pressures were achieved. The sections below give the target provenance, the correction from the earlier exploratory sweep, the passive EDPVR choice, and the optimizer procedure.

(sec-app-calibration-targets)=
## Target Set

Every target used by the corrected circulation sweep was audited against a literature source or marked as an interpolation between sourced anchors. The operational target set is summarized here; the full audit is archived in `cardiac-work/results/docs/target_grounding_audit.md`. The primary thesis simulations use these corrected circulation targets together with the capped-RV-EDP inverse-unloading choice described in {ref}`sec-app-reference-remodeling-sensitivity`.

| Target | Value or rule | Role in the sweep |
|---|---|---|
| RV end-systolic pressure | 22 mmHg healthy anchor from Kovacs et al.; 30 mmHg upper-normal anchor from Kovacs et al.; 75 mmHg severe-pressure anchor from Tello et al.; intermediate cases interpolated or extrapolated {cite}`kovacs2009pulmonary,tello2019tapse` | Independent mechanical loading axis |
| LV end-systolic pressure | Held at 120 mmHg, consistent with preserved systemic systolic pressure in PAH cohorts {cite}`benza2010reveal` | Prevents artificial collapse of LV-side septal load |
| LV end-diastolic pressure | Held at 8 mmHg from healthy PAWP values in Kovacs et al. {cite}`kovacs2009pulmonary` | Preserves left-sided filling pressure |
| Aortic diastolic pressure | Held at 80 mmHg | Preserves systemic pressure scale |
| Mean left atrial pressure | Held at 8 mmHg; the ESC/ERS PAWP $\leq 15$ mmHg criterion is treated as a ceiling, not a target {cite}`humbert2022esc,kovacs2009pulmonary` | Maintains a pre-capillary phenotype |
| RV end-diastolic pressure | Banded using ESC/ERS right-atrial-pressure risk strata {cite}`humbert2022esc` | Filling-pressure guardrail |
| RV ejection fraction and cardiac index | Soft targets or guardrails based on ESC/ERS risk bands {cite}`humbert2022esc` | Prevents pressure targets from producing implausible forward-flow states |
| LV ejection fraction | Held near a normal lower bound rather than forced to decline | Avoids imposing unsupported LV systolic failure; CMR meta-analysis does not support LV EF as an independent PAH prognostic marker {cite}`baggen2016cmr` |
| LV and RV end-diastolic volumes | Used as mesh-compatibility targets rather than exact constraints | Reduces the volume-ratio correction needed at the 3D--0D interface |
| LV-RV stroke-volume balance | Penalized directly | Enforces closed-loop mass consistency |

Cardiac index is used rather than absolute cardiac output because the ESC/ERS risk table reports CI. For the UKB mean mesh, a representative adult body surface area of $1.75\,\mathrm{m}^2$ is used.

(sec-app-calibration-correction)=
## Target Provenance and Correction of the Sweep

An earlier exploratory target table varied several left-sided and systemic quantities across the RV pressure spectrum, including declining LV systolic pressure, LV filling pressure, aortic diastolic pressure, and LV ejection-fraction floor. The source audit found no primary-source support for those ramps, so they were removed from the corrected sweep.

The correction matters mechanically. A declining LV pressure target does part of the work of reducing the septal transmural pressure $p_\text{LV,ES}-p_\text{RV,ES}$. With LV pressure held stable, the transmural reduction is driven mainly by the imposed RV pressure rise. The earlier exploratory simulations are still useful, but only as a loading-path sensitivity check: they show that a septal correlation ranking can change when the LV pressure path changes. The main results use the corrected 16-case circulation path with the capped-reference inverse-unloading model.

Even after correction, the optimizer must balance the RV pressure target against the geometric requirement that the cavity volumes match the mesh. The UKB mean RV cavity is approximately 77 mL, and defending that volume can push the lowest-pressure case above the ideal Kovacs-normal systolic pulmonary pressure. The thesis therefore reports achieved pressures directly rather than relying on the nominal target label.

(sec-app-calibration-edpvr)=
## Passive EDPVR Choice

The standard Regazzoni chamber model uses a linear passive end-diastolic pressure-volume relation. For the fixed UKB mesh, this tied the end-diastolic pressure and end-diastolic volume too tightly during calibration: once the unstressed volume was chosen, changing the passive slope moved both the filling pressure and the mesh-compatible filling volume together. The final calibration therefore allowed the LV and RV passive terms to use a Klotz-style exponential pressure-volume relation {cite}`klotz2006single`,

$$
p(\mathcal{V}, t) = (\mathcal{E}_A - \mathcal{E}_B) a(t) (\mathcal{V} - \mathcal{V}_0) + \frac{\mathcal{E}_B}{k_E} \bigl(e^{k_E (\mathcal{V} - \mathcal{V}_0)} - 1\bigr).
$$

Here $k_E$ controls the curvature of the passive filling response; as $k_E \to 0$, the expression reduces to the linear passive law. This is a calibration degree of freedom, not a patient-specific stiffness measurement: an earlier methodological audit on a subset of severity cases compared linear and Klotz-style passive laws, and the Klotz form was retained because it reduced the worst-case standalone end-diastolic-volume mismatch on the fixed UKB mesh while leaving pressure-target errors essentially unchanged. All sixteen capped production cases use the Klotz form. Because all proxy analyses use the achieved coupled pressures and volumes, the EDPVR choice enters the thesis only through the calibrated loading path, not as an interpreted myocardial material result. {numref}`tab-edpvr-ab-audit` summarises the achieved standalone and coupled calibration quality across the production sweep.

```{list-table} Production calibration audit across the sixteen capped-reference sweep cases, all using the Klotz-style exponential EDPVR. Standalone rows compare the optimizer's last-beat 0D values against the calibration targets (six pressure targets per case) or against the fixed mesh end-diastolic volumes. Coupled-FEM rows compare the last-beat coupled values against either the same target or against the standalone 0D last-beat value at the same parameter set. Mean and worst are taken across the sixteen cases.
:name: tab-edpvr-ab-audit
:header-rows: 1

* - Quantity
  - Mean across 16 cases
  - Worst case
* - Standalone 0D mean absolute pressure-target error
  - 0.97 mmHg
  - 4.23 mmHg (sPAP30)
* - Standalone 0D LV end-diastolic-volume mismatch vs mesh
  - 5.0%
  - 33.0% (sPAP70)
* - Standalone 0D RV end-diastolic-volume mismatch vs mesh
  - 3.2%
  - 11.1% (sPAP30)
* - Coupled FEM LV systolic-pressure miss vs target
  - 7.1 mmHg
  - 14.7 mmHg (sPAP22)
* - Coupled FEM RV systolic-pressure miss vs target
  - 9.0 mmHg
  - 17.0 mmHg (sPAP80)
* - Coupled minus standalone RV peak pressure
  - 7.4 mmHg
  - 16.9 mmHg (sPAP80)
```

The table makes two patterns visible. The standalone 0D calibration meets the six pressure targets to about 1 mmHg on average. The volume mismatches absorbed by the mesh-to-circulation ratio are typically a few percent, with one sPAP70 LV outlier (the same case flagged in {ref}`sec-app-coupling-robustness`). The coupled-minus-standalone shifts are larger than the calibration-vs-target misses, which is exactly the standalone-versus-coupled operating-point shift discussed in {ref}`sec-app-coupling-residual` below: the FEM steady state can sit roughly 7 mmHg higher than the standalone 0D steady state on the RV side, and up to 17 mmHg higher in the severe cases.

(sec-app-calibration-optimization)=
## Optimization Procedure

Each optimizer trial runs the 0D model to periodic steady state and extracts last-beat metrics: pressures, end-diastolic volumes, ejection fractions, cardiac index, and LV-RV stroke-volume imbalance. The cost function is a weighted sum of relative errors. The largest weights are assigned to the quantities that define the mechanical loading path: ventricular systolic pressures, mesh-compatible end-diastolic volumes, filling pressures, and stroke-volume balance. RV ejection fraction and cardiac index are used as guardrails so the optimizer cannot reach a pressure target by producing an implausible low-flow state.

The final search used CMA-ES through Optuna {cite}`akiba2019optuna,hansen2001completely`. This was chosen because the feasible circulation parameters are strongly correlated: for example, pulmonary resistance, compliance, chamber elastance, and blood-volume distribution must move together at high RV pressure. Neighbouring pressure cases were warm-started from one another, and the final parameter sets were re-solved for fifty beats before being written to disk and coupled to the mechanics model.

(sec-app-coupling-residual)=
## Standalone Calibration and the Coupling Residual

The optimizer above runs only the 0D Regazzoni circulation. The finite-element mechanics solve is not invoked during parameter selection — each Optuna trial advances the standalone elastance--Windkessel system to a periodic steady state and reads off the pressures, flows, and ejection fractions used in the cost. Coupling to the FEM happens only after calibration, when the parameter set chosen by Optuna is supplied to the bidirectional loop described in {ref}`sec-3d-0d-coupling`.

This standalone calibration leaves a residual when the model is coupled. The 0D ascribes a chamber pressure $\mathcal{E}(t)\,(\mathcal{V}-\mathcal{V}_0)$ via the time-varying elastance fitted by Optuna, while the FEM ascribes a chamber pressure equal to the cavity-volume Lagrange multiplier produced by the Holzapfel-Ogden material with the prescribed active tension $T_a$. These are two independent mechanical descriptions of the same chamber, anchored to the same physiological scale but not to each other. The residual has two distinct views and they differ in size by roughly a factor of three.

The first view is the *intra-beat* agreement between the two pressure predictions evaluated at the same coupled volume trajectory. In the production sPAP70 case this is 5.76 mmHg mean over the beat, equivalent to a 2.8% discrepancy in cumulative cavity work (28 mJ on a 1000 mJ total). This is what motivates the choice of solver pressure for all work calculations ({ref}`sec-solver-pressure`).

The second view is the *standalone-versus-coupled operating-point shift*. The standalone 0D pre-run settles into one periodic state at the calibrated parameters; the coupled simulation settles into a different one. {numref}`fig-pv-standalone-vs-coupled` shows both at sPAP70. The LV loop shifts modestly (peak pressure 117 → 110 mmHg, end-diastolic volume 74 → 77 mL). The RV loop shifts substantially: peak pressure 69 → 86 mmHg (+17 mmHg), end-diastolic volume 77 → 103 mL (+26 mL). The FEM's stiffness, fibre architecture, and active-tension scale together pull the closed-loop steady state away from the elastance-only equilibrium that the optimizer targeted.

```{figure} ../figures/fig_pv_standalone_vs_coupled_sPAP70.png
:name: fig-pv-standalone-vs-coupled
:width: 95%

Standalone 0D (grey dashed) versus coupled 3D--0D (solid) pressure-volume loops at the calibrated parameters of the sPAP70 case, last beat of each. The LV loop shifts modestly between standalone and coupled (peak pressure $117 \to 110$ mmHg). The RV loop shifts substantially: peak pressure rises by 17 mmHg ($69 \to 86$ mmHg) and end-diastolic volume by 26 mL ($77 \to 103$ mL). This operating-point shift is the larger of the two coupling residuals; the intra-beat agreement between the elastance prediction and the Lagrange multiplier at the same coupled volume is much smaller (5.76 mmHg for this case).
```

The operating-point shift is what makes the `sPAP*` case names calibration shorthand for the standalone-targeted RV systolic pressure rather than the achieved coupled value: the standalone calibration hits the clinical target to within 1--2 mmHg by construction, but the coupled steady state can sit 10--20 mmHg higher on the RV side in the severe cases. The chapter's pressure axes, correlations, and proxies use the coupled-achieved pressures directly, so this shift does not propagate into the proxy comparison; it does, however, mean that case labels should not be read as achieved RV systolic pressures.

Two alternatives to standalone calibration were considered and rejected. Running the FEM inside the optimizer loop would replace each cheap 0D evaluation with a full coupled solve, raising the calibration cost by orders of magnitude and adding solver-failure modes to the cost surface. Tuning the Holzapfel-Ogden parameters or active-tension scale to make FEM pressures match the standalone 0D's targets would couple tissue mechanics to circulation calibration, breaking the proxy comparison's premise that material and contraction are independent of loading.
