# Three-Dimensional Continuum Mechanics

When the heart beats, its walls undergo a complex sequence of mechanical events. During systole, the muscle fibres shorten by 15–25%, the wall thickens transmurally, and the entire ventricle twists around its long axis — a wringing motion that squeezes blood out of the cavity. During diastole, the process reverses: the muscle relaxes, the wall thins, and blood flows back in. At every instant, the tissue is being stretched, compressed, and sheared in different directions simultaneously, and the forces that arise internally — the stresses — depend on how much the tissue has deformed, in which direction, and what material it is made of.

To predict these forces and deformations quantitatively, we need a mathematical framework that can describe how a solid body changes shape under applied loads. For small deformations — a steel beam bending by a fraction of a percent — the linearized theory of elasticity is sufficient. But the heart wall deforms by tens of percent, far beyond the regime where linear approximations are valid. The appropriate framework is finite hyperelasticity, which allows for arbitrarily large deformations and defines stress through the derivative of a stored energy function with respect to strain — an approach that automatically guarantees thermodynamic consistency and objectivity under rigid-body rotation.

## Kinematics

The first question in any mechanics problem is: how do we describe the motion of the body? For a rigid object, a translation vector and a rotation matrix suffice. For a deformable solid like the myocardium, the description must be richer — every material point in the body can move independently, and we need a field that tracks the position of every point as a function of time.

The deformation is described by a smooth mapping from a reference configuration $\mathcal{B}_0$, representing the tissue in some chosen stress-free state, to the current configuration $\mathcal{B}_t$ at time $t$. A material point initially at position $\mathbf{X}$ moves to position $\mathbf{x} = \boldsymbol{\varphi}(\mathbf{X}, t)$, and the deformation gradient $\mathbf{F}$ captures how infinitesimal line elements are stretched and rotated by this mapping:

$$
\mathbf{F} = \frac{\partial \mathbf{x}}{\partial \mathbf{X}} = \mathbf{I} + \nabla_\mathbf{X} \mathbf{u},
$$

where $\mathbf{u} = \mathbf{x} - \mathbf{X}$ is the displacement field and $\mathbf{I}$ is the identity tensor. Physically, $\mathbf{F}$ is a $3 \times 3$ matrix that tells you, for any small line segment in the original body, what that segment looks like after deformation: how much it has been stretched and in which direction it has been rotated. If the body has not deformed at all, $\mathbf{F} = \mathbf{I}$; if a fibre originally pointing in the $\mathbf{f}_0$ direction has been stretched to twice its length, the magnitude $|\mathbf{F}\mathbf{f}_0| = 2$.

The scalar $J = \det \mathbf{F}$ measures the local volume change: $J > 1$ means the material has expanded, $J < 1$ that it has compressed, and $J = 1$ corresponds to isochoric (volume-preserving) deformation. For the nearly incompressible myocardium, $J$ stays close to 1 throughout the cardiac cycle.

Rather than working directly with $\mathbf{F}$, it is more convenient to use the right Cauchy-Green deformation tensor $\mathbf{C} = \mathbf{F}^\top \mathbf{F}$, which is symmetric, positive definite, and invariant to rigid-body rotation. The physical content of $\mathbf{C}$ is the same as $\mathbf{F}$ — it encodes how much the material has been stretched in every direction — but it strips out the rotation, leaving only the pure stretch information. This is desirable because a rigid rotation of the heart (picking it up and turning it) should not generate any internal stress; by formulating the constitutive law in terms of $\mathbf{C}$ rather than $\mathbf{F}$, this invariance is guaranteed automatically.

The Green-Lagrange strain tensor

$$
\mathbf{E} = \frac{1}{2}(\mathbf{C} - \mathbf{I})
$$

is a measure of how far the current deformation is from the undeformed state. It vanishes when the body undergoes pure rigid motion and is positive when material elements are stretched. The factor of $\frac{1}{2}$ is a convention that makes $\mathbf{E}$ reduce to the familiar engineering strain $\varepsilon = \Delta L / L$ in the limit of small deformations. Both $\mathbf{C}$ and $\mathbf{E}$ are defined relative to the reference configuration, making them natural objects for a material-frame description of deformation.

