(chap-appendix-circulation-calibration)=
# Circulation Calibration Audit

This appendix records the calibration audit data supporting the sweep described in {ref}`chap-calibration`: the literature provenance of each target, the Klotz EDPVR equation and the per-case calibration audit, the optimizer used, and the per-case standalone-vs-coupled operating-point shift. The calibration choices and their consequences are argued in {ref}`chap-calibration`; the data lives here.

(sec-app-calibration-targets)=
## Target Set

Every target used by the corrected circulation sweep was audited against a literature source or marked as an interpolation between sourced anchors. The full audit is archived in `cardiac-work/results/docs/target_grounding_audit.md`.

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

Cardiac index is used rather than absolute cardiac output because the ESC/ERS risk table reports CI. For the UKB mean mesh, a representative adult body surface area of $1.75\,\mathrm{m}^2$ is used. Even after correction, the optimizer must balance the RV pressure target against the geometric requirement that the cavity volumes match the mesh, and the UKB mean RV cavity (about 77 mL) can push the lowest-pressure case slightly above the ideal Kovacs-normal systolic pulmonary pressure. The thesis therefore reports achieved pressures directly rather than nominal target labels.

(sec-app-calibration-edpvr)=
## Passive EDPVR Equation and Calibration Audit

The Klotz-style exponential pressure-volume relation used by the LV and RV passive terms in the corrected calibration is

$$
p(\mathcal{V}, t) = (\mathcal{E}_A - \mathcal{E}_B) a(t) (\mathcal{V} - \mathcal{V}_0) + \frac{\mathcal{E}_B}{k_E} \bigl(e^{k_E (\mathcal{V} - \mathcal{V}_0)} - 1\bigr).
$$

Here $k_E$ controls the curvature of the passive filling response; as $k_E \to 0$, the expression reduces to the linear passive law. All sixteen capped production cases use this form. The motivation is in {ref}`chap-calibration`; {numref}`tab-edpvr-ab-audit` is the corresponding per-case audit.

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

Two patterns: the standalone 0D calibration meets the six pressure targets to about 1 mmHg on average, and the volume mismatches absorbed by the mesh-to-circulation ratio are typically a few percent (one sPAP70 LV outlier flagged in {ref}`sec-app-coupling-robustness`). The coupled-minus-standalone shifts are larger than the calibration-vs-target misses; this is the operating-point shift unpacked in {ref}`sec-app-coupling-residual`.

(sec-app-calibration-optimization)=
## Optimizer

Each optimizer trial runs the 0D model to periodic steady state and extracts last-beat metrics: pressures, end-diastolic volumes, ejection fractions, cardiac index, and LV-RV stroke-volume imbalance. The cost function is a weighted sum of relative errors, with the largest weights on the quantities that define the mechanical loading path — ventricular systolic pressures, mesh-compatible end-diastolic volumes, filling pressures, and stroke-volume balance. RV ejection fraction and cardiac index are used as guardrails so the optimizer cannot reach a pressure target by producing an implausible low-flow state.

The final search used CMA-ES through Optuna {cite}`akiba2019optuna,hansen2001completely`. CMA-ES was chosen because the feasible circulation parameters are strongly correlated: pulmonary resistance, compliance, chamber elastance, and blood-volume distribution must move together at high RV pressure. Neighbouring pressure cases were warm-started from one another, and the final parameter sets were re-solved for fifty beats before being written to disk and coupled to the mechanics model.

Known workflow inconsistency: the optimizer searches over ventricular contraction and relaxation durations $T_C, T_R$ during the standalone calibration, but these are reset to fixed production values $T_C=0.25$ s, $T_R=0.40$ s before the coupled FEM run so that the 3D active-stress waveform and the 0D ventricular elastance share one timing. A cleaner revision would exclude $T_C, T_R$ from the search space rather than searching and overriding; the calibrated standalone values are not used downstream.

(sec-app-coupling-residual)=
## Coupling Residual: Per-Case Breakdown

The two views of the coupling residual — intra-beat agreement and operating-point shift — are defined in {ref}`chap-calibration`. The diagnostic worst-case is illustrated in {numref}`fig-pv-standalone-vs-coupled`, and the all-sixteen per-case overlay is in {numref}`fig-app-pv-all-16`.

```{figure} ../figures/fig_pv_standalone_vs_coupled_sPAP70.png
:name: fig-pv-standalone-vs-coupled
:width: 95%

Standalone 0D (grey dashed) versus coupled 3D--0D (solid) pressure-volume loops at the calibrated parameters of the sPAP70 case, last beat of each. The LV loop shifts modestly between standalone and coupled (peak pressure $117 \to 110$ mmHg). The RV loop shifts substantially: peak pressure rises by 17 mmHg ($69 \to 86$ mmHg) and end-diastolic volume by 26 mL ($77 \to 103$ mL). This operating-point shift is the larger of the two coupling residuals; the intra-beat agreement between the elastance prediction and the Lagrange multiplier at the same coupled volume is much smaller (5.76 mmHg for this case).
```

```{figure} ../figures/fig_4_9_all_16_pre_post.png
:name: fig-app-pv-all-16
:width: 100%

Standalone 0D versus FEM-coupled pressure-volume loops across all sixteen sweep cases, ordered by achieved peak RV systolic pressure (FEM, coupled). Standalone loops (light dashed) are the last beat of the standalone 0D pre-run; coupled loops (solid) pair the FEM cavity Lagrange multiplier with the coupled cavity volume. The LV loop stays close to its standalone reference in every case; the RV operating-point shift grows with imposed pressure and is consistently rightward in both peak pressure and end-diastolic volume.
```

Two alternatives to standalone calibration were considered and rejected. Running the FEM inside the optimizer loop would replace each cheap 0D evaluation with a full coupled solve, raising the calibration cost by orders of magnitude and adding solver-failure modes to the cost surface. Tuning the Holzapfel-Ogden parameters or active-tension scale to make FEM pressures match the standalone 0D's targets would couple tissue mechanics to circulation calibration, breaking the proxy comparison's premise that material and contraction are independent of loading.
