(chap-calibration)=
# Pressure-Loading Sweep

This chapter defines the pressure-loading sweep used in the results. The sweep is a controlled mechanics experiment that drives the same biventricular finite-element heart through a range of RV pressure loads; it is not a patient-specific PAH progression, and the nominal case labels are not clinical severity classes {cite}`humbert2022esc,benza2010reveal`. The achieved pressures and volumes from the coupled simulations, not the nominal labels, are the quantities used in {ref}`chap-results`.

The calibration tunes the 0D Regazzoni circulation parameters in isolation: the 3D finite-element solve is not invoked during parameter selection, and the 3D mechanical model is left untouched. Parameters are tuned via Optuna; targets, optimizer, and the per-case calibration audit are in {ref}`chap-appendix-circulation-calibration`.

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

The calibrated 0D parameters are effective engineering constants, not direct measurements of vascular structure, myocardial stiffness, or contractile state in a specific patient. Their role is to provide plausible macroscopic boundary data for a fixed-geometry mechanics experiment.

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

## Target Correction From the Exploratory Sweep

The corrected target set differs from an earlier exploratory predecessor in one important way. The exploratory targets varied several left-sided and systemic quantities across the RV pressure spectrum together: declining LV systolic pressure, falling LV filling pressure, lower aortic diastolic pressure, and a sliding LV ejection-fraction floor. A source audit ({ref}`sec-app-calibration-targets`) found no primary-source support for those ramps, so they were dropped from the corrected sweep.

The correction matters mechanically. A declining LV pressure target does part of the work of reducing septal transmural pressure $p_\text{LV,ES}-p_\text{RV,ES}$. With LV pressure held stable, the transmural reduction across the corrected sweep is driven mainly by the imposed RV pressure rise. The earlier exploratory simulations are retained only as a loading-path sensitivity check: they show that a septal correlation ranking can change when the LV pressure path changes. The main results use the corrected 16-case circulation path.

## Passive EDPVR Choice

The standard Regazzoni chamber model uses a linear passive end-diastolic pressure-volume relation. On the fixed UKB mesh this tied the standalone end-diastolic pressure and volume too tightly: once the unstressed volume was chosen, changing the passive slope moved both the filling pressure and the mesh-compatible filling volume together. The corrected calibration therefore lets the LV and RV passive terms use a Klotz-style exponential pressure-volume relation {cite}`klotz2006single`; the equation and per-case calibration audit are in {ref}`sec-app-calibration-edpvr`. The Klotz form is a calibration degree of freedom, not a patient-specific stiffness measurement. The proxy analyses use only the achieved coupled pressures and volumes. The Klotz choice therefore enters the thesis through the loading path it produces, not as an interpreted myocardial material result.

(sec-coupling-residual)=
## Coupling Residual

The standalone 0D calibration leaves a residual when the model is coupled to the FEM. The 0D ascribes a chamber pressure $\mathcal{E}(t)(\mathcal{V}-\mathcal{V}_0)$ via the time-varying elastance fitted by the optimizer, while the FEM ascribes a chamber pressure equal to the cavity-volume Lagrange multiplier produced by the Holzapfel-Ogden material with the prescribed active tension. These are two independent mechanical descriptions of the same chamber, anchored to the same physiological scale but not to each other.

The residual has two distinct views and they differ in size by roughly a factor of three. The first is *intra-beat agreement*: at the same coupled volume trajectory, the elastance prediction and the Lagrange multiplier sit 5.76 mmHg apart on average over the beat in a mid-pressure case (achieved peak RV systolic 86 mmHg), equivalent to a 2.8% discrepancy in cumulative cavity work. The second is the *standalone-versus-coupled operating-point shift*: the standalone 0D pre-run settles into one periodic state and the coupled simulation settles into a different one. In the same mid-pressure case the LV loop shifts modestly (peak pressure $117\to110$ mmHg) while the RV loop shifts substantially (peak $69\to86$ mmHg, EDV $77\to103$ mL). Across the severe cases the RV operating-point shift can be 10--20 mmHg. The shift is illustrated in {numref}`fig-pv-pre-post-coupling` for the lowest- and highest-pressure cases of the sweep.

```{figure} ../figures/fig_4_6_pv_loops_pre_post_coupling.png
:name: fig-pv-pre-post-coupling
:width: 95%

Standalone 0D versus FEM-coupled pressure-volume loops for the lowest-pressure case (achieved peak RV systolic 32 mmHg, top row) and the highest-pressure case (achieved peak RV systolic 100 mmHg, bottom row). Standalone loops (dashed grey) are the last beat of the standalone 0D pre-run; coupled loops (colored) pair the cavity Lagrange-multiplier pressures from the FEM mechanics solve with the coupled cavity volumes. The LV operating point shifts modestly with coupling; the RV operating point shifts substantially in both cases, growing in volume and peak pressure relative to the standalone reference.
```

Two consequences for the rest of the thesis. First, all work calculations use the solver Lagrange-multiplier pressure rather than the 0D elastance pressure, since the multiplier is what acts on the variational boundary and the 2.8% intra-beat work discrepancy already shows the cost of the wrong choice. Second, the `sPAP*` case names are calibration shorthand for the standalone-targeted RV systolic pressure, not for the achieved coupled value; the pressure axes, correlations, and proxies in {ref}`chap-results` use the coupled-achieved pressures directly, so this shift does not propagate into the proxy comparison.

## Interpretation Limits

The fixed-geometry design is the main limitation of the sweep. The 0D model can raise RV pressure and filling pressure, but it cannot thicken the RV wall, change septal curvature, or assign pressure-dependent passive remodelling to the finite-element mesh. Those missing adaptations matter most when the calibrated severe cases are unloaded back from end diastole: a high RV end-diastolic pressure applied to the same thin RV anatomy requires a larger inferred prestretch than a remodelled RV would. Capping the RV unloading pressure is therefore a deliberately conservative calibration choice. It bounds the case-to-case variation in inferred unloaded RV that an uncapped sweep would produce in the severe cases, but it should not be mistaken for patient-specific RV hypertrophy or material remodelling.

The sweep is therefore appropriate for testing pressure-strain proxy behaviour under a controlled loading path, but the absolute RV and RV-side septal work-density magnitudes at high RV pressure should be read as fixed-anatomy quantities rather than patient-level PAH magnitudes. The calibration is not a diagnostic statement about disease severity; it provides pressure and volume boundary conditions for a controlled mechanics experiment.
