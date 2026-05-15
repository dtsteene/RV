(chap-calibration)=
# Pressure-Loading Sweep

This chapter defines the pressure-loading sweep used in the results. The sweep is a controlled mechanics experiment that drives the same biventricular finite-element heart through a range of RV pressure loads; it is not a patient-specific PAH progression. All hemodynamic quantities in this chapter and in {ref}`chap-results` are simulation outputs — achieved peak RV systolic pressure, EDV, ESV — reported directly rather than via nominal calibration targets. The per-case calibration identifiers used in the audit appendix are explained in {ref}`chap-appendix-circulation-calibration`.

The calibration tunes the 0D Regazzoni circulation parameters in isolation: the 3D finite-element solve is not invoked during parameter selection, and the 3D mechanical model is left untouched. Each case's circulation parameters — ventricular and atrial elastances, ventricular unstressed volumes, the Klotz curvature $k_E$, vascular resistances and compliances (systemic and pulmonary), and the total blood-volume offset — are tuned with a CMA-ES optimizer through Optuna {cite}`akiba2019optuna,hansen2001completely` against a weighted cost over pressure, end-diastolic volume, and stroke-balance targets. Targets, cost function, full parameter bounds, and the per-case calibration audit are in {ref}`chap-appendix-circulation-calibration`.

One workflow inconsistency is worth flagging up front. Ventricular activation timing $T_C, T_R$ also sits in the standalone search space, but the searched values are overwritten with the fixed production values $T_C=0.25$ s, $T_R=0.40$ s before the coupled run so that the 3D active-stress waveform and the 0D ventricular elastance share one timing. The searched values are therefore never used downstream; a cleaner revision would simply exclude $T_C, T_R$ from the search space.

## Loading Targets and Achieved Pressures

The sweep was designed to isolate one hemodynamic feature: increasing RV pressure with comparatively preserved LV pressure. RV systolic-pressure targets were anchored to normal pulmonary pressure estimates and severe-pressure PAH examples {cite}`kovacs2009pulmonary,tello2019tapse`; left-sided pressure targets were held constant across the sweep, keeping the LV side as a stable contrast for the imposed RV pressure rise. The full target table and rationale are given in {ref}`sec-app-calibration-targets`.

No single parameter controls one outcome. Raising pulmonary resistance lifts RV pressure, but it also changes stroke volume, venous return, filling pressures, atrial pressures, and the next beat's operating point. Because the model distributes a fixed total blood volume across compliant compartments, there is no simple "set LV preload" knob; the target state has to emerge from the closed-loop circulation. In practice, the optimizer also had to balance pressure targets against the geometric requirement that the 0D cavity volumes remain compatible with the fixed finite-element mesh.

The primary coupled runs used in {ref}`chap-results` achieved the main feature the sweep was designed to isolate. Across the last beat of the 16 simulated cases, peak LV systolic pressure stayed in the range 105 to 120 mmHg, while peak RV systolic pressure rose from about 32 to 100 mmHg. The important point for the proxy analysis is the achieved pressure path, and that path is used directly in all results computations.

The clearest summary of the sweep is the pressure-volume loop family across all sixteen cases, shown as both the standalone 0D output of the calibration and the FEM-coupled production result in {numref}`fig-pv-loops-spectrum`. The FEM-coupled bottom row is the hemodynamic stage on which the pressure-strain proxy is tested; the gap between the two rows is the operating-point shift unpacked in {ref}`sec-coupling-residual`.

```{figure} ../figures/fig_4_2_pv_loops_spectrum.png
:name: fig-pv-loops-spectrum
:width: 95%

Pressure-volume loops across the 16 sweep cases. Top row: standalone 0D last beat. Bottom row: FEM-coupled last beat, with the FEM cavity Lagrange multiplier as the pressure source. Coloured by achieved peak RV systolic pressure, same colour per case across all chapter figures.
```

