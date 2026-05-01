# Mechanical Work and the Scientific Question

Before asking whether pressure-strain work is a good proxy, we need to say what it is a proxy for. The target here is local mechanical work density: work per volume of myocardium. This unit matters because the model and the clinical index handle volume differently. The finite-element calculation integrates stress-strain work through a tissue region, so it naturally returns total regional work in joules. A pressure-strain loop has no regional volume in it; pressure times dimensionless strain has pressure units, which are equivalent to energy per volume. For that reason, this thesis compares pressure-strain loops with finite-element work divided by regional volume.

This is not the same question usually answered by clinical validation studies, which compare pressure-strain indices with things such as contractility, oxygen demand, or prognosis. Those endpoints are important, but they are not direct measurements of the hidden stress-strain work inside the tissue. The purpose of the model is therefore more specific: it gives access to the mechanical quantity that motivates interpreting a pressure-strain loop as work, but that cannot normally be measured inside a patient.

## Model-Resolved Tensor Work

Let $\Omega$ denote the reference-configuration biventricular myocardial domain, and let $\Omega_j \subseteq \Omega$ be a reference-configuration subregion (a free-wall region or the septum). Following Finsberg et al. {cite}`finsberg2019assessment`, the total internal work in $\Omega_j$ over a cardiac cycle is

$$
W_\text{int}[\Omega_j] = \int_0^T \int_{\Omega_j} \mathbf{S}(t, \mathbf{X}) : \dot{\mathbf{E}}(t, \mathbf{X}) \, dV_0 \, dt,
$$

where $\mathbf{S}$ is the second Piola-Kirchhoff stress tensor, $\mathbf{E}$ is the Green-Lagrange strain tensor, and the colon denotes the double contraction $\mathbf{S} : \dot{\mathbf{E}} = S_{ij} \dot{E}_{ij}$. This is the reference-configuration form of stress power; the same power could be written in the current configuration as $\boldsymbol{\sigma}:\mathbf{d}\,dv$, using Cauchy stress and the rate-of-deformation tensor. The pair $\mathbf{S}$ and $\mathbf{E}$ is used here because the finite-element integration is carried out on the fixed reference mesh. In discrete form, sampling the simulation at $N+1$ snapshots $t_0, t_1, \ldots, t_N$ over the cycle and applying the trapezoidal rule,

$$
W_\text{int}[\Omega_j] \approx \sum_{i=1}^{N} \int_{\Omega_j} \bar{\mathbf{S}}(t_i, \mathbf{X}) : \Delta\mathbf{E}(t_i, \mathbf{X}) \, dV_0,
$$

with $\bar{\mathbf{S}}(t_i) = \tfrac{1}{2}(\mathbf{S}(t_i) + \mathbf{S}(t_{i-1}))$ the average stress and $\Delta\mathbf{E}(t_i) = \mathbf{E}(t_i) - \mathbf{E}(t_{i-1})$ the strain increment at step $i$.

The volume integral is important. The local product $\bar{\mathbf{S}}:\Delta\mathbf{E}$ has work-density units because stress has units of energy per unit volume and strain is dimensionless. After integration over $\Omega_j$, however, $W_\text{int}[\Omega_j]$ is a total regional work in joules. The conversion back to density is done later by dividing by the reference volume of the region.

## Whole-Heart Energy Balance

Internal work is not disconnected from the work done on the blood. At the blood-wall interface, the basic intuition is Newton's third law: the blood presses on the endocardium, and the wall presses back on the blood with the same force and the opposite sign. Multiplying that shared interface force by the interface velocity gives power. Written from the wall side, it is stress-strain power in the tissue; written from the cavity side, it is pressure-volume power. The algebra below is the continuum-mechanics version of that statement, with the signs and support terms made explicit.

For the whole biventricular myocardium, stress power inside the wall must balance the traction power applied on its boundary. The algebra has two pieces. First, from the kinematic definition $\dot{\mathbf{E}} = \tfrac{1}{2}(\dot{\mathbf{F}}^T\mathbf{F} + \mathbf{F}^T\dot{\mathbf{F}})$, the symmetry of $\mathbf{S}$, and the relation $\mathbf{P} = \mathbf{F}\mathbf{S}$ between the second and first Piola-Kirchhoff stresses, a direct index calculation gives the pointwise identity $\mathbf{S}:\dot{\mathbf{E}} = \mathbf{P}:\dot{\mathbf{F}}$. The second form is useful because $\dot{\mathbf{F}} = \nabla_\mathbf{X}\mathbf{v}$ is a material gradient of the velocity $\mathbf{v} = \dot{\mathbf{x}}$, which integration by parts turns into a boundary term. Second, in the quasi-static limit, the reference-configuration momentum balance reduces to $\text{Div}\,\mathbf{P} = \mathbf{0}$; taking the inner product with $\mathbf{v}$, integrating over $\Omega$, and applying the divergence theorem gives

