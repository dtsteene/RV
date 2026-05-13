(chap-work-question)=
# Mechanical Work and the Scientific Question

This chapter writes down the two work quantities the thesis compares — the stress-strain work density returned by the finite-element model inside the wall, and the pressure-longitudinal-strain proxy used clinically — together with the energy identity that ties them at the whole-heart level. Beyond the definitions, it quantifies how much of the stress-strain work density the proxy retains: a projection and two substitutions reduce the full tensor work density to the clinical proxy, and the drop in retained work density at each step is reported on a baseline case. Most of the magnitude loss arrives at the pressure-for-stress step, while the strain-direction reduction is a smaller correction. The septum is the case where even the pressure-for-stress step is ambiguous, because the tissue is loaded by two cavities and no single scalar pressure follows from the geometry.

(sec-mechanics-notation)=
## Mechanics Notation

Before defining work, the configurations and symbols need to be fixed. The finite-element mechanics are written in a reference-configuration frame. The reference configuration $\mathcal{B}_0$ is the fixed material body used to label points in the mesh; the current configuration $\mathcal{B}_t$ is the deformed body at time $t$. A material point with reference position $\mathbf{X}\in\mathcal{B}_0$ moves to the current position

$$
\mathbf{x}=\boldsymbol{\varphi}(\mathbf{X},t)
=\mathbf{X}+\mathbf{u}(\mathbf{X},t),
$$

where $\mathbf{u}$ is the displacement field ({numref}`fig-reference-current-configuration`).

```{figure} ../figures/fig_intro_reference_current_configuration.png
:name: fig-reference-current-configuration
:width: 85%

Reference and current descriptions of the same deformation. Material points are labelled by their reference coordinates $\mathbf{X}$ on the fixed mesh and move to current coordinates $\mathbf{x}$ as the wall deforms.
```

The deformation gradient

$$
\mathbf{F} = \partial \mathbf{x}/\partial \mathbf{X} = \mathbf{I}+\nabla_{\mathbf{X}}\mathbf{u}
$$

maps infinitesimal reference line elements into the current configuration, and $J=\det\mathbf{F}$ gives the local volume ratio. The right Cauchy-Green tensor and Green-Lagrange strain are

$$
\mathbf{C}=\mathbf{F}^{\top}\mathbf{F},
\qquad
\mathbf{E}=\frac{1}{2}(\mathbf{C}-\mathbf{I}).
$$

Geometrically, $\mathbf{E}$ encodes how lengths of reference line elements change under the deformation. Substituting $d\mathbf{x}=\mathbf{F}\,d\mathbf{X}$ into $|d\mathbf{x}|^2$,

$$
|d\mathbf{x}|^2 - |d\mathbf{X}|^2
= d\mathbf{X}\cdot(2\mathbf{E})\,d\mathbf{X}.
$$

Both inputs to this contraction are reference vectors $d\mathbf{X}$, which is what is meant by saying $\mathbf{E}$ lives on the reference configuration: it acts on objects labelled on $\mathcal{B}_0$. For a unit reference vector $\mathbf{e}$, the projection $\mathbf{e}\cdot\mathbf{E}\,\mathbf{e}$ is positive when the material has stretched along $\mathbf{e}$, negative when it has shortened, and zero when there is no length change in that direction — the construction used later for the longitudinal, fibre, sheet, and sheet-normal strain components.

The rate of Green-Lagrange strain is $\dot{\mathbf{E}}$, where the dot denotes a material time derivative at fixed $\mathbf{X}$. The second Piola-Kirchhoff stress $\mathbf{S}$ is the corresponding stress measure on the reference configuration, determined by the material law. The finite-strain mechanics and constitutive law are developed in {ref}`sec-3d-mechanics`.

(sec-work-definitions)=
## Local Work and the Pressure-Strain Proxy