```{figure} ../figures/fig_intro_reference_current_configuration.png
:name: fig-reference-current-configuration
:width: 85%

Reference and current descriptions of the same deformation. Cauchy stress power, $\boldsymbol{\sigma}:\mathbf{d}$, is written on the deformed body, while $\mathbf{S}:\dot{\mathbf{E}}$ is the same mechanical power pulled back to the fixed reference mesh used by the finite-element model.
```

## Stress, Energy, and Thermodynamic Consistency

Strain describes how a body has deformed. Stress describes the internal forces that arise as a consequence of that deformation — the forces that neighboring material elements exert on each other. If you imagine cutting the heart wall along an internal surface, stress is the force per unit area that you would need to apply to the cut faces to hold them in place. It is a tensor, not a scalar, because the force on a surface depends on the orientation of that surface: the force per unit area on a surface facing radially, through the wall thickness, is different from the force on a surface facing circumferentially, along the fibre direction.

This distinction matters for the central question of this thesis. The cavity pressure $p$ is the force per unit area on the endocardial surface — the inner wall of the ventricle. It is a single number that acts in the direction perpendicular to the wall (the transmural direction). The internal stress $\mathbf{S}$, by contrast, is a full $3 \times 3$ tensor that describes forces in all directions simultaneously: the fibre-direction stress $S_{ff}$ represents tension along the muscle fibres, the transmural stress $S_{nn}$ represents compression through the wall thickness, and the off-diagonal components represent shearing forces. Cavity pressure determines the normal stress at the endocardial boundary ($\sigma_{nn}|_\text{endo} = -p$), but it does not directly determine the fibre stress or the shear stresses inside the wall. Those internal stresses follow from equilibrium, geometry, material anisotropy, active contraction, and the constraints imposed by the rest of the heart. This indirect relationship — between a scalar boundary pressure and a tensorial internal field — is what makes the pressure-strain proxy an approximation rather than an identity, and it is what we quantify in the results.

### The stress power and energy conjugacy

The concept of mechanical work — stress times strain rate, integrated over the body — is central to this thesis, and the relationship between stress, strain, and work follows from the mechanical power balance. For a body $\mathcal{B}$ with surface tractions $\mathbf{t}$ and no body forces, the total rate of work done by external forces on the body is

$$
\mathcal{P}_\text{ext} = \int_{\partial\mathcal{B}} \mathbf{t} \cdot \dot{\mathbf{x}} \, dA,
$$

where $\dot{\mathbf{x}}$ is the velocity of a material point on the surface. Here "external" means external to the solid body: it is the power of tractions acting on the myocardium. For a pressure-loaded cavity, this is the opposite sign to the hydraulic pump work done by the myocardium on the blood. By the divergence theorem and the balance of linear momentum ($\text{div}\,\boldsymbol{\sigma} = \mathbf{0}$ in quasi-statics), this boundary power equals the internal stress power:

$$
\mathcal{P}_\text{int} = \int_{\mathcal{B}} \boldsymbol{\sigma} : \mathbf{d} \, dv,
$$

where $\mathbf{d} = \frac{1}{2}(\nabla\dot{\mathbf{x}} + \nabla\dot{\mathbf{x}}^\top)$ is the rate of deformation tensor (the symmetric part of the spatial velocity gradient) and $dv$ is the current volume element. The product $\boldsymbol{\sigma} : \mathbf{d}$ is the stress power per unit current volume — the rate at which mechanical energy is being stored or dissipated at each point in the body.

This expression is correct but inconvenient for computation, because the integral is over the current (deformed) configuration, which changes at every time step. We can pull it back to the fixed reference configuration using the identity $dv = J \, dV_0$ and the kinematic relation between the spatial rate of deformation and the material time derivative of the Green-Lagrange strain:

$$
\boldsymbol{\sigma} : \mathbf{d} = \frac{1}{J} \mathbf{S} : \dot{\mathbf{E}}.
$$

