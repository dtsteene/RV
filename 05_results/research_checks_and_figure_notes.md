# Research Checks And Figure Notes

This is a working note for the thesis writing session on 2026-04-25. It is not in the table of contents. The point is to keep track of places where the thesis should either cite something directly or stay deliberately cautious.

## Claims To Keep Conservative

- Do not describe the finite-element tensor work as an unquestionable truth standard. Use "model-resolved tensor work", "finite-element tensor work", or "the tensor work computed by the model".
- Do not describe the fixed-geometry pressure sweep as clinical PAH progression. It is a controlled loading-path sensitivity test.
- Do not claim that transmural pressure is generally best for septal work. It is meaningful for pressure difference, septal flattening, and D-sign mechanics, but it did not preserve septal work magnitudes in the present ratio tests.
- Do not claim that mean pressure is now the clinically correct septal pressure. The safer statement is that two-sided pressure choices were more stable for septal magnitude preservation in this model.
- Do not treat pressure-volume area as proof that regional pressure-strain loops measure metabolic energy. Suga supports the whole-ventricle pressure-volume framework; the regional proxy is a separate approximation.

## Literature Checks Worth Doing

1. Septal mechanics and ventricular interdependence.
   - Need a strong source for the plain statement that septal position/flattening is governed by the pressure difference and by RV pressure/volume loading.
   - Good search terms: "ventricular interdependence septal flattening pressure overload", "D-shaped left ventricle pulmonary hypertension septal curvature", "interventricular septum pressure difference mechanics".

2. PAH pressure overload versus volume/remodelling.
   - The thesis currently frames PAH mainly as RV pressure overload, while acknowledging that real patients also change RV volume, wall thickness, stiffness, and shape.
   - Check whether the PAH sources already used (`humbert2022.pdf`, `kovacs2009.pdf`, `tello2019.pdf`) support that balance, or whether a dedicated RV remodelling review should be cited.

3. Suga and regional work.
   - `/home/dtsteene/citations/01_work_loop_foundations/suga1979_total_energy_cardiac_oxygen.pdf` supports whole-ventricle pressure-volume area as an energetic framework.
   - It should not be stretched into a claim that fibre stress-strain work or pressure-strain loops are automatically the biological truth at regional scale.
   - If the discussion says anything stronger, read Delhaas and Russell again and keep the wording narrow.

4. Existing biventricular finite-element work.
   - We should avoid implying that nobody has studied biventricular geometry.
   - Finsberg/Henrik-related work is already cited for patient-specific biventricular finite-element modelling. Additional local sources now cover broader regional-work modelling: `wang2012myocardial`, `namani2020effects`, `pluijmert2017determinants`, `ahmadbakir2018multiphysics`, and `craine2024successful`.
   - If the intro or Chapter 1 makes a novelty claim, the novelty should be the proxy-vs-tensor-work comparison under biventricular pressure assignment, not biventricular mechanics itself and not regional work as a general FEM object.

5. Clinical measurability of better stress proxies.
   - LV pressure, RV systolic pressure, wall thickness, curvature, and cavity radius are all measurable in principle, but each adds error.
   - Need a citation if the discussion claims RV pressure estimates from tricuspid regurgitation are often unavailable or inaccurate.

## Figure Ideas

1. Minimal mechanics cartoon: free wall versus septum.
   - Left panel: free wall with one adjacent pressure and one tissue wall.
   - Right panel: septum with LV pressure on one side and RV pressure on the other.
   - Purpose: make the "one-pressure wall" versus "two-sided shared wall" idea obvious before the results table.

2. Septal directional work decomposition.
   - This should only be used if recomputed cleanly from the same per-cell data used for the final results.
   - Do not reuse the older "sheet-normal dominates the septum" story without checking it. Later per-cell checks suggested a different decomposition, with fibre work contributing much more than the first quick analysis implied.
   - A safe figure would show the actual final directional components case by case, without forcing the interpretation in advance.

3. Old versus corrected pressure paths.
   - A small figure showing LV and RV peak pressure across cases in the old handover data and the corrected data.
   - Purpose: make the sign/ranking flip less mysterious. The reader can see that the old LV pressure moved with severity, while the corrected LV pressure is nearly preserved.

4. Keep current result figures minimal.
   - The strongest current set is:
     - free-wall single-case ratio;
     - free-wall ratio across sweep;
     - old/new septal ratio error;
     - septal lambda scan.
   - Avoid adding many dense correlation heatmaps unless the text needs them. The story is clearer when the figures answer one question each.

## Diagnostic Plot Sweep, 2026-04-26

This was a triage of older and per-run diagnostic plots under
`cardiac-work/results/sims/*/analysis` and
`cardiac-work/results/comparisons/presentation`.

