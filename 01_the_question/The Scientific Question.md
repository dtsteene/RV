# Mechanical Work and the Scientific Question

Before asking whether pressure-strain work is a good proxy, we need to say what it is a proxy for. In this thesis the answer is local mechanical work density in the myocardial wall. The finite-element model knows the stress and strain at each point in the tissue, so it can compute this quantity directly. Over the whole biventricular myocardium, the same stress-strain work is tied to the familiar pressure-volume work at the cavity boundaries. The clinical pressure-strain index enters only after that point is clear: it is a measurable shortcut for a mechanical quantity that cannot normally be measured inside a patient.

Let $\Omega$ denote the reference-configuration biventricular myocardial domain, and let $\Omega_j \subseteq \Omega$ be a reference-configuration subregion (a free-wall region or the septum). Following Finsberg et al. {cite}`finsberg2019assessment`, the total internal work in $\Omega_j$ over a cardiac cycle is

$$
W_\text{int}[\Omega_j] = \int_0^T \int_{\Omega_j} \mathbf{S}(t, \mathbf{X}) : \dot{\mathbf{E}}(t, \mathbf{X}) \, d\mathbf{X} \, dt,
$$

where $\mathbf{S}$ is the second Piola-Kirchhoff stress tensor, $\mathbf{E}$ is the Green-Lagrange strain tensor, and the colon denotes the double contraction $\mathbf{S} : \dot{\mathbf{E}} = S_{ij} \dot{E}_{ij}$. This is the reference-configuration form of stress power; the same power could be written in the current configuration as $\boldsymbol{\sigma}:\mathbf{d}\,dv$, using Cauchy stress and the rate-of-deformation tensor. The pair $\mathbf{S}$ and $\mathbf{E}$ is used here because the finite-element integration is carried out on the fixed reference mesh. In discrete form, sampling the simulation at $N+1$ snapshots $t_0, t_1, \ldots, t_N$ over the cycle and applying the trapezoidal rule,

$$
W_\text{int}[\Omega_j] \approx \sum_{i=1}^{N} \int_{\Omega_j} \bar{\mathbf{S}}(t_i, \mathbf{X}) : d\mathbf{E}(t_i, \mathbf{X}) \, d\mathbf{X},
$$

with $\bar{\mathbf{S}}(t_i) = \tfrac{1}{2}(\mathbf{S}(t_i) + \mathbf{S}(t_{i-1}))$ the average stress and $d\mathbf{E}(t_i) = \mathbf{E}(t_i) - \mathbf{E}(t_{i-1})$ the strain increment at step $i$.

The next point is that this internal work is not disconnected from the work done on the blood. Taken over the whole biventricular myocardium, and neglecting inertia at cardiac timescales, the integral $\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,d\mathbf{X}$ equals the power exchanged at the cavity surfaces plus any work done by non-cavity supports. If the epicardium and base did no work, the cycle-integrated identity would reduce to

$$
\int_0^T \!\! \int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,d\mathbf{X}\,dt \;=\; \oint P_\text{LV}\,dV_\text{LV} \;+\; \oint P_\text{RV}\,dV_\text{RV}.
$$

The identity says that the same signed power exchange can be computed in two equivalent ways: from stress and strain inside the myocardium, or from tractions and velocities at the chamber boundaries. The identity is stated from the viewpoint of the solid wall. With the normal convention adopted below (outward normal of the solid, pointing into the cavity), the rate $P\dot V$ is negative during chamber ejection and positive during filling. The positive stroke-work magnitude traditionally reported in cardiology is the opposite sign, $-\oint P\,dV$, because it is the work done by the ventricle on the blood rather than the pressure work done by the blood on the wall. The signed solid-wall form is used throughout the derivation and in all comparisons between tensor work and cavity work that follow.

