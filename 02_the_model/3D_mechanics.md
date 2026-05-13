(sec-3d-mechanics)=
# Ventricular Wall Mechanics

The work definitions in {ref}`sec-work-definitions` use the stress-strain power $\mathbf{S}:\dot{\mathbf{E}}$ as a reference quantity, where $\mathbf{S}$ is the second Piola-Kirchhoff stress and $\dot{\mathbf{E}}$ is the rate of the Green-Lagrange strain. This section gives the ventricular-wall mechanics that produce those stress and strain fields, using the finite-deformation notation ($\mathbf{F}, J, \mathbf{C}, \mathbf{E}$) developed in {ref}`sec-mechanics-notation`. The heart wall deforms by tens of percent, beyond the regime where linear approximations are valid; the appropriate framework is finite hyperelasticity, which allows for large deformations and defines stress through the derivative of an objective stored-energy function {cite}`holzapfel2000nonlinear`.

The constitutive law follows from thermodynamics. The Clausius-Duhem inequality requires that for a hyperelastic (non-dissipative) material the stress power equals the rate of change of stored energy, $\mathbf{S}:\dot{\mathbf{E}} = \dot{\Psi}$. Restricting $\Psi$ to depend on $\mathbf{C}$ (rather than $\mathbf{F}$, so rigid rotations generate no internal stress) and demanding the equality hold for every admissible motion pins down the constitutive relation

$$
\mathbf{S} = 2\frac{\partial\Psi}{\partial\mathbf{C}}.
$$

The whole mechanical behaviour of the material — anisotropy, stiffening, energy storage and release — is encoded in the scalar function $\Psi(\mathbf{C})$. Derivations are in {ref}`chap-appendix-energy-identity`.

(sec-holzapfel-ogden)=
## The Holzapfel-Ogden Constitutive Model

The thermodynamic framework above tells us that the passive mechanics of the myocardium can be specified through a scalar stored-energy function $\Psi(\mathbf{C})$. The challenge is choosing a $\Psi$ that captures the mechanical behavior of cardiac tissue: its anisotropy (much stiffer along muscle fibres than across them), its exponential stiffening at large strains, and its incompressibility.

The myocardium is an anisotropic material: it is stiffer and stronger along the direction of its muscle fibres than perpendicular to them, and this directional dependence is essential to reproduce the twisting deformation of the heart during systole. We model the passive mechanical behavior of the myocardium using the Holzapfel-Ogden constitutive law {cite}`holzapfel2009constitutive`, a structurally motivated model that decomposes the strain energy into isotropic, anisotropic, and volumetric contributions:

$$
\Psi = \Psi_\text{iso} + \Psi_\text{aniso} + \Psi_\text{vol}.
$$

The isotropic term accounts for the mechanically isotropic background tissue — the collagen network, the elastin, and the fluid-filled extracellular matrix — and takes the form

$$
\Psi_\text{iso} = \frac{a}{2b}\left(e^{b(I_1 - 3)} - 1\right),
$$

where $I_1 = \text{tr}\,\mathbf{C}$ is the first invariant of the right Cauchy-Green tensor, encoding the isotropic stretch of the material, and $a$ and $b$ are positive material parameters. The exponential form is the defining feature of biological soft tissue mechanics. At small strains the tissue is compliant, allowing the ventricle to fill easily during diastole; at large strains the exponential kicks in and the tissue stiffens rapidly, protecting it from overstretch. The parameter $a$ sets the overall stiffness scale (in kPa), while $b$ controls how quickly the stiffening occurs — a larger $b$ means the tissue transitions from compliant to stiff over a narrower range of strain.

The general Holzapfel-Ogden anisotropic term can add contributions from the fibre direction $\mathbf{f}_0$, the sheet direction $\mathbf{s}_0$, and fibre-sheet shear, all defined in the reference configuration by the local architecture assigned to the mesh. The pseudo-invariants capturing the squared stretches along the fibre and sheet directions and the fibre-sheet coupling are

$$
I_{4f} = \mathbf{f}_0 \cdot (\mathbf{C}\mathbf{f}_0),
\qquad
I_{4s} = \mathbf{s}_0 \cdot (\mathbf{C}\mathbf{s}_0),
\qquad
I_{8fs} = \mathbf{f}_0 \cdot (\mathbf{C}\mathbf{s}_0).
$$

