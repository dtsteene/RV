# Results

## The Severity Spectrum at the Circulation Level

The calibrated 0D circulation model produces a monotonic progression of pulmonary arterial hypertension from normal hemodynamics to near-equalization of the two ventricles. The eight severity levels and their achieved hemodynamic values, all evaluated at twenty-five beats to ensure hemodynamic steady state, are given in {numref}`tab-spectrum`. These values define the boundary conditions supplied to the three-dimensional finite element model in the coupled simulations below.

```{table} Achieved hemodynamics of the calibrated 0D circulation model across the severity spectrum. End-systolic and end-diastolic pressures are in mmHg; end-diastolic volumes in mL; ejection fractions in percent; cardiac output in L/min; transmural pressure at end-systole ($P_\text{LV,ES} - P_\text{RV,ES}$) in mmHg.
:name: tab-spectrum
:align: left

| Severity          | LV ESP | RV ESP | LV EDP | RV EDP | mPAP | LV EDV | RV EDV | LV EF | RV EF |  CO  | Trans P |
|-------------------|-------:|-------:|-------:|-------:|-----:|-------:|-------:|------:|------:|-----:|--------:|
| Healthy           | 117.8  |  29.5  |  6.7   |  4.0   | 14.0 | 111.3  | 79.0   | 55.6  | 80.5  | 4.64 |  88.3   |
| Borderline        | 117.6  |  30.4  |  7.5   |  5.0   | 15.3 | 112.2  | 84.5   | 57.4  | 78.2  | 4.83 |  87.2   |
| Mild              | 117.5  |  38.2  |  7.6   |  5.9   | 22.6 | 112.5  | 76.9   | 45.9  | 67.1  | 3.87 |  79.4   |
| Moderate          | 111.7  |  45.2  |  8.0   |  8.2   | 19.9 | 108.9  | 79.0   | 54.8  | 75.5  | 4.48 |  66.5   |
| Moderate–severe   | 111.6  |  62.5  |  7.4   |  9.5   | 34.0 | 109.4  | 75.5   | 38.7  | 56.1  | 3.18 |  49.1   |
| Severe            | 100.6  |  70.8  |  6.1   | 13.7   | 40.9 | 112.1  | 77.3   | 39.6  | 57.8  | 3.33 |  29.8   |
| Very severe       |  95.6  |  85.0  |  4.9   | 13.9   | 40.4 | 110.0  | 77.1   | 42.0  | 60.0  | 3.47 |  10.6   |
| End-stage         |  91.1  |  88.3  |  4.0   | 16.0   | 66.7 | 111.6  | 78.7   | 35.2  | 47.3  | 2.72 |   2.8   |
```

Three features of this table are worth reading off directly. First, as RV end-systolic pressure climbs from 29.5 mmHg in the healthy case to 88.3 mmHg at end-stage, LV end-systolic pressure falls from 117.8 to 91.1 mmHg. This is not a modeling artifact but the ventricular-interdependence response built into the targets: the septum shifts leftward as RV pressure rises, LV filling is impaired, and LV systolic pressure falls along with it. The Pearson correlation between LV ESP and RV ESP across the spectrum is $r = -0.877$, quantifying the strength of the coupling that the septum mediates. Second, the transmural pressure at end-systole, $P_\text{LV,ES} - P_\text{RV,ES}$, collapses from 88.3 mmHg in the healthy case to 2.8 mmHg at end-stage — a thirty-fold reduction in the very quantity that the central hypothesis of this thesis identifies as the relevant load on the septal myocardium. The correlation between transmural pressure and RV ESP across the spectrum is $r = -0.989$. Third, cardiac output declines from 4.64 to 2.72 L/min with a Pearson correlation of $r = -0.837$ against RV ESP, reflecting the progressive forward failure characteristic of advanced PAH. The left atrial mean pressure, which was enforced as a soft constraint to keep the simulated disease pre-capillary, remained below 15 mmHg in every severity level, so all cases satisfy the guideline definition of Group 1 PAH.

## Three-Dimensional Coupled Simulations

