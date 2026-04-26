# Finish-By-Next-Week Plan

This is a working note, not a rendered thesis chapter. It is meant to keep the last week focused.

## The Main Rule

Do not try to make the thesis broader now. Make it defensible.

The strongest thesis is:

> We test a pressure simplification in a controlled biventricular model. The simplification works best where the wall has one adjacent cavity pressure. It becomes ambiguous in the septum because the septum is shared tissue loaded by both cavities. The fixed-geometry pressure sweep is not clinical PAH progression; it is a sensitivity test showing that proxy rankings can depend on the loading path.

This is enough. It is honest, mechanical, and useful.

## What To Read First

### 1. Your own Results and Discussion

Read these before reading more papers:

- `05_results/results.md`
- `06_discussion/discussion.md`

Goal: every paragraph should answer one of these:

- What was measured?
- What changed?
- Why does it make mechanical sense?
- What should the reader not over-interpret?

If a paragraph does not answer one of those, cut it or move it to notes.

### 2. Russell 2012

Purpose: defend what clinical pressure-strain work actually is.

Read only for:

- how LV pressure is estimated;
- what is validated;
- what is not validated;
- the limitation about geometry/force.

Do not use Russell to claim regional pressure-strain work is a direct energy measurement.

### 3. Delhaas 1994

Purpose: defend why stress-strain loop area is mechanically and metabolically interesting.

Read only for:

- fibre stress-fibre strain area;
- relation to regional oxygen demand / blood flow;
- the fact that this is LV-focused and uses a model estimate of stress.

Do not let this turn into "therefore fibre work is the true target." It supports fibre work as important, not as the only valid work measure.

### 4. Suga 1979

Purpose: defend the PV-loop / pressure-volume-area background.

Read only for:

- PVA as whole-ventricle framework;
- relation to oxygen consumption;
- why this motivates work-based thinking.

Do not use Suga to claim regional pressure-strain loops measure regional energy exactly.

### 5. Finsberg / biventricular PAH modelling

Purpose: defend novelty and scope.

Read only for:

- patient-specific biventricular models already exist;
- they can fit pressure, volume, and strain data;
- this thesis is not novel because it has a biventricular mesh, but because it tests pressure-strain proxy choices against model-resolved tensor work in a biventricular setting.

### 6. PAH and ventricular interdependence

Purpose: defend the clinical background.

Read only for:

- PAH changes RV pressure, volume, wall thickness, septal position, and LV filling;
- D-shaped LV / septal flattening comes from ventricular interaction and pressure/volume loading;
- real PAH is not a fixed-geometry pressure sweep.

Use this to justify caution, not to pretend the sweep is a clinical cohort.

## What Not To Read Now

- Do not deep-read broad cardiac mechanics reviews unless a thesis sentence needs them.
- Do not start a new literature section about RV remodelling.
- Do not chase every possible septum mechanics paper.
- Do not open a new patient-specific mesh story unless the simulations are ready and the figures are clean.
- Do not try to prove a new clinical proxy in the final week.

## Weak Spots To Double-Check

### 1. Directional septal work

This is currently risky.

Earlier notes said sheet-normal work carried about 63% of septal work. The current per-cell corrected table in `results/analysis/septum_mechanics/septum_case_values.csv` does not show that same story: fibre work is larger than sheet-normal work in the current signed density values.

Action:

- Do not put the 63% sheet-normal claim in the thesis unless the definitions are reconciled.
- If directional decomposition is used, first write a small verification note explaining whether the comparison is signed work, absolute work, cumulative work, or time-integrated component magnitude.
- Until then, keep the septum argument based on pressure assignment and ratio preservation, not directional dominance.

### 2. Ratio error needs to stay understandable

The Results now defines the ratio error mathematically. Keep it. It makes the table less black-box.

Make sure the reader understands:

- free-wall ratio error is an absolute LV/RV ratio difference;
- septum ratio error is mean absolute log error over septum/LV and septum/RV ratios;
- a log error of 0.18 is about a 20% multiplicative error.

### 3. The pressure sweep is not PAH progression

This is now said in several places. Keep it, but do not over-repeat it.

Best version:

> The sweep is a controlled loading-path sensitivity test. Real PAH changes pressure, geometry, stiffness, activation, and volume together.

### 4. The model is still valuable

This is one of the best framing points.

Best version:

> The simulation is a favourable test of the pressure simplification because pressure, strain, geometry, and model-resolved tensor work are all known in the same system. If the proxy is ambiguous even here, that ambiguity is mechanical, not only clinical measurement noise.

### 5. Clinical claims

Keep the clinical claim conservative:

- OK: "septal pressure assignment should be interpreted with caution."
- OK: "two-sided pressure choices may be more mechanically appropriate for septal magnitude comparisons."
- Not OK: "mean pressure should replace LV pressure clinically."
- Not OK: "this proves the best septal work formula in PAH patients."

## Figure Priorities

### Keep

- Free-wall versus septum schematic.
- Free-wall single-case ratio.
- Free-wall ratio across sweep.
- Old/new pressure-path figure.
- Old/new septal ratio-error figure.
- Septal lambda scan.

### Add only if time

1. A small "ratio error definition" schematic.
   - Could show tensor ratio vs proxy ratio with the formula.
   - Nice but not necessary because the math is now in text.

2. A clean pressure waveform example.
   - One healthy/low RV pressure and one high RV pressure case.
   - Useful if the reader needs to see the actual pressure loops behind the sweep.

3. Directional septal work decomposition.
   - Only after definitions are reconciled.
   - Do not add this figure just because it looks interesting.

## Work Plan With Codex

### Day 1

Polish Results and Discussion until they are the strongest chapters.

Tasks:

- read every paragraph aloud;
- remove vague claims;
- check every number against CSV/script output;
- make sure each figure is referenced before it appears;
- make captions explain the point, not just the content.

### Day 2

Make the Methods/Model chapters consistent with the final Results.

Tasks:

- remove old "three patient cases" language;
- make the fixed-geometry design explicit;
- ensure 0D/3D pressure distinction is clear;
- keep math where it helps and cut prose that only sounds fancy.

### Day 3

Citation and literature pass.

Tasks:

- Russell, Delhaas, Suga, Finsberg, Humbert/Kovacs/Tello;
- add citations only where they defend a sentence;
- avoid building a literature museum.

### Day 4

Figure pass.

Tasks:

- make all figure captions standalone;
- remove clutter from any figure that does not need it;
- check that every figure answers one question.

### Day 5

Full build and final read.

Tasks:

- install/run MyST or Jupyter Book if needed;
- fix broken references;
- search for old claims;
- final pass on abstract and conclusion.