The bottom-row coupled RV loops start at about 32 mmHg, not at the 22 mmHg healthy anchor in the target table {cite}`kovacs2009pulmonary`. The standalone optimizer overshoots the four lowest-pressure targets by roughly 9 to 15 mmHg — it cannot reach 22 mmHg while also matching the mesh-compatible end-diastolic volumes and stroke-volume balance — and from the mid-pressure cases onward it hits target to within a few mmHg. The FEM coupling then adds another 5 mmHg on average to the RV peak across the sweep (range −4 to +17 mmHg); the per-case audit is in {ref}`sec-app-calibration-edpvr`. A Klotz-style exponential extension {cite}`klotz2006single` was added to the LV and RV passive terms to give the optimizer some independent curvature at the low-pressure end; it helped the standalone calibration slightly but did not change any downstream result — the central proxy comparisons in {ref}`chap-results` are unchanged when the linear form is used (see {ref}`chap-appendix-reference-state`).

(sec-coupling-residual)=
## Coupling Residual

The standalone 0D calibration leaves a residual when the model is coupled to the FEM. The 0D ascribes a chamber pressure via the time-varying elastance fitted by the optimizer — a single scalar elastance applied to a lumped chamber. The FEM ascribes a chamber pressure equal to the cavity-volume Lagrange multiplier required by the Holzapfel-Ogden material to keep the actual 3D cavity volume at the coupled value, in a heart with helical fibres and prescribed active stress. These are two independent mechanical descriptions of the same chamber: they sit in the same numeric range because each was independently designed to give realistic cardiac pressures, but no equation forces them to agree at a given volume and time — they tend to agree because both were calibrated to plausible cardiac pressures, not because they share an internal constraint.

The walk-through that follows uses a mid-pressure case (achieved peak RV systolic 66 mmHg coupled) to make the residual concrete. The standalone 0D calibration runs the circulation model on its own for thirty beats and settles into a periodic state ({numref}`fig-standalone-convergence`). The first few beats are pure warm-up — visible as the lightest, wildest curves in the figure — and they are harmless: the optimizer's cost function scores parameters only on last-beat metrics, and only the converged state is handed to the coupled mechanics solve. What matters is that the calibrated elastance dictates a clean limit cycle once initial transients have decayed.

```{figure} ../figures/fig_4_6_standalone_convergence.png
:name: fig-standalone-convergence
:width: 95%

Standalone 0D pressure-volume convergence for the mid-pressure case (achieved peak RV systolic 66 mmHg coupled). Each of the thirty pre-coupling beats is plotted, coloured by beat order (light = early, dark = late), with the converged last beat drawn bold (LV blue, RV red).
```

When the FEM takes over, the converged coupled limit cycle is not the same as the standalone one ({numref}`fig-coupling-jump`). The LV loop changes modestly because the LV is calibrated to the same end-diastolic mesh volume and a stable systemic load, so the Holzapfel-Ogden cavity pressure follows the standalone limit cycle closely (peak pressure $117\to110$ mmHg). The RV operating point shifts further in the same case (peak $59\to66$ mmHg, end-diastolic volume $78\to95$ mL), because the same FE wall is now responding to the imposed pulmonary load through its actual constitutive law rather than through the lumped elastance.

```{figure} ../figures/fig_4_7_coupling_jump.png
:name: fig-coupling-jump
:width: 95%

Operating-point shift between converged standalone and coupled limit cycles for the mid-pressure case. Standalone 0D last beat (grey dashed) versus FEM-coupled last beat (bold).
```

The coupled simulation reaches that new limit cycle over a few beats ({numref}`fig-coupled-convergence`). Beat one launches from the standalone state — visible as the lightest curve, close to the dashed reference in the figure above — and the system settles toward the bold converged loop within five or six beats. After convergence, the elastance prediction and the cavity Lagrange multiplier sit a few mmHg apart on average over the beat at the same coupled volume trajectory, a small fraction of cumulative cavity work; the per-case breakdown is in {ref}`sec-app-coupling-residual`. Intra-beat agreement is therefore reasonable once the limit cycle is reached, and the residual that matters in practice is the operating-point shift accumulated during the transient.

