(chap-work-question)=
# Mechanical Work and the Scientific Question

This chapter defines the two work quantities compared in the thesis: the regional finite-element stress-strain work density $w_\text{int}[\Omega_j]$ and the pressure-longitudinal-strain proxy $w_{\text{PS},ll}[\Omega_j]$. It also states the energy identity used as a numerical check. Pressure is a boundary load rather than a local stress, longitudinal strain is one component of the full deformation state, and the septum is biventricular tissue for which no single cavity pressure is unambiguous. The purpose here is to make those quantities precise before they are tested in {ref}`chap-results`.

(sec-mechanics-notation)=
## Mechanics Notation

The mechanics are written in a reference-configuration frame. A material point with reference position $\mathbf{X}\in\mathcal{B}_0$ moves to the current position

$$
\mathbf{x}=\boldsymbol{\varphi}(\mathbf{X},t)
=\mathbf{X}+\mathbf{u}(\mathbf{X},t),
$$

where $\mathbf{u}$ is the displacement field. The deformation gradient

$$
\mathbf{F} = \frac{\partial \mathbf{x}}{\partial \mathbf{X}}
= \mathbf{I}+\nabla_{\mathbf{X}}\mathbf{u}
$$

maps infinitesimal reference line elements into the current configuration, and $J=\det\mathbf{F}$ gives the local volume ratio. The right Cauchy-Green tensor and Green-Lagrange strain are

$$
\mathbf{C}=\mathbf{F}^{\top}\mathbf{F},
\qquad
\mathbf{E}=\frac{1}{2}(\mathbf{C}-\mathbf{I}).
$$

A dot denotes a material time derivative at fixed $\mathbf{X}$, so $\dot{\mathbf{E}}$ is the rate of Green-Lagrange strain. The stress paired with $\mathbf{E}$ in this reference-frame work expression is the second Piola-Kirchhoff stress $\mathbf{S}$. The product $\mathbf{S}:\dot{\mathbf{E}}$ has units of power per reference volume, Pa/s or J m$^{-3}$ s$^{-1}$. After integration in time it has units J m$^{-3}$, equivalent to Pa. The detailed finite-strain mechanics and constitutive law are given in {ref}`sec-3d-mechanics`.

(sec-work-definitions)=
## Local Work and the Pressure-Strain Proxy

Thick-wall ventricular analyses already showed that pressure cannot stand in for an internal stress field as an identity: stresses vary through the wall, and a useful mean wall-stress estimate is not the same thing as a resolved local stress {cite}`mirsky1969left`. Computing local work density rather than a wall-stress scale therefore needs the local stress and strain fields, which is the step into continuum mechanics.

The local rate of mechanical work in a deforming material is the tensor contraction $\mathbf{S}:\dot{\mathbf{E}}$, where $\mathbf{S}$ is the second Piola-Kirchhoff stress and $\dot{\mathbf{E}}$ is the rate of the Green-Lagrange strain. Both are evaluated on the fixed reference mesh used by the finite-element solver, which is the natural pair for the work-density calculation in the reference configuration {cite}`holzapfel2000nonlinear`. This is the local work-rate density used throughout the thesis.

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

The sign convention is kept explicit because the raw loop integrals are signed. With the strain convention used here, systolic shortening in a loaded direction gives a negative strain increment, so the accumulated stress-strain work and pressure-strain loop areas are often negative when written directly as $\int p\,d\varepsilon$ or $\int \mathbf{S}:\dot{\mathbf{E}}\,dt$. The analysis therefore uses the signed quantities when discussing component balances or loop orientation, but reports positive work-density magnitudes for ratios and magnitude errors by taking absolute values consistently across both integrals. When a figure shows signed plateau values, the caption states this directly.

The pressure-longitudinal-strain proxy lives on the same density scale by construction. For a region $\Omega_j$ and an assigned pressure $p_j(t)$,

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

The longitudinal strain used in the model is a clinical analogue rather than an image-derived measurement. The geometry-generation step saves an apex-to-base direction field from the LDRB construction as the `apex_gradient` field. During postprocessing this raw apico-basal direction is first projected into the local wall tangent plane, using the endocardium-to-epicardium geometric direction $\mathbf{e}_r$ as the radial direction,

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

This removes the transmural component of the apico-basal field before the strain projection is computed. The resulting tangent-longitudinal direction is then used as a fixed reference-direction projection of Green-Lagrange strain,

