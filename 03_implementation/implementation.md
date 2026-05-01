# Implementation and Challenges

The model chapter described the equations. This chapter describes the implementation choices that mattered for using the simulation as a reference for myocardial work. The goal was not only to obtain plausible pressure-volume loops, but to compute stress, strain, and regional tensor-work densities accurately enough to compare them with pressure-strain proxies.

The most important practical lesson was that global loop behaviour is not a sufficient validation target. A run can eject a plausible volume and still have incorrect stress fields, inconsistent work integration, or mismatched pressure histories. The checks below therefore focus on the field-level quantities used later in the results chapter.

The practical fixes below had different origins. The unloading workflow and the library-level deviatoric-stress issue came through supervisory debugging with Henrik Finsberg. My implementation work focused mainly on the tensor-work postprocessing: checking energy budgets, matching the solver boundary terms, and separating the 0D and 3D pressure histories. They are described together here because they define the final simulation and postprocessing pipeline.

## Prestress And Reference Configuration

The image-derived mesh represents the heart in a loaded end-diastolic shape, not in a stress-free reference configuration. If that mesh were used directly as the reference state, the constitutive law would treat an already pressurised geometry as unloaded, and the subsequent stress and strain fields would be biased.

To avoid this, an unloaded reference was estimated with the backward displacement method of Bols et al. {cite}`bols2013computational`, following the broader prestressing strategy used in patient-specific biomechanics {cite}`gee2010computational`. The practical unloading workflow used here was set up with Henrik Finsberg's guidance. In short, the mesh is repeatedly loaded with the target end-diastolic pressures, the resulting displacement is used to update the reference coordinates, and the process continues until the loaded configuration reproduces the image-derived end-diastolic geometry. The same basal and Robin support definitions used in the main mechanics solve are carried through this step so that the reference configuration and boundary supports remain consistent.

The coupled simulation then starts from the estimated unloaded reference, inflates to the image-derived end-diastolic state, and proceeds through the cardiac cycle. This makes the stress-strain history a history relative to the constitutive reference state, rather than relative to an already loaded image frame.

## Field-Level Stress Check

The most consequential code issue in the project was a stress error in the compressible material path of `fenicsx-pulse`. The Holzapfel-Ogden law depends on the finite-strain state through $\mathbf{C}$ and $J$, equivalently through the full Green-Lagrange strain tensor $\mathbf{E}$. In the problematic implementation, the stress routine received only the deviatoric part of the strain state, so the volumetric contribution was dropped.

The error was not obvious from the pressure-volume loops. The runs completed, ejection fractions were plausible, and the loop shapes looked qualitatively normal. The problem appeared when mean fibre stresses and regional work scales were compared with reported myocardial stress and work ranges {cite}`delhaas1994regional,finsberg2019assessment`. The stress magnitudes were too low, and Henrik Finsberg identified that the compressible library path was dropping the volumetric part of the strain state.

After the full strain state was passed to the stress calculation, the pressure-volume behaviour remained qualitatively similar, but the stress magnitudes and work budgets moved into the expected range. This is why the thesis treats stress magnitude, tensor-work closure, and pressure-strain consistency as implementation checks, not just secondary outputs.

## Tensor-Work Extraction

Regional tensor work was computed from the stress-strain contraction

$$
W_\mathrm{int}[\Omega_j] = \sum_i \int_{\Omega_j} \bar{\mathbf{S}}_i : \Delta \mathbf{E}_i \, dV_0 ,
$$

where $\Omega_j$ is a myocardial region, $\bar{\mathbf{S}}_i$ is the timestep-average second Piola-Kirchhoff stress, and $\Delta\mathbf{E}_i$ is the Green-Lagrange strain increment. This integral is most consistent when evaluated at the quadrature points where the constitutive law is evaluated during Newton assembly.

During development, a large work-budget mismatch appeared when replayed stress and strain fields were integrated offline. Projected DG fields were an obvious suspect because stress and strain products can be sensitive to projection near regional interfaces and through the thin septum. Later replay tests showed a more nuanced picture: DG1 gave nearly the same integrated regional tensor work as Quadrature6 once the stress, pressure, and boundary-work bookkeeping had been fixed, whereas DG0 remained too crude for high-pressure septal work. The earlier mismatch is therefore best read as part of the wider tensor-work debugging history, not as evidence that DG1 is intrinsically unusable.

The final pipeline keeps the work calculation at quadrature level because this is the most direct match to the constitutive evaluation used by the solver and gives the tightest energy closure. The current stress is evaluated directly from the UFL constitutive expression, previous stress and strain states are stored in a degree-six quadrature space, and DG0 is used only as a cellwise partition for extracting per-cell integrals after the quadrature-level integrand has already been formed. This makes the regional cell outputs sum to the same value as the scalar domain assembly, up to numerical precision. The DG0, DG1, and Quadrature6 sensitivity checks are reported in the numerical robustness appendix.

## Solver-Consistent Boundary Work

The internal tensor work is only a useful energy check if the external work is computed with the same assumptions as the mechanics solver. Two details mattered.

First, the Robin spring support is applied in the current configuration and only in the deformed normal direction. A reference-configuration formula using the full displacement vector overestimates the spring work because it penalises tangential sliding that the solver does not penalise. The postprocessing therefore uses the same deformed-normal and surface-measure mapping as the variational form.

Second, cavity pressure work must use the nonlinear cavity-volume functional, not the small-displacement approximation $\int \mathbf{N}\cdot\Delta\mathbf{u}\,dS_0$. At finite deformation, the linearised volume change is noticeably biased during the phases that dominate work. The final calculation uses

$$
W_\mathrm{cav} = \sum_i \bar p_i \, \Delta \mathcal{V}_i ,
$$

with solver cavity pressure converted to SI units and $\Delta\mathcal{V}_i$ taken from the same cavity-volume functional used by the coupled mechanics solve. Work densities are then reported as J/m$^3$, equivalently Pa or kPa. With quadrature-level internal work, solver-consistent Robin work, and nonlinear cavity-volume changes, the checked replay cases close the energy balance to the $10^{-4}$ relative level.

## 0D-3D Pressure Bookkeeping

The coupled simulation contains two pressure-like quantities. The 0D circulation has an elastance pressure, while the 3D mechanics solve has a cavity-pressure Lagrange multiplier that enforces the cavity volume constraint. These are related, but they are not interchangeable.

This distinction became visible during checkpoint postprocessing. When boundary work was recomputed offline using the 0D pressure history, the energy balance showed a large discrepancy. During the live solve, where the boundary work used the Lagrange multiplier pressure, the same calculation closed tightly. The fix was to save the solver pressure multiplier at each time step together with the displacement checkpoint.

All final tensor-work checks and pressure-strain proxy calculations therefore use the 3D solver cavity pressures. The 0D model remains essential because it supplies the coupled loading path, but the mechanical work calculation uses the pressure that actually appears in the 3D variational problem.

## Fixed Cardiac Clock

The production coupled simulations use a fixed cardiac clock: 75 beats per minute, with ventricular activation starting at the beginning of the beat, contraction duration $T_C=0.25$ s, and relaxation duration $T_R=0.40$ s. These timing values are part of the mechanics protocol and are not retuned across the pressure-loading cases.

This matters because standalone 0D parameter files can contain timing values from circulation fitting. Those values describe the standalone elastance model, not a change in 3D activation. When a circulation parameter file is loaded into the coupled driver, the mechanics timing is reset to the fixed protocol. The pressure sweep therefore changes the 0D loading and chamber/circulation parameters, while the 3D geometry, material law, active-tension law, peak active tension, fibre field, and activation timing are held fixed.
