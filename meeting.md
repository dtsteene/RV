# Meeting: The Septal Work Dilemma


:::{admonition} Research Question
:class: important
**How do we measure RV and Septal Work clinically?**
In the clinic, Regional Work is estimated using **Pressure-Strain Loops** ($\text{Area} = \oint P \cdot d\epsilon$).
For the Free Walls, the pressure is ($P_{LV}$ or $P_{RV}$).
**But for the Septum, which pressure should be used?**
* $P_{LV}$?
* $P_{RV}$?
* Transseptal Pressure ($P_{LV} - P_{RV}$)?
:::

## The Simulation Framework
We are using a fully coupled electromechanical "Digital Twin" to answer this.

* **Pulse (Mechanics):** Solves "True" fiber stress ($\sigma$) and strain ($\epsilon$) locally.
* **Circulation (Hemodynamics):** Provides the $P_{LV}$ and $P_{RV}$ boundary conditions.
* **The Setup:** We compare a **Healthy Control** vs. **Acute Pulmonary Hypertension (PH)**.

---

## The Methodology: Ground Truth vs. Clinical Surrogate

We are comparing the "Real" work calculated by the physics engine against the "Estimated" work available to a clinician.

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} The Ground Truth (Fiber Work)
:class-header: bg-success text-white
**Metric:** Fiber Stress-Strain Area
$$W_{fiber} = \oint \sigma_{fiber} \cdot d\epsilon_{fiber}$$
* **Source:** Finite Element Model.
* **Meaning:** The actual metabolic energy consumed by the local tissue fibers.
:::

:::{grid-item-card} The Clinical Surrogate (Pressure Work)
:class-header: bg-info text-white
**Metric:** Pressure-Strain Area
$$W_{clin} = \oint P_{chamber} \cdot d\epsilon_{long}$$
* **Source:** Catheter ($P$) + Echo Strain ($\epsilon$).
* **The Problem:** For the Septum, **what is $P_{chamber}$?**
:::
::::

---

##  Some results so far

### Less Pulmonary Hypertension

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item}
```{figure} CONTROL/plots/stress_strain_loops_last_beat.png
:name: control-fiber
:width: 100%
**True Fiber Work (Ground Truth)**
The Septum (Green) makes a wide, counter-clockwise loop. It is doing positive work.
```
:::

:::{grid-item}
```{figure} CONTROL/plots/pressure_strain_loops_last_beat.png
:name: control-pressure
:width: 100%
**Pressure-Strain (Clinical Surrogate)**
Using $P_{LV}$ (Top Row), the Septal loop looks similar to the Free Wall.
```
:::
::::

### Pulmonary Hypertension

*This is where the metrics decouple.*

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item}
```{figure} ../PH/plots/stress_strain_loops_last_beat.png
:name: PH-fiber
:width: 100%
**True Fiber Work (Ground Truth)**
**Look at the Green Loop.** It is distorted and figure-8 shaped. The Septum has mechanically failed.
```
:::

:::{grid-item}
```{figure} PH/plots/pressure_strain_loops_last_beat.png
:name: ph-pressure
:width: 100%
**Pressure-Strain (Clinical Surrogate)**
If we calculate Septal Work using $P_{LV}$ (Top Row), we still see a large area!
**The clinical metric might be "lying" by ignoring the RV back-pressure.**
```
:::
::::

-----

## Transseptal Pressure?

Our data suggests that using $P_{LV}$ to calculate Septal Work in PH patients leads to a massive overestimation of septal function.
```{figure} PH/plots/work_comparison_bars_last_beat.png
:name: work-bars
:width: 80%
:align: center

**Bar Chart Comparison:** Note the discrepancy between the PV-derived work (Top Left) and Fiber Work (Bottom Left) for the Septum.
```

