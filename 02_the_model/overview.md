(chap-model)=
# The Computational Model

The previous chapter framed the model as the upper rung of a ladder of mechanical descriptions. Pressure-volume work gives whole-chamber pump work. Pressure-strain work gives a clinically measurable regional index. Laplace-type reasoning adds the first wall-stress correction by including geometry and thickness. The finite-element model is used because the RV free wall and septum require still more structure: local three-dimensional geometry, thick-wall equilibrium, fibre anisotropy, active contraction, boundary support, and two interacting ventricular cavities.

The model therefore has to describe two coupled objects at once. The first is the ventricular wall itself: a three-dimensional deforming solid whose stiffness depends on direction and whose active tension is applied along the local fibre direction. This direction-dependence is what *anisotropic* means. Myocardium is easier to stretch across the fibres than along them, so the local fibre architecture matters for deformation, stress, active contraction, and the work-density components analysed later. The second object is the circulation: a closed hydraulic network that determines when the ventricles fill, when they eject, and what pressure load each chamber works against.

Each model ingredient answers a limitation of a simpler description. The geometry supplies the local wall shape and the RV/septal anatomy that a global Laplace radius cannot represent. The fibre field supplies the local material axes used by both passive stiffness and active tension. The finite-strain constitutive law converts deformation into tensor stress rather than a single wall-stress scale. The active-stress law adds contraction along the fibres. The boundary and cavity conditions define how pressure, basal support, and epicardial support act on the solid. The zero-dimensional circulation supplies a closed-loop loading path rather than an isolated prescribed pressure trace.

The coupling can be summarized in one sentence: the circulation asks the finite-element heart to realize a pair of cavity volumes, and the finite-element heart solves for the mesh displacement and the pressures required to do so. Volumes therefore pass from the zero-dimensional circulation model to the three-dimensional mechanics model; pressures pass back in the opposite direction. Stress, strain, and work are then evaluated from the solved displacement field and material law. This volume-controlled formulation is the backbone of the simulations reported here.

The implementation combines three open-source components. `cardiac-geometries` {cite}`cardiac_geometries` generates and labels the biventricular mesh. `fenicsx-pulse` {cite}`fenicsx_pulse` solves the finite-strain mechanics problem, including cavity-volume constraints, active stress, boundary conditions, and prestressing. `circulation` {cite}`circulation` provides the closed-loop four-chamber circulation model of Regazzoni et al. {cite}`regazzoni2022cardiac`. The pipeline runs in two stages: a one-time preparation phase that constructs the simulation state, then the coupled time loop that advances it. The five preparation steps are summarised in {numref}`fig-pipeline-prep`.

```{figure} ../figures/fig_2_0a_preparation.png
:name: fig-pipeline-prep
:width: 100%

Preparation pipeline, run once before the coupled solve. Each arrow carries the artefact produced by the upstream step: mesh and surface tags, the fibre-sheet-normal frame $(\mathbf{f}_0,\mathbf{s}_0,\mathbf{n}_0)$, the periodic 0D state $\mathbf{y}_\text{0D}^{ED}$, and the mesh-to-circulation scale factors $s_\text{LV},s_\text{RV}$. The dashed exit hands the unloaded reference configuration $\mathcal{B}_0$ to the coupled solve.
```

Once preparation has produced a calibrated reference configuration, the coupled solve advances one time step at a time. The 0D circulation requests target LV and RV cavity volumes; the mechanics solver finds the displacement field that satisfies these volumes under the prescribed active tension and returns the corresponding cavity pressures as Lagrange multipliers. {numref}`fig-pipeline-loop` shows this exchange together with the auxiliary input and output streams.

```{figure} ../figures/fig_2_0b_coupled_solve.png
:name: fig-pipeline-loop
:width: 80%

Coupled 3D--0D time step. The 0D circulation supplies target cavity volumes $\mathcal{V}^{*}_\text{LV},\mathcal{V}^{*}_\text{RV}$; the mechanics solver returns the corresponding Lagrange multipliers $p_\text{LV},p_\text{RV}$. The Blanco-waveform active tension $T_a(t)$ is a prescribed time-series input; stress, strain, and work-density fields are recorded as post-processing readouts.
```

The model description follows this pipeline. {ref}`sec-geometry-anatomical-model` defines the mesh and anatomical tags. {ref}`sec-fibers` explains how the local fibre-sheet-normal frame is assigned. {ref}`sec-3d-mechanics` gives the finite-strain kinematics, passive Holzapfel-Ogden material law, active-stress contribution, equilibrium problem, and boundary/support conditions. {ref}`sec-active-contraction` then focuses on the time course and spatial assignment of active tension, and {ref}`sec-0d-circulation` gives the standalone 0D model and the 3D--0D coupling.

(sec-simulation-practice)=
## The Simulation in Practice

The simulation runs as a sequence of preparation phases followed by the coupled time loop. The mesh is loaded and tagged. The LDRB algorithm assigns fibres ({ref}`sec-fibers`). The 0D circulation is run by itself for several beats until periodic. A fixed mesh-to-circulation volume scale is computed for each ventricle ({ref}`sec-3d-0d-coupling`). The mesh is then prestressed so that the image-derived geometry plays the role of a loaded end-diastolic state ({ref}`chap-implementation`). In the primary sweep, the RV end-diastolic pressure used during inverse unloading is capped to avoid a very small RV reference in the severe fixed-geometry cases, while the image-derived end-diastolic mesh remains the loaded target.

The main coupled loop advances one time step at a time. The circulation proposes target LV and RV volumes, the Blanco activation waveform {cite}`blanco2010computational` sets the active tension, and the finite-element solver returns the displacement field together with the Lagrange multipliers that act as the cavity pressures.

The key feature is that the expensive mechanics solve and the circulation advance are coupled only through volumes and pressures. This makes the model interpretable: when a loading parameter is changed in the 0D circulation, the finite-element heart responds through the same mechanical problem, with the same geometry, fibres, constitutive law, active tension waveform, and boundary conditions.
