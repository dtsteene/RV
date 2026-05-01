# Mechanical Work and the Scientific Question

This thesis compares a clinically measurable pressure-strain index with a model-resolved stress-strain work density. That comparison only makes sense if the hierarchy of mechanical descriptions is clear. A pressure-volume loop, a pressure-strain loop, a simple wall-stress estimate, and a finite-element tensor-work calculation are related, but they are not interchangeable. Each keeps some mechanics and discards other mechanics.

The finite-element model is useful here for a specific reason. Pressure-strain indices make regional statements about myocardial work, and regional work depends on mechanics that pressure, longitudinal strain, and simple wall-stress formulas do not resolve. The model gives a controlled setting in which those hidden variables are known, so the pressure-strain reduction can be tested rather than assumed.

The operational quantities are the regional tensor work density $w_\text{int}[\Omega_j]$ and the pressure-longitudinal-strain proxy $w_{\text{PS},ll}[\Omega_j]$. The continuum-mechanics discussion below explains why stress power is the local work quantity. The energy-balance section checks that the numerical implementation computes that quantity consistently with the boundary work implied by the solved model.

## Building Up To A Local Work Model

This chapter moves in two directions. First, it asks what mechanical information must be added to estimate local myocardial work inside a model. Then it asks what is lost when those layers are removed until only the clinical pressure-longitudinal-strain proxy remains. The first direction explains why the model is needed. The second motivates the simplification cascade later in the chapter.

The starting point is pressure-volume work. A ventricular pressure-volume loop has a strong mechanical meaning because its area is the external work exchanged between the ventricular wall and the blood. It is the right level of description if the question is how much work a chamber performs as a pump. But it is silent about where that work is produced inside the wall. The same chamber pressure and volume change can be compatible with many different regional stress and strain patterns.

Clinical pressure-length and pressure-strain loops move one step closer to regional work by pairing chamber pressure with local shortening {cite}`forrester1974pressure_length,tyberg1974segmental,urheim2005regional,russell2012novel`. The practical appeal is clear: pressure and deformation can be measured or estimated in patients. The mechanical reduction is also clear. Chamber pressure is used where local myocardial stress would be needed, and one measured strain component is used where the full deformation state would be needed.

Simple wall-stress arguments already show that the pressure substitution cannot be an identity. Pressure is a boundary load. Wall stress is an internal response that also depends on geometry and thickness. Thick-wall ventricular analyses add another layer: stresses vary through the wall, and a useful mean wall-stress estimate is not the same thing as a resolved local stress field {cite}`mirsky1969left`.

To compute local work density rather than a wall-stress scale, the model has to keep the local stress and strain fields. That is the step into continuum mechanics. The myocardium undergoes finite deformation. Strain cannot be reduced to a small-displacement scalar. Stress cannot be reduced to one wall-tension number. Work density is the local stress power integrated through time. Early passive models treated ventricular myocardium as incompressible hyperelastic, anisotropic tissue. Large-scale beating-heart finite-element work then showed why regional mechanics also depends on geometry, fibre architecture, active tension, and electrical activation {cite}`guccione1991passive,mcculloch1992large`.

A stress-power formula is therefore only the foundation. The model also needs a passive material law, fibre architecture, active tension, boundary support, cavity constraints, and a circulation that determines ventricular loading. These layers are defined in the model chapter. They draw on structurally motivated myocardial material laws, rule-based fibre assignment, and coupled 3D--0D mechanics frameworks {cite}`holzapfel2009constitutive,streeter1969fiber,bayer2012novel,kerckhoffs2007coupling,regazzoni2022cardiac,piersanti2022closed`.

This coupling matters for the present thesis because the pressure used in the proxy is also the pressure produced by the mechanics solve. It is the Lagrange multiplier needed to enforce the cavity volume in the current geometry, material state, and active contraction.

The endpoint of this upward construction is a mechanically explicit test system. Its assumptions define the scope of the result. Within that scope, the stress and strain fields hidden from the clinical proxy become available, including the two-sided loading of the septum. That makes it possible to ask the reverse question: how much of this model-resolved local work survives when it is collapsed back down to pressure-longitudinal-strain work?

## Local Work And Chamber Work

