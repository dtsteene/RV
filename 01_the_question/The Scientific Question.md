# The Scientific Question

The previous chapter argued that mechanical work is the natural currency linking what the heart does mechanically to what it costs metabolically, that the tensor volume integral $\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,d\mathbf{X}$ and the cavity $\oint P\,dV$ describe the same quantity at different resolutions, and that the clinical pressure-strain proxy carries Suga's construction from the whole chamber down to the segment by substituting a scalar chamber pressure for the full stress tensor. It also pointed to the regions where that framework has not been computationally tested: the right ventricle as a whole, whose regional mechanics have received far less attention than the left, and within it the wall it shares with the left ventricle, where the proxy's pressure assumption is genuinely ambiguous. This chapter states the question formally. The two work quantities are defined, the identity connecting the tensor integral to the chamber-level pressure-volume work is derived, and the hypothesis under test is posed as a well-defined comparison.

The ground-truth quantity against which the proxies are compared is the internal mechanical work computed directly from the stress and strain tensor fields of the finite element simulation. Let $\Omega$ denote the reference-configuration biventricular myocardial domain, and let $\Omega_j \subseteq \Omega$ be a reference-configuration subregion (a free-wall region or the septum). Following Finsberg et al. {cite}`finsberg2019assessment`, the total internal work in $\Omega_j$ over a cardiac cycle is

$$
W_\text{int}[\Omega_j] = \int_0^T \int_{\Omega_j} \mathbf{S}(t, \mathbf{X}) : \dot{\mathbf{E}}(t, \mathbf{X}) \, d\mathbf{X} \, dt,
$$

where $\mathbf{S}$ is the second Piola-Kirchhoff stress tensor, $\mathbf{E}$ is the Green-Lagrange strain tensor, and the colon denotes the double contraction $\mathbf{S} : \dot{\mathbf{E}} = S_{ij} \dot{E}_{ij}$. In discrete form, sampling the simulation at $N+1$ snapshots $t_0, t_1, \ldots, t_N$ over the cycle and applying the trapezoidal rule,

$$
W_\text{int}[\Omega_j] \approx \sum_{i=1}^{N} \int_{\Omega_j} \bar{\mathbf{S}}(t_i, \mathbf{X}) : d\mathbf{E}(t_i, \mathbf{X}) \, d\mathbf{X},
$$

with $\bar{\mathbf{S}}(t_i) = \tfrac{1}{2}(\mathbf{S}(t_i) + \mathbf{S}(t_{i-1}))$ the average stress and $d\mathbf{E}(t_i) = \mathbf{E}(t_i) - \mathbf{E}(t_{i-1})$ the strain increment at step $i$.

An identity connects this field-level integral to the chamber-level pressure-volume work. Taken over the whole biventricular myocardium and in the quasi-static limit that applies at cardiac timescales, the integral $\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,d\mathbf{X}$ equals the sum of the two chamber-level pressure-volume rates plus any traction work on non-cavity boundaries, and under idealized boundary conditions in which the epicardium is free and the basal ring is clamped it collapses over one cardiac cycle to

$$
\int_0^T \!\! \int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,d\mathbf{X}\,dt \;=\; \oint P_\text{LV}\,dV_\text{LV} \;+\; \oint P_\text{RV}\,dV_\text{RV}.
$$

This is the mathematical content of the informal statement, made in the introduction, that the tensor and the chamber-level forms of cardiac work describe the same quantity at different resolutions: the cavity loops are the boundary reading of the internal field. The identity is stated in signed form: with the normal convention adopted below (outward normal of the solid, pointing into the cavity), the rate $P\dot V$ is negative during chamber ejection and positive during filling, and the positive stroke-work magnitude traditionally reported in cardiology is $-\oint P\,dV$. The signed form is used throughout the derivation and in all comparisons between tensor work and cavity work that follow.

The derivation takes three steps. First, from the kinematic definition $\dot{\mathbf{E}} = \tfrac{1}{2}(\dot{\mathbf{F}}^T\mathbf{F} + \mathbf{F}^T\dot{\mathbf{F}})$, the symmetry of $\mathbf{S}$, and the relation $\mathbf{P} = \mathbf{F}\mathbf{S}$ between the second and first Piola-Kirchhoff stresses, a direct index calculation gives the pointwise identity $\mathbf{S}:\dot{\mathbf{E}} = \mathbf{P}:\dot{\mathbf{F}}$. The second form is the useful one, because $\dot{\mathbf{F}} = \nabla_\mathbf{X}\mathbf{v}$ is a material gradient of the velocity $\mathbf{v} = \dot{\mathbf{x}}$ that integration by parts will turn into a boundary term. Second, in the quasi-static limit — an accurate approximation for the myocardium at physiological timescales — the reference-configuration momentum balance reduces to $\text{Div}\,\mathbf{P} = \mathbf{0}$; taking the inner product with $\mathbf{v}$, integrating over $\Omega$, and applying the divergence theorem gives the classical virtual-work identity,