$$
\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,dV_0 \;=\; \int_{\partial\Omega} \mathbf{t}_0 \cdot \mathbf{v}\,dA \;=\; \int_{\partial\omega} \mathbf{t}\cdot\mathbf{v}\,da,
$$

where $\mathbf{t}_0 = \mathbf{P}\mathbf{N}$ is the nominal traction per unit reference area on the reference boundary $\partial\Omega$, and $\mathbf{t}$ is the Cauchy traction per unit current area on the deformed boundary $\partial\omega$. The two surface integrals describe the same physical force, written either on the reference patch or on the current patch. The volume integral of internal stress power equals the surface integral of external traction power.

Applying this to the heart, the deformed boundary $\partial\omega$ splits into two endocardial surfaces $\Gamma_\text{endo}^\text{LV}$ and $\Gamma_\text{endo}^\text{RV}$, an epicardial surface $\Gamma_\text{epi}$, and a basal ring $\Gamma_\text{base}$. On each endocardial surface the blood applies scalar pressure $p$, so the Cauchy traction on the wall is

$$
\mathbf{t} = -p\mathbf{n},
$$

where $\mathbf{n}$ is the outward unit normal of the deformed solid. This is the equal-and-opposite interface force written with the solid-wall sign convention. The power delivered through that surface is

$$
\int_{\Gamma_\text{endo}} \mathbf{t}\cdot\mathbf{v}\,da \;=\; -p \int_{\Gamma_\text{endo}} \mathbf{v}\cdot\mathbf{n}\,da \;=\; p\,\dot{\mathcal{V}},
$$

using the kinematic identity $\dot{\mathcal{V}} = -\int_{\Gamma_\text{endo}}\mathbf{v}\cdot\mathbf{n}\,da$: a wall velocity in the $+\mathbf{n}$ direction points from the solid into the cavity and reduces the enclosed volume. The distributed surface-power integral becomes the familiar chamber quantity $p\dot{\mathcal{V}}$. With this solid-wall sign convention, $p\dot{\mathcal{V}}$ is negative during ejection; the positive stroke-work magnitude reported in cardiology is the opposite sign, $-\oint p\,d\mathcal{V}$. Collecting all four surface contributions,

$$
\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,dV_0 \;=\; p_\text{LV}\,\dot{\mathcal{V}}_\text{LV} \;+\; p_\text{RV}\,\dot{\mathcal{V}}_\text{RV} \;+\; \dot W_\text{epi} \;+\; \dot W_\text{base},
$$

with $\dot W_\text{epi}$ and $\dot W_\text{base}$ the support-power integrals on the remaining non-cavity surfaces. These terms are present because the numerical heart is not floating freely in space. The epicardium and base are supported by Robin-type springs to stabilize the model and represent surrounding tissue constraint. The basal surface also has one fixed displacement component to remove rigid-body motion, but that constraint does no work because the constrained velocity component is zero. After integration over time, the mechanical energy absorbed by the spring supports enters as $W_\text{epi} + W_\text{base}$.

If the epicardium and base were fully free, those support terms would vanish and the cycle-integrated identity would reduce to the sum of the LV and RV pressure-volume work terms,

$$
\int_0^T \!\! \int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,dV_0\,dt \;=\; \oint p_\text{LV}\,d\mathcal{V}_\text{LV} \;+\; \oint p_\text{RV}\,d\mathcal{V}_\text{RV}.
$$

In the actual simulation the support terms are small but included. {numref}`fig-energy-balance` shows the identity closing in practice on the UKB synthetic baseline: the tensor integral and the sum of cavity work and Robin boundary work overlap throughout the cycle, with a final-time residual of $4.76 \times 10^{-5}$ J, or $0.0476$ mJ ($7.0 \times 10^{-5}$ relative to $|W_\text{tensor}(T)| = 0.6806$ J). This residual is the discretization noise floor of the trapezoidal accumulation rather than a physical discrepancy.

