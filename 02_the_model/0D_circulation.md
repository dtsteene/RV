# The Zero-Dimensional Circulation Model

A finite element model of the myocardium, however detailed, cannot beat realistically in isolation. Without a circulatory system imposing pressure boundary conditions at the endocardial surfaces, there is no way to determine what pressures the ventricles should develop, or when the valves should open and close, or how the hemodynamic state should evolve from beat to beat. The heart is a pump embedded in a closed hydraulic loop, and its behavior is shaped at every moment by the impedance of the vessels it is pumping into and the compliance of the vessels it is pumping from.

To provide this circulatory context, we couple the three-dimensional finite element model to a zero-dimensional lumped-parameter model of the complete cardiovascular system. In a zero-dimensional model, the spatial distribution of quantities like pressure and flow rate is discarded; each element of the cardiovascular circuit — a blood vessel, a valve, a cardiac chamber — is represented by a single ordinary differential equation relating pressure, volume, and flow at its inlet and outlet. This is the same principle that underlies the electrical circuit analogy frequently used in physiology teaching, where pressure corresponds to voltage, volumetric flow rate corresponds to current, and the mechanical resistance of a vessel corresponds to an electrical resistor. The analogy is more than pedagogical: the governing equations for linear RC circuits and linear fluidic circuits are mathematically identical, which is why circuit simulation methods can be directly applied to lumped-parameter cardiovascular models.

The specific model we use is the closed-loop four-chamber formulation of Regazzoni et al. {cite}`regazzoni2022cardiac`, implemented in the `circulation` software package {cite}`circulation`.

## State Variables and Circuit Topology

The model state is a vector $\mathbf{y}(t) \in \mathbb{R}^{12}$ consisting of the four chamber volumes $V_\text{LA}, V_\text{LV}, V_\text{RA}, V_\text{RV}$, the four vascular pressures $P_\text{AR,sys}, P_\text{VEN,sys}, P_\text{AR,pul}, P_\text{VEN,pul}$, and the four vascular flow rates $Q_\text{AR,sys}, Q_\text{VEN,sys}, Q_\text{AR,pul}, Q_\text{VEN,pul}$. The topology of the circuit is a closed loop: blood flows from the left atrium through the mitral valve into the left ventricle, through the aortic valve into the systemic arterial compartment, through the systemic venous compartment and the tricuspid valve into the right ventricle, through the pulmonary valve into the pulmonary arterial compartment, through the pulmonary venous compartment, and back into the left atrium.

Each cardiac chamber has a time-varying elastance $E(t)$ that determines how cavity pressure responds to volume. The chamber pressure is

$$
P_\text{ch}(t) = E(t) \bigl( V(t) - V_0 \bigr),
$$

where $V_0$ is the unstressed volume. The elastance function follows the Blanco activation model {cite}`blanco2010computational`:

$$
E(t) = E_A \, f(t) + E_B,
$$

where $E_A$ is the active (contractile) elastance, $E_B$ is the passive (diastolic) elastance, and $f(t)$ is a smooth activation function that rises from 0 to 1 during contraction and returns to 0 during relaxation. The activation function is defined piecewise using cosine segments parametrized by the contraction onset $t_C$, contraction duration $T_C$, and relaxation duration $T_R$:

$$
f(t) = \begin{cases}
\frac{1}{2}\!\left(1 - \cos\!\left(\frac{\pi}{T_C}(t - t_C)\right)\right) & t_C \leq t < t_C + T_C, \\[4pt]
\frac{1}{2}\!\left(1 + \cos\!\left(\frac{\pi}{T_R}(t - t_C - T_C)\right)\right) & t_C + T_C \leq t < t_C + T_C + T_R, \\[4pt]
0 & \text{otherwise}.
\end{cases}
$$

The four cardiac valves are modeled as ideal diodes with finite forward resistance $R_\text{min}$ and a large backward resistance $R_\text{max}$. The flow through a valve between upstream pressure $P_\text{up}$ and downstream pressure $P_\text{down}$ is

$$
Q_\text{valve} = \frac{P_\text{up} - P_\text{down}}{R(P_\text{up}, P_\text{down})}, \qquad R = \begin{cases} R_\text{min} & P_\text{up} > P_\text{down}, \\ R_\text{max} & \text{otherwise}. \end{cases}
$$

The systemic and pulmonary vascular beds are each represented by two compartments — arterial and venous — connected by resistive and inductive elements. Each arterial compartment has a compliance $C_\text{AR}$, a resistance $R_\text{AR}$, and an inductance $L_\text{AR}$ that captures the inertia of blood in the large vessels; the venous compartment is analogous with parameters $C_\text{VEN}$, $R_\text{VEN}$, and $L_\text{VEN}$.

## The ODE System

Conservation of volume in the four chambers gives

$$
\begin{aligned}
\dot{V}_\text{LA} &= Q_\text{VEN,pul} - Q_\text{MV}, \\
\dot{V}_\text{LV} &= Q_\text{MV} - Q_\text{AV}, \\
\dot{V}_\text{RA} &= Q_\text{VEN,sys} - Q_\text{TV}, \\
\dot{V}_\text{RV} &= Q_\text{TV} - Q_\text{PV},
\end{aligned}
$$