The derivation is included to fix the sign and the units, but the idea is simple: stress power inside the wall must equal traction power on its boundary. First, from the kinematic definition $\dot{\mathbf{E}} = \tfrac{1}{2}(\dot{\mathbf{F}}^T\mathbf{F} + \mathbf{F}^T\dot{\mathbf{F}})$, the symmetry of $\mathbf{S}$, and the relation $\mathbf{P} = \mathbf{F}\mathbf{S}$ between the second and first Piola-Kirchhoff stresses, a direct index calculation gives the pointwise identity $\mathbf{S}:\dot{\mathbf{E}} = \mathbf{P}:\dot{\mathbf{F}}$. The second form is useful because $\dot{\mathbf{F}} = \nabla_\mathbf{X}\mathbf{v}$ is a material gradient of the velocity $\mathbf{v} = \dot{\mathbf{x}}$, which integration by parts turns into a boundary term. In the quasi-static limit, the reference-configuration momentum balance reduces to $\text{Div}\,\mathbf{P} = \mathbf{0}$; taking the inner product with $\mathbf{v}$, integrating over $\Omega$, and applying the divergence theorem gives

$$
\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,d\mathbf{X} \;=\; \int_{\partial\Omega} \mathbf{t}_0 \cdot \mathbf{v}\,dA \;=\; \int_{\partial\omega} \mathbf{t}\cdot\mathbf{v}\,da,
$$

where $\mathbf{t}_0 = \mathbf{P}\mathbf{N}$ is the nominal traction per unit reference area on the reference boundary $\partial\Omega$, and $\mathbf{t}$ is the Cauchy traction per unit current area on the deformed boundary $\partial\omega$. The two surface integrals describe the same physical force, written either on the reference patch or on the current patch. The volume integral of internal stress power equals the surface integral of external traction power.

The third step applies this to the heart. The deformed boundary $\partial\omega$ splits into two endocardial surfaces $\Gamma_\text{endo}^\text{LV}$ and $\Gamma_\text{endo}^\text{RV}$, an epicardial surface $\Gamma_\text{epi}$, and a basal ring $\Gamma_\text{base}$. On each endocardial surface the blood applies pressure $P$, so the Cauchy traction on the wall is

$$
\mathbf{t} = -P\mathbf{n},
$$

where $\mathbf{n}$ is the outward unit normal of the deformed solid. The power delivered through that surface is

$$
\int_{\Gamma_\text{endo}} \mathbf{t}\cdot\mathbf{v}\,da \;=\; -P \int_{\Gamma_\text{endo}} \mathbf{v}\cdot\mathbf{n}\,da \;=\; P\,\dot V,
$$

using the kinematic identity $\dot V = -\int_{\Gamma_\text{endo}}\mathbf{v}\cdot\mathbf{n}\,da$: a wall velocity in the $+\mathbf{n}$ direction points from the solid into the cavity and reduces the enclosed volume. The distributed surface-power integral becomes the familiar chamber quantity $P\dot V$. Collecting all four surface contributions,

$$
\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,d\mathbf{X} \;=\; P_\text{LV}\,\dot V_\text{LV} \;+\; P_\text{RV}\,\dot V_\text{RV} \;+\; W_\text{epi} \;+\; W_\text{base},
$$

with $W_\text{epi}$ and $W_\text{base}$ the traction-velocity integrals on the remaining non-cavity surfaces. These terms are present because the numerical heart is not floating freely in space. The epicardium and base are supported by Robin-type springs to stabilize the model and represent surrounding tissue constraint. The basal surface also has one fixed displacement component to remove a rigid-body mode, but that constraint does no work because the constrained velocity component is zero. The mechanical energy absorbed by the spring supports enters $W_\text{epi} + W_\text{base}$.

If the epicardium and base were fully free, those support terms would vanish and the cycle integral would reduce to the simple cavity-work identity above. In the actual simulation they are small but included. {numref}`fig-energy-balance` shows the identity closing in practice on the UKB synthetic baseline: the tensor integral and the sum of cavity work and Robin boundary work overlap throughout the cycle, with a final-time residual of order $10^{-5}$ J (relative error $\sim 10^{-4}$). This residual is the discretization noise floor of the trapezoidal accumulation rather than a physical discrepancy.

