# Finsberg Reading Notes

These notes are for thesis writing, not for inclusion as a chapter.

Sources read:
- `/home/dtsteene/citations/03_computational_cardiac_mechanics/finsberg2017_phd_thesis.pdf`
- `/home/dtsteene/citations/01_work_loop_foundations/finsberg2019_assessment_regional_myocardial_work.pdf`

## Useful Points For This Thesis

### 1. Models Estimate Things We Cannot Measure

Finsberg's early thesis framing is useful: imaging measures anatomy and motion, while mechanics models can estimate quantities that are hard or impossible to measure directly in vivo, such as myocardial stress, contractility, elastance, and regional work.

This supports our framing:

> The finite-element model is not used because it is biological truth. It is used because it gives access to a mechanically consistent stress-strain work field that cannot be measured directly.

### 2. But Biomarkers Are Only As Good As The Input Data

His closing remarks are very relevant. He says that biomarkers extracted from a data-driven model cannot be better than the data used to constrain the model. He also warns that with enough degrees of freedom one can fit almost any data, so identifiability and validation matter.

This supports our honest limitation section:

> The model-resolved work is a model output, not a direct measurement. The controlled sweep removes some sources of uncertainty, but it does not remove dependence on geometry, material law, fibre architecture, activation, pressure tuning, and boundary conditions.

### 3. Regional Work Should Add Up To Stroke Work

Paper 4 gives a very clean motivation for our ratio analysis. Finsberg argues that an ideal regional work measure should sum to the whole-ventricle stroke work from the pressure-volume loop. That is exactly the reason magnitude preservation matters.

This is stronger than saying only "does the proxy correlate with work across cases?"

Good thesis wording:

> A high correlation can mean that the proxy ranks cases correctly, but it does not mean that it preserves the mechanical accounting of work. The stronger requirement is whether regional work estimates preserve the work balance implied by the pressure-volume loop.

### 4. Pressure-Strain Can Be Useful But Quantitatively Small

In Paper 4, pressure-strain work is much smaller than the finite-element stress-strain work and the PV-loop work. Yet pressure-strain still captures useful relative efficiency/wasted-work patterns.

This supports our two-level result:

1. Pressure-strain loops can be clinically useful for relative comparisons.
2. They should not automatically be read as quantitative mechanical work.

This is very close to our current result: free-wall ratios are reasonable, but septal magnitude depends strongly on pressure choice.

### 5. Fibre Work Is Important, But Not The Whole Work

Paper 4 reports fibre stress-strain work as roughly 60% of full tensor work in the LV cases, with the remaining work coming from cross-fibre directions. This is a useful answer to the worry that fibre work might be the "real" thing and full tensor work might be overkill.

Better interpretation:

> Fibre work is mechanically important and clinically intuitive, especially because active contraction is fibre-aligned. But the full tensor work is the natural work accounting measure. The difference between fibre and full tensor work is not noise; it is the cost of wall thickening, shear, and cross-fibre deformation.

### 6. Geometry, Wall Thickness, And Curvature Are Known Weaknesses Of Pressure-Strain

Paper 4 states the pressure-strain limitation very directly: using chamber pressure as stress assumes all segments have the same stress, regardless of size, curvature, or wall thickness.

This is exactly where our biventricular/septal study enters:

> If this assumption is already questionable within the LV, it becomes more questionable in the septum, where there are two adjacent pressures instead of one.

### 7. Reference Geometry Matters

The PhD thesis spends real space on unloaded/reference geometry. Image-based geometry is loaded by blood pressure; stress and strain depend on the reference configuration. For biventricular geometries, unloading can become unstable because the RV free wall can buckle or collide with the septum.

This is useful for methods/limitations, especially if we discuss patient-specific meshes or high-RV-pressure simulations.

### 8. Boundary Conditions Matter

Finsberg explicitly says cardiac boundary conditions are difficult and not settled. Paper 4 also notes that basal constraints can affect stress estimates near the base.

This supports our caution around basal/epicardial support work and why the energy-balance figure includes the Robin boundary contribution.

## How This Changes The Thesis

The main lesson is that our thesis should not sell pressure-strain work as "validated" or "invalidated" in one sentence.

The more honest structure is:

1. Whole-heart PV work gives the mechanical accounting target.
2. Finite-element stress-strain work gives a regional decomposition of that accounting inside the model.
3. Pressure-strain loops are clinically useful approximations, especially for relative patterns.
4. The question is where the approximation preserves useful mechanical structure and where it breaks.
5. Free walls behave well because the pressure assignment is physically simple.
6. The septum is hard because it is a shared wall, not because the model is mysterious.