$$
\varepsilon_{ll,j}(t)
= \frac{1}{|\Omega_{j,0}|}
\int_{\Omega_j}
\mathbf{l}_0(\mathbf{X}) \cdot
\mathbf{E}(t,\mathbf{X})\,
\mathbf{l}_0(\mathbf{X})\,dV_0 .
$$

The per-cell postprocessing uses the same tangent-longitudinal definition locally: it assembles $\Delta E_{ll}=\mathbf{l}_0\cdot\Delta\mathbf{E}\,\mathbf{l}_0$ over each cell and accumulates pressure times that strain increment with a trapezoidal pressure average. The pressure used for these pressure-strain integrals is the solver cavity pressure, namely the Lagrange multiplier pressure that enforces the cavity-volume constraint in the finite-element mechanics problem. The standalone zero-dimensional pressures are still part of the coupled circulation, but they are not the pressure used for the final pressure-strain proxy integrals.

The pressure assignment is straightforward only in the free walls. The LV free wall is paired with $p_\text{LV}$ and the RV free wall with $p_\text{RV}$. The septum is shared tissue with LV pressure on one face and RV pressure on the other, and assigning one scalar pressure to it is already a mechanical assumption.

For the septum, the tested pressure choices are defined from the two solver cavity pressures and, for the spatially varying choices, from a transventricular coordinate. The one-sided choices are $p_\text{LV}$ and $p_\text{RV}$. The transmural choice is $p_\text{LV}-p_\text{RV}$, the mean choice is $\tfrac{1}{2}(p_\text{LV}+p_\text{RV})$, and the nearest-side choice assigns $p_\text{LV}$ to cells on the LV side and $p_\text{RV}$ to cells on the RV side. The through-wall weighted choice uses a scalar $\lambda(\mathbf{X})$ that is one on the LV side and zero on the RV side, so that

$$
p_\lambda(t,\mathbf{X})
= \lambda(\mathbf{X})p_\text{LV}(t)
+ [1-\lambda(\mathbf{X})]p_\text{RV}(t).
$$

In the canonical postprocessing, $\lambda$ is the saved LV-to-RV Laplace scalar when available. If the Euclidean distance coordinate $\tau=d_\text{LV}/(d_\text{LV}+d_\text{RV})$ is used instead, the equivalent LV weight is $1-\tau$. This convention matters: the words "LV side" and "RV side" refer to the pressure weight, not merely to the name of the scalar field.

The scale difference between cavity pressure and local stress is large in the simulations. In the UKB baseline cascade used below, the regional mean fibre stress $S_{ff}$ peaks at about 68 kPa on the LV side and 56 kPa on the RV side, while the corresponding cavity pressures peak at about 16 kPa and 3.9 kPa. The pressure-for-stress substitution is therefore not expected to preserve absolute work-density magnitude. The useful question is whether it preserves regional ratios and rankings.

The stress-power form is only the foundation. Each model layer used in the simulations below affects the stress and strain estimates returned to $w_\text{int}[\Omega_j]$ and therefore affects the proxy comparison. A small-deformation, isotropic, linear-elastic description would give wrong stress magnitudes and wrong stress allocation, because cardiac tissue undergoes finite deformation and is mechanically anisotropic. The simulations therefore use a transversely isotropic Holzapfel-Ogden hyperelastic passive law together with a rule-based fibre assignment with helical transmural variation, since fibre and cross-fibre stresses differ substantially in active tissue {cite}`holzapfel2009constitutive,streeter1969fiber,bayer2012novel`.

Active contraction is equally necessary. Without an active tension term, the wall would behave as a passive elastic membrane during systole, with all stress attributed to cavity pressure and none to internal contraction. A prescribed Blanco activation waveform supplies the active stress along the fibre direction so that systole is generated inside the wall rather than imposed from outside {cite}`blanco2010computational`.

The heart in the chest is also not free-floating. It is constrained by the pericardium and by the great-vessel attachments at the base, so the model retains epicardial Robin springs and a partial basal Dirichlet condition. Without these supports the simulation would exhibit rigid-body motion and unphysical wall thinning.