For the reference beat in {numref}`fig-energy-balance`, the final tensor work is $-680.59$ mJ, the cavity work is $-680.73$ mJ, and the Robin work is $+0.091$ mJ, about $0.013\%$ of the tensor total. The whole-heart energy budget is therefore dominated by the $p\,\dot{\mathcal{V}}$ exchange between the wall and the blood. The Robin term is a small stabilization cost, not a meaningful store of physiological energy in this run.

```{figure} ../figures/fig_energy_balance_validation.png
:name: fig-energy-balance
:width: 85%

Numerical verification of the energy-balance identity. The cumulative tensor work $\int_0^t\!\!\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,dV_0\,dt'$ (red) and the cumulative cavity pressure work plus Robin support work (black dashed) overlap throughout the cycle. UKB synthetic baseline, final beat of a six-beat sequence; final-time residual $4.8 \times 10^{-5}$ J ($7 \times 10^{-5}$ relative). The cavity contribution is $-680.7$ mJ; the Robin contribution is $+0.09$ mJ, about $0.01\%$ of the tensor total, small enough that the curve labelled "boundary + Robin" is, to graphical accuracy, the cavity $p\,\dot{\mathcal{V}}$ work.
```

This is why tensor work is not just a number the code happens to produce. The model is idealized, but the quantity itself is not invented by the model. It is the standard way that continuum mechanics writes stress doing work through deformation. Integrated over the whole biventricular myocardium, $\mathbf{S}:\dot{\mathbf{E}}$ recovers the pressure-volume work at the cavities, up to the small support terms. It is therefore the model's internal mechanical work measure: local stress-strain power whose spatial integral accounts for the pump work.

The useful consequence is therefore not that every region has its own exact pressure-volume identity. It is that tensor stress-strain work is a local quantity whose integral gives the whole-heart mechanical work. This makes it a natural reference for regional decomposition: the model can integrate the same work density over the LV free wall, RV free wall, and septum. The clinical pressure-strain index is then tested as a measurable approximation to that regional tensor-work density, replacing local stress with chamber pressure and full tensor strain with longitudinal strain.

## Work Density and the Clinical Proxy

The comparison must also keep the units aligned. The finite-element integral $W_\text{int}$ is a regional energy because the local stress-strain density has been integrated through the wall. The clinical pressure-strain index is different: it does not include a regional myocardial volume. It accumulates pressure times a regional strain curve; because pressure has units of energy per volume and strain is dimensionless, the loop area is already a density-like quantity. The finite-element reference is therefore converted to the same units by dividing by the region volume,

$$
w_\text{int}[\Omega_j] = \frac{W_\text{int}[\Omega_j]}{|\Omega_{j,0}|},
\qquad
|\Omega_{j,0}| = \int_{\Omega_j} dV_0.
$$

This keeps the volume information on the finite-element side of the comparison. In the model, $|\Omega_{j,0}|$ is the exact reference volume of the integration region. The clinical-style pressure-strain quantity remains what it is in practice: pressure times strain accumulated around a loop, not an independently measured regional energy in joules.

That is the lineage of pressure-length and pressure-strain work. A pressure-length loop combines chamber pressure with the changing length of a myocardial segment. Early experiments could measure that length using sonomicrometry, in which implanted ultrasonic crystals record distances inside the tissue. This is invasive, but it gave a way to test whether a pressure-length loop behaved like a segmental work index. Pressure-strain loops keep the same idea but replace absolute segment length with strain, a dimensionless deformation measure that can be obtained from imaging. Urheim et al. used longitudinal strain from strain Doppler, and Russell et al. made the method clinically practical by combining speckle-tracking strain with an estimated LV pressure curve {cite}`urheim2005regional,russell2012novel`.

The important point for this thesis is the type of strain being used. The clinical strain input is longitudinal image-based strain, not myocardial fibre strain; standardized speckle-tracking components are longitudinal, circumferential, and radial rather than fibre projections {cite}`voigt2015definitions`. Contemporary clinical practice and consensus are centred on LV global longitudinal strain and RV free-wall longitudinal strain, while pressure-strain myocardial work is built by combining longitudinal strain curves with an estimated or measured pressure curve {cite}`abawi2022noninvasive,sade2023current,thomas2025clinical,lakatos2024right`. The primary clinical proxy in this thesis is therefore a pressure-longitudinal-strain work-density index.

