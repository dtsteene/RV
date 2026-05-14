(chap-calibration)=
# Pressure-Loading Sweep

This chapter defines the pressure-loading sweep used in the results. The sweep is a controlled mechanics experiment that drives the same biventricular finite-element heart through a range of RV pressure loads; it is not a patient-specific PAH progression, and the nominal case labels are not clinical severity classes {cite}`humbert2022esc,benza2010reveal`. All hemodynamic quantities in {ref}`chap-results` are simulation outputs — achieved peak RV systolic pressure, EDV, ESV — never the nominal target. Cases are labelled `sPAP*` for the standalone calibration target (systolic pulmonary-artery pressure). Achieved values are reported as peak RV systolic chamber pressure, both for what optimization hits during the standalone 0D pre-run and for what the coupled simulation produces after the operating-point shift in {ref}`sec-coupling-residual`; {ref}`chap-results` uses the coupled-achieved value throughout. The two names refer to the same physical quantity in different roles — vascular target versus chamber outcome — and keeping them separate makes the target-versus-achieved gap legible.

The calibration tunes the 0D Regazzoni circulation parameters in isolation: the 3D finite-element solve is not invoked during parameter selection, and the 3D mechanical model is left untouched. Each case's circulation parameters — ventricular and atrial elastances, ventricular unstressed volumes, the Klotz curvature $k_E$, vascular resistances and compliances (systemic and pulmonary), and the total blood-volume offset — are tuned with a CMA-ES optimizer through Optuna {cite}`akiba2019optuna,hansen2001completely` against a weighted cost over pressure, end-diastolic volume, and stroke-balance targets. Ventricular activation timing is also searched during the standalone calibration but pinned to the production values $T_C=0.25$ s, $T_R=0.40$ s for the coupled run, so the 3D active-stress waveform and the 0D ventricular elastance share one timing. Targets, cost function, full parameter bounds, and the per-case calibration audit are in {ref}`chap-appendix-circulation-calibration`.

## Loading Targets and Achieved Pressures

The sweep was designed to isolate one hemodynamic feature: increasing RV pressure with comparatively preserved LV pressure. RV systolic-pressure targets were anchored to normal pulmonary pressure estimates and severe-pressure PAH examples {cite}`kovacs2009pulmonary,tello2019tapse`; left-sided pressure targets were held stable to avoid imposing an unsupported decline in LV systolic load. The full target table and rationale are given in {ref}`sec-app-calibration-targets`.

No single parameter controls one outcome. Raising pulmonary resistance lifts RV pressure, but it also changes stroke volume, venous return, filling pressures, atrial pressures, and the next beat's operating point. Because the model distributes a fixed total blood volume across compliant compartments, there is no simple "set LV preload" knob; the target state has to emerge from the closed-loop circulation. In practice, the optimizer also had to balance pressure targets against the geometric requirement that the 0D cavity volumes remain compatible with the fixed finite-element mesh.

The primary coupled runs used in {ref}`chap-results` achieved the main feature the sweep was designed to isolate. Across the last beat of the 16 simulated cases, peak LV systolic pressure stayed in the range 105 to 120 mmHg, while peak RV systolic pressure rose from about 32 to 100 mmHg. The important point for the proxy analysis is the achieved pressure path, and that path is used directly in all results computations.

The clearest summary of the sweep is the pressure-volume loop family in {numref}`fig-pv-loops-spectrum`. The same biventricular geometry is driven through a controlled range of RV pressure loading anchored to the PAH literature, while the LV side remains comparatively preserved. This is the hemodynamic stage on which the pressure-strain proxy is tested.

```{figure} ../figures/fig_4_2_pv_loops_spectrum.png
:name: fig-pv-loops-spectrum
:width: 95%

Pressure-volume loops for the 16-case pressure-loading sweep, using the FEM cavity pressures from the volume-constrained mechanics solve. The RV loop rises from near-normal pressure toward systemic pressure, while the LV loop remains comparatively preserved.
```

## Passive EDPVR Choice

The standard Regazzoni chamber model uses a linear passive end-diastolic pressure-volume relation. On the fixed UKB mesh this tied the standalone end-diastolic pressure and volume too tightly: once the unstressed volume was chosen, changing the passive slope moved both the filling pressure and the mesh-compatible filling volume together. The calibration therefore lets the LV and RV passive terms use a Klotz-style exponential pressure-volume relation {cite}`klotz2006single`; the equation and per-case calibration audit are in {ref}`sec-app-calibration-edpvr`. The Klotz form is a calibration degree of freedom, not a patient-specific stiffness measurement. The proxy analyses use only the achieved coupled pressures and volumes. The Klotz choice therefore enters the thesis through the loading path it produces, not as an interpreted myocardial material result.

(sec-coupling-residual)=
## Coupling Residual

The standalone 0D calibration leaves a residual when the model is coupled to the FEM. The 0D ascribes a chamber pressure via the time-varying elastance with Klotz passive extension fitted by the optimizer, while the FEM ascribes a chamber pressure equal to the cavity-volume Lagrange multiplier produced by the Holzapfel-Ogden material with the prescribed active tension. These are two independent mechanical descriptions of the same chamber, anchored to the same physiological scale but not to each other.

