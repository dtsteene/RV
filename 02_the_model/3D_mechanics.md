(sec-3d-mechanics)=
# Finite-Strain Mechanics of the Ventricular Wall

The work definitions in {ref}`sec-work-definitions` use the stress-strain power $\mathbf{S}:\dot{\mathbf{E}}$ as a reference quantity. This section gives the ventricular-wall mechanics that produce those stress and strain fields. It is the full model behind the compact notation introduced earlier: finite deformation, passive material response, active fibre tension, equilibrium, cavity-volume constraints, boundary support, and the finite-element discretization.

When the heart beats, its walls undergo a complex sequence of mechanical events. During systole, the muscle fibres shorten by 15–25%, the wall thickens transmurally, and the entire ventricle twists around its long axis — a wringing motion that squeezes blood out of the cavity. During diastole, the process reverses: the muscle relaxes, the wall thins, and blood flows back in. At every instant, the tissue is being stretched, compressed, and sheared in different directions simultaneously, and the forces that arise internally — the stresses — depend on how much the tissue has deformed, in which direction, and what material it is made of.

To predict these forces and deformations quantitatively, we need a mathematical framework that can describe how a solid body changes shape under applied loads. For small deformations — a steel beam bending by a fraction of a percent — the linearized theory of elasticity is sufficient. The heart wall, however, deforms by tens of percent, far beyond the regime where linear approximations are valid. The appropriate framework is finite hyperelasticity, which allows for large deformations and defines stress through the derivative of an objective stored-energy function {cite}`holzapfel2000nonlinear`.

In the hierarchy introduced in {ref}`chap-introduction`, this is the step beyond Laplace-type wall-stress estimates. Laplace reasoning is useful because it shows that pressure, curvature, and thickness set a wall-stress scale. It is not enough for the present question because myocardial work depends on a local tensor stress and a local tensor strain, not on one membrane-stress number. The formulation below describes how those tensor fields are computed in the finite-element model.

(sec-kinematics)=
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

is a measure of how far the current deformation is from the undeformed state. It vanishes when the body undergoes pure rigid motion and is positive when material elements are stretched. The factor of $\frac{1}{2}$ is a convention that makes $\mathbf{E}$ reduce to the small-strain measure $\varepsilon = \Delta L / L$ in the limit of infinitesimal deformations. Both $\mathbf{C}$ and $\mathbf{E}$ are defined relative to the reference configuration, making them natural objects for a material-frame description of deformation.

(sec-stress-energy)=
## Stress, Energy, and Hyperelasticity

Strain describes how a body has deformed. Stress describes the internal forces that arise as a consequence of that deformation — the forces that neighbouring material elements exert on each other. If you imagine cutting the heart wall along an internal surface, stress is the force per unit area you would need to apply to the cut faces to hold them in place. It is a tensor, not a scalar, because the force on a surface depends on the orientation of that surface: the force on a surface facing radially through the wall thickness is different from the force on a surface facing circumferentially along the fibre direction.

The local rate of mechanical work in a deforming body is the stress power. In the current configuration this is $\boldsymbol{\sigma}:\mathbf{d}$ per unit deformed volume, where $\boldsymbol{\sigma}$ is the Cauchy stress and $\mathbf{d}$ is the rate-of-deformation tensor. A standard kinematic identity {cite}`holzapfel2000nonlinear` lets us pull this back to the reference configuration as

$$
\boldsymbol{\sigma}:\mathbf{d}\,dv \;=\; \mathbf{S}:\dot{\mathbf{E}}\,dV_0,
$$

where $\mathbf{S}$ is the second Piola-Kirchhoff stress and $\dot{\mathbf{E}}$ is the rate of the Green-Lagrange strain. Both $\mathbf{S}$ and $\mathbf{E}$ live on the reference mesh, so $\mathbf{S}:\dot{\mathbf{E}}$ is the natural work pair for a Lagrangian formulation. This is the *energy-conjugate* identity quoted in {ref}`sec-work-definitions`; the algebra is given in {ref}`chap-appendix-energy-identity`.

The constitutive law follows from thermodynamics. The Clausius-Duhem inequality requires that for a hyperelastic (non-dissipative) material the stress power equals the rate of change of stored energy, $\mathbf{S}:\dot{\mathbf{E}} = \dot{\Psi}$. Taking $\Psi = \Psi(\mathbf{C})$ and demanding the equality hold for every admissible motion pins down the constitutive relation

$$
\mathbf{S} = 2\frac{\partial\Psi}{\partial\mathbf{C}}.
$$

