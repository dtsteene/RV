# The Computational Model

Simulating a beating heart involves at least two distinct levels of physical description that must be reconciled with one another. At the tissue level, the myocardium is a soft biological material undergoing large, anisotropic deformations driven by active contraction of its constituent muscle fibers. Capturing this requires a spatially resolved model that tracks the displacement, stress, and strain at every point in the ventricular wall — the domain of continuum mechanics and the finite element method. At the system level, the heart is a pump embedded in a closed circulatory loop, and its mechanical output is shaped by the pressure and flow conditions imposed by the arteries and veins it is connected to. Capturing this requires a model of the entire cardiovascular circuit, including the four chambers, the valve dynamics, the arterial compliance, and the vascular resistance of both the systemic and pulmonary circulations.

These two levels of description must be coupled, and the coupling is bi-directional. The hemodynamic load from the circulation determines the pressure boundary conditions that the finite element model must satisfy, while the cavity volume changes computed by the finite element model drive the flow dynamics in the circulation. Neither model can run in isolation and produce physiologically meaningful results: a finite element heart with prescribed volume changes will not develop the right pressures unless the circulation is present to impose the correct load, and the circulation model cannot produce realistic hemodynamics unless it receives accurate cavity volumes from the deforming heart geometry.

The framework used in this thesis is built on three open-source software components maintained by Henrik Finsberg at Simula Research Laboratory. The first is `cardiac-geometries` {cite}`cardiac_geometries`, which handles the generation of bi-ventricular meshes and the assignment of myocardial fiber orientations. The second is `fenicsx-pulse` {cite}`fenicsx_pulse`, which implements the finite element mechanics solver: the large-deformation hyperelastic material laws, the active contraction model, the cavity pressure constraints, and the prestressing algorithm. The third is `circulation` {cite}`circulation`, which implements the zero-dimensional lumped-parameter model of the full cardiovascular circuit, including the closed-loop four-chamber formulation of Regazzoni et al. {cite}`regazzoni2022cardiac` with Windkessel representations of the arterial vasculature. Together, these three components form the complete simulation pipeline, implemented within the broader FEniCSx ecosystem {cite}`baratta2023dolfinx` described in the geometry chapter. {numref}`fig-pipeline` shows the complete data flow between the components.

```{figure} ../figures/fig_2_0_pipeline_overview.png
:name: fig-pipeline
:width: 90%

End-to-end simulation pipeline. Geometry generation (`cardiac-geometries`) produces a tagged biventricular mesh; LDRB fiber assignment populates the quadrature-space fibre, sheet, and sheet-normal fields; a 0D pre-run brings the circulation (`circulation`) to hemodynamic steady state and fixes the volume-scaling ratio; prestressing recovers the unloaded reference; the main coupled loop alternates between the FEM mechanics solver (`fenicsx-pulse`) and the 0D circulation at every time step, exchanging cavity volumes and Lagrange-multiplier pressures; checkpoints of displacement, active tension, and solver pressures are written to disk for offline metric replay.
```

The following sections describe each element of the model in turn. We begin with the geometry and the software infrastructure, since the spatial domain and computational environment determine everything downstream. We then describe the fiber architecture that gives the myocardium its mechanical anisotropy, followed by the constitutive laws governing the passive elastic response of the tissue and the active contraction that drives the heart's pumping function. Finally, we describe the zero-dimensional circulation model and the numerical strategy used to couple it to the three-dimensional finite element solver.

For the scientific question, the model is not only a way of producing plausible pressure-volume loops. It is the controlled setting in which the hidden quantities absent from echocardiography — regional stress tensors, strain tensors, boundary work, and exact regional reference volumes — are all known at the same time. This is what lets the clinical pressure-longitudinal-strain proxy be compared against the model-resolved tensor work density rather than only against another global hemodynamic surrogate.

## The Simulation in Practice

The components described in the subsequent sections come together in a single simulation script that drives the complete cardiac cycle. Understanding the overall structure of this script is useful context for the implementation challenges described later, which can otherwise appear as isolated difficulties rather than problems that arise at specific points in a well-defined pipeline.

The simulation begins with geometry loading and fiber assignment. The biventricular mesh is generated or read from disk, scaled to meters, and oriented with the base normal along the $x$-axis. The LDRB algorithm then solves the Laplace equations and assigns the fiber, sheet, and sheet-normal directions at every quadrature point, storing the result in three function spaces of different resolution as described in the following section.

Before the coupled simulation begins, the circulation model is run alone for ten beats from an initial state determined by the mesh end-diastolic volumes. This pre-run brings the 0D model to a hemodynamically periodic steady state and produces the end-diastolic pressures and volumes that will initialize the coupled simulation. A volume scaling ratio is computed from this result: the ratio of the mesh end-diastolic volume to the steady-state 0D volume provides a multiplicative factor that converts every subsequent volume request from the circulation model into the geometric frame of the finite element mesh. This ratio coupling, described in detail in the 0D circulation section, decouples the anatomical scale of the mesh from the hemodynamic calibration of the circulation parameters.

The prestressing phase runs next. The backward displacement method applies the end-diastolic pressures from the 0D pre-run and iterates toward the stress-free reference configuration that, when inflated to those pressures, reproduces the original mesh geometry. Once this reference configuration is established, the mesh coordinates are updated and the fiber fields are remapped to the new reference. An inflation ramp then deforms the mesh back from the reference to the end-diastolic target volumes, ensuring that the starting state of the coupled simulation is mechanically consistent.

The main coupled loop is driven by the circulation model's time integration. At each time step, the circulation solver calls a callback function that receives the target cavity volumes and returns the corresponding cavity pressures. Inside the callback, the active tension array is updated according to the Blanco waveform, the finite element problem is solved for the displacement that achieves mechanical equilibrium at the prescribed volumes, and the cavity pressures are extracted from the Lagrange multipliers of the cavity constraints. The metrics calculator, which holds the accumulated work integrals and tracks the stress and strain fields, records its quantities at every call. Checkpoint files are written to disk periodically so that the results are preserved even if the simulation terminates early.

In compressed form, the entire pipeline is the following sequence of phases. The notation here is deliberately schematic — assignment is written `←`, library calls are abbreviated, and the per-step solve is a single line that hides the Newton iterations described in the 3D mechanics section.

```text
load_mesh();  scale_to_meters();  orient_base()
fiber, sheet, normal ← LDRB(mesh, α_endo, α_epi, β)
state_0D            ← circulation.run_alone(n_beats = 10)         # warm-up
ratio               ← mesh_V_ED / state_0D.V_ED                   # fixed scaling
u_ref               ← prestress(mesh, P_ED, backward_displacement)
u                   ← inflate(u_ref, V_target = mesh_V_ED)        # back to ED

for t in cycle:
    V_LV*, V_RV*    ← circulation.advance(state_0D, t)
    Ta(t)           ← blanco(t, peak = 100 kPa)
    u, P_LV, P_RV   ← FEM.solve(V = ratio · V*,  Ta = Ta(t))      # Newton + adaptive substep
    state_0D        ← circulation.update(P_LV, P_RV)
    metrics.record(u, S, E, Ta, P)
    if checkpoint_step:  write(u, Ta, P)
```

The two sources of nonlinearity — the FEM equilibrium solve at fixed cavity volume and the 0D-to-FEM volume scaling — are deliberately decoupled, and the metrics calculator is a passive observer that never modifies the simulation state. The same loop structure is what makes offline replay of the metrics from a saved displacement checkpoint possible: rerunning the metrics call after a change to `metrics_calculator.py` does not require re-solving the FEM problem.
