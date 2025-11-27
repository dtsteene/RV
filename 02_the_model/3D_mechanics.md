# 3D Continuum Mechanics

To simulate the passive mechanical response of the heart—how it stretches and resists deformation—we use the framework of **finite hyperelasticity**. This approach is necessary because the heart undergoes large deformations that linear elasticity cannot capture {cite}`main_pdf`.



## Kinematics

We describe the deformation of the heart using the **deformation gradient tensor**, $F$:

$$
F = I + \nabla u
$$

Where $u$ is the displacement field. From $F$, we compute the **Right Cauchy-Green deformation tensor** ($C$), which provides a measure of strain that is invariant to rigid-body rotation:

$$
C = F^T F
$$

## The Strain Energy Function

The mechanical properties of the myocardium are defined by a **Strain Energy Function** ($\Psi$). This scalar function represents the potential energy stored in the material per unit reference volume. The stress in the material is derived from this energy:

$$
S = 2 \frac{\partial \Psi}{\partial C}
$$

Where $S$ is the Second Piola-Kirchhoff stress tensor.

## The Holzapfel-Ogden Model

We model the myocardium as a **transversely isotropic material** using the Holzapfel-Ogden law {cite}`holzapfel2009constitutive`. This model accounts for the fact that heart muscle is stiffer along the fiber direction than across it.



The strain energy function is split into three distinct contributions:

$$
\Psi = \Psi_{iso} + \Psi_{aniso} + \Psi_{vol}
$$

**1. Isotropic Matrix ($\Psi_{iso}$)**
: Represents the non-fibrous background tissue (collagen, elastin).
$$\Psi_{iso} = \frac{a}{2 b} \left( e^{b(I_1 - 3)} - 1 \right)$$

**2. Anisotropic Fibers ($\Psi_{aniso}$)**
: Represents the stiffness of the muscle fibers ($f_0$) and sheets ($s_0$).
$$\Psi_{aniso} = \frac{a_f}{2 b_f} \left( e^{b_f (I_{4f} - 1)^2} - 1 \right) + \frac{a_s}{2 b_s} \left( e^{b_s (I_{4s} - 1)^2} - 1 \right)$$
Where $I_{4f} = f_0 \cdot (C f_0)$ is the squared stretch along the fiber direction.

**3. Incompressibility ($\Psi_{vol}$)**
: Enforces that the heart muscle volume remains (nearly) constant (using a penalty parameter $\kappa$).
$$\Psi_{vol} = \frac{\kappa}{2} (J - 1)^2$$

:::{note} Implementation in FEniCSx
In `fenicsx-pulse`, this material model is implemented automatically. We simply need to specify the material parameters ($a, b, a_f, b_f, \dots$) in the configuration {cite}`fenicsx_pulse`.
:::