The local rate of mechanical work in a deforming material is the tensor contraction $\mathbf{S}:\dot{\mathbf{E}}$, where $\mathbf{S}$ is the second Piola-Kirchhoff stress and $\dot{\mathbf{E}}$ is the rate of the Green-Lagrange strain. Because both tensors are written on the reference configuration, their contraction gives the stress power per unit reference volume — the rate at which mechanical energy is expended in a small piece of the wall, with units Pa/s, equivalent to J m$^{-3}$ s$^{-1}$ {cite}`holzapfel2000nonlinear`. This work-rate density is the model-side quantity that the rest of the chapter integrates and compares against the clinical pressure-strain proxy.

Because $\mathbf{S}:\dot{\mathbf{E}}$ is evaluated point by point, the density can be integrated over any reference-configuration subregion $\Omega_j \subseteq \Omega$ — the LV free wall, the RV free wall, the septum, or the whole myocardium. The internal work over a cardiac cycle is

$$
W_\text{int}[\Omega_j]
= \int_0^T \int_{\Omega_j}
\mathbf{S}(t,\mathbf{X}) : \dot{\mathbf{E}}(t,\mathbf{X}) \, dV_0 \, dt,
$$

where the colon denotes double contraction {cite}`delhaas1994regional,finsberg2017phd`. The regional decomposition used in this thesis comes from changing the integration domain $\Omega_j$ while keeping the definition of work fixed.

In sampled simulation output, the cycle integral is accumulated with a trapezoidal rule,

$$
W_\text{int}[\Omega_j] \approx
\sum_{i=1}^{N}
\int_{\Omega_j}
\bar{\mathbf{S}}(t_i,\mathbf{X}) : \Delta\mathbf{E}(t_i,\mathbf{X}) \, dV_0,
$$

with $\bar{\mathbf{S}}(t_i)=\tfrac{1}{2}(\mathbf{S}(t_i)+\mathbf{S}(t_{i-1}))$ and $\Delta\mathbf{E}(t_i)=\mathbf{E}(t_i)-\mathbf{E}(t_{i-1})$. There is no separate factor of $\Delta t$ in this expression because $\dot{\mathbf{E}}\,dt$ has already been integrated over the timestep as the strain increment $\Delta\mathbf{E}$.

This regional integral has units of energy. A clinical pressure-strain loop carries no regional myocardial volume; pressure times dimensionless strain has pressure units, equivalent to work per volume. The finite-element reference is therefore converted to a work density by dividing by the reference volume of the region,

$$
w_\text{int}[\Omega_j]
= \frac{W_\text{int}[\Omega_j]}{|\Omega_{j,0}|},
\qquad
|\Omega_{j,0}| = \int_{\Omega_j} dV_0.
$$

This $w_\text{int}[\Omega_j]$ is the model-side reference quantity in the thesis: not a patient-level ground truth, but the internally consistent stress-strain work density produced by the chosen geometry, material law, activation, boundary conditions, and circulation coupling.

Strain itself has three anatomical wall directions — longitudinal, circumferential, and radial — and speckle-tracking echocardiography can in principle resolve all three, with tagged cardiac MRI recovering a richer regional strain tensor {cite}`tee2013imaging,voigt2015definitions`. Clinical practice currently endorses only the longitudinal component: in the recent ASE/EACVI consensus {cite}`thomas2025clinical`, radial strain is ruled out for routine use because of poor inter-vendor reproducibility, and circumferential because the published clinical evidence base is too thin. Pressure-strain myocardial-work analysis therefore uses longitudinal strain — how much a segment shortens or lengthens along the long axis — as its deformation input {cite}`russell2012novel,abawi2022noninvasive`.

The pressure-longitudinal-strain proxy lives on the same density scale by construction. For a region $\Omega_j$ with assigned pressure $p_j(t)$ and regional longitudinal strain $\varepsilon_{ll,j}(t)$,

$$
w_{\text{PS},ll}[\Omega_j]
= \int_0^T p_j(t)\,\dot{\varepsilon}_{ll,j}(t)\,dt
= \oint p_j\,d\varepsilon_{ll,j}.
$$

In the sampled simulation output,

$$
w_{\text{PS},ll}[\Omega_j] \approx
\sum_{i=1}^{N}
\bar p_j(t_i)\,\Delta\varepsilon_{ll,j}(t_i),
$$