The basic local statement in mechanics is that work in a deforming material comes from stress acting through deformation. In one dimension this is the familiar density-like product $\sigma\,d\varepsilon$. In three dimensions the scalar product becomes a tensor contraction. Written in the current configuration, the local stress power is $\boldsymbol{\sigma}:\mathbf{d}$, where $\boldsymbol{\sigma}$ is the Cauchy stress and $\mathbf{d}$ is the rate-of-deformation tensor. This is the continuum-mechanics work-density idea, independent of the particular cardiac material model used later. The finite-element expression used here is the same stress power pulled back to the reference mesh:

$$
\boldsymbol{\sigma}:\mathbf{d}\,dv
= \mathbf{S}:\dot{\mathbf{E}}\,dV_0,
$$

with $\mathbf{S}$ the second Piola-Kirchhoff stress and $\mathbf{E}$ the Green-Lagrange strain {cite}`holzapfel2000nonlinear`. This pair is energy-conjugate in the reference configuration, so the contraction $\mathbf{S}:\dot{\mathbf{E}}$ is the fixed-mesh form of the same local stress power. What the cardiac model contributes is the estimate of those stress and strain fields.

This is the conceptual step between pressure-volume work and the hyperelastic model solved later. The pressure-volume loop uses a boundary force scale, pressure, and a chamber motion, volume change. Continuum mechanics instead resolves work density inside the wall from stress and deformation at each material point. The model layers introduced later then determine how those fields are estimated.

Pressure-volume work is the corresponding chamber-level boundary expression of the same mechanical exchange. When the wall presses on the blood, the boundary force can be represented by the cavity pressure and the boundary motion by the change in cavity volume. The positive stroke-work magnitude is

$$
SW = \left|\oint p\,dV\right|,
$$

the work exchanged between the ventricular wall and the blood over one beat. This is the same mechanical idea behind the classical cardiac pressure-volume loop and the pressure-volume area framework used in whole-ventricle energetics {cite}`frank1899grundform,suga1979total`. It is a strong chamber-level quantity, but it has no regional wall information. It does not tell us how much work was carried by the LV free wall, the RV free wall, or the interventricular septum.

The finite-element model gives a way to estimate the corresponding local mechanical quantity. Let $\Omega$ denote the reference-configuration biventricular myocardium. Because $\mathbf{S}:\dot{\mathbf{E}}$ is evaluated point by point in the tissue, the same density can be integrated over whatever region is relevant. For a reference-configuration subregion $\Omega_j \subseteq \Omega$, such as the LV free wall, RV free wall, septum, or the whole myocardium, the internal work over a cardiac cycle is

$$
W_\text{int}[\Omega_j]
= \int_0^T \int_{\Omega_j}
\mathbf{S}(t,\mathbf{X}) : \dot{\mathbf{E}}(t,\mathbf{X}) \, dV_0 \, dt,
$$

where the colon denotes double contraction {cite}`delhaas1994regional,finsberg2019assessment`. The pair $\mathbf{S}$ and $\mathbf{E}$ is used because the finite-element calculation is carried out on the fixed reference mesh. This is the reference-configuration form of the same stress-power idea. The regional decomposition used in this thesis comes from changing the integration domain $\Omega_j$ while keeping the definition of work fixed.

In sampled simulation output, the cycle integral is accumulated with a trapezoidal rule,

$$
W_\text{int}[\Omega_j] \approx
\sum_{i=1}^{N}
\int_{\Omega_j}
\bar{\mathbf{S}}(t_i,\mathbf{X}) : \Delta\mathbf{E}(t_i,\mathbf{X}) \, dV_0,
$$

with $\bar{\mathbf{S}}(t_i)=\tfrac{1}{2}(\mathbf{S}(t_i)+\mathbf{S}(t_{i-1}))$ and $\Delta\mathbf{E}(t_i)=\mathbf{E}(t_i)-\mathbf{E}(t_{i-1})$.

This regional integral has units of energy. A clinical pressure-strain loop has no regional myocardial volume in it. Pressure times dimensionless strain has pressure units, equivalent to work per volume. The finite-element reference is therefore converted to work density by dividing by the reference volume of the region,

$$
w_\text{int}[\Omega_j]
= \frac{W_\text{int}[\Omega_j]}{|\Omega_{j,0}|},
\qquad
|\Omega_{j,0}| = \int_{\Omega_j} dV_0.
$$

This is the target quantity in the thesis: model-resolved regional mechanical work density, the internally defined estimate of the local stress-strain work density implied by the chosen finite-element model.

## The Clinical Pressure-Strain Proxy

