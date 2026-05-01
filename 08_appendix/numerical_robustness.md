# Numerical Robustness Appendix

This appendix collects the numerical checks that support the main pressure-strain conclusions. The purpose is not to claim that the simulations are free of numerical uncertainty. The purpose is to show where that uncertainty was tested, which quantities were sensitive, and why the final production choices were retained.

## Production Configuration

The production simulations use the compressible biventricular mechanics formulation, second-order tetrahedral displacement elements, a characteristic mesh length of 5 mm, and six coupled beats. Regional tensor work density is computed offline from the saved displacement checkpoints over the final beat. The current stress is evaluated from the UFL constitutive expression at quadrature points, previous stress and strain states are stored in a degree-six quadrature space, and DG0 test functions are used only to extract cellwise integrals from the quadrature-level work density.

The basal support combines Robin springs on the epicardium and base with a partial basal Dirichlet condition that fixes only the base-normal/global-x displacement component. It is not a full basal clamp. The remaining two displacement components on the basal surface are free to slide.

The robustness checks are summarized in {numref}`tab-numerical-robustness-summary`. The main pattern is consistent across them: hemodynamics and free-wall ratios are comparatively stable, while septal absolute work density is the quantity that most deserves caution.

```{table} Summary of numerical checks supporting the production configuration.
:name: tab-numerical-robustness-summary
:align: left

| Check | Evidence | Consequence for interpretation |
|---|---|---|
| Energy-consistent postprocessing | Quadrature-level tensor work closes the whole-heart boundary-work budget to about $10^{-5}$--$10^{-4}$ relative error | The regional tensor-work reference is computed from the same mechanics that drives the cavities |
| Mesh convergence | h=5 differs from h=3.75 by less than 0.8% for hemodynamics and less than about 3% for free-wall ratios; severe septal work differs by about 5--7% | Free-wall conclusions are robust; high-pressure septal magnitudes are reported with mesh sensitivity in mind |
| Full sweep rerun at h=5 | In the 16 paired cases, LV/RV pressures shifted by at most 1.8%/1.1% and free-wall ratios by a few percent | The final sweep should be read from the h=5 rerun; the h=10 sweep is retained only as a resolution comparison |
| Basal support audit | The production condition fixes only the base-normal/global-x component; tangential basal sliding remains | The model does not use a full basal clamp |
| No-Dirichlet variants | Endpoint cases failed during end-diastolic inflation after removing the basal displacement constraint | The partial constraint is a stabilizing modelling choice in this production setup |
| Postprocessing space replay | DG1 stays within about 1.2% of Quadrature6 for integrated regional tensor work; DG0 underestimates high-pressure septal work | DG1 is adequate for integrated regional totals in this check; DG0 is too crude for septal work; Quadrature6 is retained as the conservative production path |
| Robin work budget | Signed net Robin work is below about 0.2% of cavity boundary work in checked endpoint cases | Robin springs are part of the model definition but do not dominate the reported work-density results |
```

## Energy-Consistent Postprocessing

The model-resolved reference quantity is the tensor work density

$$
w_\mathrm{int}[\Omega_j] =
\frac{1}{|\Omega_{j,0}|}
\int_0^T\int_{\Omega_{j,0}}\mathbf{S}:\dot{\mathbf{E}}\,dV_0\,dt.
$$

Early postprocessing attempts projected stress and strain into discontinuous Galerkin spaces before integrating this quantity. During development, these projected-field replays were associated with large energy-budget discrepancies: smooth-looking stress and strain fields could still give work totals that were far too small compared with the boundary work. Later replay tests showed that this was not simply a DG1-versus-quadrature issue. Once the stress evaluation, pressure history, and boundary-work bookkeeping had been corrected, DG1 reproduced integrated regional work closely. DG0, however, still suppressed high-pressure septal work. The final pipeline therefore uses quadrature-level stress evaluation as the conservative production path rather than as proof that DG1 totals are unusable.

The final method avoids projecting the current stress before integration. The current stress is evaluated directly from the constitutive law at quadrature points, previous stress and strain are stored in a degree-six quadrature space for the trapezoidal time rule, and the DG0 space is used only as a cellwise partition of unity. As a hard implementation check, the sum of the DG0 per-cell work values is compared with an independent scalar domain integral of the same quadrature-level expression. In the checked runs, this agreement is at machine precision, confirming that the cellwise extraction is not changing the integrated work.

The external work terms were also matched to the solver formulation. Cavity work uses the actual solver cavity pressures, not the 0D elastance pressures, and the volume change is computed from the nonlinear cavity-volume expression rather than a linearized surface displacement. Robin work uses the same deformed-normal/Nanson formulation as the variational boundary condition. With these choices, the whole-heart tensor work and boundary-work budget close to the small residual shown in the main text.

