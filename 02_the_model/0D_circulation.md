# The Zero-Dimensional Circulation Model

A finite element model of the myocardium, however detailed, cannot beat realistically in isolation. Without a circulatory system, there is no way to determine what volumes the ventricles should fill to, what pressures they should develop, when the valves should open and close, or how the hemodynamic state should evolve from beat to beat. The heart is a pump embedded in a closed hydraulic loop, and its behavior is shaped at every moment by the impedance of the vessels it is pumping into and the compliance of the vessels it is pumping from.

To provide this circulatory context, we couple the three-dimensional finite element model to a zero-dimensional lumped-parameter model of the complete cardiovascular system. In a zero-dimensional model, the spatial distribution of quantities like pressure and flow rate is discarded; each element of the cardiovascular circuit — a blood vessel, a valve, a cardiac chamber — is represented by a single ordinary differential equation relating pressure, volume, and flow at its inlet and outlet. This is the same principle that underlies the electrical circuit analogy frequently used in physiology teaching, where pressure corresponds to voltage, volumetric flow rate corresponds to current, and the mechanical resistance of a vessel corresponds to an electrical resistor. The analogy is more than pedagogical: the governing equations for linear RC circuits and linear fluidic circuits are mathematically identical, which is why circuit simulation methods can be directly applied to lumped-parameter cardiovascular models.

The specific model we use is the closed-loop four-chamber formulation of Regazzoni et al. {cite}`regazzoni2022cardiac`, implemented in the `circulation` software package {cite}`circulation`. The coupling idea is older than this specific implementation. Early finite-element heart models often prescribed cavity pressure or volume histories, or connected the ventricle only to a simple afterload. Kerckhoffs et al. gave a clear early closed-loop version: the finite-element ventricles and the lumped systemic and pulmonary circulation are advanced together, and the ventricular pressures are iterated until the cavity volumes in the two models agree {cite}`kerckhoffs2007coupling`. Regazzoni et al. later wrote the same volume-consistency idea in a more explicit 3D--0D mathematical framework, including an energy balance for the coupled model {cite}`regazzoni2022cardiac`. Piersanti et al. extended that framework to biventricular electromechanics, where the LV and RV pressures enter as Lagrange multipliers enforcing the two cavity-volume constraints {cite}`piersanti2022closed`.

## State Variables and Circuit Topology

The model state is a vector $\mathbf{y}(t) \in \mathbb{R}^{12}$ consisting of the four chamber volumes $\mathcal{V}_\text{LA}, \mathcal{V}_\text{LV}, \mathcal{V}_\text{RA}, \mathcal{V}_\text{RV}$, the four vascular pressures $p_\text{AR,sys}, p_\text{VEN,sys}, p_\text{AR,pul}, p_\text{VEN,pul}$, and the four vascular flow rates $Q_\text{AR,sys}, Q_\text{VEN,sys}, Q_\text{AR,pul}, Q_\text{VEN,pul}$. The topology of the circuit is a closed loop: blood flows from the left atrium through the mitral valve into the left ventricle, through the aortic valve into the systemic arterial compartment, through the systemic venous compartment and the tricuspid valve into the right ventricle, through the pulmonary valve into the pulmonary arterial compartment, through the pulmonary venous compartment, and back into the left atrium. {numref}`fig-0d-network` shows the resulting closed-loop network with all four chambers, four valves, and the systemic and pulmonary Windkessel branches.

```{figure} ../figures/fig_2_10_0d_network.png
:name: fig-0d-network
:width: 90%

Network diagram of the closed-loop four-chamber circulation model. The four cardiac chambers (LA, LV, RA, RV) are drawn as time-varying elastances; the four valves (mitral, aortic, tricuspid, pulmonary) as ideal diodes with finite forward and large backward resistance; and the systemic and pulmonary vasculature as RCL Windkessel branches with arterial and venous compartments. Arrows indicate the direction of forward flow during a single cardiac cycle.
```