For the reference beat in {numref}`fig-energy-balance`, the cavity work is $-680.7$ mJ and the Robin work is $+0.09$ mJ, about $0.01\%$ of the tensor total. The whole-heart energy budget is therefore dominated by the $P\,\dot V$ exchange between the wall and the blood. The Robin term is a small stabilization cost, not a meaningful store of physiological energy in this run.

```{figure} ../figures/fig_energy_balance_validation.png
:name: fig-energy-balance
:width: 85%

Numerical verification of the energy-balance identity. The cumulative tensor work $\int_0^t\!\!\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,d\mathbf{X}\,dt'$ (red) and the total boundary contribution $\int_{\partial\omega} \mathbf{t}\cdot\mathbf{v}\,da\,dt' + W_\text{Robin}$ (black dashed) overlap throughout the cycle. UKB synthetic baseline, final beat of a six-beat sequence; final-time residual $4.8 \times 10^{-5}$ J ($7 \times 10^{-5}$ relative). The cavity contribution is $-680.7$ mJ; the Robin contribution is $+0.09$ mJ, about $0.01\%$ of the tensor total — small enough that the curve labelled "boundary + Robin" is, to graphical accuracy, the cavity $P\,\dot V$ work.
```

This is why tensor work is not just a number the code happens to produce. The endocardial interface transmits force between wall and blood: the blood pushes on the wall, and the wall pushes back on the blood. The stresses inside the wall carry that load through the tissue. The model is idealized, but the quantity itself is not invented by the model. It is the standard way that continuum mechanics writes stress doing work through deformation. Integrated over the whole biventricular myocardium, $\mathbf{S}:\dot{\mathbf{E}}$ recovers the pressure-volume work at the cavities, up to the small support terms. It is the model's internal mechanical work density: local stress-strain power whose spatial integral accounts for the pump work.

This claim still has an important limit. The identity is a whole-heart identity, not a regional one. No exact version exists for a subregion $\Omega_j$ on its own, because a subregion exchanges forces with neighbouring tissue across internal material interfaces. The internal work over the septum or a free wall is therefore not, in general, the pressure-volume work of a single chamber. This keeps the claim honest. Tensor work density is the model's local mechanical work density, but a regional pressure-strain loop is not a local pressure-volume identity. It is a practical approximation motivated by the global energy balance and by the clinical accessibility of pressure and strain.

This distinction also fixes the units. Clinical echocardiographic work indices do not first estimate a regional myocardial volume and then compute energy in joules. They accumulate pressure times strain, so the result has units of pressure, or equivalently energy per unit volume. The finite-element model does know the regional reference volume exactly. To compare like with like, this thesis compares the clinical pressure-strain index with volume-normalized tensor work,

$$
w_\text{int}[\Omega_j] = \frac{W_\text{int}[\Omega_j]}{V_j},
\qquad
V_j = \int_{\Omega_j} d\mathbf{X}.
$$

This keeps the volume information on the finite-element side of the comparison. In the model, $V_j$ is the exact reference volume of the integration region. The clinical-style pressure-strain quantity remains what it is in practice: pressure times strain accumulated around a loop, not an independently measured regional energy in joules.

The clinical shortcut removes two pieces of information. First, it uses chamber pressure where a mechanical work calculation would use local myocardial stress. Second, it uses one image-based strain component where a mechanical work calculation would use the full strain tensor. This is not a flaw in clinical imaging; it is the price of measuring something useful in a patient. The stress tensor inside the wall is not measurable in routine care, and the full strain tensor is not routinely available either. What clinicians can often obtain is a pressure scale and a longitudinal strain curve.