Clinical pressure-strain work comes from a different direction. Earlier pressure-length studies used chamber pressure and measured segment length to form regional loop areas {cite}`forrester1974pressure_length,tyberg1974segmental`. Later pressure-strain methods replaced segment length with image-based strain, making the approach more practical for echocardiography {cite}`urheim2005regional,russell2012novel,abawi2022noninvasive`. Recent RV applications follow the same basic construction, using RV pressure and RV longitudinal or free-wall longitudinal strain {cite}`wang2022apply,lakatos2024right`.

For a region $\Omega_j$ and an assigned pressure $p_j(t)$, the pressure-longitudinal-strain proxy used here is

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

where $\bar p_j(t_i)=\tfrac{1}{2}(p_j(t_i)+p_j(t_{i-1}))$ and $\Delta\varepsilon_{ll,j}(t_i)=\varepsilon_{ll,j}(t_i)-\varepsilon_{ll,j}(t_{i-1})$. No regional volume factor appears. If an absolute model-side energy estimate were desired, this density-like index could be multiplied by the known finite-element region volume. That is not how the clinical index is measured. The comparison in this thesis therefore keeps the clinical-side proxy as pressure times longitudinal strain and compares it with $w_\text{int}$.

The pressure assignment is straightforward only in the free walls. The LV free wall is paired with $p_\text{LV}$ and the RV free wall with $p_\text{RV}$. The septum is different. It is shared tissue with LV pressure on one face and RV pressure on the other. Assigning one scalar pressure to the septum is already a mechanical assumption. The tested choices are the two cavity pressures, their difference, mean pressure, nearest-side pressure, and through-wall weighted pressure.

Pressure is a boundary load rather than a local myocardial stress measurement. At an endocardial surface, the Cauchy traction condition is $\boldsymbol{\sigma}\mathbf{n}=-p\mathbf{n}$, so pressure fixes the normal traction applied by the blood. It does not determine the fibre, circumferential, longitudinal, or shear stresses inside the wall. Those follow from equilibrium, geometry, material law, active contraction, and support conditions.

The scale difference is large in the simulations. In the UKB baseline cascade used below, the regional mean fibre stress $S_{ff}$ peaks at about 68 kPa on the LV side and 56 kPa on the RV side, while the corresponding cavity pressures peak at about 16 kPa and 3.9 kPa. Thick-wall analyses make the same qualitative point: pressure is a boundary load, not a resolved wall-stress field {cite}`mirsky1969left`.

The strain choice is also a reduction. Clinical imaging can report longitudinal, circumferential, and radial deformation. Cardiac MRI tagging can provide more complete three-dimensional regional strain information {cite}`tee2013imaging,voigt2015definitions`. Clinical pressure-strain myocardial-work workflows, however, are usually built from longitudinal strain rather than myocardial fibre strain or a full local strain tensor {cite}`russell2012novel,abawi2022noninvasive,thomas2025clinical`. Measuring additional strain directions would reduce one part of the approximation. It would not by itself turn pressure-strain work into tensor work, because the matching local stress components would still be unmeasured. The fibre-aligned quantities used later in the results are therefore model-side diagnostics, not alternative clinical measurements.

## Energy Identity And Numerical Verification

The stress-power statement also implies a whole-heart energy identity. At the blood-wall interface, Newton's third law gives the intuition: the blood presses on the endocardium and the wall presses back with the same force and the opposite sign. Multiplying that shared interface force by the interface velocity writes the same power from the wall side or from the cavity side.

Algebraically, the reference-configuration step uses the energy-conjugate identity $\mathbf{S}:\dot{\mathbf{E}}=\mathbf{P}:\dot{\mathbf{F}}$. Here $\mathbf{P}=\mathbf{F}\mathbf{S}$ and $\dot{\mathbf{F}}=\nabla_\mathbf{X}\mathbf{v}$. In quasi-static equilibrium, $\operatorname{Div}\mathbf{P}=\mathbf{0}$. Multiplying by the velocity $\mathbf{v}$, integrating over $\Omega$, and applying the divergence theorem gives {cite}`holzapfel2000nonlinear`:

$$
\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,dV_0
= \int_{\partial\Omega} \mathbf{t}_0\cdot\mathbf{v}\,dA
= \int_{\partial\omega} \mathbf{t}\cdot\mathbf{v}\,da.
$$