In the standalone 0D circulation model, each cardiac chamber has a time-varying elastance $\mathcal{E}(t)$ that determines how cavity pressure responds to volume. The chamber pressure is

$$
p_\text{ch}(t) = \mathcal{E}(t) \bigl( \mathcal{V}(t) - \mathcal{V}_0 \bigr),
$$

where $\mathcal{V}_0$ is the unstressed chamber volume. The elastance function follows the Blanco activation model {cite}`blanco2010computational`:

$$
\mathcal{E}(t) = \mathcal{E}_B + (\mathcal{E}_A - \mathcal{E}_B) f(t),
$$

where $\mathcal{E}_A$ is the peak systolic elastance, $\mathcal{E}_B$ is the passive diastolic elastance, and $f(t)$ is a smooth activation function that rises from 0 to 1 during contraction and returns to 0 during relaxation. {numref}`fig-elastance` shows the resulting time-varying elastance $\mathcal{E}(t)$ for both ventricles at the healthy calibration over two cardiac cycles, with the asymptotic passive values $\mathcal{E}_B$ marked. The LV elastance peaks roughly six times higher than the RV — the structural reflection of the systemic versus pulmonary pressure regimes the two chambers operate against. The activation function is defined piecewise using cosine segments parametrized by the contraction onset $t_C$, contraction duration $T_C$, and relaxation duration $T_R$:

$$
f(t) = \begin{cases}
\frac{1}{2}\!\left(1 - \cos\!\left(\frac{\pi}{T_C}(t - t_C)\right)\right) & t_C \leq t < t_C + T_C, \\[4pt]
\frac{1}{2}\!\left(1 + \cos\!\left(\frac{\pi}{T_R}(t - t_C - T_C)\right)\right) & t_C + T_C \leq t < t_C + T_C + T_R, \\[4pt]
0 & \text{otherwise}.
\end{cases}
$$

In the coupled 3D--0D simulations, this elastance law is not used as the mechanical pressure law for the LV and RV myocardium. Instead, the 0D model advances the closed-loop circulation and sends target LV and RV volumes to the finite-element solver; the FEM cavity-volume constraints then return the mechanically consistent LV and RV pressures. The elastance formulation remains important for the standalone circulation warm-up, for the atrial chambers, and for defining the calibrated hemodynamic state that the coupled model follows.

```{figure} ../figures/fig_2_12_elastance.png
:name: fig-elastance
:width: 80%

Time-varying elastance $\mathcal{E}(t) = \mathcal{E}_B + (\mathcal{E}_A - \mathcal{E}_B) f(t)$ for the LV and RV chambers at the healthy calibration over two cardiac cycles. The dotted horizontal lines mark the passive end-diastolic baselines $\mathcal{E}_B$. The LV systolic elastance peak is roughly six times the RV value, reflecting the difference in systemic versus pulmonary afterload. The Klotz nonlinear modification described in the calibration chapter modifies the passive component without changing the active part of this curve.
```

The four cardiac valves are modeled as ideal diodes with finite forward resistance $R_\text{min}$ and a large backward resistance $R_\text{max}$. The flow through a valve between upstream pressure $p_\text{up}$ and downstream pressure $p_\text{down}$ is

$$
Q_\text{valve} = \frac{p_\text{up} - p_\text{down}}{R(p_\text{up}, p_\text{down})}, \qquad R = \begin{cases} R_\text{min} & p_\text{up} > p_\text{down}, \\ R_\text{max} & \text{otherwise}. \end{cases}
$$

The systemic and pulmonary vascular beds are each represented by two compartments — arterial and venous — connected by resistive and inductive elements. Each arterial compartment has a scalar compliance $C_\text{AR}$, a resistance $R_\text{AR}$, and an inductance $L_\text{AR}$ that captures the inertia of blood in the large vessels; the venous compartment is analogous with parameters $C_\text{VEN}$, $R_\text{VEN}$, and $L_\text{VEN}$. Here $C$ denotes vascular compliance, not the right Cauchy-Green tensor $\mathbf{C}$ used in the mechanics chapter.

## The ODE System