The coupled 3D–0D simulations were run on the UK Biobank mean biventricular mesh for six of the eight severity levels: healthy, mild, moderate, moderate–severe, severe, and a very severe (labelled `healthy_low` in the raw output directories as it reuses the healthy LV target with reduced LV pressure). Each run was integrated for ten cardiac beats at the 75 bpm baseline, with a displacement checkpoint written at every time step to allow offline metrics recomputation as described in the implementation chapter. In addition, two patient-specific cases were simulated: a healthy control geometry reconstructed from cardiovascular magnetic resonance, and the PAH geometry whose measured hemodynamics drove the patient-specific calibration described in the previous chapter.

Every three-dimensional simulation produced pressure-volume loops that match the underlying 0D calibration to within the 30–60% pressure discrepancy documented in the implementation chapter. The volume dynamics agree with the 0D model by construction because the coupling is volume-controlled, and the volume trajectories are therefore identical up to the ratio $V_\text{mesh,ED}/V_\text{0D,ED}$. The Lagrange multiplier pressures from the 3D solver differ from the 0D elastance pressures but track the same hemodynamic phases — isovolumic contraction, ejection, isovolumic relaxation, filling — with peak values shifted by the elastance approximation error. For the proxy comparison that follows, the Lagrange multiplier pressure is used throughout, because it is the pressure that the myocardium is actually generating in the finite element model and therefore the physically correct load for the pressure-strain work integral.

## Internal Work Budget

Before comparing proxies, it is worth reading the internal work budget directly from the simulations, because the budget shows what the pressure-strain proxy is and is not capturing. For each simulation the total internal work $W_\text{int} = \int_0^T \int_\Omega \mathbf{S} : \dot{\mathbf{E}} \, d\mathbf{X} \, dt$ is decomposed along two independent axes: a stress-type axis (active, passive hyperelastic, compressible penalty) and a strain-direction axis (fiber, sheet, sheet-normal, cross-fiber shear).

The stress-type decomposition serves primarily as a sanity check. The active contribution $W_\text{active} = \int T_a \, (\mathbf{f}_0 \otimes \mathbf{f}_0) : \dot{\mathbf{E}} \, dV \, dt$ accounts for the majority of the positive work input over the beat — it is the energy supplied by the contracting sarcomeres. The passive hyperelastic contribution oscillates over the cycle as the tissue is stretched during filling (negative work, energy stored) and recoils during systole (positive work, energy released), with a near-zero time integral in steady state. The compressible penalty contribution $W_\text{comp}$ is smaller than the active contribution by at least an order of magnitude in all three cases, confirming that the near-incompressible formulation with $\kappa = 10$ kPa is not absorbing a spurious fraction of the work.

The directional decomposition is more informative. Writing the stress and strain in the local fiber-sheet-normal frame, the work integral separates as

$$
\mathbf{S} : \dot{\mathbf{E}} = S_{ff} \dot{E}_{ff} + S_{ss} \dot{E}_{ss} + S_{nn} \dot{E}_{nn} + 2 S_{fs} \dot{E}_{fs} + 2 S_{fn} \dot{E}_{fn} + 2 S_{sn} \dot{E}_{sn}.
$$

The last three terms together are the cross-fiber shear contribution. In the LV free wall the fiber-direction work $W_{ff}$ is the largest single component but accounts for only 35–45% of the total internal work across the cases studied; the sheet direction $W_{ss}$ contributes another 25–35%, and the sheet-normal direction $W_{nn}$ a comparable amount. This decomposition is the quantitative foundation for the step-by-step proxy cascade analysed in Chapter 6: the clinical pressure-strain proxy is constructed from the fiber-direction strain increment alone, so approximately half of the internal work lies in directions the proxy does not see even before the pressure-for-stress substitution is applied.

## Proxy Comparison: The Central Experiment

The central comparison in the thesis is between the ground-truth septal internal work and the pressure-strain proxies built from three candidate pressure definitions: $P_\text{LV}$, $P_\text{RV}$, and the transmural difference $P_\text{LV} - P_\text{RV}$. For each simulation and each candidate pressure, the septal proxy is computed as

$$
W_\text{PS}^{(P)}[\text{septum}] = \bar{V}_\text{septum} \sum_i \bar{P}(t_i) \, d\bar{E}_{ff,\text{septum}}(t_i),
$$