That is the lineage of pressure-length and pressure-strain work. Pressure-length loops were introduced as approximate indices of segmental work, with the important caveat that a true regional mechanical measure would require local stress rather than chamber pressure {cite}`forrester1974pressure_length,tyberg1974segmental`. Urheim et al. replaced segment length with longitudinal strain from strain Doppler, and Russell et al. made the method clinically practical by combining speckle-tracking strain with an estimated LV pressure curve {cite}`urheim2005regional,russell2012novel`. The important point for this thesis is the type of strain being used. The clinical strain input is longitudinal image-based strain, not myocardial fibre strain; standardized speckle-tracking components are longitudinal, circumferential, and radial rather than fibre projections {cite}`voigt2015definitions`. Contemporary clinical practice and consensus are centred on LV global longitudinal strain and RV free-wall longitudinal strain, while pressure-strain myocardial work is built by combining longitudinal strain curves with an estimated or measured pressure curve {cite}`abawi2022noninvasive,sade2023current,thomas2025clinical,lakatos2024right`. The primary clinical proxy in this thesis is therefore a pressure-longitudinal-strain work-density index.

For a region $\Omega_j$, the clinical proxy used in this thesis is written without a regional volume factor:

$$
w_{\text{PS},ll}[\Omega_j] \approx \sum_{i=1}^{N} \bar{P}_j(t_i) \, d\varepsilon_{ll,j}(t_i),
$$

where $d\varepsilon_{ll,j}$ is the volume-averaged longitudinal strain increment and $P_j$ is the pressure assigned to that region. If one wanted an absolute energy estimate inside the finite-element model, this index could be multiplied by the known reference volume $V_j$. That is not how the clinical index is obtained, however, and it would mix an exact model-side quantity into the clinical-side proxy. The comparisons in this thesis therefore match $w_{\text{PS},ll}$ against the tensor work density $w_\text{int}$.

For the free wall of either ventricle, the pressure choice is straightforward: the LV free wall uses $P_\text{LV}$, and the RV free wall uses $P_\text{RV}$. The septum is different. It is shared tissue, with LV pressure on one side and RV pressure on the other. Assigning one pressure to the septum is therefore already a mechanical assumption. The tested choices are $P_\text{LV}$ alone, $P_\text{RV}$ alone, the pressure difference $P_\text{LV} - P_\text{RV}$, and two-sided choices such as the mean of $P_\text{LV}$ and $P_\text{RV}$.

Clinical studies have usually tested pressure-strain work against quantities that matter in patients. That is the right thing for clinical studies to do. Early pressure-length and pressure-strain studies compared loop areas with invasive pressure-length or sonomicrometry-based measurements {cite}`forrester1974pressure_length,tyberg1974segmental,urheim2005regional`. Russell et al. validated the non-invasive pressure-strain construction against invasive pressure measurements, a geometry-adjusted work estimate, and FDG-PET glucose metabolism in patients with left bundle branch block {cite}`russell2012novel`. Delhaas et al. {cite}`delhaas1994regional` estimated regional fibre stress-strain work and compared it with regional blood flow and oxygen demand, while recent RV work by Lakatos et al. related an RV pressure-strain index to invasive pressure-volume-derived contractility {cite}`lakatos2024right`.

These comparisons are useful, but they do not all test the same thing. Glucose uptake and oxygen use ask whether the tissue paid an energetic cost. Contractility asks whether the ventricle can generate pressure for its loading conditions. Sonomicrometry and pressure-strain loops ask whether a measurable loop area behaves like a regional work index. These are downstream clinical and physiological questions. The mechanical question is more direct: does chamber pressure times a scalar strain increment preserve the local stress-strain work density that gives the index its name?

This thesis uses model-resolved stress-strain work density as the reference because the simulation can answer that mechanical question directly. This does not mean tensor work density captures every biological cost of contraction. Oxygen use and glucose uptake also include basal metabolism, excitation-contraction coupling, ion handling, heat, and substrate effects. It means that, inside the finite-element model, the hidden mechanical fields are known. The same coupled system produces the pressures, strains, geometry, stresses, tensor work, and tensor work density. That lets us test the pressure-strain proxy against the quantity it most directly claims to approximate.