This is a fundamental result in continuum mechanics, and it is worth seeing where it comes from. The velocity gradient in the current configuration is $\mathbf{l} = \dot{\mathbf{F}}\mathbf{F}^{-1}$, and its symmetric part is $\mathbf{d} = \frac{1}{2}(\mathbf{l} + \mathbf{l}^\top)$. The Cauchy stress is related to the second Piola-Kirchhoff stress by $\boldsymbol{\sigma} = J^{-1}\mathbf{F}\mathbf{S}\mathbf{F}^\top$. Substituting both into the stress power and using the fact that the time derivative of the Green-Lagrange strain is $\dot{\mathbf{E}} = \frac{1}{2}(\dot{\mathbf{F}}^\top\mathbf{F} + \mathbf{F}^\top\dot{\mathbf{F}}) = \mathbf{F}^\top\mathbf{d}\,\mathbf{F}$, one obtains

$$
\boldsymbol{\sigma} : \mathbf{d} = J^{-1}\mathbf{F}\mathbf{S}\mathbf{F}^\top : \mathbf{d} = J^{-1}\mathbf{S} : (\mathbf{F}^\top\mathbf{d}\,\mathbf{F}) = J^{-1}\mathbf{S} : \dot{\mathbf{E}},
$$

where the second equality uses the trace identity $(\mathbf{F}\mathbf{A}\mathbf{F}^\top) : \mathbf{B} = \mathbf{A} : (\mathbf{F}^\top\mathbf{B}\,\mathbf{F})$ for symmetric tensors. The internal power over the whole body then becomes

$$
\mathcal{P}_\text{int} = \int_{\mathcal{B}} \boldsymbol{\sigma} : \mathbf{d} \, dv = \int_{\mathcal{B}_0} \frac{1}{J}\mathbf{S} : \dot{\mathbf{E}} \cdot J \, dV_0 = \int_{\mathcal{B}_0} \mathbf{S} : \dot{\mathbf{E}} \, dV_0.
$$

The factors of $J$ cancel, and we arrive at the result that the total mechanical power in the body is $\int_{\mathcal{B}_0} \mathbf{S} : \dot{\mathbf{E}} \, dV_0$ — an integral over the fixed reference configuration with no $J$ factors, no deformed geometry, and no ambiguity about which configuration the integration is performed over.

This is the precise sense in which $\mathbf{S}$ and $\mathbf{E}$ are **energy conjugate**: their double contraction $\mathbf{S} : \dot{\mathbf{E}}$ gives the stress power per unit reference volume. Other stress-strain pairs are also energy conjugate — the Cauchy stress $\boldsymbol{\sigma}$ with the rate of deformation $\mathbf{d}$, for instance — but the pair $(\mathbf{S}, \mathbf{E})$ is the most natural for a Lagrangian (reference-frame) formulation because both quantities are defined on the reference configuration. When we compute the total mechanical work over a cardiac cycle as

$$
W = \int_0^T \int_{\mathcal{B}_0} \mathbf{S} : \dot{\mathbf{E}} \, dV_0 \, dt,
$$

we are computing the mechanical work implied by this continuum model. This is still a model output, not a direct biological measurement. Its role in this thesis is simpler: it is the tensor work computed from the finite element stress and strain fields. For regional pressure-strain comparisons, this tensor work is divided by the relevant regional reference volume so that the clinical-style pressure-strain index is compared with a tensor work density.

### The Clausius-Duhem inequality and hyperelasticity

The relationship between the strain energy function and the stress tensor is not an arbitrary modeling choice — it is forced by thermodynamics. The second law of thermodynamics, expressed locally for a continuum, takes the form of the Clausius-Duhem inequality. For a purely mechanical process (no heat conduction, no temperature changes), it reduces to

$$
\mathbf{S} : \dot{\mathbf{E}} - \dot{\Psi} \geq 0,
$$

which states that the stress power must be at least as large as the rate of change of stored energy — the difference being the dissipation, which cannot be negative. For a hyperelastic material, which by definition stores all mechanical energy without dissipation, the inequality becomes an equality:

$$
\mathbf{S} : \dot{\mathbf{E}} = \dot{\Psi}.
$$

This is the constitutive constraint. Since $\Psi = \Psi(\mathbf{C})$ depends on the deformation only through $\mathbf{C}$, the chain rule gives