For a region $\Omega_j$ and an assigned pressure $p_j(t)$, the continuous pressure-longitudinal-strain proxy can be written as the signed pressure-strain loop area

$$
w_{\text{PS},ll}[\Omega_j]
= \int_0^T p_j(t)\,\dot{\varepsilon}_{ll,j}(t)\,dt
= \oint p_j\,d\varepsilon_{ll,j}.
$$

In the sampled simulation output, this is accumulated with the same trapezoidal idea used for the tensor work:

$$
w_{\text{PS},ll}[\Omega_j] \approx \sum_{i=1}^{N} \bar{p}_j(t_i) \, \Delta\varepsilon_{ll,j}(t_i),
$$

where $\bar p_j(t_i)=\tfrac{1}{2}\left(p_j(t_i)+p_j(t_{i-1})\right)$ is the average pressure over the time step and $\Delta\varepsilon_{ll,j}(t_i)=\varepsilon_{ll,j}(t_i)-\varepsilon_{ll,j}(t_{i-1})$ is the regional longitudinal strain increment. No regional volume factor appears. If one wanted an absolute energy estimate inside the finite-element model, this index could be multiplied by the known reference volume $|\Omega_{j,0}|$. That is not how the clinical index is obtained, however, and it would mix an exact model-side quantity into the clinical-side proxy. The comparisons in this thesis therefore match $w_{\text{PS},ll}$ against the tensor work density $w_\text{int}$.

For the free wall of either ventricle, the adjacent cavity pressure is the least ambiguous pressure assignment: the LV free wall is paired with $p_\text{LV}$, and the RV free wall with $p_\text{RV}$. This does not assume that the proxy must work; it only states the pressure choice being tested. The septum is different. It is shared tissue, with LV pressure on one side and RV pressure on the other. Assigning one pressure to the septum is therefore already a mechanical assumption. The tested choices are $p_\text{LV}$ alone, $p_\text{RV}$ alone, the pressure difference $p_\text{LV} - p_\text{RV}$, and two-sided choices such as the mean of $p_\text{LV}$ and $p_\text{RV}$.

## Why Pressure Is Not Expected To Equal Stress

The pressure-for-stress substitution deserves a careful pause because pressure and stress have the same physical units. It can therefore look suspicious when the model reports tissue stresses or stress-strain work-density scales that are much larger than the cavity pressure. The reason is that cavity pressure is only one boundary traction component. At the endocardial surface the Cauchy traction condition is

$$
\boldsymbol{\sigma}\mathbf{n} = -p\mathbf{n},
$$

so the pressure fixes the normal force per deformed area applied by the blood to the wall. It does not say that every stress component inside the myocardium equals $p$. In particular, it does not set the fibre stress, circumferential stress, longitudinal stress, or shear stresses. Those components are whatever they must be for the curved, anisotropic, actively contracting wall to satisfy mechanical equilibrium with the imposed cavity volumes, material law, fibre architecture, and boundary supports.

A simple pressurized cylinder already shows why internal tensile stress can exceed pressure. For a thin cylindrical wall with radius $r$ and thickness $h$, force balance gives the hoop-stress scale

$$
\sigma_{\theta\theta} \approx p\,\frac{r}{h},
$$

while a spherical wall gives $\sigma_{\theta\theta}\approx p\,r/(2h)$. Thus the stress scale is not just pressure; it is pressure multiplied by a geometric lever arm. If $r/h$ is three to five, wall stress components of several times the cavity pressure are expected even before adding active contraction. The same conclusion holds in the thick-wall cylinder solution. For inner radius $r_i$, outer radius $r_o$, internal pressure $p$, and zero external pressure, the inner-wall hoop stress is

$$
\sigma_{\theta\theta}(r_i)
= p\,\frac{r_i^2+r_o^2}{r_o^2-r_i^2}.
$$

For example, if $r_i=20$ mm and $r_o=30$ mm, this factor is about $2.6$. This is only a passive pressure-inflation scale. In the beating-heart model, active fibre tension, anisotropic stiffness, wall curvature, basal and epicardial support, and ventricular interaction can all further change the local tensor components. Some stress is also internally balanced within the wall rather than appearing one-for-one as cavity pressure.