This is not a postulate but a consequence: for a non-dissipative elastic material, satisfying the second law at every point and for every deformation forces the stress to be the derivative of a stored-energy function with respect to the strain. The whole mechanical behaviour of the material — anisotropy, stiffening, energy storage and release — is encoded in the scalar function $\Psi(\mathbf{C})$. The standard Clausius-Duhem derivation is in {ref}`chap-appendix-energy-identity`.

The second Piola-Kirchhoff stress $\mathbf{S}$ is a reference-configuration quantity: it describes forces referred to the undeformed geometry, and is mathematically convenient but lacks the immediate "force per unit area as measured right now" interpretation. That role belongs to the Cauchy stress,

$$
\boldsymbol{\sigma} = J^{-1}\mathbf{F}\mathbf{S}\mathbf{F}^\top,
$$

which is what an embedded pressure sensor would measure — force per unit deformed area, in the current configuration. The transformation accounts for the rotation and stretch of the surface on which the force acts (through $\mathbf{F}$) and the change in area of that surface (through $J^{-1}$). The two stress measures contain the same physical information referred to different configurations; the Piola-Kirchhoff pair is preferred for computation because the reference domain does not change shape during the simulation.

(sec-holzapfel-ogden)=
## The Holzapfel-Ogden Constitutive Model

The thermodynamic framework above tells us that the passive mechanics of the myocardium can be specified through a scalar stored-energy function $\Psi(\mathbf{C})$. The stress follows by differentiation, and the Newton linearization uses the corresponding derivative of the stress. The challenge is choosing a $\Psi$ that captures the mechanical behavior of cardiac tissue: its anisotropy (much stiffer along muscle fibres than across them), its exponential stiffening at large strains, and its near-incompressibility.

The myocardium is an anisotropic material: it is stiffer and stronger along the direction of its muscle fibres than perpendicular to them, and this directional dependence is essential to reproduce the twisting deformation of the heart during systole. We model the passive mechanical behavior of the myocardium using the Holzapfel-Ogden constitutive law {cite}`holzapfel2009constitutive`, a structurally motivated model that can decompose the strain energy into contributions from the isotropic ground matrix, the muscle fibres, the cross-fibre sheet direction, and fibre-sheet coupling. In the simulations reported here, the transversely isotropic parameter set in `fenicsx-pulse` is used, so the passive anisotropy comes from the fibre term while the sheet and fibre-sheet coefficients are set to zero:

$$
\Psi = \Psi_\text{iso} + \Psi_\text{aniso} + \Psi_\text{vol}.
$$

The isotropic term accounts for the mechanically isotropic background tissue — the collagen network, the elastin, and the fluid-filled extracellular matrix — and takes the form

$$
\Psi_\text{iso} = \frac{a}{2b}\left(e^{b(I_1 - 3)} - 1\right),
$$

where $I_1 = \text{tr}\,\mathbf{C}$ is the first invariant of the right Cauchy-Green tensor, encoding the isotropic stretch of the material, and $a$ and $b$ are positive material parameters. The exponential form is the defining feature of biological soft tissue mechanics: unlike a metal spring, which responds linearly (double the stretch, double the force), the myocardium stiffens by orders of magnitude as it is stretched further. At small strains the tissue is compliant, allowing the ventricle to fill easily during diastole; at large strains the exponential kicks in and the tissue stiffens rapidly, protecting it from overstretch. The parameter $a$ sets the overall stiffness scale (in kPa), while $b$ controls how quickly the stiffening occurs — a larger $b$ means the tissue transitions from compliant to stiff over a narrower range of strain.

The general Holzapfel-Ogden anisotropic term can add contributions from the fibre direction $\mathbf{f}_0$, the sheet direction $\mathbf{s}_0$, and fibre-sheet shear, all defined in the reference configuration by the local architecture assigned to the mesh. Using the pseudo-invariants $I_{4f} = \mathbf{f}_0 \cdot (\mathbf{C}\mathbf{f}_0)$ and $I_{4s} = \mathbf{s}_0 \cdot (\mathbf{C}\mathbf{s}_0)$, which measure the squared stretch along each structural direction, the anisotropic energy is

$$
\Psi_\text{aniso} =
\frac{a_f}{2b_f}\left(e^{b_f\langle I_{4f}-1\rangle_+^2} - 1\right)
+ \frac{a_s}{2b_s}\left(e^{b_s\langle I_{4s}-1\rangle_+^2} - 1\right)
+ \frac{a_{fs}}{2b_{fs}}\left(e^{b_{fs} I_{8fs}^2} - 1\right),
$$