### Engineering debug dashboards

Representative files:

```text
/home/dtsteene/D1/cardiac-work/results/sims/2026-04-23/UKB_6beats_run_1047450/analysis/last_beat/engineering_debug.png
/home/dtsteene/D1/cardiac-work/results/sims/2026-04-23/UKB_6beats_run_1047450/analysis/all_beats/engineering_debug.png
/home/dtsteene/D1/cardiac-work/results/sims/2026-04-23/UKB_6beats_run_1047457/analysis/last_beat/engineering_debug.png
```

Verdict: excellent quality-control material, too busy for the main thesis.

The useful thesis idea is not the whole five-panel dashboard. It is the trimmed
validation message:

> The quadrature-level internal work overlaps the exact boundary-plus-Robin
> work, while passive elastic work returns close to zero over a cycle.

If a figure is needed in the implementation chapter or appendix, remake it as
one or two clean panels rather than reusing the dashboard:

- cumulative internal work versus exact boundary + Robin work;
- optional active/passive/compressible split as a numerical sanity check.

Do not use the dashboard's "Clinical PV vs Exact Boundary Work" panel directly
from the corrected n=16 runs. In the saved all-beat and last-beat diagnostics,
the 0D clinical volume/pressure histories are not a reliable last-beat signal
for that plot, so the blue clinical-PV curve can appear flat or misleading.
The solver pressure, FEM volume-change, and exact boundary work are the relevant
quantities for the implementation validation.

### Old stress-pressure plots

Representative files:

```text
/home/dtsteene/D1/cardiac-work/results/comparisons/presentation/ukb_spectrum/stress_strain_spectrum.png
/home/dtsteene/D1/cardiac-work/results/comparisons/presentation/ukb_spectrum/stress_components_spectrum.png
/home/dtsteene/D1/cardiac-work/results/comparisons/presentation/patient_healthy_vs_pah/pressure_vs_transmural_stress.png
/home/dtsteene/D1/cardiac-work/results/comparisons/presentation/patient_healthy_vs_pah/stress_loops.png
```

Verdict: good exploratory ideas, but do not reuse as final result figures unless
they are regenerated from the corrected pipeline.

The strongest conceptual point is:

> Cavity pressure is a scalar boundary load, while myocardial stress is a local
> tensor field. Pressure can be a useful stress scale in free walls, but it is
> not identical to fibre, sheet, normal, or shear stress inside the myocardium.

The corrected n=16 quick check supports this caution: peak septal fibre stress
tracks peak transmural pressure strongly in the corrected sweep
(`r = +0.968`), but that is a peak-stress statement, not a work-density proxy
statement. It should not be used to override the ratio results, where two-sided
pressure choices preserve septal work-density magnitudes better than
transmural pressure.

Per-run `stress_analysis.png` files from April are not useful as final figures:
the stress curves are essentially blank in the inspected runs, likely because
the old Cauchy-stress metric keys are absent or renamed. Treat those plots as a
retired diagnostic path.

### Abandoned figure ideas

- `proxy_validation.png` is too crowded and uses rate-like scatter comparisons
  that are harder to explain than the current ratio/correlation figures.
- `loops.png` is pedagogically useful, but the existing cascade-loop figure is
  a better place to show how information is lost through simplification.
- `work_redistribution_spectrum.png` is superseded by the current regional
  ratio analysis and the new work-component breakdown.
- `stress_components_spectrum.png` is visually interesting and supports the
  "tensor work contains more than fibre work" point, but the cleaner final
  version is the corrected n=16 component figure already added to Results.
- The RV Lakatos bridge is worth keeping: it directly connects the RV free-wall
  result to clinical pressure-strain validation, while still using model-resolved
  tensor work as the thesis target.

## Possible Extra Analyses

1. Recompute septal directional decomposition as a publication-quality figure.
   - Current numbers are not stable enough to be a main argument unless regenerated from the final per-cell pipeline.
   - If this is done, the figure should state clearly whether it shows signed work, absolute work, work density, or a component fraction.

2. Patient meshes as geometry tests.
   - Run the free-wall and septal ratio analysis on the patient-specific meshes once those simulations are stable.
   - Main question: does adjacent pressure remain good for free walls when wall thickness and RV shape change?

3. Higher-resolution septal test.
   - The through-wall pressure idea is physically attractive, but current septal layer resolution is limited.
   - A refined septum or idealized biventricular wall would be the right way to test detailed through-wall stress claims.

## Source Audit Link

- The current source-status checklist is in `SOURCE_AUDIT.md`.
- Any citation used for a scientific or methodological claim should either have a local PDF/source file or be removed/softened before submission.