$$
\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,d\mathbf{X} \;=\; \int_{\partial\Omega} \mathbf{t}_0 \cdot \mathbf{v}\,dA \;=\; \int_{\partial\omega} \mathbf{t}\cdot\mathbf{v}\,da,
$$

where $\mathbf{t}_0 = \mathbf{P}\mathbf{N}$ is the nominal traction per unit reference area on the reference boundary $\partial\Omega$, and $\mathbf{t}$ is the Cauchy traction per unit current area on the deformed boundary $\partial\omega$. The two surface integrals coincide because Nanson's formula equates $\mathbf{t}_0\,dA = \mathbf{t}\,da$: the same physical force on the same material element, parameterized by either the reference or the current patch. The volume integral of internal stress power equals the surface integral of external traction power.

The third step specializes this to the heart. The deformed boundary $\partial\omega$ splits into two endocardial surfaces $\Gamma_\text{endo}^\text{LV}$ and $\Gamma_\text{endo}^\text{RV}$, an epicardial surface $\Gamma_\text{epi}$, and a basal ring $\Gamma_\text{base}$, all taken in the current configuration where the pressure load is naturally expressed. On each endocardium the cavity pressure acts as a spatially uniform follower load with Cauchy traction $\mathbf{t} = -P\mathbf{n}$, where $\mathbf{n}$ is the outward unit normal of the deformed solid, and the rate of work contributed by that surface factors as

$$
\int_{\Gamma_\text{endo}} \mathbf{t}\cdot\mathbf{v}\,da \;=\; -P \int_{\Gamma_\text{endo}} \mathbf{v}\cdot\mathbf{n}\,da \;=\; P\,\dot V,
$$

where the second equality is the kinematic statement $\dot V = -\int_{\Gamma_\text{endo}}\mathbf{v}\cdot\mathbf{n}\,da$: wall motion in the $+\mathbf{n}$ direction — outward from the solid, into the cavity — reduces the enclosed cavity volume. The endocardial surface integral collapses to the scalar product of chamber pressure and rate of volume change. Collecting all four surface contributions,

$$
\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,d\mathbf{X} \;=\; P_\text{LV}\,\dot V_\text{LV} \;+\; P_\text{RV}\,\dot V_\text{RV} \;+\; W_\text{epi} \;+\; W_\text{base},
$$