Conservation of volume in the four chambers gives

$$
\begin{aligned}
\dot{\mathcal{V}}_\text{LA} &= Q_\text{VEN,pul} - Q_\text{MV}, \\
\dot{\mathcal{V}}_\text{LV} &= Q_\text{MV} - Q_\text{AV}, \\
\dot{\mathcal{V}}_\text{RA} &= Q_\text{VEN,sys} - Q_\text{TV}, \\
\dot{\mathcal{V}}_\text{RV} &= Q_\text{TV} - Q_\text{PV},
\end{aligned}
$$

where $Q_\text{MV}, Q_\text{AV}, Q_\text{TV}, Q_\text{PV}$ are the valve flows computed from the diode model above. Conservation of volume in the vascular compartments, using the scalar constitutive relation $\mathcal{V} = C p$ for the elastic vessels, gives the pressure dynamics:

$$
\begin{aligned}
\dot{p}_\text{AR,sys} &= \frac{Q_\text{AV} - Q_\text{AR,sys}}{C_\text{AR,sys}}, \\
\dot{p}_\text{VEN,sys} &= \frac{Q_\text{AR,sys} - Q_\text{VEN,sys}}{C_\text{VEN,sys}}, \\
\dot{p}_\text{AR,pul} &= \frac{Q_\text{PV} - Q_\text{AR,pul}}{C_\text{AR,pul}}, \\
\dot{p}_\text{VEN,pul} &= \frac{Q_\text{AR,pul} - Q_\text{VEN,pul}}{C_\text{VEN,pul}}.
\end{aligned}
$$

The flow rates through the vascular compartments obey momentum conservation with resistive dissipation and vessel inertance:

$$
\begin{aligned}
\dot{Q}_\text{AR,sys} &= \frac{p_\text{AR,sys} - p_\text{VEN,sys} - R_\text{AR,sys}\,Q_\text{AR,sys}}{L_\text{AR,sys}}, \\
\dot{Q}_\text{VEN,sys} &= \frac{p_\text{VEN,sys} - p_\text{RA} - R_\text{VEN,sys}\,Q_\text{VEN,sys}}{L_\text{VEN,sys}}, \\
\dot{Q}_\text{AR,pul} &= \frac{p_\text{AR,pul} - p_\text{VEN,pul} - R_\text{AR,pul}\,Q_\text{AR,pul}}{L_\text{AR,pul}}, \\
\dot{Q}_\text{VEN,pul} &= \frac{p_\text{VEN,pul} - p_\text{LA} - R_\text{VEN,pul}\,Q_\text{VEN,pul}}{L_\text{VEN,pul}}.
\end{aligned}
$$

This is a system of twelve coupled ODEs — four volume equations, four pressure equations, and four flow equations — with the algebraic valve flow relations and the time-varying elastance functions embedded in the right-hand side. The system is stiff because the valve resistances switch between $R_\text{min}$ and $R_\text{max}$ (a ratio of order $10^7$), producing rapid transitions in the flow signals at valve opening and closing events. The system is integrated forward in time using a stiff ODE solver with an analytically provided Jacobian, which substantially improves the convergence of the implicit time-stepping scheme.

## Coupling the 3D and 0D Models

The link between the finite element model and the circulation model is an exchange of cavity volume and cavity pressure at each time step. The circulation model advances the closed-loop state and provides target LV and RV cavity volumes. The finite element solver then deforms the myocardium to match those volumes while satisfying mechanical equilibrium, and returns the cavity pressures required to enforce the two volume constraints. These pressures are fed back to the circulation model, where they affect valve states, arterial pressures, and flow rates on the next step.

A practical complication arises from the fact that the end-diastolic cavity volume of the finite element mesh does not, in general, exactly match the end-diastolic volume of the 0D circulation. The mesh has a fixed anatomical size, while the 0D steady state is determined by effective hemodynamic parameters. In the calibration used here, end-diastolic volumes are included as mesh-compatibility targets, but exact equality cannot be assumed and may conflict with pressure, flow, and ejection-fraction targets. We therefore keep an explicit interface map: a fixed volume ratio scales the volume requests from the 0D model into the frame of the FEM mesh,

