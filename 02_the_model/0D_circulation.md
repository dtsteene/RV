# 0D Circulation Model

To simulate a beating heart, we must account for the blood flow in and out of the ventricles. We couple our high-fidelity 3D heart model to a simplified **0D (lumped-parameter)** model of the entire circulatory system.

We use the **Regazzoni (2020)** circulation model, implemented in the `circulation` library {cite}`circulation`. This is a closed-loop model that includes the four chambers of the heart and the systemic and pulmonary vascular loops.

## The Concept: Hydraulic Analogies

In 0D modeling, we use electrical circuit analogies to represent fluid dynamics. The mapping between the two domains is as follows:

| Hydraulic Quantity | Electrical Analogy | Physical Meaning |
| :--- | :--- | :--- |
| **Pressure ($P$)** | Voltage ($V$) | Potential energy driving the flow |
| **Flow ($Q$)** | Current ($I$) | Rate of volume transport |
| **Volume ($V$)** | Charge ($q$) | Quantity of fluid |
| **Resistance ($R$)** | Resistor | Friction in vessels/valves |
| **Compliance ($C$)** | Capacitor | Elasticity of vessel walls |
| **Inertance ($L$)** | Inductor | Inertia of blood mass |

## The Systemic & Pulmonary Loops

Both the systemic (body) and pulmonary (lung) circulations are modeled using **3-element Windkessel (RCR)** blocks. This captures the essential physics of arterial load.



**Proximal Resistance ($R_{AR}$)**
: The resistance of the large arteries (Aorta/Pulmonary Artery).

**Compliance ($C_{AR}$)**
: The elasticity of the large arteries, which store blood during systole and release it during diastole (the "Windkessel effect").

**Distal Resistance ($R_{VEN}$)**
: The resistance of the arterioles and capillaries, which determines the mean arterial pressure.

The governing equation for pressure in an arterial compartment is:

$$
\frac{dP}{dt} = \frac{Q_{in} - Q_{out}}{C}
$$

Where flow $Q$ is driven by the pressure gradient: $Q = \Delta P / R$.

## Coupling: The 3D-0D Interface

The critical link between the 3D finite element model and this 0D circuit is the exchange of **Cavity Volume** and **Cavity Pressure**. This two-way coupling ensures that the heart pumps against a realistic, dynamic load.

```{mermaid}
flowchart LR
    subgraph FEM ["3D Finite Element Model"]
        A[Deformation]
    end

    subgraph Circ ["0D Circulation Model"]
        B[Lumped Parameter Solver]
    end

    A -- "Cavity Volume (V)" --> B
    B -- "Cavity Pressure (P)" --> A
    
    style FEM fill:#f9f,stroke:#333,stroke-width:2px
    style Circ fill:#bbf,stroke:#333,stroke-width:2px
```