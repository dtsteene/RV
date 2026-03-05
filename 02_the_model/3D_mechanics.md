# Three-Dimensional Continuum Mechanics

The heart wall undergoes deformations that are too large to describe with the small-strain linearized elasticity familiar from structural engineering. Peak fiber strains in the myocardium reach 15–25% during systole, and the theory of linear elasticity, which assumes displacements are infinitesimally small relative to the body's dimensions, loses its validity well before that regime. The appropriate framework is finite hyperelasticity, which allows for arbitrarily large deformations and defines stress through the derivative of a stored energy function with respect to strain — an approach that automatically guarantees thermodynamic consistency and objectivity under rigid-body rotation {cite}`holzapfel2000nonlinear`.

## Kinematics

The deformation of the body is described by a smooth mapping from a reference configuration $\mathcal{B}_0$, representing the tissue in some chosen stress-free state, to the current configuration $\mathcal{B}_t$ at time $t$. A material point initially at position $\mathbf{X}$ moves to position $\mathbf{x} = \boldsymbol{\varphi}(\mathbf{X}, t)$, and the deformation gradient $\mathbf{F}$ captures how infinitesimal line elements are stretched and rotated by this mapping:

$$
\mathbf{F} = \frac{\partial \mathbf{x}}{\partial \mathbf{X}} = \mathbf{I} + \nabla_\mathbf{X} \mathbf{u},
$$

where $\mathbf{u} = \mathbf{x} - \mathbf{X}$ is the displacement field and $\mathbf{I}$ is the identity tensor. The scalar $J = \det \mathbf{F}$ measures the local volume change: $J > 1$ means the material has expanded, $J < 1$ that it has compressed, and $J = 1$ corresponds to isochoric (volume-preserving) deformation.

Rather than working directly with $\mathbf{F}$, it is more convenient to use the right Cauchy-Green deformation tensor $\mathbf{C} = \mathbf{F}^\top \mathbf{F}$, which is symmetric, positive definite, and invariant to rigid-body rotation. The Green-Lagrange strain tensor

$$
\mathbf{E} = \frac{1}{2}(\mathbf{C} - \mathbf{I})
$$

vanishes when the body undergoes pure rigid motion and is positive when material elements are stretched. Both $\mathbf{C}$ and $\mathbf{E}$ are defined relative to the reference configuration, making them natural objects for a material-frame description of deformation.

## The Strain Energy Function and Stress

In hyperelasticity, the mechanical response of the material is encoded in a scalar strain energy function $\Psi(\mathbf{C})$ that gives the elastic energy stored per unit reference volume. The stress arising from this deformation is then recovered by differentiation:

$$
\mathbf{S} = 2 \frac{\partial \Psi}{\partial \mathbf{C}},
$$

where $\mathbf{S}$ is the second Piola-Kirchhoff stress tensor — a quantity defined in the reference configuration that describes the force per unit reference area acting on an oriented surface element. When results need to be interpreted in the current configuration, the Cauchy stress $\boldsymbol{\sigma} = J^{-1} \mathbf{F} \mathbf{S} \mathbf{F}^\top$ is used instead. The Piola-Kirchhoff framework is more natural for computation because the reference domain does not change shape during the simulation, simplifying the formulation of the governing equations.

## The Holzapfel-Ogden Constitutive Model

The myocardium is an anisotropic material: it is stiffer and stronger along the direction of its muscle fibers than perpendicular to them, and this directional dependence is essential to reproduce the characteristic twisting deformation of the heart during systole. We model the passive mechanical behavior of the myocardium using the Holzapfel-Ogden constitutive law {cite}`holzapfel2009constitutive`, a structurally motivated model that decomposes the strain energy into contributions from the isotropic ground matrix, the muscle fibers, and the cross-fiber sheet direction {cite}`finsberg2019assessment`:

$$
\Psi = \Psi_\text{iso} + \Psi_\text{aniso} + \Psi_\text{vol}.
$$

The isotropic term accounts for the mechanically isotropic background tissue — the collagen network, the elastin, and the fluid-filled extracellular matrix — and takes the form

$$
\Psi_\text{iso} = \frac{a}{2b}\left(e^{b(I_1 - 3)} - 1\right),
$$

where $I_1 = \text{tr}\,\mathbf{C}$ is the first invariant of the right Cauchy-Green tensor, encoding the isotropic stretch of the material, and $a$ and $b$ are positive material parameters. The exponential form stiffens the response at large strains, which is characteristic of biological soft tissues.

The anisotropic term adds contributions from the fiber direction $\mathbf{f}_0$ and the sheet direction $\mathbf{s}_0$, defined in the reference configuration by the fiber architecture assigned to the mesh. Using the pseudo-invariants $I_{4f} = \mathbf{f}_0 \cdot (\mathbf{C}\mathbf{f}_0)$ and $I_{4s} = \mathbf{s}_0 \cdot (\mathbf{C}\mathbf{s}_0)$, which measure the squared stretch along each structural direction, the anisotropic energy is