where $Q_\text{MV}, Q_\text{AV}, Q_\text{TV}, Q_\text{PV}$ are the valve flows computed from the diode model above. Conservation of volume in the vascular compartments, using the constitutive relation $V = CP$ for the elastic vessels, gives the pressure dynamics:

$$
\begin{aligned}
\dot{P}_\text{AR,sys} &= \frac{Q_\text{AV} - Q_\text{AR,sys}}{C_\text{AR,sys}}, \\
\dot{P}_\text{VEN,sys} &= \frac{Q_\text{AR,sys} - Q_\text{VEN,sys}}{C_\text{VEN,sys}}, \\
\dot{P}_\text{AR,pul} &= \frac{Q_\text{PV} - Q_\text{AR,pul}}{C_\text{AR,pul}}, \\
\dot{P}_\text{VEN,pul} &= \frac{Q_\text{AR,pul} - Q_\text{VEN,pul}}{C_\text{VEN,pul}}.
\end{aligned}
$$

The flow rates through the vascular compartments obey momentum conservation with resistive dissipation and vessel inertance:

$$
\begin{aligned}
\dot{Q}_\text{AR,sys} &= \frac{P_\text{AR,sys} - P_\text{VEN,sys} - R_\text{AR,sys}\,Q_\text{AR,sys}}{L_\text{AR,sys}}, \\
\dot{Q}_\text{VEN,sys} &= \frac{P_\text{VEN,sys} - P_\text{RA} - R_\text{VEN,sys}\,Q_\text{VEN,sys}}{L_\text{VEN,sys}}, \\
\dot{Q}_\text{AR,pul} &= \frac{P_\text{AR,pul} - P_\text{VEN,pul} - R_\text{AR,pul}\,Q_\text{AR,pul}}{L_\text{AR,pul}}, \\
\dot{Q}_\text{VEN,pul} &= \frac{P_\text{VEN,pul} - P_\text{LA} - R_\text{VEN,pul}\,Q_\text{VEN,pul}}{L_\text{VEN,pul}}.
\end{aligned}
$$

This is a system of twelve coupled ODEs — four volume equations, four pressure equations, and four flow equations — with the algebraic valve flow relations and the time-varying elastance functions embedded in the right-hand side. The system is stiff because the valve resistances switch between $R_\text{min}$ and $R_\text{max}$ (a ratio of order $10^7$), producing rapid transitions in the flow signals at valve opening and closing events. The system is integrated forward in time using a stiff ODE solver with an analytically provided Jacobian, which substantially improves the convergence of the implicit time-stepping scheme.

## Coupling the 3D and 0D Models

The link between the finite element model and the circulation model is an exchange of cavity volume and cavity pressure at each time step. The 0D model prescribes the ventricular volumes as a function of time over the cardiac cycle — because in the coupled system the ventricular volumes come from the deforming three-dimensional geometry rather than from a parameterized chamber elastance function. Given a target volume, the finite element solver deforms the myocardium to match that volume while satisfying mechanical equilibrium, and returns the resulting cavity pressure. This pressure is then fed back into the 0D model to update the valve states, the arterial pressures, and the flow rates for the next time step.

A practical complication arises from the fact that the end-diastolic cavity volume of the finite element mesh does not, in general, match the end-diastolic volume that the 0D model was calibrated to produce. The mesh is generated from an idealized or patient-specific geometry with a specific anatomical size, while the 0D model is tuned to reproduce the hemodynamic targets from clinical data. Rather than attempting to rescale either model to match the other — which would require either reshaping the geometry or abandoning the clinical calibration of the 0D parameters — we introduce a fixed volume ratio that scales the volume requests from the 0D model into the frame of the FEM mesh:

$$
V_\text{FEM}(t) = \frac{V_\text{mesh,ED}}{V_\text{0D,ED}} \cdot V_\text{0D}(t).
$$

Here $V_\text{mesh,ED}$ is the end-diastolic cavity volume measured directly from the unloaded finite element mesh, and $V_\text{0D,ED}$ is the end-diastolic volume of the same cavity at steady state in the 0D simulation. The ratio of these two quantities is computed once at the beginning of the simulation and held fixed throughout. The result is that the 0D model drives the volume dynamics in the correct physiological proportions, while the FEM model deforms within its own geometric scale. The pressure that emerges from the FEM solution reflects the actual stiffness of the discretized myocardium, so the pressure-volume relationship is not imposed but computed.

This coupling scheme is implemented as a callback function that the 0D solver invokes at each time step. The callback receives the target volume, calls the finite element solver to compute the equilibrium displacement for that volume, extracts the resulting cavity pressure from the Lagrange multiplier associated with the incompressibility constraint, and returns this pressure to the 0D solver. The nonlinear finite element problem is solved using a Newton-Krylov method with line search; if the Newton iterations fail to converge at a given time step, the step is subdivided into smaller substeps to improve convergence. This adaptive substep strategy adds robustness during the rapid volume changes at valve opening and closing, where the stiffness of the mechanical problem changes abruptly.