Cavity pressure is not externally imposed in vivo. It emerges from the interaction between ventricular ejection and the systemic and pulmonary networks, so a coupled zero-dimensional closed-loop circulation is solved alongside the mechanics, exchanging volume and pressure with each cavity at every timestep {cite}`kerckhoffs2007coupling,regazzoni2022cardiac`. The pressure used in $w_{\text{PS},ll}[\Omega_j]$ is itself a product of this machinery: it is the Lagrange multiplier needed to enforce the cavity volume in the current geometry, material state, and active contraction.

Finally, the imaging-derived geometry corresponds to an already-loaded heart rather than a stress-free reference. A separate inverse-elasticity prestressing step recovers the stress-free configuration before the cycle begins; without it, internal stresses would be miscounted from the first beat {cite}`bols2013computational,gee2010computational`. {ref}`chap-model` describes these model layers in detail; the point here is that none of them is decorative.

Naming what the model leaves out is part of the same scope statement. The volumetric formulation is slightly compressible, with a bulk-modulus penalty that closes the volumetric energy density at finite stiffness rather than enforcing $J=1$ exactly. This avoids volumetric locking on tetrahedral elements and keeps the Newton iterates well conditioned. A strictly incompressible formulation is also implemented and can be selected at run time, and the per-cycle compressible-work residual is reported by the postprocessing pipeline as a routine sanity check. In the production runs that residual is a small fraction of the total internal work, small enough that the compressible substitution is not load-bearing for the work-density results below.

The passive law is purely hyperelastic, so stress relaxation, hysteresis, and rate-dependence of real myocardium are absent. The 3D mechanics domain is biventricular and basally truncated: atria, valves, the fibrous skeleton, and great vessels appear only in the 0D circulation, and the basal plane is a flat geometric clip rather than the anatomical atrioventricular valve plane attached to atrial tissue.

The clipped basal plane carries a real mechanical cost. The atrioventricular plane displacement that contributes to ventricular filling in vivo, on the order of ten millimetres during systole, is replaced here by a partial basal Dirichlet condition that fixes one displacement component while leaving the others free. Atrial filling and valve dynamics therefore enter the ventricles through the 0D coupling rather than through 3D wall mechanics.

Active tension is prescribed as a Blanco waveform with a uniform peak amplitude across the LV free wall, the septum, and the RV free wall, so electrophysiology, calcium handling, conduction delays, and any regional activation differences are not modelled. The pericardium is approximated by Robin springs on the epicardium rather than solved as a contact problem with a separate pericardial body, and there is no fluid-structure interaction with the blood, which enters only as a Lagrange-multiplier cavity pressure on the endocardium.

None of these simplifications is physically benign in the abstract, but together they bound the scope of the result: the thesis tests how a clinical pressure-strain proxy compares with finite-element stress-strain work in a biventricular, hyperelastic, electromechanically prescribed, pericardially Robin-supported simulation, not in a fully resolved electromechanical heart-thorax model.

(sec-energy-identity)=
## Energy Identity And Numerical Verification

The stress-power statement also implies a whole-heart energy identity. At the blood-wall interface, the blood pushes on the endocardium and the wall pushes back with the same force and the opposite sign. Multiplying that interface force by velocity gives power, with units J/s. The same mechanical exchange can therefore be written either as boundary pressure-volume power or as stress-strain power inside the wall.

Algebraically, the reference-configuration step uses the energy-conjugate identity $\mathbf{S}:\dot{\mathbf{E}}=\mathbf{P}:\dot{\mathbf{F}}$. Here $\mathbf{P}=\mathbf{F}\mathbf{S}$ and $\dot{\mathbf{F}}=\nabla_\mathbf{X}\mathbf{v}$. In quasi-static equilibrium, $\operatorname{Div}\mathbf{P}=\mathbf{0}$. Multiplying by the velocity $\mathbf{v}$, integrating over $\Omega$, and applying the divergence theorem gives {cite}`holzapfel2000nonlinear`:

$$
\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,dV_0
= \int_{\partial\Omega} \mathbf{t}_0\cdot\mathbf{v}\,dA
= \int_{\partial\omega} \mathbf{t}\cdot\mathbf{v}\,da.
$$

Here $\mathbf{t}_0=\mathbf{P}\mathbf{N}$ is the nominal traction on the reference boundary and $\mathbf{t}$ is the Cauchy traction on the deformed boundary. The two surface integrals describe the same boundary power, written on the reference and current configurations.