$$
\Psi_\text{aniso} = \frac{a_f}{2b_f}\left(e^{b_f(I_{4f}-1)^2} - 1\right) + \frac{a_s}{2b_s}\left(e^{b_s(I_{4s}-1)^2} - 1\right) + \frac{a_{fs}}{2b_{fs}}\left(e^{b_{fs} I_{8fs}^2} - 1\right),
$$

where $I_{8fs} = \mathbf{f}_0 \cdot (\mathbf{C}\mathbf{s}_0)$ captures the coupling between the fiber and sheet directions, and $a_f$, $b_f$, $a_s$, $b_s$, $a_{fs}$, $b_{fs}$ are additional material parameters. The fiber and sheet terms activate only in extension — their integrands vanish when $I_{4f} \leq 1$ or $I_{4s} \leq 1$, reflecting the observation that muscle fibers and collagen sheets offer little resistance to compression along their length.

The volumetric term penalizes deviations from the incompressible limit:

$$
\Psi_\text{vol} = \frac{\kappa}{2}(J-1)^2,
$$

where $\kappa$ is the bulk modulus. The myocardium is very nearly incompressible — its fluid content prevents substantial volume change — but enforcing strict incompressibility requires a mixed finite element formulation that, while accurate, is more complex to implement and can suffer from numerical locking depending on the element choice. We use the nearly incompressible compressible formulation with $\kappa = 10$ kPa, which is large relative to the shear stiffness parameters and drives $J$ close to unity without imposing it exactly. The material parameters used throughout this study are $a = 0.33$ kPa, $b = 8.0$, $a_f = 0.876$ kPa, $b_f = 7.46$, $a_s = 0.485$ kPa, $b_s = 8.41$, $a_{fs} = 0.216$ kPa, and $b_{fs} = 5.98$.

## The Equilibrium Problem

The governing equations follow from the balance of linear momentum. In the absence of body forces and with inertial effects neglected — the quasi-static approximation appropriate for a cardiac simulation where the timescales of interest are much longer than elastic wave propagation — the strong form in the reference configuration reads

$$
\text{Div}\,\mathbf{P} = \mathbf{0} \quad \text{in } \mathcal{B}_0,
$$

where $\mathbf{P} = \mathbf{F}\mathbf{S}$ is the first Piola-Kirchhoff stress tensor and Div denotes the divergence with respect to the reference coordinates $\mathbf{X}$. This equation is supplemented by boundary conditions that we specify below, and by the constitutive relation $\mathbf{S} = \mathbf{S}_\text{passive}(\mathbf{C}) + \mathbf{S}_\text{active}(t)$ that combines the hyperelastic response and the active contraction described in the next section.

Multiplying by a test displacement $\delta\mathbf{u} \in \mathcal{V}_0$ — the space of kinematically admissible variations that vanish where Dirichlet conditions are imposed — and integrating by parts yields the weak form: find $\mathbf{u} \in \mathcal{V}$ such that

$$
G(\mathbf{u}; \delta\mathbf{u}) = \int_{\mathcal{B}_0} \mathbf{S}(\mathbf{u}) : \delta\mathbf{E}(\mathbf{u}; \delta\mathbf{u}) \, dV - \int_{\partial\mathcal{B}_0} \mathbf{T} \cdot \delta\mathbf{u} \, dA = 0 \quad \forall \, \delta\mathbf{u} \in \mathcal{V}_0,
$$

where $\delta\mathbf{E} = \frac{1}{2}(\mathbf{F}^\top \nabla\delta\mathbf{u} + \nabla\delta\mathbf{u}^\top \mathbf{F})$ is the variation of the Green-Lagrange strain, itself a function of the current deformation through $\mathbf{F}$. The notation $G(\mathbf{u}; \delta\mathbf{u})$ emphasizes that the residual is nonlinear in the solution $\mathbf{u}$ and linear in the test function $\delta\mathbf{u}$: the stress $\mathbf{S}$ depends on $\mathbf{u}$ through $\mathbf{C} = (\mathbf{I} + \nabla\mathbf{u})^\top(\mathbf{I} + \nabla\mathbf{u})$, and the variation $\delta\mathbf{E}$ depends on $\mathbf{u}$ through $\mathbf{F}$.

## Boundary Conditions

The boundary $\partial\mathcal{B}_0$ is partitioned into four non-overlapping regions. The left and right ventricular endocardial surfaces $\Gamma_\text{LV}$ and $\Gamma_\text{RV}$ carry the pressure tractions supplied by the circulation model:

$$
\mathbf{T} = -P_\text{LV} J \mathbf{F}^{-\top}\mathbf{N} \quad \text{on } \Gamma_\text{LV}, \qquad \mathbf{T} = -P_\text{RV} J \mathbf{F}^{-\top}\mathbf{N} \quad \text{on } \Gamma_\text{RV},
$$