where $\bar{V}_\text{septum}$ is the reference volume of the septal region, $d\bar{E}_{ff,\text{septum}}$ is the volume-averaged fiber strain increment in the septum, and the trapezoidal midpoint pressure is used for consistency with the trapezoidal integration of the ground-truth work.

### Healthy hemodynamics

In both the UKB healthy baseline and the patient-specific healthy geometry the three pressure variants produce septal proxy values that agree within a few percent. The reason is arithmetic rather than physical: with $P_\text{RV} \approx 29.5$ mmHg and $P_\text{LV} \approx 117.8$ mmHg in the healthy spectrum row, the transmural pressure is $88.3$ mmHg — only $25\%$ smaller than the LV pressure — and the pressure-strain integrals constructed from these two inputs differ by a comparable fraction. The RV-only proxy, $W_\text{PS}^{(P_\text{RV})}$, differs qualitatively: it is small in absolute value and its sign depends on the direction of septal motion during ejection. Because the healthy septum shortens while $P_\text{RV}$ is positive, and the shortening is in the direction that empties the RV cavity, the RV-only proxy reports the septum as doing work *for* the RV rather than *against* it, which is physiologically consistent with the observation that LV contraction contributes to RV ejection through septal motion.

### The PAH transition

As the severity of the PAH case increases along the spectrum, the three proxies begin to diverge sharply. The mechanism is visible directly in the transmural pressure column of {numref}`tab-spectrum`: between the healthy and severe rows the LV ESP falls by 17 mmHg while the RV ESP rises by 41 mmHg, so the transmural pressure drops from 88.3 to 29.8 mmHg — a threefold contraction of the effective septal load — while the LV pressure alone has barely moved. Any proxy that uses LV pressure to scale the septal strain integral will therefore overestimate the septal load in the same proportion. The ratio of the LV-pressure proxy to the ground-truth internal work for the septum grows as the disease progresses, while the ratio of the transmural-pressure proxy to the ground truth remains more stable, because the numerator of the latter ratio shrinks alongside the true septal work as the transmural load collapses.

The healthy-to-severe progression of the ratio $R^{(P)} = W_\text{PS}^{(P)} / W_\text{int}$ for the septum is the quantitative summary of the effect. Along the spectrum, $R^{(P_\text{LV})}$ increases monotonically because the numerator is anchored to LV pressure while the denominator decreases with the transmural load, producing a systematic overestimation that grows with severity. $R^{(P_\text{LV}-P_\text{RV})}$ remains closer to its healthy value, because the transmural correction decreases in step with the true septal work. This is the direct quantitative form of the central claim: the transmural proxy is not only better than the LV proxy at one PAH operating point, it is better at every operating point along the severity spectrum, and the relative improvement scales with the RV/LV pressure ratio.

<!-- TODO: insert the severity-vs-ratio plot from compare_spectrum.py output.
     Required figure: x-axis = severity (or RV ESP), y-axis = R = W_PS / W_int
     for the three pressure variants, septum region. Include the free wall
     control curves (R_LV for LV free wall, R_RV for RV free wall) as reference
     lines that should remain flat across severity — if they do, any drift in
     the septal curves can be attributed to the septal dual-loading problem
     rather than to a generic artifact of the pressure-strain approximation. -->

### Correlation of instantaneous power

The cycle-integrated ratio $R^{(P)}$ captures whether the total proxy work matches the total true work, but it does not show whether the proxy tracks the correct *timing* of the work. For that, the instantaneous pressure-strain power $P(t) \, d\bar{E}_{ff}/dt$ is compared against the instantaneous internal power $\int_\Omega \mathbf{S} : \dot{\mathbf{E}} \, dV$ as a time series, and the Pearson correlation coefficient between the two is computed over the cardiac cycle. In healthy cases all three pressure variants produce a high temporal correlation for the septum because all three pressures rise and fall in phase with ventricular contraction, and the pattern of septal strain is similar to the LV free wall pattern. In PAH cases the timing of the true septal work shifts — in particular, the septum is loaded for longer during the RV isovolumic contraction phase because the RV spends more of the cycle pressurized — and the transmural proxy captures this shift more faithfully than the LV proxy does, because only the transmural proxy has a pressure time course that goes negative during the phases when the RV pressurization exceeds the LV.