The walk-through that follows uses the mid-pressure case (sPAP60, achieved peak RV systolic 66 mmHg coupled) to make the residual concrete. The standalone 0D calibration runs the circulation model on its own for thirty beats and settles into a periodic state ({numref}`fig-standalone-convergence`). The first few beats are pure warm-up — visible as the lightest, wildest curves in the figure — and they are harmless: the optimizer's cost function scores parameters only on last-beat metrics, and only the converged state is handed to the coupled mechanics solve. What matters is that the calibrated elastance and Klotz passive curve dictate a clean limit cycle once initial transients have decayed.

```{figure} ../figures/fig_4_6_standalone_convergence.png
:name: fig-standalone-convergence
:width: 95%

Standalone 0D pressure-volume convergence for the mid-pressure case (sPAP60, achieved peak RV systolic 66 mmHg coupled). Each of the thirty pre-coupling beats is plotted, coloured by beat order (light = early, dark = late) with the converged last beat drawn bold (LV blue, RV red). The wild early curves are pre-convergence warm-up — they are not part of what the optimizer scores or what the coupled solve uses downstream.
```

When the FEM takes over, the converged coupled limit cycle is not the same as the standalone one ({numref}`fig-coupling-jump`). The LV loop changes modestly because the LV is calibrated to the same end-diastolic mesh volume and a stable systemic load, so the Holzapfel-Ogden cavity pressure follows the standalone limit cycle closely (peak pressure $117\to110$ mmHg). The RV operating point shifts more in the same case (peak $59\to66$ mmHg, end-diastolic volume $78\to95$ mL), because the same FE wall is now responding to the imposed pulmonary load through its actual constitutive law rather than through the lumped elastance.

```{figure} ../figures/fig_4_7_coupling_jump.png
:name: fig-coupling-jump
:width: 95%

Operating-point shift between converged standalone and coupled limit cycles (sPAP60). Standalone 0D last beat (grey dashed) versus FEM-coupled last beat (bold). The LV loop is nearly coincident; the RV loop shifts in both peak pressure and end-diastolic volume. The transient that takes the system from one limit cycle to the other is shown in {numref}`fig-coupled-convergence`.
```

The coupled simulation reaches that new limit cycle over a few beats ({numref}`fig-coupled-convergence`). Beat one launches from the standalone state — visible as the lightest curve, close to the dashed reference in the figure above — and the system settles toward the bold converged loop within five or six beats. After convergence, the elastance prediction and the cavity Lagrange multiplier sit a few mmHg apart on average over the beat at the same coupled volume trajectory, a small fraction of cumulative cavity work; the per-case breakdown is in {ref}`sec-app-coupling-residual`. Intra-beat agreement is therefore reasonable once the limit cycle is reached, and the residual that matters in practice is the operating-point shift accumulated during the transient.

```{figure} ../figures/fig_4_8_coupled_convergence.png
:name: fig-coupled-convergence
:width: 95%

FEM-coupled pressure-volume convergence for the mid-pressure case (sPAP60). Each curve is one of the coupled beats, plotted with the FEM cavity Lagrange-multiplier pressure paired with the 0D-side volume, coloured by beat order with the last beat drawn bold (LV blue, RV red). The coupled system reaches a new periodic state within a few beats.
```

The pattern holds across the sweep ({numref}`fig-all-16-pre-post`). The LV loop stays close to its standalone reference in every case, while the RV operating point shifts substantially in the mid- and high-pressure cases — by 10--20 mmHg in peak pressure at the severe end. The proxy analysis uses the achieved coupled pressures and volumes; the standalone references shown here are for diagnostic comparison only.

```{figure} ../figures/fig_4_9_all_16_pre_post.png
:name: fig-all-16-pre-post
:width: 100%

Standalone 0D versus FEM-coupled pressure-volume loops across all sixteen sweep cases, ordered by achieved peak RV systolic pressure (FEM, coupled). Standalone loops (light dashed) are the last beat of the standalone 0D pre-run; coupled loops (solid) pair the FEM cavity Lagrange-multiplier pressure with the coupled cavity volume. The LV loop stays close to its standalone reference in every case; the RV operating-point shift grows with imposed pressure.
```

Two consequences for the rest of the thesis. First, all work calculations use the solver Lagrange-multiplier pressure rather than the 0D elastance pressure, since the multiplier is what acts on the variational boundary. Second, the `sPAP*` case names are calibration shorthand for the standalone-targeted RV systolic pressure, not for the achieved coupled value; the pressure axes, correlations, and proxies in {ref}`chap-results` use the coupled-achieved pressures directly, so this shift does not propagate into the proxy comparison.

## Interpretation Limits

The fixed-geometry design is the main limitation of the sweep. The 0D model can raise RV pressure and filling pressure, but it cannot thicken the RV wall, change septal curvature, or assign pressure-dependent passive remodelling to the finite-element mesh. Those missing adaptations matter most when the calibrated severe cases are unloaded back from end diastole: a high RV end-diastolic pressure applied to the same thin RV anatomy requires a larger inferred prestretch than a remodelled RV would. Capping the RV unloading pressure is therefore a deliberately conservative calibration choice. It bounds the case-to-case variation in inferred unloaded RV that an uncapped sweep would produce in the severe cases, but it should not be mistaken for patient-specific RV hypertrophy or material remodelling.

The sweep is therefore appropriate for testing pressure-strain proxy behaviour under a controlled loading path, but the absolute RV and RV-side septal work-density magnitudes at high RV pressure should be read as fixed-anatomy quantities rather than patient-level PAH magnitudes. The calibration is not a diagnostic statement about disease severity; it provides pressure and volume boundary conditions for a controlled mechanics experiment.