$$
\mathcal{V}_\text{FEM}(t) = \frac{\mathcal{V}_\text{mesh,ED}}{\mathcal{V}_\text{0D,ED}} \cdot \mathcal{V}_\text{0D}(t).
$$

Here $\mathcal{V}_\text{mesh,ED}$ is the end-diastolic cavity volume measured directly from the image-derived finite-element mesh, and $\mathcal{V}_\text{0D,ED}$ is the end-diastolic volume of the same cavity at steady state in the 0D simulation. The ratio of these two quantities is computed once at the beginning of the simulation and held fixed throughout. When the 0D calibration is close to the mesh volume this correction is small; when it is not, the 0D model still supplies the timing and relative volume change while the FEM model deforms within its own geometric scale. The pressure that emerges from the FEM solution reflects the actual stiffness of the discretized myocardium, so the pressure-volume relationship is not imposed but computed.

This coupling scheme is implemented as a callback function that the 0D solver invokes at each time step. The callback receives the target volume, calls the finite element solver to compute the equilibrium displacement for that volume, extracts the resulting cavity pressure from the Lagrange multiplier associated with the cavity-volume constraint, and returns this pressure to the 0D solver. If the nonlinear mechanics solve becomes difficult at a given time step, the requested volume and activation update is subdivided into smaller substeps. This adds robustness during rapid volume changes without changing the mathematical coupling: the circulation still provides target volumes, and the mechanics solve still returns the pressures required to realize them. The structure of the callback can be summarised in a few lines:

```text
def coupling_callback(t, calV_LV*, calV_RV*):
    Ta(t)         ← blanco_waveform(t, peak = 100 kPa)
    u             ← FEM.solve(calV_LV = ratio_LV · calV_LV*,
                              calV_RV = ratio_RV · calV_RV*,
                              Ta   = Ta(t))         # Newton + adaptive substep
    p_LV          ← lagrange_multiplier(u, Γ_LV)
    p_RV          ← lagrange_multiplier(u, Γ_RV)
    return p_LV, p_RV
```

Volumes flow into the FEM solver, pressures flow back out, and the active tension that drives the contraction is updated as a function of the global cycle time before each solve. {numref}`fig-coupling-schematic` summarises the same bidirectional handshake graphically.

```{figure} ../figures/fig_2_11_coupling_schematic.png
:name: fig-coupling-schematic
:width: 75%

Bidirectional 3D--0D coupling. At each time step the 0D solver advances the circulation state and emits target cavity volumes $\mathcal{V}_\text{LV}^{*}, \mathcal{V}_\text{RV}^{*}$; these are scaled by the fixed mesh-to-0D volume ratio and passed to the FEM solver, which finds the displacement field that satisfies mechanical equilibrium at the prescribed volumes; the resulting cavity Lagrange multipliers $p_\text{LV}, p_\text{RV}$ are returned to the 0D solver to advance the next step. Volumes flow one way, pressures flow the other; the volume scaling ratio is computed once at simulation start and held fixed.
```

### Solver Pressure Used for Work

The pressure used for mechanical work calculations must be the pressure from the mechanics solve. The scalar elastance relation in the 0D model can provide a chamber pressure for the standalone circulation, but in the coupled 3D--0D run the mechanically consistent cavity pressure is the Lagrange multiplier that enforces the FEM cavity-volume constraint. This multiplier is the endocardial traction required to achieve the target volume with the current geometry, fibre field, constitutive law, boundary conditions, and active tension.

This distinction matters in postprocessing. A circulation pressure history and a solver-pressure history can both exist on disk, but they do not play the same role. The circulation history is useful for hemodynamic context. Boundary work, energy closure, and the pressure-strain proxies in the results chapter use the solver Lagrange-multiplier pressure, because it is synchronized with the saved deformation states and is the pressure actually associated with the finite-element equilibrium problem.
