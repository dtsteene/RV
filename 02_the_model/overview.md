# The Computational Model

The model has to describe two coupled objects at once. The first is the ventricular wall itself: a three-dimensional deforming solid whose fibres actively contract and whose stiffness depends on direction. This direction-dependence is what *anisotropic* means. Myocardium is easier to stretch across the fibres than along them, so the local fibre architecture matters for both deformation and stress. The second object is the circulation: a closed hydraulic network that determines when the ventricles fill, when they eject, and what pressure load each chamber works against.

The coupling can be summarized in one sentence: the circulation asks the finite-element heart to realize a pair of cavity volumes, and the finite-element heart returns the pressures required to do so. Volumes therefore pass from the zero-dimensional circulation model to the three-dimensional mechanics model; pressures pass back in the opposite direction. This volume-controlled formulation is the backbone of the simulations reported here.

The implementation combines three open-source components. `cardiac-geometries` {cite}`cardiac_geometries` generates and labels the biventricular mesh. `fenicsx-pulse` {cite}`fenicsx_pulse` solves the finite-strain mechanics problem, including cavity-volume constraints, active stress, boundary conditions, and prestressing. `circulation` {cite}`circulation` provides the closed-loop four-chamber circulation model of Regazzoni et al. {cite}`regazzoni2022cardiac`. {numref}`fig-pipeline` shows how these pieces are used in one end-to-end run.

```{figure} ../figures/fig_2_0_pipeline_overview.png
:name: fig-pipeline
:width: 100%

End-to-end simulation pipeline. The geometry and fibre fields define the finite-element heart. A zero-dimensional circulation pre-run establishes a periodic hemodynamic state and a fixed mesh-to-circulation volume scaling. Prestressing constructs the unloaded reference configuration. During the main loop, the circulation sends target LV and RV volumes to the mechanics solver, active tension is prescribed, and the solver returns cavity pressures. Stress-strain quantities are recorded from the solved state.
```

The sections below follow this pipeline. The geometry section defines the mesh and anatomical tags. The fibre section explains how the local fibre-sheet-normal frame is assigned. The mechanics section gives the finite-strain continuum model and boundary conditions. The active-contraction section describes how active stress is prescribed in time, and the circulation section then gives the 0D model and the 3D--0D coupling.

## The Simulation in Practice

The simulation itself is a sequence of preparation phases followed by the coupled time loop. First, the biventricular mesh is loaded, scaled to SI units, oriented, and given anatomical tags. The fibre architecture is then assigned with the LDRB algorithm, which solves Laplace problems on the mesh to build smooth anatomical coordinates before rotating them into fibre, sheet, and sheet-normal directions.

Second, the 0D circulation is run by itself for several beats until it reaches a periodic state. This warm-up gives a consistent set of end-diastolic pressures and volumes before the expensive 3D solve begins. Because the clipped finite-element mesh and the calibrated 0D circulation do not have identical cavity volumes, a fixed volume scale is computed for each ventricle,

$$
s_\text{LV} = \frac{V_{\text{LV,mesh}}^\text{ED}}{V_{\text{LV,0D}}^\text{ED}},
\qquad
s_\text{RV} = \frac{V_{\text{RV,mesh}}^\text{ED}}{V_{\text{RV,0D}}^\text{ED}}.
$$

Later, when the circulation requests a volume $V_\text{0D}^{*}(t)$, the mechanics solver receives the scaled target $s\,V_\text{0D}^{*}(t)$. This preserves the fractional filling and ejection pattern from the circulation while respecting the physical size of the mesh. The details and limitations of this choice are discussed in the 0D circulation section.

Third, the mesh is prestressed. The image-derived geometry represents a loaded end-diastolic heart, not an unloaded stress-free body. The backward displacement method therefore estimates a reference configuration that, when inflated to the end-diastolic pressures from the 0D warm-up, reproduces the original mesh. The coupled simulation starts from this mechanically consistent end-diastolic state.

The main coupled loop then advances one time step at a time. The circulation proposes target LV and RV volumes, the Blanco activation waveform {cite}`blanco2010computational` sets the active tension, the finite-element solver finds the displacement field that satisfies mechanical equilibrium at those volumes, and the resulting Lagrange multipliers are returned as the LV and RV cavity pressures. Stress, strain, and work-density metrics are recorded from this solved state but do not alter the simulation.

In compressed form, the pipeline is:

```text
mesh, tags          ← load_and_prepare_geometry()
fiber, sheet, normal ← LDRB(mesh, tags)
state_0D            ← circulation.run_alone(n_beats = 10)
s_LV, s_RV          ← V_mesh^ED / V_0D^ED
u_ref               ← prestress(mesh, P_0D^ED)
u                   ← inflate_to_end_diastole(u_ref)

for t in cycle:
    V_LV*, V_RV*    ← circulation.advance(state_0D, t)
    Ta(t)           ← Blanco_activation(t)
    u, P_LV, P_RV   ← FEM.solve(V = s · V*,  Ta = Ta(t))
    state_0D        ← circulation.update(P_LV, P_RV)
    metrics.record(u, S, E, Ta, P)
```

The key feature is that the expensive mechanics solve and the circulation advance are coupled only through volumes and pressures. This makes the model interpretable: when a loading parameter is changed in the 0D circulation, the finite-element heart responds through the same mechanical problem, with the same geometry, fibres, constitutive law, active tension waveform, and boundary conditions.