Put more plainly: clinical studies ask whether pressure-strain work is useful. This thesis asks whether it is mechanically honest. The model is not a replacement for clinical validation. It is a controlled test of the approximation that clinical validation cannot isolate, because in patients geometry, pressure estimation, segmentation, material properties, remodelling, and disease history all change together.

Finite-element stress-strain work has also been used before. Later studies used fibre or tensor work to analyse MRI-based LV mechanics, coronary perfusion, biventricular geometry and fibre architecture, LVAD interaction, and CRT response {cite}`wang2012myocardial,namani2020effects,pluijmert2017determinants,ahmadbakir2018multiphysics,craine2024successful`. Finsberg et al. {cite}`finsberg2019assessment` is the closest direct predecessor for the proxy-versus-model comparison: in patient-specific LV mechanics models, pressure-strain loops preserved useful relative information while underestimating absolute model-resolved work and, in a dyssynchronous case, even disagreeing with stress-strain loop orientation in the septum. Craine et al. {cite}`craine2024successful` likewise compared model-resolved regional work with simplified estimates using ventricular pressure as a stress surrogate.

The gap left by this literature is not that regional work has never been modelled, or that pressure-strain loops have never been tested. The gap is narrower. The right-ventricular side of the pressure-strain approximation has much less model-resolved validation than the LV, and the septum adds a separate pressure-assignment problem. Patient-specific biventricular finite-element models have been used to estimate regional stress and contractility in healthy subjects and in pulmonary arterial hypertension {cite}`finsberg2018efficient,finsberg2019computational`, and clinical studies have begun applying pressure-strain methods to RV work in pulmonary hypertension {cite}`wang2022apply,lakatos2024right`. Lakatos et al. are especially relevant here: they found that RV pressure-strain myocardial work derived from RV pressure and 3D echocardiographic GLS correlated with invasive RV contractility, whereas RV GLS and ejection fraction mainly reflected loading and coupling {cite}`lakatos2024right`. That makes the RV free wall a useful bridge between clinical pressure-strain work and model-resolved mechanics. The interventricular septum then asks a harder pressure-choice question: it is shared tissue loaded by both chambers, so LV pressure, RV pressure, transmural pressure, and two-sided pressure choices encode different mechanical assumptions.

This is a favourable test for the pressure-strain proxy. There is no imaging noise, no uncertain blood-pressure estimate, and no unmeasured patient remodelling hidden in the comparison. If a pressure assignment fails or changes rank even here, the problem is not just measurement noise. It is an ambiguity in the pressure simplification itself. In real patients the same approximation would have to survive additional uncertainty on top of that ambiguity.

The finite-element model can also form a fibre-aligned diagnostic in which the longitudinal increment $d\varepsilon_{ll}$ is replaced by the fibre increment $dE_{ff} = d\mathbf{E}:(\mathbf{f}_0 \otimes \mathbf{f}_0)$. This quantity is not a clinical pressure-strain proxy, because speckle-tracking myocardial work does not measure fibre strain. It is used only sparingly in the results as a model-side check on how much of the error comes from the clinical strain-direction reduction, as opposed to the pressure-for-stress substitution.

One way to see what the proxy loses is to remove mechanical information step by step. {numref}`fig-cascade` traces three steps on the UKB synthetic baseline for the LV. The gap between the full contraction $\mathbf{S}:\dot{\mathbf{E}}$ and the fibre-normal term $S_{ff}\,\dot E_{ff}$ is the cross-fibre and shear work density discarded by projecting onto one direction; visually it is small. The much larger drop, from $S_{ff}\,\dot E_{ff}$ to $P_\text{cav}\,\dot E_{ff}$, is the pressure-for-stress substitution and accounts for most of the magnitude loss. The final, smaller step from $P_\text{cav}\,\dot E_{ff}$ to $P_\text{cav}\,\dot\varepsilon_{ll}$ is the strain-component reduction that follows from clinical echocardiographic measurement. Taken together these three simplifications leave the final clinical proxy at roughly a fifth of the full tensor work density in the LV on this case. The same cascade in the RV is qualitatively similar but with smaller absolute magnitudes and an even larger fractional loss at the pressure-for-stress step; this is taken up in the results chapter. The septum is the difficult case, because it is loaded by both ventricles, which makes the pressure-for-stress substitution ambiguous before any numbers are computed.