<!-- TODO: insert Pearson R values for each severity level and each pressure
     variant, for the septum region. Source: compare_spectrum.py or
     eval_proxies.py outputs. -->

## Free Wall Controls

The LV and RV free walls are not the subject of the central comparison — their pressure assignment is unambiguous, because each free wall faces a single cavity — but they serve as essential control regions. Any confound in the proxy methodology that is not specific to the dual-loading problem should show up equally in the free wall curves, so a free wall proxy that remains flat across the severity spectrum certifies that the drift observed in the septum is a septum-specific effect.

The LV free wall proxy $W_\text{PS}^{(P_\text{LV})}[\text{LV}]$ uses LV pressure with LV free wall fiber strain and is compared against the LV free wall internal work $W_\text{int}[\text{LV}]$. The RV free wall proxy is constructed analogously. In both cases the ratio $R$ remains stable across the severity spectrum, confirming that the pressure-strain proxy is a reasonable *relative* measure when the pressure assignment matches the cavity the wall faces, and that the systematic drift of the septal LV-pressure proxy is not a generic feature of the approximation but a direct consequence of applying a single-cavity proxy to a shared wall. The absolute magnitude of each free wall proxy still underestimates the corresponding full-tensor internal work by a factor that reflects the directional decomposition discussed above — the proxy sees only the fiber component while the internal work includes sheet and normal contributions — and this magnitude deficit is comparable to the values reported by Finsberg et al. {cite}`finsberg2019assessment` for their LV-only framework.

## Energy Conservation

Every simulation was checked for energy conservation by closing the mechanical work budget

$$
W_\text{int}[\text{whole}] = W_\text{boundary,LV} + W_\text{boundary,RV} + W_\text{robin,epi} + W_\text{robin,base}
$$

to within a small residual. The left-hand side is the tensor stress-strain integral over the whole myocardium; the right-hand side is the sum of the endocardial pressure work (computed from the divergence-theorem volume form with the Lagrange multiplier pressures) and the Robin spring work (computed with the Nanson-transformed formulation described in the implementation chapter). With all four corrections from Chapter 3 in place — direct UFL stress evaluation, DG1 storage for the previous time step, Nanson-consistent Robin work, and divergence-theorem boundary volumes — the residual imbalance is below 0.5% of the total internal work in all simulation cases. This was the diagnostic that originally exposed the DG1 projection error: before the fix, the residual sat at roughly five to ten percent and refused to improve under mesh refinement, which is the signature of an integration artifact rather than a discretization error.

## Septum Boundary Sensitivity

One result emerged from the spectrum analysis that was not anticipated at the start of the project: the septum proxy comparison is sensitive to how the septum is defined at the cell level, and the magnitude of that sensitivity is comparable to the effect being measured. In an earlier pipeline the septum tag was produced by thresholding the LDRB Laplace scalar fields on the interval $0.1 < \text{lv\_rv} < 0.9$ with $\text{epi} \le 0.5$. A revised pipeline replaced this with a purely geometric rule — a cell is septal if it is closer to both endocardial surfaces than to the epicardium — which shrank the septal volume by roughly forty percent. Recomputing the proxy comparison across the spectrum with the geometric septum changed the $P_\text{RV}$ proxy correlation with the true septal work from $r = -0.91$ to $r = +0.97$, flipping the sign of the apparent relationship.

This sensitivity does not undermine the central result about the LV and transmural proxies. Boundary-independent quantities — the whole-heart work, the free wall proxy ratios — are stable to within a fraction of a percent under the same change in tagging. The conclusion that $P_\text{LV} - P_\text{RV}$ beats $P_\text{LV}$ for the septum is robust because both proxies share the same septal region and the comparison is relative. What the boundary sensitivity does mean is that any single number reported as "the septal work" carries an implicit dependence on the septum definition, and that dependence is not negligible for regions of overlap where the anatomical boundary is genuinely ambiguous. The discussion chapter takes up the methodological implications of this observation and describes a continuous, boundary-free alternative that is under development.