$$
\dot{\Psi} = \frac{\partial \Psi}{\partial \mathbf{C}} : \dot{\mathbf{C}} = 2\frac{\partial \Psi}{\partial \mathbf{C}} : \dot{\mathbf{E}},
$$

where the factor of 2 comes from $\dot{\mathbf{C}} = 2\dot{\mathbf{E}}$ (since $\mathbf{E} = \frac{1}{2}(\mathbf{C} - \mathbf{I})$ and $\mathbf{I}$ is constant). Substituting into the energy balance:

$$
\mathbf{S} : \dot{\mathbf{E}} = 2\frac{\partial \Psi}{\partial \mathbf{C}} : \dot{\mathbf{E}}.
$$

Since this must hold for every possible motion — every $\dot{\mathbf{E}}$ — the tensors multiplying $\dot{\mathbf{E}}$ must be equal:

$$
\mathbf{S} = 2 \frac{\partial \Psi}{\partial \mathbf{C}}.
$$

This is the constitutive law of hyperelasticity. It is not a postulate but a consequence: the only way for a non-dissipative elastic material to satisfy the second law of thermodynamics at every point and for every deformation is for the stress to be the derivative of a stored energy function with respect to the strain. The entire mechanical behavior of the material — how stiff it is, how it responds to stretching in different directions, how it stores and releases energy — is encoded in the single scalar function $\Psi(\mathbf{C})$.

### Stress measures and their physical meaning

The second Piola-Kirchhoff stress $\mathbf{S}$ is a reference-configuration quantity: it describes forces referred to the undeformed geometry. While mathematically convenient, it does not have the immediate physical interpretation of "force per unit area as measured right now." That role belongs to the Cauchy stress:

$$
\boldsymbol{\sigma} = J^{-1} \mathbf{F} \mathbf{S} \mathbf{F}^\top.
$$

The Cauchy stress is what an embedded pressure sensor would measure — force per unit deformed area, in the current configuration. The transformation $\boldsymbol{\sigma} = J^{-1}\mathbf{F}\mathbf{S}\mathbf{F}^\top$ accounts for two things: the rotation and stretch of the surface on which the force acts (through $\mathbf{F}$), and the change in area of that surface (through $J^{-1}$). The two stress measures contain the same physical information but are referred to different configurations: $\mathbf{S}$ "lives" on the reference body, $\boldsymbol{\sigma}$ on the deformed body. The Piola-Kirchhoff framework is more natural for computation because the reference domain does not change shape during the simulation, and the energy conjugacy $\mathbf{S} : \dot{\mathbf{E}}$ provides the cleanest path to work integration.

## The Holzapfel-Ogden Constitutive Model

The thermodynamic framework above tells us that all we need to fully specify the passive mechanics of the myocardium is a single scalar function $\Psi(\mathbf{C})$. Everything else — the stress, the tangent stiffness, the stored energy, the work — follows by differentiation. The challenge is choosing a $\Psi$ that captures the mechanical behavior of cardiac tissue: its pronounced anisotropy (much stiffer along muscle fibres than across them), its exponential stiffening at large strains, and its near-incompressibility.

The myocardium is an anisotropic material: it is stiffer and stronger along the direction of its muscle fibres than perpendicular to them, and this directional dependence is essential to reproduce the characteristic twisting deformation of the heart during systole. We model the passive mechanical behavior of the myocardium using the Holzapfel-Ogden constitutive law {cite}`holzapfel2009constitutive`, a structurally motivated model that can decompose the strain energy into contributions from the isotropic ground matrix, the muscle fibres, the cross-fibre sheet direction, and fibre-sheet coupling {cite}`finsberg2019assessment`. In the simulations reported here, the transversely isotropic parameter set in `fenicsx-pulse` is used, so the passive anisotropy comes from the fibre term while the sheet and fibre-sheet coefficients are set to zero:

$$
\Psi = \Psi_\text{iso} + \Psi_\text{aniso} + \Psi_\text{vol}.
$$

The isotropic term accounts for the mechanically isotropic background tissue — the collagen network, the elastin, and the fluid-filled extracellular matrix — and takes the form