Here $\mathbf{t}_0=\mathbf{P}\mathbf{N}$ is the nominal traction on the reference boundary and $\mathbf{t}$ is the Cauchy traction on the deformed boundary. The two surface integrals describe the same boundary power, written on the reference and current configurations.

On the LV and RV endocardial surfaces, the Cauchy traction is pressure, $\mathbf{t}=-p\mathbf{n}$. Together with $\dot{\mathcal{V}}=-\int_{\Gamma_\text{endo}}\mathbf{v}\cdot\mathbf{n}\,da$, the two minus signs combine and the endocardial surface term becomes $p\,\dot{\mathcal{V}}$ under the sign convention used here. The whole-heart power balance therefore has the schematic form

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

Numerical verification of the energy-balance identity. The cumulative tensor work $\int_0^t\!\!\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,dV_0\,dt'$ (red) and the cumulative cavity pressure work plus Robin support work (black dashed) overlap throughout the cycle. UKB synthetic baseline, final beat of a six-beat sequence; final-time residual $4.8 \times 10^{-5}$ J ($7 \times 10^{-5}$ relative). The cavity contribution is $-680.7$ mJ; the Robin contribution is $+0.09$ mJ, about $0.01\%$ of the tensor total, small enough that the curve labelled "boundary + Robin" is, to graphical accuracy, the cavity $p\,\dot{\mathcal{V}}$ work.
```

The energy-balance figure is therefore an implementation check. It shows that the computed stress-strain work and boundary work close for the solved model within the discretization tolerance of the accumulation. Its scope is numerical consistency: the code computes the continuum identity accurately enough before the resulting tensor-work density is used to test the pressure-strain reduction.

## Literature Gap And Mechanical Test

Clinical validation studies usually test pressure-strain work against patient-relevant endpoints. That is appropriate, but those endpoints do not isolate the pressure-for-stress approximation. Glucose uptake and oxygen use ask whether tissue paid a metabolic cost. Contractility asks whether the ventricle can generate pressure for its loading conditions. Pressure-length and pressure-strain loops ask whether an accessible loop behaves like a regional work index. These are important physiological questions, but they are not direct measurements of local myocardial stress-strain work.

Finite-element stress-strain work has also been used before. Regional fibre or tensor work has been studied in LV, biventricular, perfusion, dyssynchrony, and CRT settings {cite}`finsberg2019assessment,wang2012myocardial,pluijmert2017determinants,ahmadbakir2018multiphysics,craine2024successful`. Patient-specific biventricular mechanics frameworks have been used to estimate regional stress and contractility in healthy subjects and in pulmonary arterial hypertension {cite}`finsberg2018efficient,finsberg2019computational`. Coupled 3D--0D frameworks provide the pressure-volume loading context for such mechanics models {cite}`kerckhoffs2007coupling,regazzoni2022cardiac,piersanti2022closed`.

The gap addressed here is narrower than "regional work has not been modelled." The gap is how a clinical-style pressure-longitudinal-strain proxy behaves when checked against model-resolved tensor work in the RV free wall and in the septum. The RV free wall matters because RV pressure-strain indices are now being proposed clinically as more informative than RV strain alone {cite}`lakatos2024right`. The septum matters because it is a shared wall and no single cavity pressure is an unambiguous local stress surrogate there.

The controlled pressure-loading sweep is designed for that mechanical test. The biventricular mesh, passive material law, fibre field, active-tension waveform, basal support, and cavity-volume coupling are held fixed. What changes is the calibrated zero-dimensional circulation used to drive the same mechanics model through a range of RV pressure loads. The high-resolution sweep contains 16 nominal RV-pressure cases. Achieved peak RV pressure spans roughly 31--89 mmHg while peak LV pressure remains comparatively stable, about 100--109 mmHg. The sweep is a loading-path sensitivity experiment, not clinical PAH progression.

## Simplification Cascade

One way to make the proxy reduction visible is to remove mechanical information step by step. The cascade used in the next two figures moves from full tensor work density to fibre-direction stress-strain work, then to cavity pressure with fibre strain, and finally to cavity pressure with longitudinal strain. For this diagnostic only, the myocardium is split into LV-side and RV-side territories by solving a Laplace problem with value zero on the LV endocardium and one on the RV endocardium, then cutting the resulting coordinate at $0.5$. The pressure-based steps use the corresponding cavity pressure, denoted $p_\text{cav}$.

The main effect is large: replacing fibre stress by cavity pressure causes most of the absolute magnitude loss. This is consistent with the pressure-stress scale difference above. The final pressure-longitudinal-strain proxy is therefore not expected to match tensor work density by absolute scale. The useful questions are whether it preserves regional work-density ratios and whether it ranks cases consistently across the pressure-loading sweep.

```{figure} ../figures/fig_cascade_cumulative.png
:name: fig-cascade
:width: 80%

