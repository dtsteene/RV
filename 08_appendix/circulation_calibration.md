```{raw} latex
\appendix
```

(chap-appendix-circulation-calibration)=
# Circulation Calibration Audit

This appendix records the calibration audit data supporting the sweep described in {ref}`chap-calibration`: the literature provenance of each target, the constant and per-case target values, the Klotz EDPVR equation, the cost function and weight table, an Optuna trial trace for one representative case, and the per-case standalone-vs-coupled operating-point shift. The calibration choices and their consequences are argued in {ref}`chap-calibration`; the data lives here. All coupled-realized values reported below use the FEM cavity Lagrange multiplier (the formally correct cavity pressure for boundary work, as motivated in {ref}`sec-coupling-residual`), not the 0D-side pressure prediction during the coupled run.

(sec-app-calibration-targets)=
## Target Set

Every target used by the corrected circulation sweep was audited against a literature source or marked as an interpolation between sourced anchors.

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

Case identifiers `sPAP*` appear only in this appendix, as audit row labels for the sixteen calibration cases. The number after `sPAP` is the standalone RV systolic-pressure target in mmHg (the calibration input), not the achieved coupled value. The main thesis chapters refer to the same cases by their achieved coupled peak RV systolic pressure.

(sec-app-per-case)=
## Per-Case Targets and Achieved Values

The four left-sided pressure targets and the aortic diastolic pressure are held constant across the sixteen cases: LV systolic 120 mmHg, LV end-diastolic 8 mmHg, aortic diastolic 80 mmHg, mean left atrial 8 mmHg. The fixed UKB mesh end-diastolic volumes are LV 111.5 mL and RV 76.8 mL. The varying per-case targets are RV systolic pressure (the loading axis) and RV end-diastolic pressure (which moves in three bands following Humbert Table 16: 5 mmHg for the four lowest cases, 10 mmHg for the next four, 16 mmHg for the eight highest). {numref}`tab-app-per-case` lists the varying targets together with the standalone-realized and FEM-coupled-realized values for each case.

```{list-table} Per-case calibration audit for the sixteen-case production sweep. Standalone columns are the 0D last-beat values from the optimizer's final parameter set; coupled columns are the FEM cavity Lagrange-multiplier peaks from the last beat of each coupled simulation. All pressures in mmHg.
:name: tab-app-per-case
:header-rows: 2

* - Case
  - RV ESP
  -
  -
  - RV EDP
  -
  - LV peak
* -
  - target
  - standalone
  - coupled
  - target
  - standalone
  - coupled
* - sPAP22
  - 22
  - 26.9
  - 30.8
  - 5
  - 5.2
  - 101.9
* - sPAP25
  - 25
  - 36.0
  - 38.1
  - 5
  - 5.0
  - 107.3
* - sPAP30
  - 30
  - 34.9
  - 38.7
  - 5
  - 5.0
  - 108.0
* - sPAP35
  - 35
  - 40.6
  - 44.2
  - 5
  - 5.1
  - 107.5
* - sPAP45
  - 45
  - 45.3
  - 47.9
  - 5
  - 5.0
  - 105.3
* - sPAP50
  - 50
  - 50.1
  - 52.8
  - 10
  - 10.0
  - 108.7
* - sPAP55
  - 55
  - 55.2
  - 51.6
  - 10
  - 10.1
  - 106.5
* - sPAP60
  - 60
  - 59.6
  - 60.4
  - 10
  - 10.1
  - 104.5
* - sPAP65
  - 65
  - 64.6
  - 65.5
  - 10
  - 10.2
  - 104.2
* - sPAP70
  - 70
  - 70.0
  - 74.9
  - 16
  - 16.0
  - 100.6
* - sPAP75
  - 75
  - 75.0
  - 72.7
  - 16
  - 15.9
  - 106.9
* - sPAP80
  - 80
  - 80.1
  - 84.9
  - 16
  - 16.0
  - 106.9
* - sPAP85
  - 85
  - 85.0
  - 82.3
  - 16
  - 16.0
  - 110.6
* - sPAP87
  - 87
  - 87.0
  - 82.6
  - 16
  - 16.0
  - 107.7
* - sPAP92
  - 92
  - 92.0
  - 88.3
  - 16
  - 16.0
  - 108.2
* - sPAP95
  - 95
  - 95.1
  - 87.9
  - 16
  - 16.0
  - 107.0
```

Three patterns. First, the RV systolic standalone column hits target to about a millimetre from sPAP45 upward, but at the four lowest cases (sPAP22 through sPAP35) the standalone overshoots the target by 5--11 mmHg even with the Klotz exponential addition. This is the linear-EDPVR tightness identified in {ref}`chap-calibration`: at the low-pressure end the optimizer cannot simultaneously satisfy the low RV systolic target, the constant filling and aortic targets, and the mesh-compatible end-diastolic volumes. Klotz mitigates this only marginally. Second, the coupled RV column shifts the standalone value by a few mmHg in either direction (signed mean $+0.4$ mmHg, range $-7.1$ to $+4.9$ mmHg), so the FEM coupling is not consistently upward. The lowest coupled-achieved RV systolic pressure across the sweep is 30.8 mmHg at sPAP22. Third, the coupled LV peak undershoots the 120 mmHg target by 10--20 mmHg in every case; this is the LV-side FEM-vs-0D residual unpacked in {ref}`sec-app-coupling-residual` and does not propagate into the proxy comparison because the proxy uses the coupled-achieved pressure directly.

