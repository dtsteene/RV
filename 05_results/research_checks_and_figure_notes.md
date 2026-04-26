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
