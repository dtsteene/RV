(chap-model)=
# The Computational Model

Chapter 1 established the stress-strain work density $\mathbf{S}:\dot{\mathbf{E}}$ as the reference quantity for the proxy comparison. The finite-element model that produces those stress and strain fields requires local three-dimensional geometry, thick-wall equilibrium, fibre anisotropy, active contraction, boundary support, and two interacting ventricular cavities.

The model describes two coupled objects. The ventricular wall is a three-dimensional deforming solid whose stiffness depends on direction (what *anisotropic* means — myocardium is easier to stretch across the fibres than along them) and whose active tension is applied along the local fibre direction. The circulation is a closed hydraulic network that determines when the ventricles fill, when they eject, and what pressure load each chamber works against.

Each ingredient answers a limitation of a simpler description. The geometry supplies the local wall shape and the RV/septal anatomy. The fibre field supplies the local material axes used by both passive stiffness and active tension. The finite-strain constitutive law converts deformation into tensor stress. The active-stress law adds contraction along the fibres. The boundary and cavity conditions define how pressure, basal support, and epicardial support act on the solid. The zero-dimensional circulation supplies a closed-loop loading path rather than a prescribed pressure trace.

The implementation combines three open-source components. `cardiac-geometries` {cite}`cardiac_geometries` generates and labels the biventricular mesh. `fenicsx-pulse` {cite}`fenicsx_pulse` solves the finite-strain mechanics problem, including cavity-volume constraints, active stress, boundary conditions, and prestressing. `circulation` {cite}`circulation` provides the closed-loop four-chamber circulation model of Regazzoni et al. {cite}`regazzoni2022cardiac`.

A one-time preparation phase builds the mesh, assigns fibres, runs the 0D model to periodicity, and inverse-unloads the image-derived geometry to a reference configuration. The coupled solve then advances in time as shown in {numref}`fig-pipeline-loop`: the 0D circulation requests target cavity volumes, and the mechanics solver returns the Lagrange multipliers that act as cavity pressures.

```{figure} ../figures/fig_2_0b_coupled_solve.png
:name: fig-pipeline-loop
:width: 80%

Coupled 3D--0D time step. The 0D circulation supplies target cavity volumes $\mathcal{V}^{*}_\text{LV},\mathcal{V}^{*}_\text{RV}$; the mechanics solver returns the corresponding Lagrange multipliers $p_\text{LV},p_\text{RV}$. The Blanco-waveform active tension $T_a(t)$ is a prescribed time-series input; stress, strain, and work-density fields are recorded as post-processing readouts.
```

The remainder of the chapter follows the pipeline. {ref}`sec-geometry-anatomical-model` defines the mesh and anatomical tags. {ref}`sec-fibers` explains how the local fibre-sheet-normal frame is assigned. {ref}`sec-3d-mechanics` gives the finite-strain kinematics, passive Holzapfel-Ogden material law, active-stress contribution including the Blanco activation waveform, equilibrium problem, and boundary/support conditions. {ref}`sec-0d-circulation` then gives the standalone 0D model and the 3D--0D coupling.
