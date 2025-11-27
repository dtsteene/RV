# Building the Digital Heart

To model the electromechanical behavior of the heart, we rely on a stack of open-source software tools. This project is built upon the FEniCSx ecosystem, a modern, high-performance finite element framework.

## The Ecosystem

Our computational pipeline consists of three primary components created and maintained by my supervisor Henrik Finsberg:

`cardiac-geometries`
: This tool handles the generation of idealized bi-ventricular meshes. It creates the geometry, defines the fiber and sheet orientations (crucial for anisotropic muscle contraction), and tags the relevant subdomains (Left Ventricle, Right Ventricle, Septum, American Heart Assiciation segments) {cite}`cardiac_geometries`.

`fenicsx-pulse`
: This library provides the physics solvers. It implements the large-deformation mechanics (finite elasticity), the active contraction models, and the coupling to the 0D circulation. It is designed specifically for cardiac mechanics {cite}`fenicsx_pulse`.

`circulation`
: This module simulates the 0D "plumbing" of the cardiovascular system. It models the blood flow in and out of the heart using lumped-parameter (Windkessel) models, representing the resistance and compliance of the systemic and pulmonary arteries {cite}`circulation`.

## The Workflow

The modeling process follows a linear pipeline. In the following chapters, we will explore each of these steps in detail, starting with the geometry.

```{mermaid}
graph LR
    A[Geometry Generation] --> B[Physics Definition];
    B --> C[Coupling];
    C --> D[Simulation];
    
    click A "Start here: Creating the mesh"
```

1. Geometry Generation Create the mesh and assign fibers.

2. Physics Definition Define material properties (Holzapfel-Ogden) and active stress models.

3. Coupling Connect the 3D heart model to the 0D circulation model.

4. Simulation Solve the coupled system over multiple cardiac cycles.
