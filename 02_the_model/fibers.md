# Myocardial Fiber Architecture

The mechanical function of the heart is heavily dependent on the orientation of its muscle fibers.

:::{note} Key Concept: Anisotropy
The myocardium is an **anisotropic material**, meaning its mechanical properties are direction-dependent. It is stiffer and contracts more strongly in the direction of the fibers compared to the transverse direction.
:::



## The LDRB Algorithm

To assign realistic fiber orientations to our idealized geometry, we use the **Laplace-Dirichlet Rule-Based (LDRB)** algorithm. This method solves a series of potential problems (Laplace equations) on the mesh to define a local coordinate system at every point:

**Transmural Distance ($d$)**
: A coordinate varying from 0 (Endocardium) to 1 (Epicardium).

**Apico-Basal Distance**
: A coordinate varying from the apex to the base.

**Circumferential Direction**
: The direction orthogonal to the other two, following the curvature of the wall.

## Fiber Angles

Using this local coordinate system, the fiber helix angle ($\alpha$) is varied linearly across the wall thickness:

$$
\alpha = \alpha_{endo} (1 - d) + \alpha_{epi} d
$$

Where $d$ is the normalized transmural distance. In our model, we use standard physiological values to recreate the characteristic "double-helical" structure:

* **Endocardium:** $\alpha_{endo} = +60^\circ$ (Right-handed helix)
* **Epicardium:** $\alpha_{epi} = -60^\circ$ (Left-handed helix)

This linear variation creates the twisting motion (torsion) that is critical for efficient blood ejection.