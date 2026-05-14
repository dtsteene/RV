(sec-0d-circulation)=
# The Zero-Dimensional Circulation Model

The three-dimensional finite-element heart is coupled to a zero-dimensional lumped-parameter circulation model. Each element of the circuit — vessel, valve, cardiac chamber — is represented by an ordinary differential equation relating pressure, volume, and flow at its inlet and outlet.

The specific model is the closed-loop four-chamber formulation of Regazzoni et al. {cite}`regazzoni2022cardiac`, implemented in the `circulation` software package {cite}`circulation`. The volume-consistency coupling between a finite-element ventricle and a lumped circulation follows Kerckhoffs et al. {cite}`kerckhoffs2007coupling`.

(sec-0d-state-topology)=
## Components

The model state is a vector $\mathbf{y}(t) \in \mathbb{R}^{12}$ consisting of the four chamber volumes $\mathcal{V}_\text{LA}, \mathcal{V}_\text{LV}, \mathcal{V}_\text{RA}, \mathcal{V}_\text{RV}$, the four vascular pressures $p_\text{AR,sys}, p_\text{VEN,sys}, p_\text{AR,pul}, p_\text{VEN,pul}$, and the four vascular flow rates $Q_\text{AR,sys}, Q_\text{VEN,sys}, Q_\text{AR,pul}, Q_\text{VEN,pul}$. The topology of the circuit is a closed loop: blood flows from the left atrium through the mitral valve into the left ventricle, through the aortic valve into the systemic arterial compartment, through the systemic venous compartment and the tricuspid valve into the right ventricle, through the pulmonary valve into the pulmonary arterial compartment, through the pulmonary venous compartment, and back into the left atrium. {numref}`fig-0d-network` shows the resulting closed-loop network with all four chambers, four valves, and the systemic and pulmonary Windkessel models.

```{figure} ../figures/fig_2_10_0d_network.png
:name: fig-0d-network
:width: 90%

Closed-loop four-chamber circulation. The four chambers (LA, LV, RA, RV) are time-varying elastances; the four valves (MV, AV, TV, PV, drawn as diamonds along the flow arrows) are modelled as switching diodes with a small forward resistance $R_\text{min}$ when open and a large backward resistance $R_\text{max}$ when closed; the systemic and pulmonary vasculature are $R$-$C$-$L$ Windkessels with separate arterial and venous compartments. Arrows trace the forward-flow direction across one cardiac cycle.
```

In the standalone 0D circulation model, each cardiac chamber has a time-varying elastance $\mathcal{E}(t)$ that determines how cavity pressure responds to volume. The chamber pressure is

$$
p_\text{ch}(t) = \mathcal{E}(t) \bigl( \mathcal{V}(t) - \mathcal{V}_0 \bigr),
$$

where $\mathcal{V}_0$ is the unstressed chamber volume. The elastance function follows the Blanco activation model {cite}`blanco2010computational`:

$$
\mathcal{E}(t) = \mathcal{E}_A\,a(t) + \mathcal{E}_B,
$$

where $\mathcal{E}_A$ is the active-elastance amplitude (peak elastance is $\mathcal{E}_A + \mathcal{E}_B$), $\mathcal{E}_B$ is the passive diastolic elastance, and $a(t)$ is the piecewise-cosine activation waveform defined in {ref}`sec-total-stress-active`, parametrized by the contraction onset $t_C$, contraction duration $T_C$, and relaxation duration $T_R$. For the LV and RV ventricles in the production calibration, the passive limb is replaced by a Klotz-style exponential pressure-volume extension that recovers the linear form as its curvature parameter $k_E \to 0$; the equation, the motivation, and the per-case audit are in {ref}`chap-calibration` and {ref}`sec-app-calibration-edpvr`. {numref}`fig-elastance` shows the resulting time-varying elastance $\mathcal{E}(t)$ for both ventricles at the healthy calibration over two cardiac cycles. At this calibration the LV systolic pressure reaches approximately 120 mmHg and the RV approximately 30 mmHg over the 0.8 s cardiac cycle; full per-chamber and per-compartment parameter values are tabulated in {ref}`chap-calibration`.

In the coupled 3D--0D run, the elastance law is replaced by the FE-solver Lagrange multipliers for the LV and RV ventricles; the atrial pressures $p_\text{LA}, p_\text{RA}$ (which enter the venous-return flow ODEs below) still come from the elastance relation, as do all chamber pressures during the standalone calibration warm-up.

```{figure} ../figures/fig_2_12_elastance.png
:name: fig-elastance
:width: 80%

Time-varying elastance $\mathcal{E}(t) = \mathcal{E}_A\,a(t) + \mathcal{E}_B$ for the LV and RV chambers at the healthy calibration over two cardiac cycles. The dotted horizontal lines mark the passive baselines $\mathcal{E}_B$. The LV systolic elastance peak is roughly six times the RV value, reflecting the difference in systemic versus pulmonary afterload; the resulting cavity pressures of $\sim$120 and $\sim$30 mmHg follow from $p = \mathcal{E}\,(\mathcal{V} - \mathcal{V}_0)$ with the larger RV operating volume narrowing the pressure ratio to about four-to-one.
```