(sec-app-calibration-edpvr)=
## Passive EDPVR Equation and Calibration Audit

The Klotz-style exponential pressure-volume relation used by the LV and RV passive terms in the corrected calibration is

$$
p(\mathcal{V}, t) = (\mathcal{E}_A - \mathcal{E}_B) a(t) (\mathcal{V} - \mathcal{V}_0) + \frac{\mathcal{E}_B}{k_E} \bigl(e^{k_E (\mathcal{V} - \mathcal{V}_0)} - 1\bigr).
$$

Here $k_E$ controls the curvature of the passive filling response; as $k_E \to 0$, the expression reduces to the linear passive law. All sixteen capped production cases use this form. The motivation is in {ref}`chap-calibration`. {numref}`tab-edpvr-ab-audit` summarizes the standalone and coupled residuals across the sweep; {numref}`tab-app-per-case` gives the per-case detail.

```{list-table} Summary calibration residuals across the sixteen capped-reference sweep cases. Pressure errors are computed against the per-case target table; coupled values use the FEM cavity Lagrange multiplier. Volume mismatches compare the standalone 0D last-beat volume against the fixed mesh end-diastolic volume.
:name: tab-edpvr-ab-audit
:header-rows: 1

* - Quantity
  - Mean across 16 cases
  - Worst case
* - Standalone 0D mean absolute pressure-target error (96 cells: 6 pressure targets × 16 cases)
  - 0.97 mmHg
  - 17.5 mmHg (sPAP30 Ao DBP single-cell outlier)
* - Standalone 0D RV systolic-pressure miss vs target (16 cells)
  - 1.8 mmHg
  - 11.0 mmHg (sPAP25)
* - Standalone 0D LV end-diastolic-volume mismatch vs mesh
  - 5.0%
  - 33.0% (sPAP70)
* - Standalone 0D RV end-diastolic-volume mismatch vs mesh
  - 3.2%
  - 11.1% (sPAP30)
* - Coupled FEM LV systolic-pressure miss vs target
  - 13.6 mmHg
  - 19.4 mmHg (sPAP70)
* - Coupled FEM RV systolic-pressure miss vs target
  - 5.0 mmHg
  - 13.1 mmHg (sPAP25)
* - Coupled minus standalone RV peak pressure (signed, mean and range)
  - $+0.4$ mmHg
  - range $-7.1$ to $+4.9$ mmHg
```

The standalone calibration is tight on the constant left-sided targets and on the RV systolic target from the mid-pressure cases upward, but it overshoots the RV systolic target by 5--11 mmHg at the four lowest cases. The volume mismatches absorbed by the mesh-to-circulation ratio are typically a few percent. The worst standalone single-cell error (17.5 mmHg at sPAP30 Ao DBP) is a one-off optimizer outlier on a pressure that does not affect the proxy comparison. On the coupled side the LV peak undershoots target by about 14 mmHg on average — a systematic residual between the 0D-fitted elastance and the FEM material response that is unpacked in {ref}`sec-app-coupling-residual`. The coupled RV peak miss is smaller and the coupling shift between standalone and coupled RV peaks is small and bidirectional, not consistently upward as a 0D-side comparison would suggest.

(sec-app-calibration-optimization)=
## Optimizer

Each optimizer trial runs the 0D model to periodic steady state and extracts last-beat metrics: pressures, end-diastolic volumes, ejection fractions, cardiac index, and LV--RV stroke-volume imbalance.

### Cost Function

Let $M_q$ denote the standalone 0D last-beat realized value for quantity $q$ and let $T_q$ denote its target. The cost function combines a weighted relative-error sum on the pressure and volume targets, a stroke-volume balance penalty, and three soft-floor barriers tied to ESC/ERS risk bands:

$$
J = \sum_{q \in \mathcal{P} \cup \mathcal{V}} w_q \, \tilde{r}(M_q, T_q) \;+\; w_{SV} \frac{|SV_{LV} - SV_{RV}|}{\max(1,\, SV_{LV})} \;+\; \Phi_{\text{guard}}
$$

with the dynamic-weighted relative-error function

$$
\tilde{r}(M, T) = \frac{|M - T|}{|T|} \cdot \min\!\left(1, \frac{|M - T|}{0.05\, |T|}\right),
$$

which scales linearly down to zero as the relative error drops below 5% so that the optimizer focuses on the remaining gaps rather than continuing to refine targets it has already hit. $\mathcal{P}$ is the six-element pressure-target set, $\mathcal{V} = \{LV_{EDV}, RV_{EDV}\}$ is the mesh-compatibility pair, and $\Phi_{\text{guard}}$ is a sum of three soft-floor penalties (LV ejection fraction, RV ejection fraction, cardiac index) that activate only when the realized value falls below the corresponding ESC band floor. The base weights are:

| Term | Base weight $w$ | Activation |
|---|---:|---|
| RV systolic pressure | 200 | always |
| LV systolic pressure | 200 | always |
| RV end-diastolic pressure | 150 | always |
| LV end-diastolic pressure | 150 | always |
| Mean left atrial pressure | 150 | always |
| Aortic diastolic pressure | 100 | always |
| LV mesh-compatible EDV | 400 | always |
| RV mesh-compatible EDV | 400 | always |
| LV/RV stroke-volume balance | 300 | always |
| LV ejection fraction floor | 400 | only when $\text{LVEF} <$ floor |
| RV ejection fraction floor | 300 | only when $\text{RVEF} <$ floor |
| Cardiac index floor | 500 | only when $\text{CI} <$ floor |
| Stroke-volume periodic-convergence drift | 200 | always |

The two largest weights — mesh-compatible EDVs at 400 each — defend the geometric link between the 0D model and the FEM mesh; the next layer (systolic pressures at 200) defines the mechanical loading path; the soft floors (200--500 below ESC bands) act as one-sided guardrails preventing the optimizer from reaching a pressure target by producing an implausible low-flow or low-ejection-fraction state.

### Convergence

CMA-ES is run through Optuna {cite}`akiba2019optuna,hansen2001completely` with 3000 trials per case. Each trial evaluates the 0D model to periodic steady state on a single CPU; the search budget covers about an hour of wall time per case at this resolution. {numref}`fig-app-optuna-trace` shows the trial-by-trial cost values for one representative case (sPAP60). The running minimum reaches a flat plateau within roughly the first half of the budget and the trial cloud sits within a factor of about two of the running best for the remainder of the search, consistent with CMA-ES exploring a tight neighborhood of the optimum rather than continuing to push downhill. The same diagnostic was inspected for each of the sixteen cases; all reach a comparably flat plateau before the trial budget is exhausted.

```{figure} ../figures/fig_app_optuna_trace.png
:name: fig-app-optuna-trace
:width: 95%

Optuna trial trace for the representative sPAP60 case. Grey dots are per-trial cost values from the standalone-only CMA-ES search; the red line is the running minimum across trials. Both axes log-scaled vertically; the running best plateaus around trial 1500 and remains within a few percent of the final best for the rest of the budget.
```

### Optimizer choices and workflow inconsistency

CMA-ES was chosen because the feasible circulation parameters are strongly correlated: pulmonary resistance, compliance, chamber elastance, and blood-volume distribution must move together at high RV pressure. Neighbouring pressure cases were warm-started from one another, and the final parameter sets were re-solved for fifty beats before being written to disk and coupled to the mechanics model.

Known workflow inconsistency: the optimizer searches over ventricular contraction and relaxation durations $T_C, T_R$ during the standalone calibration, but these are reset to fixed production values $T_C=0.25$ s, $T_R=0.40$ s before the coupled FEM run so that the 3D active-stress waveform and the 0D ventricular elastance share one timing. A cleaner revision would exclude $T_C, T_R$ from the search space rather than searching and overriding; the calibrated standalone values are not used downstream.

(sec-app-coupling-residual)=
## Coupling Residual: Per-Case Breakdown

The two views of the coupling residual — intra-beat agreement and operating-point shift — are defined in {ref}`chap-calibration`. The diagnostic worst-case is illustrated in {numref}`fig-pv-standalone-vs-coupled`, and the all-sixteen per-case overlay is in {numref}`fig-app-pv-all-16`.

```{figure} ../figures/fig_pv_standalone_vs_coupled_sPAP70.png
:name: fig-pv-standalone-vs-coupled
:width: 95%

Standalone 0D (grey dashed) versus coupled 3D--0D (solid) pressure-volume loops at the calibrated parameters of the sPAP70 case, last beat of each. The pressure source for the coupled curve is the 0D-side elastance prediction during the coupled run (not the FEM cavity Lagrange multiplier); the LM-vs-elastance gap is the intra-beat agreement residual. Using the FEM LM instead, the coupled RV peak for sPAP70 is 74.9 mmHg — closer to the standalone last-beat value of 70.0 mmHg than the 0D-side trace suggests.
```

```{figure} ../figures/fig_4_9_all_16_pre_post.png
:name: fig-app-pv-all-16
:width: 100%

Standalone 0D versus FEM-coupled pressure-volume loops across all sixteen sweep cases, ordered by achieved peak RV systolic pressure (FEM, coupled). Standalone loops (light dashed) are the last beat of the standalone 0D pre-run; coupled loops (solid) pair the FEM cavity Lagrange multiplier with the coupled cavity volume.
```

Two alternatives to standalone calibration were considered and rejected. Running the FEM inside the optimizer loop would replace each cheap 0D evaluation with a full coupled solve, raising the calibration cost by orders of magnitude and adding solver-failure modes to the cost surface. Tuning the Holzapfel-Ogden parameters or active-tension scale to make FEM pressures match the standalone 0D's targets would couple tissue mechanics to circulation calibration, breaking the proxy comparison's premise that material and contraction are independent of loading.