$$
\Psi_\text{iso} = \frac{a}{2b}\left(e^{b(I_1 - 3)} - 1\right),
$$

where $I_1 = \text{tr}\,\mathbf{C}$ is the first invariant of the right Cauchy-Green tensor, encoding the isotropic stretch of the material, and $a$ and $b$ are positive material parameters. The exponential form is the defining feature of biological soft tissue mechanics: unlike a metal spring, which responds linearly (double the stretch, double the force), the myocardium becomes dramatically stiffer as it is stretched further. At small strains the tissue is compliant, allowing the ventricle to fill easily during diastole; at large strains the exponential kicks in and the tissue stiffens rapidly, protecting it from overstretch. The parameter $a$ sets the overall stiffness scale (in kPa), while $b$ controls how quickly the stiffening occurs — a larger $b$ means the tissue transitions from compliant to stiff over a narrower range of strain.

The general Holzapfel-Ogden anisotropic term can add contributions from the fibre direction $\mathbf{f}_0$, the sheet direction $\mathbf{s}_0$, and fibre-sheet shear, all defined in the reference configuration by the local architecture assigned to the mesh. Using the pseudo-invariants $I_{4f} = \mathbf{f}_0 \cdot (\mathbf{C}\mathbf{f}_0)$ and $I_{4s} = \mathbf{s}_0 \cdot (\mathbf{C}\mathbf{s}_0)$, which measure the squared stretch along each structural direction, the anisotropic energy is

$$
\Psi_\text{aniso} = \frac{a_f}{2b_f}\left(e^{b_f(I_{4f}-1)^2} - 1\right) + \frac{a_s}{2b_s}\left(e^{b_s(I_{4s}-1)^2} - 1\right) + \frac{a_{fs}}{2b_{fs}}\left(e^{b_{fs} I_{8fs}^2} - 1\right),
$$

where $I_{8fs} = \mathbf{f}_0 \cdot (\mathbf{C}\mathbf{s}_0)$ captures the coupling between the fibre and sheet directions, and $a_f$, $b_f$, $a_s$, $b_s$, $a_{fs}$, $b_{fs}$ are additional material parameters. The fibre and sheet terms activate only in extension — their integrands vanish when $I_{4f} \leq 1$ or $I_{4s} \leq 1$, reflecting the observation that muscle fibres and collagen sheets offer little resistance to compression along their length. For the transversely isotropic parameter set used here, $a_s = a_{fs} = 0$, so the sheet and fibre-sheet terms vanish and the passive directional stiffening is fibre-dominated.

The volumetric term penalizes deviations from the incompressible limit:

$$
\Psi_\text{vol} = \frac{\kappa}{4}\left(J^2 - 1 - 2\ln J\right),
$$

where $\kappa$ is the bulk modulus. The myocardium is very nearly incompressible — its fluid content prevents substantial volume change — but enforcing strict incompressibility requires a mixed finite element formulation that, while accurate, is more complex to implement and can suffer from numerical locking depending on the element choice. We use the nearly incompressible compressible formulation with $\kappa = 1000$ kPa, which is large relative to the shear stiffness parameters and drives $J$ close to unity without imposing it exactly. The material parameters used throughout this study are the `fenicsx-pulse` transversely isotropic Holzapfel-Ogden defaults: $a = 2.280$ kPa, $b = 9.726$, $a_f = 1.685$ kPa, $b_f = 15.779$, with $a_s = b_s = a_{fs} = b_{fs} = 0$.

{numref}`fig-holzapfel-ogden` shows the resulting stress–stretch response for an isochoric uniaxial stretch applied along the fibre direction and along a transverse direction, computed by differentiating the strain energy function at the parameters used in the simulations. The isotropic background term gives a soft, gradually stiffening response. Adding the fibre anisotropic term produces the much stiffer exponential response above $\lambda = 1$. The asymmetry between extension and compression is visible in the curves: below $\lambda = 1$ the fibre contribution vanishes, while above $\lambda = 1$ it rapidly dominates the response.

