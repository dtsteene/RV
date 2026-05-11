(sec-0d-circulation)=
# The Zero-Dimensional Circulation Model

A finite element model of the myocardium, however detailed, cannot beat realistically in isolation. Without a circulatory system, there is no way to determine what volumes the ventricles should fill to, what pressures they should develop, when the valves should open and close, or how the hemodynamic state should evolve from beat to beat. The heart is a pump embedded in a closed hydraulic loop, and its behavior is shaped at every moment by the impedance of the vessels it is pumping into and the compliance of the vessels it is pumping from.

To provide this circulatory context, we couple the three-dimensional finite element model to a zero-dimensional lumped-parameter model of the cardiovascular system. In a 0D model, the spatial distribution of pressure and flow is discarded; each element of the circuit — a vessel, a valve, a cardiac chamber — is represented by an ordinary differential equation relating pressure, volume, and flow at its inlet and outlet. This is the standard hydraulic-electrical analogy: pressure corresponds to voltage, flow to current, vascular resistance to a resistor, and the governing ODEs are identical.

The specific model used is the closed-loop four-chamber formulation of Regazzoni et al. {cite}`regazzoni2022cardiac`, implemented in the `circulation` software package {cite}`circulation`. The volume-consistency idea — finite-element ventricles and a lumped circulation advanced together, with pressures iterated until cavity volumes agree — was first written explicitly by Kerckhoffs et al. {cite}`kerckhoffs2007coupling`. Piersanti et al. extended the framework to biventricular electromechanics, with LV and RV pressures entering as Lagrange multipliers enforcing the two cavity-volume constraints {cite}`piersanti2022closed`.

(sec-0d-state-topology)=
## State Variables and Circuit Topology

The model state is a vector $\mathbf{y}(t) \in \mathbb{R}^{12}$ consisting of the four chamber volumes $\mathcal{V}_\text{LA}, \mathcal{V}_\text{LV}, \mathcal{V}_\text{RA}, \mathcal{V}_\text{RV}$, the four vascular pressures $p_\text{AR,sys}, p_\text{VEN,sys}, p_\text{AR,pul}, p_\text{VEN,pul}$, and the four vascular flow rates $Q_\text{AR,sys}, Q_\text{VEN,sys}, Q_\text{AR,pul}, Q_\text{VEN,pul}$. The topology of the circuit is a closed loop: blood flows from the left atrium through the mitral valve into the left ventricle, through the aortic valve into the systemic arterial compartment, through the systemic venous compartment and the tricuspid valve into the right ventricle, through the pulmonary valve into the pulmonary arterial compartment, through the pulmonary venous compartment, and back into the left atrium. {numref}`fig-0d-network` shows the resulting closed-loop network with all four chambers, four valves, and the systemic and pulmonary Windkessel models.

```{figure} ../figures/fig_2_10_0d_network.png
:name: fig-0d-network
:width: 90%

Closed-loop four-chamber circulation. The four chambers (LA, LV, RA, RV) are time-varying elastances; the four valves (MV, AV, TV, PV, drawn as diamond glyphs along the flow arrows) are ideal diodes with finite forward and large backward resistance; the systemic and pulmonary vasculature are $R$-$C$-$L$ Windkessels with separate arterial and venous compartments. Arrows trace the forward-flow direction across one cardiac cycle.
```

In the standalone 0D circulation model, each cardiac chamber has a time-varying elastance $\mathcal{E}(t)$ that determines how cavity pressure responds to volume. The chamber pressure is

$$
p_\text{ch}(t) = \mathcal{E}(t) \bigl( \mathcal{V}(t) - \mathcal{V}_0 \bigr),
$$

where $\mathcal{V}_0$ is the unstressed chamber volume. The elastance function follows the Blanco activation model {cite}`blanco2010computational`:

$$
\mathcal{E}(t) = \mathcal{E}_B + (\mathcal{E}_A - \mathcal{E}_B) f(t),
$$

where $\mathcal{E}_A$ is the peak systolic elastance, $\mathcal{E}_B$ is the passive diastolic elastance, and $f(t)$ is the same piecewise-cosine activation waveform defined in {ref}`sec-active-contraction`, parametrized by the contraction onset $t_C$, contraction duration $T_C$, and relaxation duration $T_R$. {numref}`fig-elastance` shows the resulting time-varying elastance $\mathcal{E}(t)$ for both ventricles at the healthy calibration over two cardiac cycles, with the asymptotic passive values $\mathcal{E}_B$ marked. The LV elastance peaks roughly six times higher than the RV — the structural reflection of the systemic versus pulmonary pressure regimes the two chambers operate against.