Here $dA$ denotes area on the reference boundary and $da$ denotes area on the current, deformed boundary. On the LV and RV endocardial surfaces, the Cauchy traction is pressure, $\mathbf{t}=-p\mathbf{n}$. Together with $\dot{\mathcal{V}}=-\int_{\Gamma_\text{endo}}\mathbf{v}\cdot\mathbf{n}\,da$, the two minus signs combine and the endocardial surface term becomes $p\,\dot{\mathcal{V}}$ under the sign convention used here. The whole-heart power balance therefore has the schematic form

$$
\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,dV_0
= p_\text{LV}\,\dot{\mathcal{V}}_\text{LV}
+ p_\text{RV}\,\dot{\mathcal{V}}_\text{RV}
+ \dot W_\text{epi}
+ \dot W_\text{base},
$$

where the last two terms are the powers exchanged with the epicardial and basal support conditions. If the non-cavity supports were absent, the cycle-integrated identity would reduce to the familiar pressure-volume work terms. In the actual simulation the supports are part of the model definition, so their work is included.

```{figure} ../figures/fig_energy_balance_validation.png
:name: fig-energy-balance
:width: 85%

Numerical verification of the energy-balance identity. The cumulative stress-strain work $\int_0^t\!\!\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,dV_0\,dt'$ (red) and the cumulative cavity pressure work plus Robin support work (black dashed) overlap throughout the cycle. Synthetic UK Biobank baseline, final beat of a six-beat sequence; final-time residual $4.8 \times 10^{-5}$ J ($7 \times 10^{-5}$ relative). The cavity contribution is $-680.7$ mJ; the Robin contribution is $+0.09$ mJ, about $0.01\%$ of the internal work total, small enough that the curve labelled "boundary + Robin" is, to graphical accuracy, the cavity $p\,\dot{\mathcal{V}}$ work.
```

The energy-balance figure is therefore an implementation check. It shows that the computed stress-strain work and boundary work close for the solved model within the discretization tolerance of the accumulation. Its scope is numerical consistency: the code computes the continuum identity accurately enough before the resulting work density is used to test the pressure-strain reduction.

(sec-literature-gap)=
## Prior Work And Test Scope

Clinical validation studies usually test pressure-strain work against patient-relevant endpoints. That is appropriate, but those endpoints do not isolate the pressure-for-stress approximation. Glucose uptake and oxygen use ask whether tissue paid a metabolic cost. Contractility asks whether the ventricle can generate pressure for its loading conditions. Pressure-length and pressure-strain loops ask whether an accessible loop behaves like a regional work index. These are important physiological questions, but they are not direct measurements of local myocardial stress-strain work.

Finite-element stress-strain work has been used before. Regional fibre work and full stress-strain work have been studied in LV, biventricular, perfusion, dyssynchrony, and CRT settings {cite}`finsberg2017phd,wang2012myocardial,pluijmert2017determinants,ahmadbakir2018multiphysics,craine2024successful`. Patient-specific biventricular mechanics frameworks have been used to estimate regional stress and contractility in healthy subjects and in pulmonary arterial hypertension {cite}`finsberg2018efficient,finsberg2019computational`. Coupled 3D--0D frameworks provide the pressure-volume loading context for such mechanics models {cite}`kerckhoffs2007coupling,regazzoni2022cardiac,piersanti2022closed`.

The gap addressed here is narrower than "regional work has not been modelled." What is missing is a quantitative check of how a clinical-style pressure-longitudinal-strain proxy behaves when compared with finite-element stress-strain work in the RV free wall and the septum specifically — the two cases where the one-pressure assumption is least obvious.

The controlled pressure-loading sweep is designed for that mechanical test. The biventricular mesh, passive material law, fibre field, active-tension waveform, basal support, and cavity-volume coupling are held fixed. What changes is the calibrated zero-dimensional circulation used to drive the same mechanics model through a range of RV pressure loads. The high-resolution sweep contains 16 nominal RV-pressure cases. Achieved peak RV pressure spans roughly 31--89 mmHg while peak LV pressure remains comparatively stable, about 100--109 mmHg. The sweep is a loading-path sensitivity experiment, not clinical PAH progression.

