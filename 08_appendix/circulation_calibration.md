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

Here $k_E$ controls the curvature of the passive filling response; as $k_E \to 0$, the expression reduces to the linear passive law. This was used as a calibration degree of freedom, not as a patient-specific stiffness measurement. The evidence for retaining it was modest and practical: linear and nonlinear variants produced similar pressure-target errors and nearly identical 0D--FEM pressure drift, but the nonlinear variant reduced the worst end-diastolic volume mismatch and slightly reduced the worst coupled RV systolic pressure miss. Because all proxy analyses use the achieved coupled pressures and volumes, the EDPVR choice enters the thesis only through the calibrated loading path, not as an interpreted myocardial material result.

```{list-table} Linear and nonlinear EDPVR audit from the saved 0D calibrations and coupled FEM handover runs.
:name: tab-edpvr-ab-audit
:header-rows: 1

* - Check
  - Linear EDPVR
  - Klotz-style nonlinear EDPVR
  - Interpretation
* - Corrected 8-case standalone 0D calibration: mean absolute pressure-target error
  - 1.25 mmHg
  - 1.22 mmHg
  - Essentially identical
* - Corrected 8-case standalone 0D calibration: mean / worst EDV mismatch
  - 3.67% / 16.9%
  - 3.28% / 8.6%
  - Nonlinear reduced the worst volume mismatch
* - Corrected 8-case coupled FEM handover: mean / worst RV systolic pressure miss
  - 4.61 / 11.4 mmHg
  - 4.55 / 8.8 mmHg
  - Only a small nonlinear advantage
* - Corrected 8-case coupled FEM handover: mean LV / RV pressure drift
  - 0.35 / 0.17 mmHg
  - 0.35 / 0.17 mmHg
  - No meaningful difference in pressure consistency
```

(sec-app-calibration-optimization)=
## Optimization Procedure

Each optimizer trial runs the 0D model to periodic steady state and extracts last-beat metrics: pressures, end-diastolic volumes, ejection fractions, cardiac index, and LV-RV stroke-volume imbalance. The cost function is a weighted sum of relative errors. The largest weights are assigned to the quantities that define the mechanical loading path: ventricular systolic pressures, mesh-compatible end-diastolic volumes, filling pressures, and stroke-volume balance. RV ejection fraction and cardiac index are used as guardrails so the optimizer cannot reach a pressure target by producing an implausible low-flow state.

The final search used CMA-ES through Optuna {cite}`akiba2019optuna,hansen2001completely`. This was chosen because the feasible circulation parameters are strongly correlated: for example, pulmonary resistance, compliance, chamber elastance, and blood-volume distribution must move together at high RV pressure. Neighbouring pressure cases were warm-started from one another, and the final parameter sets were re-solved for fifty beats before being written to disk and coupled to the mechanics model.

(sec-app-coupling-residual)=
## Standalone Calibration and the Coupling Residual

The optimizer above runs only the 0D Regazzoni circulation. The finite-element mechanics solve is not invoked during parameter selection — each Optuna trial advances the standalone elastance--Windkessel system to a periodic steady state and reads off the pressures, flows, and ejection fractions used in the cost. Coupling to the FEM happens only after calibration, when the parameter set chosen by Optuna is supplied to the bidirectional loop described in {ref}`sec-3d-0d-coupling`.

This standalone calibration leaves a residual when the model is coupled. The 0D ascribes a chamber pressure $\mathcal{E}(t)\,(\mathcal{V}-\mathcal{V}_0)$ via the time-varying elastance fitted by Optuna, while the FEM ascribes a chamber pressure equal to the cavity-volume Lagrange multiplier produced by the Holzapfel-Ogden material with the prescribed active tension $T_a$. These are two independent mechanical descriptions of the same chamber, anchored to the same physiological scale but not to each other. In the eight-case audit reported in {numref}`tab-edpvr-ab-audit`, the achieved-versus-target RV systolic pressure miss was 4.55 mmHg mean and 8.8 mmHg worst under the nonlinear EDPVR; in the production sPAP70 case the intra-beat agreement between the elastance prediction and the Lagrange multiplier was 5.76 mmHg, which translates into a 2.8% (28 mJ on 1000 mJ) discrepancy in cumulative cavity work and motivates the choice of solver pressure for all work calculations ({ref}`sec-solver-pressure`). The coupled steady state runs at the FEM's operating point; the 0D adapts to whatever pressure the FEM returns. The residual therefore reflects how far the standalone-calibrated elastance sits from the FEM's mechanics at the same volume, not a numerical error.

Two alternatives to standalone calibration were considered and rejected. Running the FEM inside the optimizer loop would replace each cheap 0D evaluation with a full coupled solve, raising the calibration cost by orders of magnitude and adding solver-failure modes to the cost surface. Tuning the Holzapfel-Ogden parameters or active-tension scale to make FEM pressures match the standalone 0D's targets would couple tissue mechanics to circulation calibration, breaking the proxy comparison's premise that material and contraction are independent of loading.