where $\bar p_j(t_i)=\tfrac{1}{2}(p_j(t_i)+p_j(t_{i-1}))$ and $\Delta\varepsilon_{ll,j}(t_i)=\varepsilon_{ll,j}(t_i)-\varepsilon_{ll,j}(t_{i-1})$. No regional volume factor appears, so the proxy is naturally a density-like index.

Both cycle integrals come out negative under the natural convention because systolic shortening in a loaded direction gives a negative strain increment. We report absolute magnitudes throughout; where a figure or component-balance discussion uses signed values, the caption says so.

The scale difference between cavity pressure and local stress is large in the simulations. Cardiac muscle is strongly anisotropic and the fibre direction carries the dominant active stress in systole {cite}`holzapfel2009constitutive`, so a natural directional candidate for this comparison is the fibre stress $S_{ff}$. In the baseline case, regional mean $S_{ff}$ peaks at about 68 kPa on the LV side and 56 kPa on the RV side, while the corresponding cavity pressures peak at about 16 kPa and 3.9 kPa. The pressure-for-stress substitution is therefore not expected to preserve absolute work-density magnitude.

The longitudinal strain used in the model is a clinical analogue rather than an image-derived measurement. It represents the best-case version of what clinical strain attempts to measure: the apico-basal direction in the wall tangent plane, defined exactly by the geometry rather than estimated from imaging. The pressure-strain proxy is therefore tested with idealized strain inputs, so any failure here points to the mechanical reduction rather than measurement error. The geometry-generation step saves an apex-to-base direction field from the LDRB construction as the `apex_gradient` field. This raw gradient carries a transmural component, but clinical longitudinal strain — measured in long-axis imaging planes that lie approximately tangent to the wall — has no transmural component by construction. During postprocessing this raw apico-basal direction is therefore first projected into the local wall tangent plane, using the endocardium-to-epicardium geometric direction $\mathbf{e}_r$ as the radial direction,

$$
\mathbf{l}_0(\mathbf{X})
=
\frac{
\tilde{\mathbf{l}}(\mathbf{X})
- [\tilde{\mathbf{l}}(\mathbf{X})\cdot\mathbf{e}_r(\mathbf{X})]\mathbf{e}_r(\mathbf{X})
}{
\left\|
\tilde{\mathbf{l}}(\mathbf{X})
- [\tilde{\mathbf{l}}(\mathbf{X})\cdot\mathbf{e}_r(\mathbf{X})]\mathbf{e}_r(\mathbf{X})
\right\|
}.
$$

This standard Gram-Schmidt projection removes the transmural component of the apico-basal field. The regional longitudinal strain $\hat\varepsilon_{ll,j}$ is the volume average of the strain projection $\mathbf{l}_0\cdot\mathbf{E}\,\mathbf{l}_0$ over $\Omega_j$, evaluated relative to the mechanical reference configuration:

$$
\hat\varepsilon_{ll,j}(t)
= \frac{1}{|\Omega_{j,0}|}
\int_{\Omega_j}
\mathbf{l}_0(\mathbf{X}) \cdot
\mathbf{E}(t,\mathbf{X})\,
\mathbf{l}_0(\mathbf{X})\,dV_0.
$$

For the clinical-style pressure-strain signal, the plotted strain is zeroed at the start of the analysed beat, which corresponds to end diastole in the periodic simulation:

$$
\varepsilon_{ll,j}(t)
= \hat\varepsilon_{ll,j}(t)-\hat\varepsilon_{ll,j}(t_\mathrm{ED}).
$$

This subtraction matches the clinical convention that strain is measured relative to the end-diastolic frame. It does not change the pressure-strain loop area, because $w_{\text{PS},ll}$ uses increments $\Delta\varepsilon_{ll,j}$; it only fixes the displayed zero level of the strain trace. The same projection and start-of-beat increment convention are applied per cell during postprocessing. The pressure used in $w_{\text{PS},ll}$ is the solver cavity pressure that enforces the cavity-volume constraint, not the standalone 0D circulation pressure (see {ref}`chap-model` for the coupling).