where $I_{8fs} = \mathbf{f}_0 \cdot (\mathbf{C}\mathbf{s}_0)$ captures the coupling between the fibre and sheet directions, and $a_f$, $b_f$, $a_s$, $b_s$, $a_{fs}$, $b_{fs}$ are additional material parameters. The operator $\langle x\rangle_+=\max(x,0)$ switches the fibre and sheet terms off in compression, reflecting the observation that fibres and collagen sheets offer little resistance to compression along their length. For the transversely isotropic parameter set used here, $a_s = a_{fs} = 0$, so the sheet and fibre-sheet terms vanish and the passive directional stiffening is fibre-dominated.

The volumetric term penalizes deviations from the incompressible limit:

$$
\Psi_\text{vol} = \frac{\kappa}{4}\left(J^2 - 1 - 2\ln J\right),
$$

where $\kappa$ is the bulk modulus. The myocardium is nearly incompressible — its fluid content prevents substantial volume change — but enforcing strict incompressibility requires a mixed finite element formulation that, while accurate, is more complex to implement and can suffer from numerical locking depending on the element choice. We use the nearly incompressible compressible formulation with $\kappa = 1000$ kPa, which is large relative to the shear stiffness parameters and drives $J$ close to unity without imposing it exactly. The material parameters used throughout this study are the `fenicsx-pulse` transversely isotropic Holzapfel-Ogden defaults, listed in {numref}`tab-ho-parameters`.

```{table} Passive material parameters used in the transversely isotropic Holzapfel-Ogden law.
:name: tab-ho-parameters
:align: left

| Parameter | Value | Unit |
|---|---:|---|
| $a$ | 2.280 | kPa |
| $b$ | 9.726 | dimensionless |
| $a_f$ | 1.685 | kPa |
| $b_f$ | 15.779 | dimensionless |
| $a_s$ | 0 | kPa |
| $b_s$ | 0 | dimensionless |
| $a_{fs}$ | 0 | kPa |
| $b_{fs}$ | 0 | dimensionless |
| $\kappa$ | 1000 | kPa |
```

{numref}`fig-holzapfel-ogden` shows the resulting stress–stretch response for an isochoric uniaxial stretch applied along the fibre direction and along a transverse direction, computed by differentiating the strain energy function at the parameters used in the simulations. The isotropic background term gives a soft, gradually stiffening response. Adding the fibre anisotropic term produces the much stiffer exponential response above $\lambda = 1$. The asymmetry between extension and compression is visible in the curves: below $\lambda = 1$ the fibre contribution vanishes, while above $\lambda = 1$ it rapidly dominates the response.

```{figure} ../figures/fig_2_7_holzapfel_ogden.png
:name: fig-holzapfel-ogden
:width: 75%

Stress–stretch response of the transversely isotropic Holzapfel-Ogden constitutive law used throughout this study. The engineering stress $\partial \Psi / \partial \lambda$ is computed numerically from the closed-form strain energy under isochoric uniaxial loading. Loading along the fibre direction (red) recruits the fibre anisotropic term and produces a stiff exponential response above $\lambda = 1$; loading transverse to the fibres (grey) shows the isotropic ground-matrix response. Below $\lambda = 1$ the fibre contribution vanishes, so both curves collapse onto the isotropic response.
```

(sec-total-stress-active)=
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

The scalar $T_a(t)$ is the active tension, and $\mathbf{f}_0\otimes\mathbf{f}_0$ projects that tension onto the local fibre direction. Thus the same fibre field that makes the passive material anisotropic also defines the direction in which active contraction generates stress. {ref}`sec-active-contraction` describes the Blanco waveform used for $T_a(t)$ and its spatial assignment. For the equilibrium problem below, the important point is that at each time step the stress tensor is the sum of the passive hyperelastic stress and this fibre-aligned active contribution.

(sec-equilibrium-problem)=
## The Equilibrium Problem

The governing equations follow from the balance of linear momentum. In the absence of body forces and with inertial effects neglected — the quasi-static approximation appropriate for a cardiac simulation where the timescales of interest are much longer than elastic wave propagation — the strong form in the reference configuration reads

$$
\text{Div}\,\mathbf{P} = \mathbf{0} \quad \text{in } \mathcal{B}_0,
$$