Each is a scalar function of $\mathbf{C}$ that depends only on the local stretch along (or between) the structural directions, so the anisotropic energy can be built from directional content rather than the full deformation tensor. With the Macaulay bracket $\langle x\rangle_+=\max(x,0)$, the anisotropic energy is

$$
\Psi_\text{aniso} =
\frac{a_f}{2b_f}\left(e^{b_f\langle I_{4f}-1\rangle_+^2} - 1\right)
+ \frac{a_s}{2b_s}\left(e^{b_s\langle I_{4s}-1\rangle_+^2} - 1\right)
+ \frac{a_{fs}}{2b_{fs}}\left(e^{b_{fs} I_{8fs}^2} - 1\right),
$$

where $a_f$, $b_f$, $a_s$, $b_s$, $a_{fs}$, $b_{fs}$ are additional material parameters. The Macaulay bracket switches the fibre and sheet terms off in compression, reflecting the observation that fibres and collagen sheets offer little resistance to compression along their length. For the transversely isotropic parameter set used here, $a_s = a_{fs} = 0$, so the sheet and fibre-sheet terms vanish and the passive directional stiffening is fibre-dominated. This is the standard simplification in patient-specific cardiac FEM where biaxial / shear data to identify the full orthotropic parameter set are unavailable {cite}`pluijmert2017determinants,finsberg2017phd`. It is conservative for the proxy-validity question: real myocardium is orthotropic {cite}`holzapfel2009constitutive`, so dropping the sheet and fibre-sheet terms only reduces the cross-fibre stress-strain work that a longitudinal-strain proxy cannot recover, putting the gap reported here on the low side.

The volumetric term penalizes deviations from the incompressible limit:

$$
\Psi_\text{vol} = \frac{\kappa}{4}\left(J^2 - 1 - 2\ln J\right),
$$

where $\kappa$ is the bulk modulus. The myocardium is essentially incompressible — its fluid content prevents substantial volume change — but enforcing strict $J=1$ requires a mixed finite-element formulation that is more complex to implement and can suffer from numerical locking depending on the element choice. We instead use a penalty (nearly incompressible) formulation with $\kappa = 1000$ kPa, which is large relative to the shear stiffness parameters and drives $J$ close to unity without imposing it exactly. Results are not expected to depend on this relaxation. The material parameters used throughout this study are the `fenicsx-pulse` transversely isotropic Holzapfel-Ogden defaults, listed in {numref}`tab-ho-parameters`.

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

Engineering stress $\partial\Psi/\partial\lambda$ for the transversely isotropic Holzapfel-Ogden law under isochoric uniaxial stretch. The fibre direction (red) stiffens exponentially above $\lambda=1$; transverse to the fibres (grey) only the isotropic term acts. Both curves coincide below $\lambda=1$ because the Macaulay bracket switches the fibre term off in compression. The shaded band marks the physiological cardiac stretch range $\lambda\in[0.85,1.10]$.
```

(sec-total-stress-active)=
## Total Stress and Active Contribution

The Holzapfel-Ogden law defines the passive stress; a beating ventricle also generates fibre-aligned active tension. The total second Piola-Kirchhoff stress is

$$
\mathbf{S} = \mathbf{S}_\text{passive}(\mathbf{C}) + T_a(t)\,(\mathbf{f}_0\otimes\mathbf{f}_0),
$$

where $T_a(t)$ is a prescribed scalar active tension. This active-stress formulation adds an explicit fibre-aligned contribution rather than modelling calcium handling, electrophysiology, or crossbridge dynamics {cite}`ambrosi2012active`.

The temporal profile of $T_a$ follows the Blanco ventricular activation model {cite}`blanco2010computational`: a piecewise cosine parameterized by an onset time $t_C$, a contraction phase of duration $T_C$, and a relaxation phase of duration $T_R$. The normalized waveform is

$$
a(t) =
\begin{cases}
\tfrac{1}{2}\left[1-\cos\!\left(\tfrac{\pi(t-t_C)}{T_C}\right)\right], & t_C \le t < t_C+T_C, \\[4pt]
\tfrac{1}{2}\left[1+\cos\!\left(\tfrac{\pi(t-t_C-T_C)}{T_R}\right)\right], & t_C+T_C \le t < t_C+T_C+T_R, \\[4pt]
0, & \text{otherwise},
\end{cases}
$$

and the active tension is $T_a(t) = T_a^\text{max}\,a(t)$. The simulations use $t_C = 0$ (activation aligned with the end-diastolic mesh), $T_C = 0.25$ s, $T_R = 0.40$ s, $T_a^\text{max} = 100$ kPa, and a heart rate of 75 bpm (0.8 s cycle length). {numref}`fig-blanco-activation` shows the waveform.

```{figure} ../figures/fig_2_9_blanco_activation.png
:name: fig-blanco-activation
:width: 80%