## Mesh Convergence

The mesh-convergence study repeated three representative pressure cases, sPAP22, sPAP60, and sPAP95, using characteristic lengths of 10, 7.5, 5, and 3.75 mm. The 3.75 mm runs were used as the finest available reference.

At the production 5 mm resolution, hemodynamic quantities differed from the 3.75 mm reference by less than 0.8%. Free-wall work-density ratios were also stable, with differences below about 3%. Septal quantities were more mesh-sensitive, especially at high RV pressure. At 5 mm, septal tensor work differed from the 3.75 mm reference by about 0.2% in sPAP22, 3.8% in sPAP60, and 5.7% in sPAP95; the largest septal longitudinal-proxy discrepancy was about 6.6%. The 10 mm mesh was clearly too coarse for septal quantities in the high-pressure case, with errors up to about 18%.

The interpretation is therefore targeted: the 5 mm production mesh is sufficient for the qualitative free-wall conclusions tested here, while absolute high-pressure septal values should be read with the observed 5-7% difference between the 5 mm and 3.75 mm meshes in mind. This is a practical finest-mesh comparison, not a formal mesh-uncertainty estimate.

The final corrected pressure sweep was also rerun at 5 mm resolution. Across the 16 h=10/h=5 paired cases, achieved LV and RV end-systolic pressures changed by at most 1.8% and 1.1%, respectively. The free-wall model-resolved LV/RV tensor-work ratio changed by at most 5.4%, and the adjacent-pressure longitudinal proxy ratio by at most 8.3%. This supports the free-wall pressure-strain result as a robust regional finding rather than a consequence of the coarse 10 mm sweep.

The septum required a different interpretation. The 10 mm corrected sweep used a case-specific geometric septum mask that covered only part of the tag-3/canonical septum in several cases. In the completed 5 mm rerun, the geometric septum volume matches the tag-3 septum volume to within about 0.2%. For that reason, h=10-to-h=5 septal differences are not reported as simple mesh errors. The high-resolution septal results replace the earlier septal tables rather than merely perturbing them. This is the conservative choice: it avoids treating a change in septal definition as a change in mesh resolution.

## Basal Boundary Condition

The production basal condition fixes only the base-normal/global-x displacement component. This choice was checked in two ways.

First, the saved displacement fields were audited directly. In the completed pressure-sweep cases, the constrained basal displacement component was zero to saved precision at the checked time points, while the other two basal displacement components retained millimetre-scale sliding motion. This confirms that the final results used the intended partial constraint rather than a full basal clamp. The audit should be treated as a kinematic implementation check rather than a separate boundary-condition sensitivity study.

Second, the no-Dirichlet variant was tested by removing the basal displacement constraint while keeping the same Robin springs and the 5 mm production mesh. The sPAP22, sPAP60, and sPAP95 variants all reached the reference-configuration step but failed during end-diastolic inflation with linear solver non-convergence. A previous coarse one-beat Robin-only test had converged, but that result did not carry over to the production mesh and pressure cases. The retained basal condition is therefore best interpreted as a stabilizing constraint needed in this production setup, not as a physiological claim about the base being fixed in space.

The energetic effect of the Robin support was small compared with the cavity work in the cycle-integrated balance. In the checked endpoint cases, the signed net Robin work was below about 0.2% of the cavity boundary work.

## Postprocessing Space Sensitivity

The main postprocessing sensitivity is the choice of state/storage space used when reconstructing stress and strain histories. The final method uses degree-six quadrature storage because it most directly matches the quadrature-level constitutive evaluation and gave the tightest energy closure during development. A defence-oriented check recomputed sPAP22, sPAP60, and sPAP95 at the production 5 mm mesh with DG0 and DG1 state storage, while keeping the same degree-six integration rule. The current stress expression was still evaluated directly from the constitutive law; only the stored previous stress and strain state used the degraded space.

DG1 reproduced the Quadrature6 integrated regional tensor work closely. Across the three representative cases, the largest regional tensor-work-density difference was 1.2%, occurring in the septum. DG0 was less reliable: whole-heart and free-wall totals stayed within a few percent, but septal tensor work was underestimated by 7.7% in sPAP60 and 15.4% in sPAP95. The energy-budget residual was also smallest for Quadrature6, at about $10^{-5}$ to $10^{-4}$ relative error, compared with up to $2.7\times10^{-3}$ for DG1 and $1.5\times10^{-2}$ for DG0.

The interpretation is that the main integrated regional conclusions are not a fragile artifact of Quadrature6: DG1 gives essentially the same total regional tensor work. However, DG0 is not adequate for the high-pressure septal quantities, and the directional component decomposition is more sensitive than total work. Quadrature6 is therefore retained as the production postprocessing space because it gives the best energy closure and avoids suppressing septal stress-strain structure.