In the coupled 3D--0D simulations, this elastance law is not used as the mechanical pressure law for the LV and RV myocardium. Instead, the 0D model advances the closed-loop circulation and sends target LV and RV volumes to the finite-element solver; the FEM cavity-volume constraints then return the mechanically consistent LV and RV pressures. The elastance formulation remains important for the standalone circulation warm-up, for the atrial chambers, and for defining the calibrated hemodynamic state that the coupled model follows.

```{figure} ../figures/fig_2_12_elastance.png
:name: fig-elastance
:width: 80%

Time-varying elastance $\mathcal{E}(t) = \mathcal{E}_B + (\mathcal{E}_A - \mathcal{E}_B) f(t)$ for the LV and RV chambers at the healthy calibration over two cardiac cycles. The dotted horizontal lines mark the passive end-diastolic baselines $\mathcal{E}_B$. The LV systolic elastance peak is roughly six times the RV value, reflecting the difference in systemic versus pulmonary afterload.
```

The four cardiac valves are modeled as ideal diodes with finite forward resistance $R_\text{min}$ and a large backward resistance $R_\text{max}$. The flow through a valve between upstream pressure $p_\text{up}$ and downstream pressure $p_\text{down}$ is

$$
Q_\text{valve} = \frac{p_\text{up} - p_\text{down}}{R(p_\text{up}, p_\text{down})}, \qquad R = \begin{cases} R_\text{min} & p_\text{up} > p_\text{down}, \\ R_\text{max} & \text{otherwise}. \end{cases}
$$

The systemic and pulmonary Windkessel models are each represented by two compartments — arterial and venous — connected by resistive and inductive elements. Each arterial compartment has a scalar compliance $C_\text{AR}$, a resistance $R_\text{AR}$, and an inductance $L_\text{AR}$ that captures the inertia of blood in the large vessels; the venous compartment is analogous with parameters $C_\text{VEN}$, $R_\text{VEN}$, and $L_\text{VEN}$. Here $C$ denotes vascular compliance, not the right Cauchy-Green tensor $\mathbf{C}$ used in {ref}`sec-kinematics`.

```{table} Main variables and parameters in the closed-loop 0D circulation model.
:name: tab-0d-symbols
:align: left

| Symbol | Meaning |
|---|---|
| $\mathcal{V}_\text{LA},\mathcal{V}_\text{LV},\mathcal{V}_\text{RA},\mathcal{V}_\text{RV}$ | Chamber volumes |
| $p_\text{LA},p_\text{LV},p_\text{RA},p_\text{RV}$ | Chamber pressures |
| $p_\text{AR},p_\text{VEN}$ | Arterial and venous compartment pressures, with systemic and pulmonary subscripts |
| $Q_\text{MV},Q_\text{AV},Q_\text{TV},Q_\text{PV}$ | Mitral, aortic, tricuspid, and pulmonary valve flows |
| $Q_\text{AR},Q_\text{VEN}$ | Arterial and venous Windkessel flows |
| $\mathcal{E}_A,\mathcal{E}_B,\mathcal{V}_0$ | Active elastance, passive elastance, and unstressed chamber volume |
| $R_\text{min},R_\text{max}$ | Forward and backward valve resistances |
| $C_\text{AR},C_\text{VEN}$ | Arterial and venous compliances |
| $R_\text{AR},R_\text{VEN}$ | Arterial and venous vascular resistances |
| $L_\text{AR},L_\text{VEN}$ | Arterial and venous inertances |
```

(sec-0d-ode-system)=
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

This is a system of twelve coupled ODEs — four volume equations, four pressure equations, and four flow equations — with the algebraic valve flow relations and the time-varying elastance functions embedded in the right-hand side. The large ratio between $R_\text{min}$ and $R_\text{max}$ produces rapid transitions in the flow signals at valve opening and closure. In the standalone calibration stage, the circulation model is advanced until the last-beat pressure-volume loops are periodic to the tolerance used by the optimizer.

(sec-3d-0d-coupling)=
## Coupling the 3D and 0D Models

The link between the finite element model and the circulation model is an exchange of cavity volume and cavity pressure at each time step. The circulation model advances the closed-loop state and provides target LV and RV cavity volumes. The finite element solver then deforms the myocardium to match those volumes while satisfying mechanical equilibrium, and returns the cavity pressures required to enforce the two volume constraints. These pressures are fed back to the circulation model, where they affect valve states, arterial pressures, and flow rates on the next step.