The final sweep also keeps the septal postprocessing definitions consistent across cases. The per-cell septal and transventricular fields are computed once on the canonical generated geometry and then mapped to each prestressed checkpoint through the saved inverse-elastic displacement permutation. The work integrals themselves are still evaluated on each simulation checkpoint and over the final cardiac cycle; the canonical fields define the septal masks and LV-to-RV through-wall coordinate, while the original solver region tags identify the free-wall domains. This is different from the legacy unloaded-tagging mode kept in the code for reproducibility, which is not used as the anatomical basis for the main sweep.

(sec-simplification-cascade)=
## Simplification Cascade Diagnostic

One way to make the proxy reduction visible is to remove mechanical information step by step in a diagnostic baseline case. Here "baseline" means the synthetic UK Biobank mean geometry at the lowest-pressure production loading. {numref}`fig-cascade` shows this cascade as four cumulative work-density curves, each one a different stage of the reduction from full stress-strain work down to the clinical pressure-longitudinal-strain proxy. In this baseline diagnostic, the myocardium is split into two analysis regions by a Laplace coordinate $\tau$ satisfying $\tau=0$ on the LV endocardium and $\tau=1$ on the RV endocardium; cells with $\tau<0.5$ are assigned to the LV-side region and cells with $\tau\geq0.5$ to the RV-side region. The pressure-based steps use the corresponding cavity pressure, denoted $p_\text{cav}$.

```{figure} ../figures/fig_cascade_cumulative.png
:name: fig-cascade
:width: 80%

Cascade of work-density measures from the full tensor contraction down to the clinical pressure-strain proxy, shown for the LV-side $\tau$-split region on the synthetic UK Biobank baseline. In this diagnostic split, every myocardial cell is assigned to either the LV-side or RV-side region, so this is not the anatomical LV free wall defined in {ref}`sec-geometry-anatomical-model` and used in the later free-wall ratio tests. $\mathbf{S}:\dot{\mathbf{E}}$ is the full double contraction; $S_{ff}\,\dot E_{ff}$ is the fibre-normal component alone; $p_\text{cav}\,\dot E_{ff}$ is a model-side intermediate that substitutes cavity pressure for the fibre stress; $p_\text{cav}\,\dot\varepsilon_{ll}$ is the clinical pressure-longitudinal-strain proxy. Signed end-of-cycle plateau values: $-8.4$, $-7.4$, $-1.9$, $-1.5$ kPa. The pressure-for-stress substitution accounts for the bulk of the magnitude loss.
```

The starting quantity is the full tensor contraction $\mathbf{S}:\dot{\mathbf{E}}$ integrated over the region. This is the complete local work density within the model: every stress component acts through every conjugate strain component, including fibre, cross-fibre, sheet, sheet-normal, and shear contributions. Nothing has been thrown away yet.

The first substitution projects this contraction onto the fibre direction, keeping only $S_{ff}\,\dot E_{ff}$. The choice of the fibre direction is mechanically motivated: cardiac muscle is strongly anisotropic and the fibre direction dominates both the passive and active response in healthy tissue, so this is the natural one-dimensional projection. What is lost are the cross-fibre and sheet contributions, which are small in the free walls but non-negligible in the septum.

It is worth weighing this anatomical projection against a principal-stress alternative, because in continuum-mechanics terms a valid one-direction reduction could instead project the contraction onto the largest principal stress direction at each point. The fibre direction is preferred here for two complementary reasons. First, cardiac muscle is much stiffer along the fibre than across it and the active stress acts along $\mathbf{f}_0$, so the largest principal stress direction generally stays close to the fibre direction in healthy biventricular tissue, and a fibre projection therefore retains most of the local work-density magnitude that a principal projection would {cite}`holzapfel2009constitutive`. Second, the fibre direction is anatomically fixed in the tissue, just like longitudinal strain is anatomically fixed in the imaging frame, so both sides of the cascade project onto tissue-defined axes rather than onto a moving principal axis. A principal-stress projection is a useful model-side diagnostic in its own right, but its eigenvector can move through the cycle and has no direct clinical analogue, so it would break the parallel between the model-side intermediate and the clinical longitudinal-strain proxy that the cascade is built around.

The second substitution replaces fibre stress by cavity pressure while keeping the fibre strain rate, giving $p_\text{cav}\,\dot E_{ff}$. This is the pressure-for-stress substitution that motivates the rest of the chapter: a scalar cavity boundary load standing in for an internal stress component. What is lost is the stress-pressure scale difference documented earlier, on the order of a factor of four to five at baseline.