Cascade of work-density measures from the full tensor contraction down to the clinical pressure-strain proxy, shown for the LV-side tau-split territory on the UKB synthetic baseline. In this diagnostic split, every myocardial cell is assigned to either the LV-side or RV-side territory, so this is not the anatomical LV free wall defined in the geometry chapter and used in the later free-wall ratio tests. $\mathbf{S}:\dot{\mathbf{E}}$ is the full double contraction; $S_{ff}\,\dot E_{ff}$ is the fibre-normal component alone; $p_\text{cav}\,\dot E_{ff}$ is a model-side intermediate that substitutes cavity pressure for the fibre stress; $p_\text{cav}\,\dot\varepsilon_{ll}$ is the clinical pressure-longitudinal-strain proxy. End-of-cycle plateau values: $-8.4$, $-7.4$, $-1.9$, $-1.5$ kPa. The pressure-for-stress substitution accounts for the bulk of the magnitude loss.
```

The same simplification can also be viewed as a sequence of loop shapes. The full tensor contraction $\mathbf{S}:\dot{\mathbf{E}}$ has no single two-axis loop, because both stress and strain are tensors. Once the work is projected onto one direction, scalar loops can be drawn. The three loops here are fibre stress versus fibre strain, cavity pressure versus fibre strain, and cavity pressure versus longitudinal strain. Each loop has stress or pressure on the vertical axis and dimensionless strain on the horizontal axis, so the signed loop area has work-density units. {numref}`fig-cascade-loops` shows that the pressure substitution changes the loop geometry as well as the final scale.

```{figure} ../figures/fig_cascade_loops.png
:name: fig-cascade-loops
:width: 95%

Loop-space view of the simplification cascade on the UKB synthetic baseline. Rows show the LV-side and RV-side tau-split territories; columns show the fibre stress-strain loop $S_{ff}$ versus $E_{ff}$, the pressure-fibre-strain loop $p_\text{cav}$ versus $E_{ff}$, and the clinical pressure-longitudinal-strain loop $p_\text{cav}$ versus $\varepsilon_{ll}$. Arrows indicate the direction of time around the cardiac cycle, and the marked point is the first sampled state. The signed areas inside these loops are the final accumulated work-density values shown in {numref}`fig-cascade`. The figure makes visible how the pressure-for-stress substitution and the strain-direction reduction change the loop geometry, not only its final accumulated area.
```

## Scientific Question

The scientific question has two parts. First, in the ventricular free walls, does the adjacent-pressure longitudinal-strain proxy $w_{\text{PS},ll}[\Omega_j]$ track the tensor work density $w_\text{int}[\Omega_j]$? This is especially important in the RV free wall, where the pressure-strain approximation has much less tensor-work validation than in the LV. Second, in the interventricular septum, which pressure choice comes closest to the tensor work density? The candidates are an LV-like pressure, an RV-like pressure, the pressure difference, or a two-sided pressure that includes both cavities. In both cases, does the answer change when RV pressure is raised?

The word "track" is evaluated in two complementary ways. The first is a sweep-ranking question. Across the completed pressure-loading cases, does the proxy increase and decrease with the model-resolved tensor work density along the achieved RV-pressure path? This is measured with Pearson correlation $r$. The second is a magnitude-distribution question. Within a given simulation, does the proxy preserve the regional work-density ratios between the LV free wall, RV free wall, and septum? This is measured with ratio errors. Both views are needed. A proxy can correlate well across one loading path while still giving the wrong regional work-density balance inside the heart.

The expectation from the construction above is not that pressure-strain should reproduce tensor-work magnitude. It should not. The question is where the reduction remains mechanically useful. In the free walls, adjacent pressure is the natural scalar load and the one-pressure assumption is at its strongest. In the septum, pressure difference may help explain shape and force balance, but work density depends on local stress and strain in tissue loaded by both cavities. The aim of the model is to test these assumptions under controlled loading while keeping the geometry and material model fixed.