```{figure} ../figures/fig_cascade_cumulative.png
:name: fig-cascade
:width: 80%

Cascade of work-density measures from the full tensor contraction down to the clinical pressure-strain proxy, shown for the LV on the UKB synthetic baseline. $\mathbf{S}:\dot{\mathbf{E}}$ is the full double contraction; $S_{ff}\,\dot E_{ff}$ is the fibre-normal component alone; $P_\text{cav}\,\dot E_{ff}$ is a model-side intermediate that substitutes cavity pressure for the fibre stress; $P_\text{cav}\,\dot\varepsilon_{ll}$ is the clinical pressure-longitudinal-strain proxy. End-of-cycle plateau values: $-8.4$, $-7.4$, $-1.9$, $-1.5$ kPa. The pressure-for-stress substitution accounts for the bulk of the magnitude loss.
```

The same simplification can also be viewed as a sequence of loop shapes. The full tensor contraction is not itself a two-axis scalar loop, but the fibre-stress loop, the pressure-fibre-strain loop, and the pressure-longitudinal-strain loop can be drawn directly. {numref}`fig-cascade-loops` shows that the pressure substitution does not merely rescale the loop; it changes its shape and collapses the stress axis from tissue-level fibre stress to chamber pressure. The final longitudinal loop is therefore not just a smaller version of the fibre stress-strain loop. It is a different projection of the same cardiac cycle.

```{figure} ../figures/fig_cascade_loops.png
:name: fig-cascade-loops
:width: 95%

Loop-space view of the simplification cascade on the UKB synthetic baseline. Rows show LV and RV territories; columns show the fibre stress-strain loop $S_{ff}$ versus $E_{ff}$, the pressure-fibre-strain loop $P_\text{cav}$ versus $E_{ff}$, and the clinical pressure-longitudinal-strain loop $P_\text{cav}$ versus $\varepsilon_{ll}$. The figure makes visible how the pressure-for-stress substitution and the strain-direction reduction change the loop geometry, not only its final accumulated area.
```

The scientific question has two parts. First, in the ventricular free walls, does the adjacent-pressure longitudinal-strain proxy $w_{\text{PS},ll}[\Omega_j]$ track the tensor work density $w_\text{int}[\Omega_j]$? This is especially important in the RV free wall, where the pressure-strain approximation has much less tensor-work validation than in the LV. Second, in the interventricular septum, which pressure choice comes closest to the tensor work density: an LV-like pressure, an RV-like pressure, the pressure difference, or a two-sided pressure that includes both cavities? In both cases, does the answer change when RV pressure is raised?

The expectations are also simple. For the RV free wall, the proxy may behave roughly as Finsberg et al. found in the LV: it may capture relative trends while underestimating the absolute work-density scale. But that needs to be checked, not assumed. The RV is thinner, more crescent-shaped, normally works at much lower pressure than the LV, and has much less direct pressure-strain validation against model-resolved tissue work. For the septum, pressure choice should matter less in health, because $P_\text{RV}$ is small relative to $P_\text{LV}$. In right-ventricular pressure overload this changes. The septum is then no longer close to an LV-only wall: pressure difference should matter for septal shape and motion, while two-sided pressure choices may matter for septal work-density magnitude. The aim of the model is to test these assumptions under controlled loading.

Answering this question requires a model that simultaneously produces physiologically realistic cavity pressures and volume dynamics for both ventricles — which a stand-alone zero-dimensional circulation model can provide — and resolves the stress and strain fields inside the tissue throughout the cardiac cycle — which only a spatially resolved three-dimensional mechanics model can achieve. The coupled finite element and circulation framework described in the following chapter is built specifically to provide both.
