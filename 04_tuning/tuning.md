(chap-calibration)=
# Pressure-Loading Sweep

This chapter defines the pressure-loading sweep used in the results. The sweep is not a separate disease model and it is not a patient-specific PAH progression. It is a controlled loading experiment: the same biventricular finite-element heart is driven by different zero-dimensional circulation parameter sets so that RV pressure rises while the mechanical model itself remains fixed.

The calibration tunes the 0D Regazzoni circulation and chamber parameters in isolation: the 3D finite-element solve is not invoked during parameter selection, and the 3D mechanical model is left untouched. Across the pressure sweep, the biventricular mesh geometry, passive material law, fibre architecture, basal support condition, cavity-volume coupling formulation, ventricular activation timing, and 3D active tension are held fixed. What changes is the effective 0D circulation required to generate pressure-volume histories that are compatible with the fixed mesh. The residual that this standalone calibration leaves when the resulting parameter set is coupled to the FEM is documented in {ref}`sec-app-coupling-residual`.

The nominal case labels identify pressure-loading scenarios. They should not be read as clinical severity classes, because contemporary PAH risk models are not organized by systolic pulmonary pressure alone {cite}`humbert2022esc,benza2010reveal`. The achieved pressures and volumes from the coupled simulations, not the nominal labels, are the quantities used in {ref}`chap-results`.

## What Is Fixed and What Varies

The sweep separates the mechanical question from the circulation-fitting problem:

| Quantity | Treatment in the sweep | Reason |
|---|---|---|
| Mesh geometry and cavity volumes | Fixed to the UKB mean biventricular mesh | Isolates pressure loading from geometry sensitivity |
| 3D passive material, fibres, activation waveform, and peak active tension | Fixed | Keeps stress-strain changes attributable to loading and deformation, not retuned mechanics |
| Heart rate and ventricular activation timing | Fixed at 75 bpm with a 0.8 s cycle; coupled runs use $t_C=0$, $T_C=0.25$ s, and $T_R=0.40$ s | Keeps timing and cardiac-output scaling comparable across cases |
| Basal support and cavity coupling | Fixed | Keeps the boundary-value problem comparable across cases |
| 0D vascular and chamber elastance/volume parameters | Recalibrated per pressure case | Generates compatible pressure-volume histories for each loading scenario |
| Independent loading axis | Achieved RV systolic pressure | Provides the pressure range used in the proxy tests |

This distinction is important for interpretation. The calibrated 0D parameters are effective engineering constants, not direct measurements of vascular structure, myocardial stiffness, or contractile state in a specific patient. Their role is to provide plausible macroscopic boundary data for a fixed-geometry mechanics experiment. The detailed target set, target-source audit, passive EDPVR comparison, and optimizer procedure are collected in {ref}`chap-appendix-circulation-calibration`.

## Loading Targets and Achieved Pressures

The corrected sweep was designed to isolate one hemodynamic feature: increasing RV pressure with comparatively preserved LV pressure. RV systolic-pressure targets were anchored to normal pulmonary pressure estimates and severe-pressure PAH examples {cite}`kovacs2009pulmonary,tello2019tapse`; left-sided pressure targets were held stable to avoid imposing an unsupported decline in LV systolic load. Filling pressures, cardiac index, ejection fraction, end-diastolic volume compatibility, and LV-RV stroke-volume balance were used as guardrails rather than as independent findings. The full target table and rationale are given in {ref}`sec-app-calibration-targets`.

The inverse problem is still coupled. Raising pulmonary resistance lifts RV pressure, but it also changes stroke volume, venous return, filling pressures, atrial pressures, and the next beat's operating point. Because the model distributes a fixed total blood volume across compliant compartments, there is no simple "set LV preload" knob; the target state has to emerge from the closed-loop circulation. In practice, the optimizer also had to balance pressure targets against the geometric requirement that the 0D cavity volumes remain compatible with the fixed finite-element mesh.

The primary coupled runs used in {ref}`chap-results` achieved the main feature the sweep was designed to isolate. They use the same end-diastolic mesh target during inverse unloading but cap the RV end-diastolic unloading pressure at 5 mmHg, avoiding the severe RV reference collapse seen in the uncapped pilot. Across the last beat of the 16 simulated cases, peak LV pressure stayed in the range 105 to 120 mmHg, while peak RV pressure rose from about 32 to 100 mmHg. The important point for the proxy analysis is the achieved pressure path, and that path is used directly in all results computations.

The clearest summary of the sweep is the pressure-volume loop family in {numref}`fig-pv-loops-spectrum`. The figure shows why the sweep is useful for the thesis even though it is not a patient trajectory: the same biventricular geometry is driven through a controlled range of RV pressure loading, while the LV side remains comparatively preserved. This is the hemodynamic stage on which the pressure-strain proxy is tested.

```{figure} ../figures/fig_4_2_pv_loops_spectrum.png
:name: fig-pv-loops-spectrum
:width: 95%

Pressure-volume loops from the primary capped-reference pressure-loading spectrum, using the FEM cavity pressures returned by the volume-constrained mechanics solve. The RV loop rises from near-normal pressure toward systemic pressure, while the LV loop remains comparatively preserved. The visualized loops are more important for the proxy analysis than the nominal severity labels: all results use the achieved pressures and volumes from these coupled simulations.
```

## Interpretation Limits

The fixed-geometry design is the main limitation of the sweep. The 0D model can raise RV pressure and filling pressure, but it cannot thicken the RV wall, change septal curvature, or assign pressure-dependent passive remodelling to the finite-element mesh. Those missing adaptations matter most when the calibrated severe cases are unloaded back from end diastole: a high RV end-diastolic pressure applied to the same thin RV anatomy requires a larger inferred prestretch than a remodelled RV would. Capping the RV unloading pressure is therefore a deliberately conservative reference-state choice. It prevents the most obvious unphysical RV reference collapse, but it should not be mistaken for patient-specific RV hypertrophy or material remodelling.

The sweep is therefore appropriate for testing pressure-strain proxy behaviour under a controlled loading path, but the absolute RV and RV-side septal work-density magnitudes at high RV pressure should be read as fixed-anatomy quantities rather than patient-level PAH magnitudes. The calibration is not a diagnostic statement about disease severity; it provides pressure and volume boundary conditions for a controlled mechanics experiment.
