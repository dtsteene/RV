# Calibrating the Circulation Model

## Purpose of the Calibration

The calibration in this chapter tunes the 0D Regazzoni circulation and chamber parameters. It does **not** tune the 3D finite-element mechanics. Across the pressure sweep, the biventricular mesh geometry, passive material law, fibre architecture, basal support condition, cavity-volume coupling formulation, and 3D active tension are held fixed. What changes is the effective 0D circulation required to generate pressure-volume histories that are compatible with the fixed mesh.

The sweep is therefore a controlled mechanical loading experiment, not a simulated PAH disease trajectory. The nominal case labels identify pressure-loading scenarios. They should not be read as clinical severity classes, because contemporary PAH risk models are not organized by systolic pulmonary pressure alone {cite}`humbert2022esc,benza2010reveal`. The achieved pressures and volumes from the coupled simulations, not the nominal labels, are the quantities used in the results chapter.

The inverse problem is still difficult. Raising pulmonary resistance lifts RV pressure, but it also changes stroke volume, venous return, ventricular filling, atrial pressures, and the next beat's operating point. In a closed-loop circulation these changes return to their origin over several beats, so adjusting one parameter to fix one target often breaks another target that was previously acceptable. A further complication is that the model distributes a fixed total blood volume across compliant compartments; ventricular filling pressures emerge from that distribution rather than being prescribed directly. There is no simple "set LV preload" knob.

## What Is Fixed and What Varies

The calibration separates the mechanical question from the circulation-fitting problem:

| Quantity | Treatment in the sweep | Reason |
|---|---|---|
| Mesh geometry and cavity volumes | Fixed to the UKB mean biventricular mesh | Isolates pressure loading from geometry sensitivity |
| 3D passive material, fibres, activation, and peak active tension | Fixed | Keeps stress-strain changes attributable to loading and deformation, not retuned mechanics |
| Basal support and cavity coupling | Fixed | Keeps the boundary-value problem comparable across cases |
| 0D circulation and chamber parameters | Recalibrated per pressure case | Generates compatible pressure-volume histories for each loading scenario |
| Independent loading axis | Achieved RV systolic pressure | Provides the pressure range used in the proxy tests |

This distinction is important for interpreting the thesis. The calibrated 0D parameters are effective engineering constants, not direct measurements of vascular structure, myocardial stiffness, or contractile state in a specific patient. Their role is to provide plausible macroscopic boundary data for a fixed-geometry mechanics experiment.

## Target Set

Every target used by the corrected sweep was audited against a specific literature source or marked as an interpolation between sourced anchors. The full row-by-row audit is archived in `cardiac-work/results/docs/target_grounding_audit.md`; the operational target set is summarized here.

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
| LV and RV end-diastolic volumes | Matched to the fixed mesh cavity volumes | Makes the 0D state compatible with the 3D geometry |
| LV-RV stroke-volume balance | Penalized directly | Enforces closed-loop mass consistency |

Cardiac index is used rather than absolute cardiac output because the ESC/ERS risk table reports CI. For the UKB mean mesh we use a representative adult body surface area of $1.75\,\mathrm{m}^2$; for patient-specific calibrations outside the main thesis sweep, the patient's own anthropometric record can be used.

## Target Provenance and Correction of the Sweep

An earlier exploratory target table varied several left-sided and systemic quantities across the RV pressure spectrum: LV end-systolic pressure declined from 118 to 90 mmHg, LV end-diastolic pressure from 8 to 4 mmHg, aortic diastolic pressure from 80 to 60 mmHg, mean left atrial pressure from 8 to 7 mmHg, and the LV ejection-fraction floor from 55% to 20%. The source audit found no primary-source support for those ramps. They were therefore removed from the corrected sweep.

The correction matters mechanically. A declining LV pressure target does part of the work of reducing the septal transmural pressure $p_\text{LV,ES}-p_\text{RV,ES}$. With LV pressure held stable, the transmural reduction is driven mainly by the imposed RV pressure rise. The old simulations are still useful, but only as a loading-path sensitivity check: they show that a septal correlation ranking can change when the LV pressure path changes. The main results use the corrected 16-case sweep.

