(sec-active-contraction)=
# Active Contraction

The active-stress form used in {ref}`sec-total-stress-active` is

$$
\mathbf{S}_\text{active} = T_a(t)\,(\mathbf{f}_0\otimes\mathbf{f}_0).
$$

This section defines the scalar active tension $T_a(t)$. Biologically, $T_a$ represents the force-generating action of the sarcomeres, the molecular motors embedded within each muscle fibre. Mechanically, it is a prescribed fibre-aligned tension with stress units, reported here in kPa, that turns the passive finite-strain material into an actively contracting myocardium.

The formulation uses an active-stress approximation: activation contributes an additional fibre-aligned stress rather than modelling calcium handling, electrophysiological propagation, or crossbridge dynamics explicitly {cite}`ambrosi2012active`.

## Activation Timing and the Blanco Model

The active tension $T_a$ is a function of time within the cardiac cycle, rising from zero at the onset of systole, reaching a peak, and then decaying as the cardiomyocytes relax. The temporal profile used in this simulation follows the Blanco ventricular activation model {cite}`blanco2010computational`, which parameterizes the activation waveform by three quantities: the time of onset $t_C$, the duration of the contraction phase $T_C$, and the duration of the relaxation phase $T_R$. The waveform rises smoothly from zero during the contraction phase, reaches a peak at $T_a^\text{max}$, and decays back to zero during the relaxation phase, after which it remains at zero through the diastolic filling interval. {numref}`fig-blanco-activation` shows two cycles of the waveform using the production timing convention, with the contraction and relaxation segments highlighted.

The normalized activation waveform is

$$
a(t) =
\begin{cases}
\frac{1}{2}\left[1-\cos\left(\frac{\pi(t-t_C)}{T_C}\right)\right],
& t_C \le t < t_C+T_C, \\[6pt]
\frac{1}{2}\left[1+\cos\left(\frac{\pi(t-t_C-T_C)}{T_R}\right)\right],
& t_C+T_C \le t < t_C+T_C+T_R, \\[6pt]
0, & \text{otherwise},
\end{cases}
$$

and the active tension is $T_a(t)=T_a^\text{max}a(t)$.

```{figure} ../figures/fig_2_9_blanco_activation.png
:name: fig-blanco-activation
:width: 80%

The Blanco activation function $a(t)$ over two cardiac cycles using the production timing convention. The waveform is a piecewise cosine that rises from zero during the contraction phase of duration $T_C$ (pink), reaches a peak of unity, and decays during the relaxation phase $T_R$ (blue), remaining at zero through the rest of the cycle. In the simulations reported here, both ventricles and the septum use the same normalized waveform with $t_C=0$, $T_C=0.25$ s, $T_R=0.40$ s, and a common peak active tension of 100 kPa.
```

All production simulations use a fixed cardiac clock rather than a fitted heart rate. The heart rate is set to 75 beats per minute, giving an RR interval of 0.8 s. Because the finite-element mesh represents the end-diastolic configuration, ventricular activation is aligned with the start of the simulated beat by setting $t_C=0$. The contraction and relaxation durations are then held fixed at $T_C=0.25$ s and $T_R=0.40$ s, leaving the rest of the cycle for diastolic filling. These values are part of the fixed mechanics model, not parameters retuned across the pressure sweep.

## Spatial Assignment of Active Tension

Active tension is stored by anatomical region, so the LV free wall, septum, and RV free wall can in principle be assigned different peak amplitudes. In the simulations reported here, however, the peak active tension is held fixed at 100 kPa in all three regions. This choice keeps the contractile drive from becoming an additional region-specific tuning parameter: the different LV and RV pressure regimes then arise from geometry, boundary conditions, material response, and circulatory loading rather than from prescribing a lower RV myocardial tension.

Within each region, the same normalized Blanco waveform is used, so activation timing is spatially synchronous in the present model. Activation heterogeneity is therefore outside the scope of the pressure-loading and pressure-assignment tests.