This is not a contradiction with pressure-volume work. The whole-heart energy balance says that the integral of stress power over the myocardium matches the boundary pressure-volume work, up to the small support terms. It does not require the local stress tensor to have the same magnitude as cavity pressure at every point. A high local fibre stress can occur with little instantaneous volume change, can be balanced by other stress components, or can contribute differently depending on the local strain increment. The pressure-strain proxy should therefore not be expected to reproduce absolute tensor-work density. The defensible test is more limited: whether a chosen cavity-pressure signal preserves useful regional ratios or loading trends after this severe reduction from a tensor field to one scalar pressure.

## Literature Gap and Mechanical Test

Clinical studies have usually tested pressure-strain work against quantities that matter in patients. That is the right thing for clinical studies to do. Early pressure-length and pressure-strain studies compared loop areas with invasive segment-length measurements or sonomicrometry-based strain estimates {cite}`forrester1974pressure_length,tyberg1974segmental,urheim2005regional`. Russell et al. validated the non-invasive pressure-strain construction against invasive pressure measurements, a geometry-adjusted work estimate, and FDG-PET glucose uptake, an imaging marker of regional metabolic activity, in patients with left bundle branch block {cite}`russell2012novel`. Delhaas et al. {cite}`delhaas1994regional` estimated regional fibre stress-strain work and compared it with regional blood flow and oxygen demand, while recent RV work by Lakatos et al. related an RV pressure-strain index to invasive pressure-volume-derived contractility {cite}`lakatos2024right`.

These comparisons are useful, but they do not all test the same thing. Glucose uptake and oxygen use ask whether the tissue paid an energetic cost. Contractility asks whether the ventricle can generate pressure for its loading conditions. Invasive segment-length measurements and pressure-strain loops ask whether an accessible loop area behaves like a regional work index. These are downstream clinical and physiological questions. The mechanical question here is narrower: does chamber pressure times a scalar strain increment preserve the local stress-strain work density that motivates calling the quantity work?

This thesis uses model-resolved stress-strain work density as the reference because the simulation can answer that mechanical question directly. This does not mean tensor work density captures every biological cost of contraction. Oxygen use and glucose uptake also include basal metabolism, excitation-contraction coupling, ion handling, heat, and substrate effects. It means that, inside the finite-element model, the hidden mechanical fields are known. The same coupled system produces the pressures, strains, geometry, stresses, tensor work, and tensor work density. That lets us test the pressure-strain proxy against the quantity it most directly claims to approximate.

Put more plainly: clinical studies ask whether pressure-strain work is useful. This thesis asks whether it is mechanically honest. The model is not a replacement for clinical validation. It is a controlled test of the approximation that clinical validation cannot isolate, because in patients geometry, pressure estimation, segmentation, material properties, remodelling, and disease history all change together.

Finite-element stress-strain work has also been used before. Later studies used fibre or tensor work to analyse MRI-based LV mechanics, coronary perfusion, biventricular geometry and fibre architecture, LVAD interaction, and CRT response {cite}`wang2012myocardial,namani2020effects,pluijmert2017determinants,ahmadbakir2018multiphysics,craine2024successful`. Finsberg et al. {cite}`finsberg2019assessment` is the closest direct predecessor for the proxy-versus-model comparison: in patient-specific LV mechanics models, pressure-strain loops preserved useful relative information while underestimating absolute model-resolved work and, in a dyssynchronous case, even disagreeing with stress-strain loop orientation in the septum. Craine et al. {cite}`craine2024successful` likewise compared model-resolved regional work with simplified estimates using ventricular pressure as a stress surrogate.

The gap left by this literature is not that regional work has never been modelled, or that pressure-strain loops have never been tested. The gap is narrower. The right-ventricular side of the pressure-strain approximation has much less model-resolved validation than the LV, and the septum adds a separate pressure-assignment problem. Patient-specific biventricular finite-element models have been used to estimate regional stress and contractility in healthy subjects and in pulmonary arterial hypertension {cite}`finsberg2018efficient,finsberg2019computational`, and clinical studies have begun applying pressure-strain methods to RV work in pulmonary hypertension {cite}`wang2022apply,lakatos2024right`. The remaining question is how the clinical-style pressure simplification behaves when the RV free wall and septum are checked against tensor work in the same controlled biventricular model.