```{figure} ../figures/fig_2_7_holzapfel_ogden.png
:name: fig-holzapfel-ogden
:width: 75%

Stress–stretch response of the transversely isotropic Holzapfel-Ogden constitutive law used throughout this study. The engineering stress $\partial \Psi / \partial \lambda$ is computed numerically from the closed-form strain energy under isochoric uniaxial loading. Loading along the fibre direction (red) recruits the fibre anisotropic term and produces a stiff exponential response above $\lambda = 1$; loading transverse to the fibres (grey) shows the isotropic ground-matrix response. Below $\lambda = 1$ the fibre contribution vanishes, so both curves collapse onto the isotropic response.
```

## Total Stress and Active Contribution

The Holzapfel-Ogden law defines the passive stress $\mathbf{S}_\text{passive}(\mathbf{C})$: the stress that would arise if the myocardium were only an elastic material. A beating ventricle also generates active tension along the muscle fibres. In the active-stress formulation used here, the total second Piola-Kirchhoff stress is

$$
\mathbf{S}
= \mathbf{S}_\text{passive}(\mathbf{C})
+ \mathbf{S}_\text{active}(t),
\qquad
\mathbf{S}_\text{active}(t)
= T_a(t)\,(\mathbf{f}_0\otimes\mathbf{f}_0).
$$

The scalar $T_a(t)$ is the active tension, and $\mathbf{f}_0\otimes\mathbf{f}_0$ projects that tension onto the local fibre direction. Thus the same fibre field that makes the passive material anisotropic also defines the direction in which active contraction generates stress. The next section describes the Blanco waveform used for $T_a(t)$ and its spatial assignment. For the equilibrium problem below, the important point is that at each time step the stress tensor is the sum of the passive hyperelastic stress and this fibre-aligned active contribution.

## The Equilibrium Problem

The governing equations follow from the balance of linear momentum. In the absence of body forces and with inertial effects neglected — the quasi-static approximation appropriate for a cardiac simulation where the timescales of interest are much longer than elastic wave propagation — the strong form in the reference configuration reads

$$
\text{Div}\,\mathbf{P} = \mathbf{0} \quad \text{in } \mathcal{B}_0,
$$

where $\mathbf{P} = \mathbf{F}\mathbf{S}$ is the first Piola-Kirchhoff stress tensor and Div denotes the divergence with respect to the reference coordinates $\mathbf{X}$. This equation is supplemented by boundary and cavity-volume conditions, and by the constitutive relation for $\mathbf{S}$ defined above.

Multiplying by a test displacement $\delta\mathbf{u} \in \mathscr{V}_0$ — the space of kinematically admissible variations that vanish where Dirichlet conditions are imposed — and integrating by parts yields a nonlinear weak form. If the cavity pressures are written as scalar pressure variables $p_\text{LV}$ and $p_\text{RV}$, the mechanical residual has the schematic form

$$
G(\mathbf{u},p_\text{LV},p_\text{RV}; \delta\mathbf{u})
= \int_{\mathcal{B}_0} \mathbf{S}(\mathbf{u}) : \delta\mathbf{E}(\mathbf{u}; \delta\mathbf{u}) \, dV_0
- p_\text{LV}\,\delta \mathcal{V}_\text{LV}(\mathbf{u};\delta\mathbf{u})
- p_\text{RV}\,\delta \mathcal{V}_\text{RV}(\mathbf{u};\delta\mathbf{u})
+ G_\text{Robin}(\mathbf{u};\delta\mathbf{u})
=0.
$$

Here $\delta\mathbf{E} = \frac{1}{2}(\mathbf{F}^\top \nabla\delta\mathbf{u} + \nabla\delta\mathbf{u}^\top \mathbf{F})$ is the variation of the Green-Lagrange strain, and $\delta \mathcal{V}_\text{LV}$ and $\delta \mathcal{V}_\text{RV}$ are the variations of the nonlinear cavity-volume functionals. In the coupled production solve, $p_\text{LV}$ and $p_\text{RV}$ are not prescribed pressure histories. They are Lagrange multipliers enforcing the target LV and RV cavity volumes requested by the 0D circulation model. Equivalently, once solved, they are the follower pressures that would produce the same virtual work on the endocardial surfaces.

## Cavity Constraints and Boundary Conditions