The pressure assignment is straightforward only in the free walls. The LV free wall is paired with $p_\text{LV}$ and the RV free wall with $p_\text{RV}$. The septum is shared tissue with LV pressure on one face and RV pressure on the other, and assigning one scalar pressure to it is already a mechanical assumption. {numref}`fig-freewall-septum-schematic` shows this asymmetry directly.

```{figure} ../figures/fig_1_2_freewall_septum.png
:name: fig-freewall-septum-schematic
:width: 85%

A free wall (left) is loaded by one cavity pressure; the septum (right) is shared tissue with LV pressure on one face and RV pressure on the other, so its scalar pressure is a choice.
```

For the septum, the tested pressure choices are defined from the two solver cavity pressures and, for the spatially varying choices, from a transventricular coordinate. The one-sided choices are $p_\text{LV}$ and $p_\text{RV}$. The transmural choice is $p_\text{LV}-p_\text{RV}$, the mean choice is $\tfrac{1}{2}(p_\text{LV}+p_\text{RV})$, and the nearest-side choice assigns $p_\text{LV}$ to cells on the LV side and $p_\text{RV}$ to cells on the RV side. The through-wall weighted choice uses a scalar $\lambda(\mathbf{X})$ that is one on the LV side and zero on the RV side, so that

$$
p_\lambda(t,\mathbf{X})
= \lambda(\mathbf{X})p_\text{LV}(t)
+ [1-\lambda(\mathbf{X})]p_\text{RV}(t).
$$

In the reference-tag postprocessing ({ref}`sec-reference-tag-postprocessing`), $\lambda$ is the saved LV-to-RV Laplace scalar — a smooth function from 1 on the LV side to 0 on the RV side, visualized in {numref}`fig-lv-rv-partition`.

The model layers that produce these stress and strain estimates — a transversely isotropic Holzapfel-Ogden passive law with rule-based fibres, prescribed Blanco active tension along $\mathbf{f}_0$, epicardial Robin springs and a partial basal Dirichlet support, two-way coupling to a closed-loop 0D circulation, and an inverse-elasticity prestressing step — are developed in {ref}`chap-model` and {ref}`chap-implementation`. Each affects the stress and strain returned to $w_\text{int}[\Omega_j]$. The model is hyperelastic and uses a nearly-incompressible penalty formulation ($\kappa = 1000$ kPa) rather than strict $J=1$ incompressibility. Activation is uniform with no electrophysiology, the base is clipped, and pericardial support is provided by Robin springs without contact or fluid-structure interaction. The thesis therefore tests the pressure-strain proxy in this scope, not in a fully resolved electromechanical heart-thorax model.

(sec-energy-identity)=
## Energy Identity

The internal stress-strain work and the boundary work done by pressure and supports on the wall are not independent. At the blood-wall interface the same mechanical exchange can be written either as stress-strain power inside the wall or as boundary power on the endocardial surface, where pressure acts through the wall's velocity. Integrated over the whole heart, that boundary power is the cavity pressure-volume work plus the work exchanged with the epicardial and basal supports:

$$
\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,dV_0
= p_\text{LV}\,\dot{\mathcal{V}}_\text{LV}
+ p_\text{RV}\,\dot{\mathcal{V}}_\text{RV}
+ \dot W_\text{epi}
+ \dot W_\text{base}.
$$

The derivation is a standard divergence-theorem argument; the full proof is in {ref}`chap-appendix-energy-identity` {cite}`holzapfel2000nonlinear`. At the whole-heart level, $w_\text{int}$ and chamber pressure-volume work are therefore equal. Any disagreement seen later between the proxy and $w_\text{int}$ comes from the regional restriction or from the substitutions tested in the cascade below, not from the work definition itself.

```{figure} ../figures/fig_energy_balance_validation.png
:name: fig-energy-balance
:width: 85%

Whole-heart energy-balance check on the synthetic UK Biobank baseline. Cumulative stress-strain work (red) and cumulative cavity pressure plus Robin support work (black dashed) overlap throughout the cycle; final-time residual $\sim 10^{-5}$ relative.
```