This controlled setting is useful because the comparison removes several confounders that would be inseparable in patients: imaging noise, uncertain pressure scaling, segmentation differences, material variation, and disease remodelling. It does not replace clinical validation. It isolates the mechanical approximation itself. If a pressure assignment fails or changes rank here, the problem is not only measurement noise; it is also an ambiguity in the pressure simplification.

Here "pressure-loading sweep" has a specific meaning. It is a set of repeated simulations of the same finite-element heart under different calibrated circulation states. The biventricular mesh, passive material law, fibre field, active-tension waveform, basal support, and cavity-volume coupling are held fixed. What changes is the zero-dimensional circulation calibration used to drive the same mechanics model through a range of RV pressure loads. The main high-resolution sweep contains 16 nominal RV-pressure cases. The achieved coupled pressures, not the nominal case names, define the analysis axis for the proxy tests: peak RV pressure spans roughly 31--89 mmHg while peak LV pressure remains comparatively stable, about 100--109 mmHg. The calibration chapter explains how those states are generated and why imperfectly matched targets are treated as calibration limits rather than biological results.

The finite-element model can also form a fibre-aligned diagnostic in which the longitudinal increment $\Delta\varepsilon_{ll}$ is replaced by the fibre increment $\Delta E_{ff} = \Delta\mathbf{E}:(\mathbf{f}_0 \otimes \mathbf{f}_0)$. This is worth checking because active contraction in the model acts along the myocardial fibres, and the passive material is also stiffest in the fibre architecture. If any single strain direction is going to retain most of the tensor-work information, fibre strain is the most favourable model-side candidate. The notation difference is deliberate: $E_{ff}$ is a component of the Green-Lagrange strain tensor projected onto the local fibre direction, while $\varepsilon_{ll}$ denotes the scalar longitudinal strain used by the clinical-style proxy. The fibre-aligned quantity is not itself a clinical pressure-strain proxy, because speckle-tracking myocardial work does not measure fibre strain. It is used only sparingly in the results as a model-side check on how much of the error comes from the clinical strain-direction reduction, as opposed to the pressure-for-stress substitution.

One way to see why exact magnitude agreement is not the right target is to remove mechanical information step by step. This sequence is the simplification cascade used in the next two figures: full tensor work density, then fibre-direction stress-strain work, then cavity pressure with fibre strain, and finally cavity pressure with longitudinal strain. {numref}`fig-cascade` shows the cumulative work-density values for these steps in the UKB synthetic baseline. For this diagnostic only, the myocardium is split into LV-side and RV-side territories by solving a Laplace problem with value zero on the LV endocardium and one on the RV endocardium, then cutting the resulting coordinate at $0.5$. This same coordinate idea is introduced in the model chapter for fibre assignment and returns in the results chapter as a through-wall septal pressure diagnostic. The pressure-based steps use the corresponding cavity pressure, denoted $p_\text{cav}$. All curves are plotted as work densities; for the pressure-based terms this is equivalent to using regional mean strain increments, because the cavity pressure is spatially uniform. The main effect is not subtle: replacing fibre stress by cavity pressure produces a large loss of absolute magnitude, exactly the kind of scale loss expected when an internal tensile stress component is replaced by a boundary pressure. The final pressure-longitudinal-strain proxy is therefore not expected to match tensor work density by mean-squared error or absolute scale. The useful questions are instead whether the proxy preserves regional work-density ratios and whether it ranks cases consistently across the pressure-loading sweep just defined.

```{figure} ../figures/fig_cascade_cumulative.png
:name: fig-cascade
:width: 80%

Cascade of work-density measures from the full tensor contraction down to the clinical pressure-strain proxy, shown for the LV-side tau-split territory on the UKB synthetic baseline. In this diagnostic split, every myocardial cell is assigned to either the LV-side or RV-side territory, so this is not the anatomical LV free wall defined in the geometry chapter and used in the later free-wall ratio tests. $\mathbf{S}:\dot{\mathbf{E}}$ is the full double contraction; $S_{ff}\,\dot E_{ff}$ is the fibre-normal component alone; $p_\text{cav}\,\dot E_{ff}$ is a model-side intermediate that substitutes cavity pressure for the fibre stress; $p_\text{cav}\,\dot\varepsilon_{ll}$ is the clinical pressure-longitudinal-strain proxy. End-of-cycle plateau values: $-8.4$, $-7.4$, $-1.9$, $-1.5$ kPa. The pressure-for-stress substitution accounts for the bulk of the magnitude loss.
```