The third substitution keeps cavity pressure but replaces fibre strain by longitudinal strain, giving $p_\text{cav}\,\dot\varepsilon_{ll}$. This is the clinical pressure-longitudinal-strain proxy. What is lost is alignment with the fibre direction: longitudinal strain is the long-axis projection in the anatomical frame, while cardiac fibres spiral well off that axis, so longitudinal strain rate carries only part of the fibre strain rate.

The four end-of-cycle plateau values on the figure make the relative cost of each substitution explicit. Projecting the full tensor contraction onto the fibre direction loses about $1.0$ kPa of LV-side work density, the cross-fibre and sheet share. Replacing fibre stress by cavity pressure loses a further $5.5$ kPa, by far the largest single drop and consistent with the pressure-stress scale gap documented above. Replacing fibre strain by longitudinal strain then loses an additional $0.4$ kPa, a smaller correction. Most of the absolute magnitude loss therefore happens at the pressure-for-stress step; the strain-direction reduction is a finer correction; and the projection onto the fibre direction sits in between. The clinical proxy is not expected to match stress-strain work density by absolute scale, so the useful questions are whether it preserves regional work-density ratios and whether it ranks cases consistently across the pressure-loading sweep.

The same simplification can also be viewed as a sequence of loop shapes. The full tensor contraction $\mathbf{S}:\dot{\mathbf{E}}$ has no single two-axis loop, because both stress and strain are tensors. Once the work is projected onto one direction, scalar loops can be drawn. The three loops here are fibre stress versus fibre strain, cavity pressure versus fibre strain, and cavity pressure versus longitudinal strain. Each loop has stress or pressure on the vertical axis and dimensionless strain on the horizontal axis, so the signed loop area has work-density units. {numref}`fig-cascade-loops` shows that the pressure substitution changes the loop geometry as well as the final scale.

```{figure} ../figures/fig_cascade_loops.png
:name: fig-cascade-loops
:width: 95%

Loop-space view of the simplification cascade on the synthetic UK Biobank baseline. Rows show the LV-side and RV-side $\tau$-split regions; columns show the fibre stress-strain loop $S_{ff}$ versus $E_{ff}$, the pressure-fibre-strain loop $p_\text{cav}$ versus $E_{ff}$, and the clinical pressure-longitudinal-strain loop $p_\text{cav}$ versus $\varepsilon_{ll}$. Arrows indicate the direction of time around the cardiac cycle, and the marked point is the first sampled state. The signed areas inside these loops are the final accumulated work-density values shown in {numref}`fig-cascade`. The figure makes visible how the pressure-for-stress substitution and the strain-direction reduction change the loop geometry, not only its final accumulated area.
```

(sec-scientific-question)=
## Scientific Question

The scientific question has two parts. First, in the ventricular free walls, does the adjacent-pressure longitudinal-strain proxy $w_{\text{PS},ll}[\Omega_j]$ track the stress-strain work density $w_\text{int}[\Omega_j]$? This is especially important in the RV free wall, where the pressure-strain approximation has much less model-side validation than in the LV. Second, in the interventricular septum, which pressure choice comes closest to the stress-strain work density? The candidates are an LV-like pressure, an RV-like pressure, the pressure difference, or a two-sided pressure that includes both cavities. In both cases, does the answer change when RV pressure is raised?

The word "track" is evaluated in two complementary ways. The first is a sweep-ranking question. Across the completed pressure-loading cases, does the proxy increase and decrease with the finite-element stress-strain work density along the achieved RV-pressure path? This is measured with Pearson correlation $r$. The second is a magnitude-distribution question. Within a given simulation, does the proxy preserve the regional work-density ratios between the LV free wall, RV free wall, and septum? This is measured with ratio errors. Both views are needed. A proxy can correlate well across one loading path while still giving the wrong regional work-density balance inside the heart.

The expectation from the construction above is not that pressure-strain should reproduce the finite-element work magnitude. It should not. The question is where the reduction remains mechanically useful. In the free walls, adjacent pressure is the natural scalar load and the one-pressure assumption is at its strongest. In the septum, pressure difference may help explain shape and force balance, but work density depends on local stress and strain in tissue loaded by both cavities. The aim is to test these assumptions inside a controlled model where the geometry and material model are held fixed.