```{figure} ../figures/fig_4_8_coupled_convergence.png
:name: fig-coupled-convergence
:width: 95%

FEM-coupled pressure-volume convergence for the mid-pressure case. Each coupled beat is plotted with the FEM cavity Lagrange-multiplier pressure paired with the coupled cavity volume, coloured by beat order with the last beat drawn bold (LV blue, RV red).
```

The pattern is consistent across all sixteen cases: the LV loop barely moves between standalone and coupled, while the RV operating point shifts predominantly rightward in both peak pressure and end-diastolic volume in the higher-pressure cases. The rightward shift is the signature of the lumped elastance underestimating the FE wall's compliance: the 0D is a single time-varying scalar, while the FE is governed by Holzapfel-Ogden with helical fibres and prescribed active stress, and the two do not share a compliance curve. The LV stays anchored because the mesh-to-circulation ratio coupling pins LV volume to the FE mesh EDV; the RV has more room to drift, especially under the capped-unloading reference state used at the severe end (see {ref}`chap-discussion` for the full mechanical reading). The per-case overlay across all sixteen cases is in {numref}`fig-app-pv-all-16`.

This standalone-then-couple architecture has a built-in tension worth naming. The optimizer's cost function never sees the FEM coupling, so the operating-point shift grows in the severe cases where the lumped-elastance representation of the chamber diverges most from the Holzapfel-Ogden FE response. What is essential for the proxy analysis is that the ordering across the sweep is preserved by the achieved coupled values — the high-pressure cases remain high-pressure after coupling — and the cross-case correlations in {ref}`chap-results` use those achieved values directly.

Two more tightly coupled alternatives were considered and rejected. Running the FEM inside the optimizer loop replaces each cheap 0D evaluation with a full coupled solve, which is orders of magnitude more expensive and adds solver-failure modes to the cost surface. Tuning the Holzapfel-Ogden parameters until FEM cavity pressures match the standalone 0D targets would close the residual, but it would defeat the proxy test itself: the thesis compares a pressure-strain proxy against the FE stress-strain work the model computes, and that comparison is only meaningful if the FE material is chosen from constitutive literature, independently of how the circulation was calibrated. Tuning the material to match a calibration target would make the FE stress field — and therefore the FE work the proxy is being compared against — a function of the calibration itself. The "comparison" would then be between two quantities that were tuned together, not a test of how well a clinical proxy recovers the physical work generated by an independently parametrized myocardium. The full reasoning is in {ref}`sec-app-calibration-optimization`.

The operational consequence is that all work calculations use the solver Lagrange-multiplier pressure rather than the 0D elastance pressure, since the multiplier is what acts on the variational boundary. The shift does not propagate into the proxy comparison, because {ref}`chap-results` uses coupled-achieved pressures directly throughout.

## Interpretation Limits

The fixed-geometry design is the main limitation of the sweep. The 0D model can raise RV pressure and filling pressure, but it cannot thicken the RV wall, change septal curvature, or assign pressure-dependent passive remodelling to the finite-element mesh. Those missing adaptations matter most when the calibrated severe cases are unloaded back from end diastole: a high RV end-diastolic pressure applied to the same thin RV anatomy requires a larger inferred prestretch than a remodelled RV would. Capping the RV unloading pressure is therefore a deliberately conservative calibration choice. It bounds the case-to-case variation in inferred unloaded RV that an uncapped sweep would produce in the severe cases, but it should not be mistaken for patient-specific RV hypertrophy or material remodelling.

The sweep is therefore appropriate for testing pressure-strain proxy behaviour under a controlled loading path, but the absolute RV and RV-side septal work-density magnitudes at high RV pressure should be read as fixed-anatomy quantities rather than patient-level PAH magnitudes.