(sec-literature-gap)=
## Prior Work and Test Scope

Clinical validation studies usually test pressure-strain work against patient-relevant endpoints. That is appropriate, but those endpoints do not isolate the pressure-for-stress approximation. Glucose uptake and oxygen use ask whether tissue paid a metabolic cost. Contractility asks whether the ventricle can generate pressure for its loading conditions. These are important physiological questions, but they are not direct measurements of local myocardial stress-strain work.

Finite-element stress-strain work has been used before. Regional fibre work and full stress-strain work have been studied in LV, biventricular, perfusion, dyssynchrony, and CRT settings {cite}`finsberg2017phd,wang2012myocardial,pluijmert2017determinants,ahmadbakir2018multiphysics,craine2024successful`. Patient-specific biventricular mechanics frameworks have been used to estimate regional stress and contractility in healthy subjects and in pulmonary arterial hypertension {cite}`finsberg2018efficient,finsberg2019computational`. Coupled 3D--0D frameworks provide the pressure-volume loading context for such mechanics models {cite}`kerckhoffs2007coupling,regazzoni2022cardiac,piersanti2022closed`.

The gap addressed here is narrower than "regional work has not been modelled." What is missing is a quantitative check of how a clinical-style pressure-longitudinal-strain proxy behaves when compared with finite-element stress-strain work in the RV free wall and the septum specifically — the two biventricular cases beyond the well-validated LV setting.

The controlled pressure-loading sweep is designed for that mechanical test. The biventricular mesh, passive material law, fibre field, active-tension waveform, basal support, and cavity-volume coupling are held fixed. What changes is the calibrated zero-dimensional circulation used to drive the same mechanics model through a range of RV pressure loads. The primary high-resolution sweep contains 16 nominal RV-pressure cases and uses capped RV end-diastolic pressure during inverse unloading to avoid an implausibly collapsed RV reference state in the severe fixed-geometry cases. Achieved peak RV pressure spans roughly 32--100 mmHg while peak LV pressure stays in the 105--120 mmHg range. The sweep is a loading-path and reference-state sensitivity experiment, not clinical PAH progression.

(sec-simplification-cascade)=
## Simplification Cascade Diagnostic

One way to make the proxy reduction visible is to remove mechanical information step by step in a diagnostic baseline case — the synthetic UK Biobank mean geometry at the lowest-pressure production loading. {numref}`fig-cascade` shows this cascade as four cumulative work-density curves, each one a different stage of the reduction from full stress-strain work down to the clinical pressure-longitudinal-strain proxy. The pressure-for-stress substitution accounts for the bulk of the magnitude loss; the directional projections are smaller corrections.

In this baseline diagnostic, the myocardium is split into two analysis regions by the same LV-to-RV Laplace scalar $\lambda$ defined above ($\lambda=1$ on the LV endocardium, $\lambda=0$ on the RV endocardium; see {numref}`fig-lv-rv-partition`); cells with $\lambda>0.5$ are assigned to the LV-side region and cells with $\lambda\leq0.5$ to the RV-side region. The pressure-based steps use the corresponding cavity pressure, denoted $p_\text{cav}$.

```{figure} ../figures/fig_cascade_cumulative.png
:name: fig-cascade
:width: 80%

Cascade of cumulative work-density measures over the cardiac cycle on the synthetic UK Biobank baseline, LV-side $\lambda$-split region (a diagnostic partition, not the anatomical LV free wall). Curves descend from $\mathbf{S}:\dot{\mathbf{E}}$ through $S_{ff}\,\dot E_{ff}$ and $p_\text{cav}\,\dot E_{ff}$ to the clinical proxy $p_\text{cav}\,\dot\varepsilon_{ll}$. Signed end-of-cycle plateau values: $-8.4$, $-7.4$, $-1.9$, $-1.5$ kPa.
```

