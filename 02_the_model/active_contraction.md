# Active Contraction

The mechanics section introduced the active-stress form used in the equilibrium problem,

$$
\mathbf{S}_\text{active} = T_a(t)\,(\mathbf{f}_0\otimes\mathbf{f}_0).
$$

This section defines the scalar active tension $T_a(t)$. Biologically, $T_a$ represents the force-generating action of the sarcomeres, the molecular motors embedded within each muscle fibre. Mechanically, it is a prescribed fibre-aligned tension with stress units, reported here in kPa, that turns the passive finite-strain material into an actively contracting myocardium.

The active contribution is deliberately simple. It captures the dominant mechanical effect of myocardial activation — tension along the fibre direction — without modelling calcium handling, electrophysiological propagation, or crossbridge dynamics explicitly.

## Activation Timing and the Blanco Model

The active tension $T_a$ is a function of time within the cardiac cycle, rising from zero at the onset of systole, reaching a peak, and then decaying as the cardiomyocytes relax. The temporal profile used in this simulation follows the Blanco ventricular activation model {cite}`blanco2010computational`, which parameterizes the activation waveform by three quantities: the time of onset $t_C$, the duration of the contraction phase $T_C$, and the duration of the relaxation phase $T_R$. The waveform rises smoothly from zero during the contraction phase, reaches a peak at $T_a^\text{max}$, and decays back to zero during the relaxation phase, after which it remains at zero through the diastolic filling interval. {numref}`fig-blanco-activation` shows two cycles of the waveform using the production timing convention, with the contraction and relaxation segments highlighted.

```{figure} ../figures/fig_2_9_blanco_activation.png
:name: fig-blanco-activation
:width: 80%

The Blanco activation function $a(t)$ over two cardiac cycles using the production timing convention. The waveform is a piecewise cosine that rises from zero during the contraction phase of duration $T_C$ (pink), reaches a peak of unity, and decays during the relaxation phase $T_R$ (blue), remaining at zero through the rest of the cycle. In the simulations reported here, both ventricles and the septum use the same normalized waveform with $t_C=0$, $T_C=0.25$ s, $T_R=0.40$ s, and a common peak active tension of 100 kPa.
```

All production simulations use a fixed cardiac clock rather than a fitted heart rate. The heart rate is set to 75 beats per minute, giving an RR interval of 0.8 s. Because the finite-element mesh represents the end-diastolic configuration, ventricular activation is aligned with the start of the simulated beat by setting $t_C=0$. The contraction and relaxation durations are then held fixed at $T_C=0.25$ s and $T_R=0.40$ s, leaving the rest of the cycle for diastolic filling. These values are part of the fixed mechanics model, not parameters retuned across the pressure sweep.

## Spatial Assignment of Active Tension

The code infrastructure represents active tension on the anatomical regions of the mesh, so the LV free wall, septum, and RV free wall can be assigned different peak amplitudes if a particular calibration requires it. In the simulations reported here, however, the peak active tension is held fixed at 100 kPa in all three regions. This choice keeps the contractile drive from becoming an additional region-specific tuning parameter: the different LV and RV pressure regimes then arise from geometry, boundary conditions, material response, and circulatory loading rather than from prescribing a lower RV myocardial tension.

The zone assignments are still important, even when the peak value is common, because the same cell tags are used throughout the analysis to integrate LV free-wall, RV free-wall, and septal work densities. Within each zone, the same normalized Blanco waveform is used, so the timing of activation is spatially synchronous in the present model.

This approach — region-aware activation storage with a shared waveform and shared peak tension — is a simplification of the physiological electromechanical activation sequence, which propagates as a wave from the apex upward and arrives at different wall segments at slightly different times. In this study, spatially uniform activation timing is treated as part of the model definition rather than as a claim about physiological synchrony. The resulting work fields should therefore be interpreted as a pressure-loading and pressure-assignment test, not as a study of activation heterogeneity.