with $W_\text{epi}$ and $W_\text{base}$ the traction-velocity integrals on the remaining surfaces. The basal ring is Dirichlet-clamped, so $\mathbf{v} = \mathbf{0}$ there and $W_\text{base}$ vanishes exactly. A fully free epicardium would contribute nothing either, and integrating the result over one cardiac cycle recovers the cyclic identity stated at the outset. In the actual simulation the epicardium is supported by Robin-type springs to prevent rigid-body motion, for reasons set out in the next chapter, and the mechanical energy absorbed by those springs enters $W_\text{epi}$. Any numerical gap between the field-level and the chamber-level work, when both are evaluated from the same run, is accounted for in that term; the residual is examined in Chapter 5. [Figure @fig-energy-balance](#fig-energy-balance) shows this identity closing in practice on the UKB synthetic baseline: the tensor integral and the sum of cavity work and Robin boundary work overlap throughout the cycle, with a final-time residual of order $10^{-5}$ J (relative error $\sim 10^{-4}$), which is the discretization noise floor of the trapezoidal accumulation rather than a physical discrepancy.

```{figure} ../figures/fig_energy_balance_validation.png
:name: fig-energy-balance
:width: 85%

Numerical verification of the energy-balance identity. The cumulative tensor stress power $\int_0^t\!\!\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,d\mathbf{X}\,dt'$ (red) and the sum of cavity pressure-volume work and Robin boundary work (black dashed) overlap throughout the cycle. The cavity contribution alone (blue) departs from the internal work during systole; the difference is exactly the mechanical energy absorbed by the Robin springs (green). UKB synthetic baseline, final beat of a six-beat sequence; final-time residual $4.8 \times 10^{-5}$ J ($7 \times 10^{-5}$ relative).
```

One further point is worth making explicit before introducing the proxy. The identity derived above is a whole-heart identity: it binds the internal stress power integrated over the entire biventricular myocardium to the chamber-level loop areas of the two cavities, up to the non-cavity boundary terms. No exact analogue exists for an arbitrary subregion $\Omega_j$ on its own, because a subregion has material interfaces with its neighbours across which tractions do work internally; the internal virtual work over $\Omega_j$ is not, in general, the pressure-volume work of a single chamber. The regional pressure-strain quantity introduced next is therefore motivated by the global relation, not derived as a local version of it, and by the pragmatic fact that regional pressure and strain are the clinically accessible inputs.

The proxy itself is inspired by the clinical pressure-strain index {cite}`russell2012novel`. Because chamber pressure and regional strain along a single axis are what is measurable non-invasively, the proxy operates not on the full double contraction $\mathbf{S}:d\mathbf{E}$ but on one scalar component of it. The fiber-direction projections $S_{ff} = \mathbf{S}:(\mathbf{f}_0 \otimes \mathbf{f}_0)$ and $dE_{ff} = d\mathbf{E}:(\mathbf{f}_0 \otimes \mathbf{f}_0)$ isolate the fiber-normal term $S_{ff}\,dE_{ff}$ of the full contraction, discarding the cross-fiber normal and the shear contributions that also enter the internal work. The pressure-strain approximation then substitutes a chamber pressure for the stress component $S_{ff}$. For a region $\Omega_j$, the resulting pressure-strain work is

$$
W_\text{PS}[\Omega_j] \approx \bar{V}_j \sum_{i=1}^{N} \bar{P}_j(t_i) \, dE_{ff,j}(t_i),
$$

where $\bar{V}_j$ is the reference volume of the region, $dE_{ff,j}$ is the volume-averaged fiber strain increment, and $P_j$ is a chamber pressure assigned to represent the mechanical load on that region. For the free wall of either ventricle the assignment is unambiguous: the LV free wall is loaded by $P_\text{LV}$, the RV free wall by $P_\text{RV}$. For the interventricular septum, loaded simultaneously by both cavities, the assignment is not unambiguous, and which choice yields the most faithful proxy is one of the questions under investigation. Three candidates are natural: $P_\text{LV}$ alone, which is the current clinical default; $P_\text{RV}$ alone, which would be the symmetric counterpart to the RV free-wall assignment; and the transmural pressure difference $P_\text{LV} - P_\text{RV}$, which captures the net pressure drop across the septal wall.

The pressure-strain proxy is the final rung of a cascade of simplifications from the full tensor integral — each rung dropping a physically distinct contribution to the internal work. [Figure @fig-cascade](#fig-cascade) shows the cascade on the UKB synthetic baseline, for the LV and RV as whole chambers. The gap between the full contraction $\mathbf{S}:\dot{\mathbf{E}}$ (black) and the fiber-normal term $S_{ff}\,\dot E_{ff}$ (green) is the cross-fiber and shear work; the gap between fiber-stress and chamber-pressure (green to blue) is the pressure-for-stress substitution; the gap between fiber-strain and longitudinal-strain (blue to red) is the strain-component reduction that follows from the clinical echocardiographic measurement. Each simplification loses quantitatively more than the one before it, and the final clinical proxy recovers roughly a fifth of the full tensor work in the LV and a tenth in the RV on this baseline case. The septum — a shared wall that does not even exist as its own region in the whole-chamber decomposition shown here — is where the pressure-for-stress step becomes genuinely ambiguous, and it is the focus of Chapter 5.

```{figure} ../figures/fig_cascade_cumulative.png
:name: fig-cascade
:width: 95%

Cascade of work measures from the full tensor integral down to the clinical pressure-strain proxy, shown per unit region volume on the UKB synthetic baseline. $\mathbf{S}:\dot{\mathbf{E}}$ is the full double contraction; $S_{ff}\,\dot E_{ff}$ is the fiber-normal component alone; $P_\text{cav}\,\dot E_{ff}$ substitutes cavity pressure for the fiber stress; $P_\text{cav}\,\dot\varepsilon_{ll}$ is the clinical pressure-longitudinal-strain proxy. Cumulative values at end of cycle are shown in the legend. Quantities are shown for the LV and RV as whole chambers; the septum is introduced as its own region in Chapter 5.
```

The scientific question has two parts. Across the biventricular myocardium — and in particular for the right ventricle, whose regional work has not previously been validated computationally against a tensor ground truth — how faithfully does $W_\text{PS}[\Omega_j]$ track $W_\text{int}[\Omega_j]$ in each region? And for the interventricular septum specifically, which of the three candidate pressures — $P_\text{LV}$, $P_\text{RV}$, or $P_\text{LV} - P_\text{RV}$ — produces the closest agreement with the tensor work? In both cases, does the answer depend on whether the cavity pressures sit in their healthy physiological balance or in a state of right-ventricular pressure overload?

The hypotheses motivating the study follow the same two-part structure. In healthy physiology, the proxy is expected to behave in the RV much as Finsberg et al. found in the LV — capturing relative regional trends while underestimating absolute magnitudes — and for the septum all three pressure candidates should perform similarly, since $P_\text{RV}$ is small relative to $P_\text{LV}$ and the transmural pressure is nearly identical to the LV pressure. In pulmonary arterial hypertension both expectations shift. The RV operates in a loading regime its free-wall architecture is not adapted for, so the proxy-tensor relationship on the RV side is itself worth re-examining; and the septum bears a transmural pressure that is no longer well approximated by $P_\text{LV}$ alone, so the transmural choice should outperform the LV pressure as a septal proxy because it is the only candidate that accounts for the opposing load that elevated RV pressure places on the RV face of the septum.

Answering this question requires a model that simultaneously produces physiologically realistic cavity pressures and volume dynamics for both ventricles — which a stand-alone zero-dimensional circulation model can provide — and resolves the stress and strain fields inside the tissue throughout the cardiac cycle — which only a spatially resolved three-dimensional mechanics model can achieve. The coupled finite element and circulation framework described in the following chapter is built specifically to provide both.