The starting quantity is the full tensor contraction $\mathbf{S}:\dot{\mathbf{E}}$ integrated over the region. This is the complete local work density within the model: every stress component acts through every conjugate strain component, including fibre, cross-fibre, sheet, sheet-normal, and shear contributions. Nothing has been thrown away yet.

The first substitution projects this contraction onto the fibre direction, keeping only $S_{ff}\,\dot E_{ff}$ — the natural one-dimensional reduction given the anisotropy of cardiac muscle. The cross-fibre and sheet contributions that are lost are small in the free walls but non-negligible in the septum.

The second substitution replaces fibre stress by cavity pressure while keeping the fibre strain rate, giving $p_\text{cav}\,\dot E_{ff}$. This is the pressure-for-stress substitution that motivates the rest of the chapter: a scalar cavity boundary load standing in for an internal stress component. What is lost is the stress-pressure scale difference documented earlier, on the order of a factor of four to five at baseline.

The third substitution replaces fibre strain by longitudinal strain, giving the clinical proxy $p_\text{cav}\,\dot\varepsilon_{ll}$. Cardiac fibres spiral well off the long axis, so longitudinal strain rate carries only part of the fibre strain rate.

The plateau values make the relative cost explicit: the fibre projection loses about $1.0$ kPa of LV-side work density, the pressure-for-stress step loses a further $5.5$ kPa, and the strain-direction reduction loses $0.4$ kPa more. The clinical proxy is not expected to match stress-strain work density by absolute scale, so the useful questions are whether it preserves regional work-density ratios and whether it ranks cases consistently across the pressure-loading sweep.

The same cascade can also be viewed as a sequence of loop shapes. Once the work is projected onto one direction, scalar pressure-strain or stress-strain loops can be drawn whose signed areas have work-density units. {numref}`fig-cascade-loops` shows the three loops — fibre stress against fibre strain, cavity pressure against fibre strain, and cavity pressure against longitudinal strain — making visible how the pressure-for-stress substitution changes loop geometry, not just final area.

```{figure} ../figures/fig_cascade_loops.png
:name: fig-cascade-loops
:width: 95%

Loop-space view of the cascade on the synthetic UK Biobank baseline. Rows: LV-side and RV-side $\lambda$-split regions. Columns: $S_{ff}$ vs $E_{ff}$, $p_\text{cav}$ vs $E_{ff}$, $p_\text{cav}$ vs $\varepsilon_{ll}$. Arrows indicate cycle direction; the marked point is the first sampled state. Signed areas are the plateau values in {numref}`fig-cascade`.
```

(sec-scientific-question)=
## Scientific Question

The scientific question has two parts. First, in the ventricular free walls, does the adjacent-pressure longitudinal-strain proxy $w_{\text{PS},ll}[\Omega_j]$ track the stress-strain work density $w_\text{int}[\Omega_j]$? This matters more in the RV free wall, where the pressure-strain approximation has much less model-side validation than in the LV. Second, in the interventricular septum, which pressure choice comes closest to the stress-strain work density? The candidates are an LV-like pressure, an RV-like pressure, the pressure difference, or a two-sided pressure that includes both cavities. In both cases, does the answer change when RV pressure is raised?

The word "track" is evaluated in two complementary ways. The first is a sweep-ranking question. Across the completed pressure-loading cases, does the proxy increase and decrease with the finite-element stress-strain work density along the achieved RV-pressure path? This is measured with Pearson correlation $r$. The second is a magnitude-distribution question. Within a given simulation, does the proxy preserve the regional work-density ratios between the LV free wall, RV free wall, and septum? This is measured with ratio errors. Both views are needed. A proxy can correlate well across one loading path while still giving the wrong regional work-density balance inside the heart.

The expectation from the construction above is not that pressure-strain should reproduce the finite-element work magnitude. It should not. The question is where the reduction remains mechanically useful. In the free walls, adjacent pressure is the natural scalar load and the one-pressure assumption is at its strongest. In the septum, pressure difference may help explain shape and force balance, but work density depends on local stress and strain in tissue loaded by both cavities.