Even after correction, the optimizer must balance the RV pressure target against the geometric requirement that the cavity volumes match the mesh. The UKB mean RV cavity is approximately 77 mL, and defending that volume can push the lowest-pressure case above the ideal Kovacs-normal systolic pulmonary pressure. The thesis therefore reports achieved pressures directly rather than hiding residual mismatch behind the nominal target label.

## Decoupling EDP and EDV: A Nonlinear EDPVR

One structural limitation of the standard Regazzoni formulation had to be resolved before the target set could be matched. The published model uses a linear time-varying elastance,

$$
p(\mathcal{V}, t) = \mathcal{E}(t) (\mathcal{V} - \mathcal{V}_0), \qquad \mathcal{E}(t) = \mathcal{E}_B + (\mathcal{E}_A - \mathcal{E}_B) a(t),
$$

where $\mathcal{E}_A$ is the active systolic elastance, $\mathcal{E}_B$ is the passive diastolic elastance, and $a(t)$ is the activation waveform. In this formulation the end-diastolic pressure and end-diastolic volume are controlled by the same parameter $\mathcal{E}_B$: once the unstressed volume $\mathcal{V}_0$ is fixed, the diastolic operating point is pinned to the single line $p_\text{ED}=\mathcal{E}_B(\mathcal{V}_\text{ED}-\mathcal{V}_0)$. For a mesh whose geometric cavity volumes are small relative to population averages, this coupling makes it hard to match both physiological EDP and the mesh EDV without distorting the rest of the loop.

The fix was to replace the passive ventricular pressure law with an exponential pressure-volume relationship, following the Klotz EDPVR framework {cite}`klotz2006single`:

$$
p(\mathcal{V}, t) = (\mathcal{E}_A - \mathcal{E}_B) a(t) (\mathcal{V} - \mathcal{V}_0) + \frac{\mathcal{E}_B}{k_E} \bigl(e^{k_E (\mathcal{V} - \mathcal{V}_0)} - 1\bigr).
$$

The new parameter $k_E$ has units of inverse volume and controls how quickly the chamber stiffens as it approaches its distensibility limit. In the limit $k_E \to 0$, the expression reduces to the original linear model. Near $\mathcal{V}_0$ the passive pressure grows approximately as $\mathcal{E}_B(\mathcal{V}-\mathcal{V}_0)$, while at larger volumes the exponential term dominates and prevents overfilling. This separates the low-pressure filling slope from the high-volume stiffening scale, allowing EDP and EDV to be matched more independently. The modification was applied to the LV and RV chambers only; the thin-walled atria remained linear.

The decision to introduce $k_E$ was empirical. Early calibration runs with the linear elastance repeatedly failed to satisfy pressure targets and mesh-volume constraints at the same time. Introducing the Klotz-style exponential term resolved these practical failure modes. It should therefore be read as a calibration device that gives the closed-loop model enough diastolic flexibility to match the mesh volumes and pressure targets, not as a claim that fitted $k_E$ values are direct measurements of patient myocardial stiffness.

```{figure} ../figures/fig_2_13_klotz_edpvr.png
:name: fig-klotz-edpvr
:width: 95%

The Klotz nonlinear end-diastolic pressure-volume relationship for the healthy LV and RV calibrations, compared with the linear law that the standard Regazzoni model uses. With $k_E=0$, the slope at $\mathcal{V}_0$ pins both the low-pressure filling response and the end-diastolic operating point onto a single line; the exponential term frees them. The filled markers show the achieved end-diastolic operating points $(\mathcal{V}_\text{ED}, p_\text{ED})$ for the healthy calibration, which sit on the compliant portion of the Klotz curve.
```

## Optimization Procedure

Each optimizer trial runs the 0D model to periodic steady state and extracts last-beat metrics: peak and end-diastolic pressures, aortic diastolic pressure, mean left atrial pressure, end-diastolic volumes, ejection fractions, cardiac index, and LV-RV stroke-volume imbalance. The cost is a weighted sum of relative errors, with target weights relaxed once a quantity is already close to its desired value:

$$
\omega_\text{eff}(\theta) =
\begin{cases}
\omega_\text{base} \cdot (|\text{err}|/\tau), & |\text{err}| < \tau, \\
\omega_\text{base}, & \text{otherwise},
\end{cases}
\qquad \tau = 5\%.
$$

The base priorities follow the mechanical role of each target. Ventricular end-systolic pressures define the loading path and the septal pressure environment. End-diastolic volumes are weighted strongly because they connect the 0D circulation to the fixed 3D mesh. End-diastolic pressures and left atrial pressure enforce plausible filling and a pre-capillary phenotype. Stroke-volume balance prevents closed-loop mass drift. RV ejection fraction and cardiac index act as soft physiological guardrails, so that the optimizer cannot reach a pressure target by producing an implausible low-flow state. Infeasible trials receive graded penalties rather than a single hard failure value, giving the optimizer information about the boundary of the feasible region.

The final search used CMA-ES through Optuna rather than the Tree-structured Parzen Estimator sampler {cite}`akiba2019optuna,hansen2001completely`. TPE was useful for early exploration, but it treats parameters largely coordinate-wise and struggled with the correlated directions of the closed-loop circulation. CMA-ES adapts a full covariance matrix and therefore learns parameter combinations such as pulmonary resistance and compliance moving together. This was especially important at high RV pressure, where feasible solutions lie on narrow correlated ridges.

Neighbouring pressure cases were warm-started from one another. A converged lower-pressure case provides a better initial point for the next pressure case than a random initialization, because the target hemodynamics change smoothly along the spectrum. Final parameter sets were re-solved for fifty beats before being written to disk and coupled to the mechanics model.

## Calibration Achievements and Limits

The corrected coupled runs used in the results chapter achieved the main feature the sweep was designed to isolate: RV pressure rises while LV pressure remains comparatively stable. Across the last beat of the 16 simulated cases, peak LV pressure stayed in the range 102 to 111 mmHg, while peak RV pressure rose from about 31 to 88 mmHg. The lowest case sits above the ideal Kovacs-normal systolic pulmonary pressure target, and the highest cases do not reach the full nominal 95 mmHg target in the coupled mechanics run. The important point for the proxy analysis is the achieved pressure path, and that path is used directly in all results computations.

The clearest summary of this calibration is the pressure-volume loop family in {numref}`fig-pv-loops-spectrum`. The figure shows why the sweep is useful for the thesis even though it is not a patient trajectory: the same biventricular geometry is driven through a controlled range of RV pressure loading, while the LV side remains comparatively preserved. This is the hemodynamic stage on which the pressure-strain proxy is tested.

```{figure} ../figures/fig_4_2_pv_loops_spectrum.png
:name: fig-pv-loops-spectrum
:width: 95%

Pressure-volume loops from the corrected pressure-loading spectrum, using the FEM cavity pressures returned by the volume-constrained mechanics solve. The RV loop rises from near-normal pressure toward systemic pressure, while the LV loop remains comparatively preserved. The visualized loops are more important for the proxy analysis than the nominal severity labels: all results use the achieved pressures and volumes from these coupled simulations.
```

It is worth being explicit about the limit of the calibration. The circulation model is a lumped-parameter abstraction, and its parameters are effective constants with no direct anatomical counterpart. A calibrated pulmonary resistance several times the healthy value does not measure any particular small vessel in any particular lung. It says that an effective resistance of that magnitude, embedded in this Windkessel circulation and coupled to this finite-element heart, produces the desired macroscopic pressure loading. The calibration is therefore not a diagnostic statement about disease severity. It provides pressure and volume boundary conditions for a controlled mechanics experiment.

Patient-specific healthy and PAH meshes are available in the wider project and motivated the calibration machinery. They are not used as the primary evidence here because the present results already show that pressure-choice conclusions can depend on the loading path. Adding patient-specific geometry without measured and well-constrained hemodynamics would change wall thickness, cavity volume, curvature, stiffness, contractility, and pressure at the same time. That extension is valuable, but it belongs as a geometry-sensitivity or patient-specific validation study rather than as a simple continuation of the fixed-geometry sweep.