The boundary $\partial\mathcal{B}_0$ is partitioned into four non-overlapping regions. The left and right ventricular endocardial surfaces $\Gamma_\text{LV}$ and $\Gamma_\text{RV}$ define the cavity-volume constraints

$$
\mathcal{V}_\text{LV}(\mathbf{u}) = \mathcal{V}_\text{LV}^*(t),
\qquad
\mathcal{V}_\text{RV}(\mathbf{u}) = \mathcal{V}_\text{RV}^*(t),
$$

where $\mathcal{V}_\text{LV}^*$ and $\mathcal{V}_\text{RV}^*$ are the target cavity volumes supplied by the circulation model after the fixed mesh-to-circulation volume scaling described later. The associated Lagrange multipliers are the solver cavity pressures. Their virtual-work contribution is equivalent to follower-pressure tractions of the form

$$
\mathbf{T} = -p_\text{LV} J \mathbf{F}^{-\top}\mathbf{N} \quad \text{on } \Gamma_\text{LV}, \qquad \mathbf{T} = -p_\text{RV} J \mathbf{F}^{-\top}\mathbf{N} \quad \text{on } \Gamma_\text{RV},
$$

where $\mathbf{N}$ is the outward unit normal in the reference configuration and the factor $J\mathbf{F}^{-\top}\mathbf{N}$ maps it to the current configuration via Nanson's formula. This pressure-traction expression is useful for interpreting the mechanics and for prestressing. In the main coupled simulation, however, the volumes are imposed and the pressures are returned by the finite-element solve.

The basal plane $\Gamma_\text{base}$ is constrained by a partial Dirichlet condition. In the mesh orientation used here, the base-normal direction is the $x$ direction, and only the basal $x$-displacement is fixed; the remaining displacement components are allowed to move. This removes the rigid-body mode associated with base-normal translation without fully clamping the basal surface.

The epicardial surface $\Gamma_\text{epi}$ and the base carry Robin-type spring conditions that model the pericardial constraint and surrounding tissue. The spring resists displacement in the direction normal to the deformed surface, using the same Nanson mapping as the pressure traction to track the current surface orientation:

$$
\mathbf{T}_\text{robin} = -k \, (\mathbf{u} \cdot \mathbf{n}) \, \mathbf{n} \quad \text{on } \Gamma_\text{epi} \cup \Gamma_\text{base},
$$

where $\mathbf{n} = J\mathbf{F}^{-\top}\mathbf{N} / |J\mathbf{F}^{-\top}\mathbf{N}|$ is the unit outward normal in the current configuration. The spring stiffnesses are $k_\text{epi} = 10^5$ Pa/m and $k_\text{base} = 10^6$ Pa/m. Because the spring acts only in the normal direction, tangential sliding of the epicardium is unresisted — a physically reasonable model of the pericardial constraint, which restricts outward motion of the heart surface but allows it to slide freely within the pericardial sac. The surface integral is evaluated over the deformed area element $|J\mathbf{F}^{-\top}\mathbf{N}| \, dS_0$ rather than the reference element $dS_0$, consistent with the formulation used for the pressure traction. These springs absorb some elastic energy at the boundaries; the implications of this are discussed in the context of the energy budget in the results chapter. {numref}`fig-bc-schematic` summarises the four boundary regions and the conditions imposed on each.

```{figure} ../figures/fig_2_8_boundary_conditions.png
:name: fig-bc-schematic
:width: 80%

Boundary and cavity conditions on the biventricular reference mesh. The LV and RV endocardial surfaces $\Gamma_\text{LV}, \Gamma_\text{RV}$ define the cavity-volume constraints; the associated pressures are Lagrange multipliers returned by the mechanics solve. The basal plane $\Gamma_\text{base}$ has only its base-normal displacement component constrained by a Dirichlet condition and is also supported by stiff Robin springs. The epicardial surface $\Gamma_\text{epi}$ is supported by softer Robin springs acting along the deformed surface normal, modelling the pericardial constraint while allowing tangential sliding.
```

## Linearization and Newton's Method