Blanco activation function $a(t)$ over two cardiac cycles: a piecewise cosine rising during the contraction phase $T_C$ (pink), peaking at unity, and decaying through the relaxation phase $T_R$ (blue).
```

The same waveform and 100 kPa amplitude are used in all three regions (LV free wall, RV free wall, septum), so activation is spatially synchronous and contractile drive is not a region-specific tuning parameter. The amplitude is of the same order as related coupled cardiac active-stress models {cite}`regazzoni2022cardiac,piersanti2022closed`; the different LV and RV pressure regimes then arise from geometry, boundary conditions, and circulatory loading rather than from a prescribed RV/LV tension difference. Heart rate and Blanco timing are nominal resting-state values held fixed across simulations; they scale the temporal axis but do not enter the per-beat work-density comparison.

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

(sec-equilibrium-problem)=
## The Equilibrium Problem

The governing equations follow from the balance of linear momentum. In the absence of body forces and with inertial effects neglected — the quasi-static approximation appropriate for a cardiac simulation where the timescales of interest are much longer than elastic wave propagation — the strong form in the reference configuration reads

$$
\text{Div}\,\mathbf{P} = \mathbf{0} \quad \text{in } \mathcal{B}_0,
$$

where $\mathbf{P} = \mathbf{F}\mathbf{S}$ is the first Piola-Kirchhoff stress tensor and Div denotes the divergence with respect to the reference coordinates $\mathbf{X}$. This equation is supplemented by the cavity-volume constraints, Robin support, and basal Dirichlet condition defined in {ref}`sec-cavity-boundary` above.

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

Here $\delta\mathbf{E} = \frac{1}{2}(\mathbf{F}^\top \nabla\delta\mathbf{u} + \nabla\delta\mathbf{u}^\top \mathbf{F})$ is the variation of the Green-Lagrange strain; $\delta\mathcal{V}_\text{LV}$ and $\delta\mathcal{V}_\text{RV}$ are the variations of the cavity-volume functionals introduced above, and $G_\text{Robin}$ is the virtual-work contribution of the Robin springs.

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

The mesh uses second-order tetrahedral elements (P2), in which the displacement field is a quadratic polynomial with ten nodes per element — four at vertices and six at edge midpoints. Compared with linear tetrahedra, quadratic elements can represent a linearly varying displacement gradient within each element {cite}`logg2012automated`. That matters here because transmural stress gradients arise when the wall is constrained by cavity volume on the endocardial side and Robin support on the epicardial or basal side. The production mesh uses a characteristic length of 5 mm (8070 cells); a finer 3.75 mm mesh (~15000 cells) is used as the mesh-convergence reference in {ref}`sec-app-mesh-convergence`.

The integrals in the weak form are evaluated by Gauss quadrature over each element and assembled by DOLFINx {cite}`baratta2023dolfinx`. The tangent system is solved by the sparse direct solver MUMPS {cite}`amestoy2001mumps` through PETSc {cite}`petsc2026manual`, which converges robustly even for the ill-conditioned systems that arise when the bulk modulus $\kappa$ is large relative to the shear stiffness.

In the FEniCSx implementation, the strain energy, stress, residual, and linearization are expressed symbolically in the Unified Form Language (UFL). The FFCx form compiler differentiates the energy automatically to produce the residual and tangent forms, which are then compiled into optimized kernels {cite}`baratta2023dolfinx`. This means that changes to the constitutive model require only editing the UFL expression for $\Psi$; the linearization, assembly, and solution infrastructure remain untouched.