where $\mathbf{N}$ is the outward unit normal in the reference configuration and the factor $J\mathbf{F}^{-\top}\mathbf{N}$ maps it to the current configuration via Nanson's formula. This is a follower load: the traction direction changes as the body deforms, which makes the pressure contribution to the tangent stiffness nonsymmetric.

The basal plane $\Gamma_\text{base}$ is constrained by a Dirichlet condition that prevents out-of-plane translation while allowing in-plane displacement, eliminating rigid-body modes without artificially constraining the deformation of the base.

The epicardial surface $\Gamma_\text{epi}$ and the base carry Robin-type spring conditions that model the pericardial constraint and surrounding tissue:

$$
\mathbf{T}_\text{robin} = -k \, \mathbf{u} \quad \text{on } \Gamma_\text{epi} \cup \Gamma_\text{base},
$$

with spring stiffnesses $k_\text{epi} = 10^5$ Pa/m and $k_\text{base} = 10^6$ Pa/m. These springs absorb some elastic energy at the boundaries; the implications of this are discussed in the context of the energy budget in Chapter 5. In the weak form, the Robin terms contribute a bilinear boundary integral $\int_\Gamma k \, \mathbf{u} \cdot \delta\mathbf{u} \, dA$ that enters the residual alongside the internal and pressure terms.

## Linearization and Newton's Method

The nonlinear residual $G(\mathbf{u}; \delta\mathbf{u}) = 0$ is solved by Newton's method. Given an iterate $\mathbf{u}^k$, the increment $\Delta\mathbf{u}$ is found from the linearized problem

$$
DG(\mathbf{u}^k; \delta\mathbf{u})[\Delta\mathbf{u}] = -G(\mathbf{u}^k; \delta\mathbf{u}) \quad \forall \, \delta\mathbf{u} \in \mathcal{V}_0,
$$

where $DG$ is the directional derivative of the residual with respect to $\mathbf{u}$ in the direction $\Delta\mathbf{u}$:

$$
DG(\mathbf{u}; \delta\mathbf{u})[\Delta\mathbf{u}] = \int_{\mathcal{B}_0} \left(\delta\mathbf{E} : \mathbb{C} : \Delta\mathbf{E} + \mathbf{S} : \Delta\delta\mathbf{E}\right) dV + \text{boundary terms},
$$

with $\mathbb{C} = 4 \frac{\partial^2 \Psi}{\partial \mathbf{C} \partial \mathbf{C}}$ the fourth-order material tangent tensor and $\Delta\delta\mathbf{E} = \frac{1}{2}(\nabla\delta\mathbf{u}^\top \nabla\Delta\mathbf{u} + \nabla\Delta\mathbf{u}^\top \nabla\delta\mathbf{u})$ the second variation of the strain. The first term in the integrand is the material stiffness, which captures how the stress changes with strain; the second is the geometric stiffness, which accounts for the change in the strain measure itself as the body deforms. Both contributions are essential for the quadratic convergence rate of Newton's method at large deformations.

## Finite Element Discretization

The displacement field is discretized as $\mathbf{u}_h = \sum_A N_A(\mathbf{X}) \, \mathbf{d}_A$, where $N_A$ are the finite element shape functions and $\mathbf{d}_A$ are the nodal displacement vectors. Inserting this representation into the weak form and choosing $\delta\mathbf{u} = N_B \mathbf{e}_i$ for each degree of freedom reduces the continuous variational problem to a nonlinear algebraic system

$$
\mathbf{R}(\mathbf{d}) = \mathbf{0},
$$

where the residual vector $\mathbf{R}$ assembles the element-level contributions from the internal stress, the pressure tractions, and the Robin springs. The Newton update at each iteration solves the tangent system $\mathbf{K}\,\Delta\mathbf{d} = -\mathbf{R}$, where $\mathbf{K} = \partial\mathbf{R}/\partial\mathbf{d}$ is the assembled tangent stiffness matrix.

The mesh uses first-order tetrahedral elements (P1), which are the simplest conforming elements for three-dimensional elasticity. At the element level, the displacement gradient is constant, which means that each element produces a single strain state — a property that limits the resolution of transmural stress gradients but is adequate at the mesh densities used here (characteristic length 5 mm, approximately 40,000–50,000 elements). The integrals in the weak form are evaluated by Gauss quadrature over each element, and the assembly over all elements is handled by DOLFINx. The tangent system is solved by a sparse direct solver (MUMPS) accessed through PETSc, which provides robust convergence even for the ill-conditioned systems that arise when the bulk modulus $\kappa$ is large relative to the shear stiffness.

In the UFL implementation, the entire derivation above — the strain energy, the stress, the residual, and its linearization — is expressed symbolically. The form compiler FFCx differentiates the energy automatically to produce the residual and tangent forms, which are then compiled into optimized C kernels. This means that changes to the constitutive model (for instance, modifying the Holzapfel-Ogden parameters or switching to a different strain energy function) require only editing the UFL expression for $\Psi$; the linearization, assembly, and solution infrastructure remain untouched.