The nonlinear system is solved by Newton's method. In the coupled cavity problem, the unknowns include both the displacement degrees of freedom and the cavity-pressure multipliers, while the target cavity volumes enter as constraints. Written only for the displacement part of the residual, a Newton increment $\Delta\mathbf{u}$ satisfies the linearized problem

$$
DG(\mathbf{u}^k; \delta\mathbf{u})[\Delta\mathbf{u}] = -G(\mathbf{u}^k; \delta\mathbf{u}) \quad \forall \, \delta\mathbf{u} \in \mathscr{V}_0,
$$

where $DG$ is the directional derivative of the residual with respect to $\mathbf{u}$ in the direction $\Delta\mathbf{u}$:

$$
DG(\mathbf{u}; \delta\mathbf{u})[\Delta\mathbf{u}] = \int_{\mathcal{B}_0} \left(\delta\mathbf{E} : \mathbb{C} : \Delta\mathbf{E} + \mathbf{S} : \Delta\delta\mathbf{E}\right) dV_0 + \text{boundary terms},
$$

with $\mathbb{C} = 4 \frac{\partial^2 \Psi}{\partial \mathbf{C} \partial \mathbf{C}}$ the fourth-order material tangent tensor and $\Delta\delta\mathbf{E} = \frac{1}{2}(\nabla\delta\mathbf{u}^\top \nabla\Delta\mathbf{u} + \nabla\Delta\mathbf{u}^\top \nabla\delta\mathbf{u})$ the second variation of the strain. The first term in the integrand is the material stiffness, which captures how the stress changes with strain; the second is the geometric stiffness, which accounts for the change in the strain measure itself as the body deforms. Both contributions are essential for the quadratic convergence rate of Newton's method at large deformations.

## Finite Element Discretization

The displacement field is discretized as $\mathbf{u}_h = \sum_A N_A(\mathbf{X}) \, \mathbf{d}_A$, where $N_A$ are the finite element shape functions and $\mathbf{d}_A$ are the nodal displacement vectors. Inserting this representation into the weak form and choosing $\delta\mathbf{u} = N_B \mathbf{e}_i$ for each degree of freedom reduces the continuous variational problem to a nonlinear algebraic system

$$
\mathbf{R}(\mathbf{d}) = \mathbf{0},
$$

where the residual vector $\mathbf{R}$ assembles the element-level contributions from the internal stress, cavity-pressure multiplier terms, and Robin springs. The Newton update at each iteration solves the tangent system $\mathbf{K}\,\Delta\mathbf{d} = -\mathbf{R}$, where $\mathbf{K} = \partial\mathbf{R}/\partial\mathbf{d}$ is the assembled tangent stiffness matrix.

The mesh uses second-order tetrahedral elements (P2), in which the displacement field is represented by quadratic polynomials with ten nodes per element — four at the vertices and six at the edge midpoints. Quadratic elements provide substantially better accuracy per degree of freedom than linear elements for problems involving bending and large deformations, because the displacement gradient varies linearly within each element rather than being piecewise constant. This means that each element can represent a linearly varying strain field, which is important for resolving the transmural stress gradients that arise when the wall is constrained by cavity volume on the endocardial side and Robin support on the epicardial or basal side. At the production mesh density used here (characteristic length 5 mm, approximately 8000 tetrahedral cells), the P2 discretization produced stable integrated work-density results; a finer 3.75 mm mesh with approximately 15000 cells was used as the mesh-convergence reference. The integrals in the weak form are evaluated by Gauss quadrature over each element, and the assembly over all elements is handled by DOLFINx. The tangent system is solved by a sparse direct solver (MUMPS) accessed through PETSc, which provides robust convergence even for the ill-conditioned systems that arise when the bulk modulus $\kappa$ is large relative to the shear stiffness.

In the UFL implementation, the entire derivation above — the strain energy, the stress, the residual, and its linearization — is expressed symbolically. The form compiler FFCx differentiates the energy automatically to produce the residual and tangent forms, which are then compiled into optimized C kernels. This means that changes to the constitutive model (for instance, modifying the Holzapfel-Ogden parameters or switching to a different strain energy function) require only editing the UFL expression for $\Psi$; the linearization, assembly, and solution infrastructure remain untouched.