The end-diastolic cavity volume of the finite-element mesh is not guaranteed to coincide with the end-diastolic volume that the 0D circulation reaches at steady state. The mesh has a fixed anatomical size, while the 0D steady state is determined by effective hemodynamic parameters that must simultaneously fit pressure, flow, ejection-fraction, and stroke-volume balance. To keep the two scales separable, we compute a fixed volume ratio that maps the 0D volume request into the frame of the FEM mesh,

$$
\mathcal{V}_\text{FEM}(t) = \frac{\mathcal{V}_\text{mesh,ED}}{\mathcal{V}_\text{0D,ED}} \cdot \mathcal{V}_\text{0D}(t).
$$

Here $\mathcal{V}_\text{mesh,ED}$ is the end-diastolic cavity volume measured directly from the image-derived mesh, and $\mathcal{V}_\text{0D,ED}$ is the corresponding volume at steady state in the standalone 0D simulation. The ratio is computed once at the beginning of each coupled run and held fixed throughout. The optimization in {ref}`chap-calibration` includes the mesh end-diastolic volumes as targets, so the ratio stays close to unity in most production cases, but the joint pressure-and-volume cost balance leaves residual mismatches that the ratio then absorbs without further intervention. {ref}`sec-app-coupling-robustness` reports the operating range across the production sweep together with a controlled sensitivity check that bounds how far the interface can be pushed before the coupled simulation breaks. The pressure that emerges from the FEM solve reflects the actual stiffness of the discretized myocardium, so the pressure-volume relationship is computed rather than imposed.

At a coupled time step, the circulation provides target volumes $\mathcal{V}^*_{\text{0D},\text{LV}}$ and $\mathcal{V}^*_{\text{0D},\text{RV}}$. These are mapped to finite-element target volumes

$$
\mathcal{V}^*_{\text{FEM},c}(t)=s_c\,\mathcal{V}^*_{\text{0D},c}(t),
\qquad c\in\{\text{LV},\text{RV}\},
$$

where $s_c=\mathcal{V}_{\text{mesh,ED},c}/\mathcal{V}_{\text{0D,ED},c}$. The mechanics solver then solves the equilibrium problem in {ref}`sec-equilibrium-problem` with the current active tension $T_a(t)$ and the two cavity-volume constraints

$$
\mathcal{V}_{c}(\mathbf{u})=\mathcal{V}^*_{\text{FEM},c}(t),
\qquad c\in\{\text{LV},\text{RV}\}.
$$

The associated Lagrange multipliers are returned as $p_\text{LV}$ and $p_\text{RV}$. Volumes are prescribed by the circulation, and pressures are returned by the finite-element equilibrium solve. {numref}`fig-coupling-schematic` summarises the same bidirectional exchange graphically.

```{figure} ../figures/fig_2_11_coupling_schematic.png
:name: fig-coupling-schematic
:width: 75%

Bidirectional 3D--0D coupling at one time step. The 0D solver emits target cavity volumes $\mathcal{V}^{*}_\text{0D}$; these pass through the fixed mesh-to-0D scaling $\mathcal{V}^{*}_\text{FEM} = s_c\,\mathcal{V}^{*}_\text{0D}$ and become cavity-volume constraints on the FEM solve, which returns the corresponding cavity Lagrange multipliers $p_\text{LV}, p_\text{RV}$. The asymmetry is the content of the figure: volumes pass through scaling, pressures return direct. The active tension $T_a(t)$ enters as a prescribed input; stress, strain, and work-density fields are recorded as readouts. The scale factors $s_\text{LV},s_\text{RV}$ are computed once at simulation start and held fixed.
```

(sec-solver-pressure)=
### Solver Pressure Used for Work

The pressure used for mechanical work calculations must be the pressure from the mechanics solve. The scalar elastance relation in the 0D model can provide a chamber pressure for the standalone circulation, but in the coupled 3D--0D run the mechanically consistent cavity pressure is the Lagrange multiplier that enforces the FEM cavity-volume constraint. This multiplier is the endocardial traction required to achieve the target volume with the current geometry, fibre field, constitutive law, boundary conditions, and active tension.

This distinction matters in postprocessing. A circulation pressure history and a solver-pressure history can both exist on disk, but they do not play the same role. The circulation history is useful for hemodynamic context. Boundary work, energy closure, and the pressure-strain proxies in {ref}`chap-results` use the solver Lagrange-multiplier pressure, because it is synchronized with the saved deformation states and is the pressure actually associated with the finite-element equilibrium problem.