where $\mathbf{P} = \mathbf{F}\mathbf{S}$ is the first Piola-Kirchhoff stress tensor and Div denotes the divergence with respect to the reference coordinates $\mathbf{X}$. This equation is supplemented by the boundary and cavity-volume conditions in {ref}`sec-cavity-boundary`: LV and RV cavity-volume constraints on $\Gamma_\text{LV}$ and $\Gamma_\text{RV}$, a partial basal displacement constraint on $\Gamma_\text{base}$, and Robin support on $\Gamma_\text{epi}\cup\Gamma_\text{base}$.

The displacement solution is sought in a kinematic space $\mathscr{V}$ of $H^1$ vector fields satisfying the basal displacement constraint. Test functions lie in the corresponding homogeneous space $\mathscr{V}_0$, so $\delta\mathbf{u}\in\mathscr{V}_0$ satisfies the same zero Dirichlet condition at the base. Multiplying the strong form by $\delta\mathbf{u}$ and integrating by parts yields a nonlinear weak form. If the cavity pressures are written as scalar pressure variables $p_\text{LV}$ and $p_\text{RV}$, the mechanical residual has the schematic form

$$
\begin{aligned}
G(\mathbf{u},p_\text{LV},p_\text{RV}; \delta\mathbf{u})
&= \int_{\mathcal{B}_0} \mathbf{S}(\mathbf{u}) : \delta\mathbf{E}(\mathbf{u}; \delta\mathbf{u}) \, dV_0 \\
&\quad - p_\text{LV}\,\delta \mathcal{V}_\text{LV}(\mathbf{u};\delta\mathbf{u})
- p_\text{RV}\,\delta \mathcal{V}_\text{RV}(\mathbf{u};\delta\mathbf{u})
+ G_\text{Robin}(\mathbf{u};\delta\mathbf{u}) = 0.
\end{aligned}
$$

Here $\delta\mathbf{E} = \frac{1}{2}(\mathbf{F}^\top \nabla\delta\mathbf{u} + \nabla\delta\mathbf{u}^\top \mathbf{F})$ is the variation of the Green-Lagrange strain, and $\delta \mathcal{V}_\text{LV}$ and $\delta \mathcal{V}_\text{RV}$ are the variations of the nonlinear cavity-volume functionals. In the coupled 3D--0D solve, $p_\text{LV}$ and $p_\text{RV}$ are not prescribed pressure histories. They are Lagrange multipliers enforcing the target LV and RV cavity volumes requested by the 0D circulation model. The equivalent pressure tractions act normal to the deformed endocardial surface.

(sec-cavity-boundary)=
## Cavity Constraints and Boundary Conditions

The boundary $\partial\mathcal{B}_0$ is partitioned into four non-overlapping regions. The left and right ventricular endocardial surfaces $\Gamma_\text{LV}$ and $\Gamma_\text{RV}$ define the cavity-volume constraints

$$
\mathcal{V}_\text{LV}(\mathbf{u}) = \mathcal{V}_\text{LV}^*(t),
\qquad
\mathcal{V}_\text{RV}(\mathbf{u}) = \mathcal{V}_\text{RV}^*(t),
$$

where $\mathcal{V}_\text{LV}^*$ and $\mathcal{V}_\text{RV}^*$ are the target cavity volumes supplied by the circulation model after the fixed mesh-to-circulation volume scaling in {ref}`sec-3d-0d-coupling`. The associated Lagrange multipliers are the solver cavity pressures. Their virtual-work contribution is equivalent to pressure tractions of the form

$$
\mathbf{T} = -p_\text{LV} J \mathbf{F}^{-\top}\mathbf{N} \quad \text{on } \Gamma_\text{LV}, \qquad \mathbf{T} = -p_\text{RV} J \mathbf{F}^{-\top}\mathbf{N} \quad \text{on } \Gamma_\text{RV},
$$

where $\mathbf{N}$ is the outward unit normal in the reference configuration and the factor $J\mathbf{F}^{-\top}\mathbf{N}$ maps it to the current configuration via Nanson's formula {cite}`holzapfel2000nonlinear`. This pressure-traction expression is useful for interpreting the mechanics and for prestressing. In the main coupled simulation, however, the volumes are imposed and the pressures are returned by the finite-element solve.

The basal plane $\Gamma_\text{base}$ is constrained by a partial Dirichlet condition. In the mesh orientation used here, the base-normal direction is the $x$ direction, and only the basal $x$-displacement is fixed; the remaining displacement components are allowed to move. This removes the rigid-body mode associated with base-normal translation without fully clamping the basal surface.

The epicardial surface $\Gamma_\text{epi}$ and the base carry Robin-type spring conditions that model the pericardial constraint and surrounding tissue. The spring resists displacement in the direction normal to the deformed surface, using the same Nanson mapping as the pressure traction to track the current surface orientation:

$$
\mathbf{T}_\text{robin} = -k \, (\mathbf{u} \cdot \mathbf{n}) \, \mathbf{n} \quad \text{on } \Gamma_\text{epi} \cup \Gamma_\text{base},
$$

where $\mathbf{n} = J\mathbf{F}^{-\top}\mathbf{N} / |J\mathbf{F}^{-\top}\mathbf{N}|$ is the unit outward normal in the current configuration. The spring stiffnesses are $k_\text{epi} = 10^5$ Pa/m and $k_\text{base} = 10^6$ Pa/m. Because the spring acts only in the normal direction, tangential sliding of the epicardium is unresisted. This is a phenomenological support condition intended to mimic pericardial and surrounding-tissue restraint, not a detailed anatomical model of the attachments. {numref}`fig-bc-schematic` summarises the four boundary regions and the conditions imposed on each.

```{figure} ../figures/fig_2_8_boundary_conditions.png
:name: fig-bc-schematic
:width: 80%

Boundary and cavity conditions on the biventricular reference mesh. The LV and RV endocardial surfaces $\Gamma_\text{LV}, \Gamma_\text{RV}$ define the cavity-volume constraints; the associated pressures are the Lagrange multipliers returned by the mechanics solve. The targets $\mathcal{V}_\text{LV}^{*}, \mathcal{V}_\text{RV}^{*}$ are supplied each step by the 0D circulation. On the basal plane $\Gamma_\text{base}$, the displacement component along the base normal, $u_n = \mathbf{u}\cdot\mathbf{n}$, is fixed to zero, while the in-plane components are left free and lightly resisted by stiff Robin springs. The epicardial surface $\Gamma_\text{epi}$ is supported by softer Robin springs acting along the deformed surface normal, modelling the pericardial constraint while allowing tangential sliding.
```

(sec-newton-method)=
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

(sec-fe-discretization)=
## Finite Element Discretization

The continuous displacement space $\mathscr{V}$ is approximated by a finite-dimensional subspace $\mathscr{V}_h\subset\mathscr{V}$ spanned by finite element basis functions. The displacement field is written as $\mathbf{u}_h = \sum_A N_A(\mathbf{X}) \, \mathbf{u}_A$, where $N_A$ are the shape functions and $\mathbf{u}_A$ are nodal displacement vectors. Inserting this representation into the weak form and choosing basis test functions reduces the continuous variational problem to a nonlinear algebraic system

$$
\mathbf{R}(\mathbf{u}_h) = \mathbf{0},
$$

where the residual vector $\mathbf{R}$ assembles the element-level contributions from the internal stress, cavity-pressure multiplier terms, and Robin springs. The Newton update at each iteration solves the tangent system $\mathbf{K}\,\Delta\mathbf{u}_h = -\mathbf{R}$, where $\mathbf{K}$ is the assembled tangent stiffness matrix.

The mesh uses second-order tetrahedral elements (P2), in which the displacement field is represented by quadratic polynomials with ten nodes per element — four at the vertices and six at the edge midpoints. Compared with linear tetrahedra, quadratic elements can represent a linearly varying displacement gradient within each element, which is useful for bending-dominated and large-deformation problems {cite}`logg2012automated`. This matters here because transmural stress gradients arise when the wall is constrained by cavity volume on the endocardial side and Robin support on the epicardial or basal side. At the production mesh density used here (characteristic length 5 mm, 8070 tetrahedral cells), the P2 discretization produced stable integrated work-density results; a finer 3.75 mm mesh with approximately 15000 cells was used as the mesh-convergence reference in {ref}`sec-app-mesh-convergence`. The integrals in the weak form are evaluated by Gauss quadrature over each element, and the assembly over all elements is handled by DOLFINx {cite}`baratta2023dolfinx`. The tangent system is solved by the sparse direct solver MUMPS {cite}`amestoy2001mumps`, accessed through PETSc {cite}`petsc2026manual`, which provides robust convergence for the ill-conditioned systems that arise when the bulk modulus $\kappa$ is large relative to the shear stiffness.

In the FEniCSx implementation, the strain energy, stress, residual, and linearization are expressed symbolically in the Unified Form Language (UFL). The FFCx form compiler differentiates the energy automatically to produce the residual and tangent forms, which are then compiled into optimized kernels {cite}`baratta2023dolfinx`. This means that changes to the constitutive model require only editing the UFL expression for $\Psi$; the linearization, assembly, and solution infrastructure remain untouched.
