(chap-appendix-energy-identity)=
# Energy Identity and Stress-Power Derivations

This appendix collects the standard continuum-mechanics derivations behind the work definitions used in the thesis: the pull-back of the stress power to the reference configuration, the energy-identity link between stress-strain work and boundary power, and the Clausius-Duhem derivation of the hyperelastic constitutive relation. None of these results is original; they are gathered here so that the main text can quote them by reference rather than re-derive them.

## Pull-back of the Stress Power

The local rate of mechanical work in a deforming body is the stress power. In the current configuration this is $\boldsymbol{\sigma}:\mathbf{d}$ per unit deformed volume, where $\boldsymbol{\sigma}$ is the Cauchy stress and $\mathbf{d} = \tfrac{1}{2}(\mathbf{l} + \mathbf{l}^\top)$ is the symmetric part of the spatial velocity gradient $\mathbf{l} = \dot{\mathbf{F}}\mathbf{F}^{-1}$.

The Cauchy stress is related to the second Piola-Kirchhoff stress by $\boldsymbol{\sigma} = J^{-1}\mathbf{F}\mathbf{S}\mathbf{F}^\top$, and the time derivative of the Green-Lagrange strain is $\dot{\mathbf{E}} = \tfrac{1}{2}(\dot{\mathbf{F}}^\top\mathbf{F} + \mathbf{F}^\top\dot{\mathbf{F}}) = \mathbf{F}^\top\mathbf{d}\,\mathbf{F}$. Substituting and using the trace identity $(\mathbf{F}\mathbf{A}\mathbf{F}^\top):\mathbf{B} = \mathbf{A}:(\mathbf{F}^\top\mathbf{B}\,\mathbf{F})$ for symmetric tensors gives

$$
\boldsymbol{\sigma}:\mathbf{d} = J^{-1}\mathbf{F}\mathbf{S}\mathbf{F}^\top:\mathbf{d} = J^{-1}\mathbf{S}:(\mathbf{F}^\top\mathbf{d}\,\mathbf{F}) = J^{-1}\mathbf{S}:\dot{\mathbf{E}}.
$$

Integrating over the body and using $dv = J\,dV_0$, the factors of $J$ cancel:

$$
\int_{\mathcal{B}} \boldsymbol{\sigma}:\mathbf{d}\,dv = \int_{\mathcal{B}_0} \mathbf{S}:\dot{\mathbf{E}}\,dV_0.
$$

This is the precise sense in which $\mathbf{S}$ and $\mathbf{E}$ are *energy conjugate*: their double contraction gives the same stress power per unit reference volume that $\boldsymbol{\sigma}:\mathbf{d}$ gives per unit current volume {cite}`holzapfel2000nonlinear`.

## Boundary Form of the Energy Identity

The reference-configuration step uses the energy-conjugate identity $\mathbf{S}:\dot{\mathbf{E}}=\mathbf{P}:\dot{\mathbf{F}}$, where $\mathbf{P}=\mathbf{F}\mathbf{S}$ is the first Piola-Kirchhoff stress and $\dot{\mathbf{F}}=\nabla_\mathbf{X}\mathbf{v}$. In quasi-static equilibrium, $\operatorname{Div}\mathbf{P}=\mathbf{0}$. Multiplying by the velocity $\mathbf{v}$, integrating over $\Omega$, and applying the divergence theorem gives {cite}`holzapfel2000nonlinear`:

$$
\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,dV_0
= \int_{\partial\Omega} \mathbf{t}_0\cdot\mathbf{v}\,dA
= \int_{\partial\omega} \mathbf{t}\cdot\mathbf{v}\,da,
$$

where $\mathbf{t}_0=\mathbf{P}\mathbf{N}$ is the nominal traction on the reference boundary $\partial\Omega$ and $\mathbf{t}$ is the Cauchy traction on the deformed boundary $\partial\omega$. The two surface integrals describe the same boundary power, written on the reference and current configurations; $dA$ and $da$ are the corresponding area elements.

On the LV and RV endocardial surfaces, the Cauchy traction is pressure, $\mathbf{t}=-p\mathbf{n}$. Combined with the kinematic identity $\dot{\mathcal{V}}=-\int_{\Gamma_\text{endo}}\mathbf{v}\cdot\mathbf{n}\,da$, the two minus signs combine and the endocardial surface term becomes $p\,\dot{\mathcal{V}}$ under the sign convention used here. Splitting the boundary into endocardial, epicardial, and basal patches yields the schematic form

$$
\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,dV_0
= p_\text{LV}\,\dot{\mathcal{V}}_\text{LV}
+ p_\text{RV}\,\dot{\mathcal{V}}_\text{RV}
+ \dot W_\text{epi}
+ \dot W_\text{base}
$$

quoted in {ref}`sec-energy-identity`. The last two terms are the powers exchanged with the epicardial Robin springs and the partial basal Dirichlet support; if those non-cavity supports were absent the cycle integral would reduce to the familiar pressure-volume work terms alone.

## Hyperelasticity from the Clausius-Duhem Inequality

The Clausius-Duhem inequality for a purely mechanical, isothermal continuum reads

$$
\mathbf{S}:\dot{\mathbf{E}} - \dot{\Psi} \geq 0,
$$

so the stress power must be at least as large as the rate of change of stored energy, the difference being dissipation. For a hyperelastic material — non-dissipative by definition — the inequality becomes an equality:

$$
\mathbf{S}:\dot{\mathbf{E}} = \dot{\Psi}.
$$

Taking $\Psi = \Psi(\mathbf{C})$ and applying the chain rule with $\dot{\mathbf{C}} = 2\dot{\mathbf{E}}$ gives

$$
\dot{\Psi} = \frac{\partial\Psi}{\partial\mathbf{C}}:\dot{\mathbf{C}} = 2\frac{\partial\Psi}{\partial\mathbf{C}}:\dot{\mathbf{E}}.
$$

Equating the two expressions for $\dot{\Psi}$ and demanding the result hold for every admissible motion (every $\dot{\mathbf{E}}$) pins down the constitutive relation:

$$
\mathbf{S} = 2\frac{\partial\Psi}{\partial\mathbf{C}}.
$$

This is not a postulate but a consequence: for a non-dissipative elastic material, satisfying the second law at every point and for every deformation forces the stress to be the derivative of a stored-energy function with respect to the strain. The whole mechanical behaviour of the material — anisotropy, stiffening, energy storage and release — is encoded in the scalar function $\Psi(\mathbf{C})$.