The four cardiac valves are modeled as ideal diodes with finite forward resistance $R_\text{min}$ and a large backward resistance $R_\text{max}$. The flow through a valve between upstream pressure $p_\text{up}$ and downstream pressure $p_\text{down}$ is

$$
Q_\text{valve} = \frac{p_\text{up} - p_\text{down}}{R(p_\text{up}, p_\text{down})}, \qquad R = \begin{cases} R_\text{min} & p_\text{up} > p_\text{down}, \\ R_\text{max} & \text{otherwise}. \end{cases}
$$

In the vascular compartments below, $C$ denotes compliance. The systemic and pulmonary Windkessel models are each represented by two compartments — arterial and venous — connected by resistive and inductive elements. Each arterial compartment has a scalar compliance $C_\text{AR}$, a resistance $R_\text{AR}$, and an inductance $L_\text{AR}$ that captures the inertia of blood in the large vessels; the venous compartment is analogous with parameters $C_\text{VEN}$, $R_\text{VEN}$, and $L_\text{VEN}$.

All chamber elastances, unstressed volumes, vascular resistances and compliances, the diastolic-curvature parameter $k_E$, and the total blood-volume distribution are case-by-case calibration parameters; {ref}`chap-calibration` describes the optimization procedure and {ref}`chap-appendix-circulation-calibration` tabulates the per-case values and search ranges.

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

where $Q_\text{MV}, Q_\text{AV}, Q_\text{TV}, Q_\text{PV}$ are the valve flows computed from the diode model above. The vascular compartments use a linear constitutive relation $\mathcal{V} = C p$ with constant compliance and zero unstressed volume, in contrast to the chamber elastance law which retains an unstressed offset $\mathcal{V}_0$ and a time-varying $\mathcal{E}(t)$. Combined with mass conservation, this gives $\dot{p} = \dot{\mathcal{V}}/C$ and the pressure equations:

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

This is a system of twelve coupled ODEs — four volume equations, four pressure equations, and four flow equations. The inertance terms $L$ represent the inertia of blood in the large vessels and smooth the rapid flow transitions across the valve diodes. The large ratio between the closed and open valve resistances $R_\text{max}/R_\text{min}$ makes the system stiff; the `circulation` package integrates it with a small fixed time step. In the standalone calibration stage, the model is advanced until the last-beat pressure-volume loops satisfy the periodicity tolerance used by the optimizer.

(sec-3d-0d-coupling)=
## Coupling the 3D and 0D Models

The link between the finite element model and the circulation model is an exchange of cavity volume and cavity pressure at each time step. The circulation model advances the closed-loop state and provides target LV and RV cavity volumes. The finite element solver then deforms the myocardium to match those volumes while satisfying mechanical equilibrium, and returns the cavity pressures required to enforce the two volume constraints. These pressures are fed back to the circulation model, where they affect valve states, arterial pressures, and flow rates on the next step.

The end-diastolic cavity volume of the finite-element mesh is not guaranteed to coincide with the end-diastolic volume that the 0D circulation reaches at steady state. The mesh has a fixed anatomical size, while the 0D steady state is determined by effective hemodynamic parameters that must simultaneously fit pressure, flow, ejection-fraction, and stroke-volume balance. To keep the two scales separable, we compute a fixed volume ratio that maps the 0D volume request into the frame of the FEM mesh,

$$
\mathcal{V}_\text{FEM}(t) = \frac{\mathcal{V}_\text{mesh,ED}}{\mathcal{V}_\text{0D,ED}} \cdot \mathcal{V}_\text{0D}(t).
$$

Here $\mathcal{V}_\text{mesh,ED}$ is the end-diastolic cavity volume measured directly from the image-derived mesh, and $\mathcal{V}_\text{0D,ED}$ is the corresponding volume at steady state in the standalone 0D simulation. The ratio is computed once at the beginning of each coupled run and held fixed throughout. The optimization in {ref}`chap-calibration` includes the mesh end-diastolic volumes as targets, so the ratio stays close to unity in most production cases, but the joint pressure-and-volume cost balance leaves residual mismatches that the ratio then absorbs without further intervention. {ref}`sec-app-coupling-robustness` reports the operating range across the production sweep together with a controlled sensitivity check that bounds how far the interface can be pushed before the coupled simulation breaks.

At each coupled time step, the scaled target volumes become cavity-volume constraints on the FE solve,

$$
\mathcal{V}_{c}(\mathbf{u})=\mathcal{V}^*_{\text{FEM},c}(t),
\qquad c\in\{\text{LV},\text{RV}\},
$$

with associated Lagrange multipliers $p_\text{LV}$ and $p_\text{RV}$ returned by the mechanics solver. The bidirectional exchange is visualized in {numref}`fig-pipeline-loop`. Boundary work, energy closure, and the pressure-strain proxies in {ref}`chap-results` use these solver multiplier pressures throughout, since they are the pressures synchronized with the saved deformation states.