The same simplification can also be viewed as a sequence of loop shapes. The full tensor contraction $\mathbf{S}:\dot{\mathbf{E}}$ has no single two-axis loop, because both stress and strain are tensors. Once the work is projected onto one direction, however, scalar loops can be drawn: fibre stress versus fibre strain, cavity pressure versus fibre strain, and cavity pressure versus longitudinal strain. In each case the vertical axis has units of stress or pressure and the horizontal axis is dimensionless strain, so the signed loop area has units of pressure, equivalently work density. As the beat moves around the loop, low-pressure filling and relaxation occupy the lower part of the plot, while contraction and ejection form the high-pressure limb. {numref}`fig-cascade-loops` shows that the pressure substitution does not merely rescale the loop; it changes its shape and collapses the stress axis from tissue-level fibre stress to chamber pressure. The final longitudinal loop is therefore not just a smaller version of the fibre stress-strain loop. It is a different projection of the same cardiac cycle.

This connects the two cascade figures directly. The curves in {numref}`fig-cascade` are cumulative signed areas: at each time point they show how much area has been swept out by the corresponding loop up to that point. The final plateau value of each curve is therefore the signed loop area, or equivalently the work density for that simplification.

```{figure} ../figures/fig_cascade_loops.png
:name: fig-cascade-loops
:width: 95%

Loop-space view of the simplification cascade on the UKB synthetic baseline. Rows show the LV-side and RV-side tau-split territories; columns show the fibre stress-strain loop $S_{ff}$ versus $E_{ff}$, the pressure-fibre-strain loop $p_\text{cav}$ versus $E_{ff}$, and the clinical pressure-longitudinal-strain loop $p_\text{cav}$ versus $\varepsilon_{ll}$. Arrows indicate the direction of time around the cardiac cycle, and the marked point is the first sampled state. The signed areas inside these loops are the final accumulated work-density values shown in {numref}`fig-cascade`. The figure makes visible how the pressure-for-stress substitution and the strain-direction reduction change the loop geometry, not only its final accumulated area.
```

## Scientific Question

The scientific question has two parts. First, in the ventricular free walls, does the adjacent-pressure longitudinal-strain proxy $w_{\text{PS},ll}[\Omega_j]$ track the tensor work density $w_\text{int}[\Omega_j]$? This is especially important in the RV free wall, where the pressure-strain approximation has much less tensor-work validation than in the LV. Second, in the interventricular septum, which pressure choice comes closest to the tensor work density: an LV-like pressure, an RV-like pressure, the pressure difference, or a two-sided pressure that includes both cavities? In both cases, does the answer change when RV pressure is raised?

The word "track" is evaluated in two complementary ways. The first is a sweep-ranking question: across the completed pressure-loading cases, does the proxy increase and decrease with the model-resolved tensor work density along the achieved RV-pressure path? This is measured with Pearson correlation $r$; keeping the sign is useful, so the results report $r$ rather than only $R^2$. The second is a magnitude-distribution question: within a given simulation, does the proxy preserve the regional work-density ratios between the LV free wall, RV free wall, and septum? This is measured with ratio errors. Both views are needed, because a proxy can correlate well across one loading path while still giving the wrong regional work-density balance inside the heart.

The expectations are also simple. The simplification cascade in {numref}`fig-cascade` and {numref}`fig-cascade-loops` shows that the pressure-strain proxy should not be expected to preserve absolute tensor-work magnitude. For the RV free wall, the question is instead whether the adjacent-pressure proxy still preserves useful trends and LV/RV work-density balance in a region that is thinner, more crescent-shaped, normally lower-pressure, and less directly validated than the LV. For the septum, pressure choice should matter less in health, because $p_\text{RV}$ is small relative to $p_\text{LV}$. In right-ventricular pressure overload this changes. The septum is then no longer close to an LV-only wall: pressure difference should matter for septal shape and motion, while two-sided pressure choices may matter for septal work-density magnitude. The aim of the model is to test these assumptions under controlled loading, while keeping the geometry and material model fixed.

Answering this question requires a model that simultaneously produces physiologically realistic cavity pressures and volume dynamics for both ventricles — which a stand-alone zero-dimensional circulation model can provide — and resolves the stress and strain fields inside the tissue throughout the cardiac cycle — which only a spatially resolved three-dimensional mechanics model can achieve. The coupled finite element and circulation framework described in the following chapter is built specifically to provide both.
