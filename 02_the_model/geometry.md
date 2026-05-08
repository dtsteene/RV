# Geometry and Simulation Cases

(sec-geometry-anatomical-model)=
## The Anatomical Model Used In This Study

The main production analyses in this thesis run on one biventricular geometry, built in three steps. The shape comes from the UK Biobank statistical atlas of Mauger et al. {cite}`mauger2019right`, taking the mean of a healthy sub-cohort of 630 cardiac MR scans as the baseline. The atlas is then cut at a single flat plane below the valves so that the basal boundary of the simulation domain is one planar surface rather than the irregular valve-annulus geometry — a standard simplification in finite-element ventricular mechanics {cite}`finsberg2018efficient,pluijmert2017determinants`. What remains is meshed and labelled by `cardiac-geometries` {cite}`cardiac_geometries`: endocardial and epicardial surfaces, the basal cap, and a cell-level partition of LV free wall, RV free wall, and septum. {numref}`fig-mesh-regions` shows the result, with the LV, RV, and septum coloured.

```{figure} ../figures/fig_2_1_mesh_regions.png
:name: fig-mesh-regions
:width: 70%

Cell-level region tags on the clipped biventricular UK Biobank baseline mesh. Short-axis cut through mid-ventricle exposing the LV cavity (right), the RV cavity (left), and the wall thickness, with the LV free wall (blue), RV free wall (pale yellow), and interventricular septum (red) visible as separate tagged regions. The mesh stops at a single planar base just below the atrioventricular valves; the atria, the valves themselves, and the RV outflow tract above the pulmonary valve are not represented; see the next figure for the basal clip. The same colour mapping is reused everywhere region-resolved quantities are shown.
```

Patient-specific healthy and PAH meshes also exist in the wider project and appear later as exploratory geometry-sensitivity checks. They are not part of the main pressure-loading sweep: keeping anatomy fixed is what lets the sweep isolate the pressure-strain approximation, rather than test it against simultaneously remodelled tissue. {ref}`chap-discussion` returns to the patient-specific cases as preliminary evidence that geometry and remodelling matter for the absolute magnitudes, but the main comparisons in this thesis use the single UKB baseline geometry.

Anything above the basal cut — the upper portion of the outflow tracts, the valve regions, the atria, and the great vessels — is not represented spatially in this thesis; its hemodynamic role is carried by the 0D circulation model described in {ref}`sec-0d-circulation`.

The constitutive framework treats the ventricular myocardium as nonlinearly elastic, incompressible, and direction-dependent, with the response organized by local fibre and sheet architecture {cite}`holzapfel2009constitutive`. Near-incompressibility is enforced numerically in the finite-element implementation; the constitutive law and its boundary conditions are given in {ref}`sec-3d-mechanics`. The endocardium and epicardium are thin lining layers, not separate volumetric materials in this model. They matter here as surfaces: blood pressure acts on the endocardial cavity boundaries, epicardial springs support the outer boundary, and both surfaces define transmural coordinates for fibre assignment. {numref}`fig-surface-tags` shows the four boundary surfaces that carry these roles.

```{figure} ../figures/fig_2_6_surface_tags.png
:name: fig-surface-tags
:width: 65%

Boundary surface tags on the clipped biventricular mesh, generated automatically by `cardiac-geometries`, which labels each connected patch of the clipped surface: the LV endocardium (deep blue), the RV endocardium (light teal), the epicardial surface (orange-tan), and the basal cap (red rim). Each tag drives a different boundary condition in the mechanics solve and is reused as Dirichlet data for the LDRB Laplace problems in {ref}`sec-fibers`; details are given in {ref}`sec-mesh-generation` below.
```

The basal-plane clip is not anatomically neutral. The RV loses proportionally far more cavity volume than the LV, because its outflow geometry is more extended near the base. Closed-cavity volumes computed on the original UKB atlas before clipping give 119.6 mL for the LV and 128.7 mL for the RV. After the clip, the LV cavity drops to 111.5 mL — a 6.8% loss — while the RV cavity drops to 76.9 mL, a 40% loss. The cavity volumes are computed by applying the divergence theorem to a closed surface — the endocardium plus the valve-opening caps for the unclipped atlas, the endocardium plus the basal plane for the clipped simulation mesh. {numref}`fig-volume-clipped` shows the discarded material directly: the unclipped atlas surface (red) sits on top of the simulation mesh (gray). The 3D--0D coupling in {ref}`sec-3d-0d-coupling` compensates for this mismatch with a fixed mesh-to-circulation volume scaling, but the simulation still runs on the clipped crescent-shaped RV shown in {numref}`fig-mesh-regions`.

```{figure} ../figures/fig_2_3_volume_clipped.png
:name: fig-volume-clipped
:width: 95%

Basal clipping in three beats. *Left:* the full UK Biobank atlas, with the four valve openings (mitral, aortic, tricuspid, pulmonary) visible as colour-tagged rings on the red epicardial surface. *Middle:* the same atlas (red) sitting on top of the retained ventricular bulk (gray) — the basal-plane cut is the boundary between them. *Right:* the simulation mesh used in the rest of this thesis. The grayish patches showing through the red cap in the middle panel are a rendering glitch where the two meshes meet along the basal cut, not actual overlap.
```

```{figure} ../figures/fig_2_3b_side_views.png
:name: fig-volume-clipped-side
:width: 90%

Side views of the full UK Biobank atlas (*left*) and the simulation mesh (*right*). The RV cavity reaches well above the basal plane, into the pulmonary outflow tract, while the LV cavity tapers earlier. The basal-plane cut therefore removes a larger fraction of the RV cavity than of the LV cavity.
```

The RV cavity surface in the simulation mesh is also not exactly the RV surface in the atlas. The UKB atlas exports the RV cavity as two separately-segmented pieces — septum-side and free-wall-side endocardia — and the meshing pipeline merges them and applies a Laplacian smoothing pass (100 iterations, relaxation 0.1) before tetrahedralization. The surface render of the unsmoothed atlas in the left panel of {numref}`fig-volume-clipped-side` looks fine on its own, but the *volume* tetrahedra needed to model the wall physics — fitting between the cavity and epicardial surfaces — degrade at the seam between the two atlas pieces unless the seam is smoothed first. The smoothing displaces the RV endocardial surface by 0.9 mm on average (up to about 7 mm locally near the seam) and thickens the RV wall against the unchanged epicardium by 1.2 mm on average, roughly a 19% relative thickening on the RV side. The LV endocardium and the epicardium are single-piece atlas surfaces and are not smoothed, so the LV wall thickness is exactly what the atlas defines.

Using one geometry is a deliberate restriction. It lets the longitudinal pressure-strain proxy be tested under controlled loading changes without simultaneously changing wall thickness, cavity size, septal curvature, or the noise of any one patient's segmentation. This makes the interpretation cleaner: when the proxy changes across the sweep, the change comes from the imposed circulation and the resulting deformation, not from a different anatomy. The cost is that the sweep should not be read as a real PAH disease trajectory. Real PAH remodelling changes geometry and material properties together with pressure {cite}`vonk2013right,vonk2017relationship,humbert2022esc`, and that is exactly what the controlled-anatomy design is built to avoid.

(sec-mesh-generation)=
## Mesh Generation

Mesh generation is handled by `cardiac_geometries.mesh.ukb()` from the `cardiac-geometries` library {cite}`cardiac_geometries`, which calls the `ukb-atlas` pipeline described above and tetrahedralizes the resulting closed surface with `gmsh`. The production mesh uses a target element edge length of 5 mm, giving approximately 8070 tetrahedral cells; a finer convergence check at 3.75 mm (approximately 15000 cells) is also run as an endpoint comparison. At the production resolution the mesh resolves the LV free wall, RV free wall, and septum as integration regions, but it is not designed to resolve detailed septal transmural layers — a limitation that matters for the through-wall septal diagnostics in {ref}`chap-results`.

The four boundary tags of {numref}`fig-surface-tags` each drive a different boundary condition in the mechanics solve. The LV and RV endocardial tags carry the cavity-volume constraints, with cavity pressures returning as Lagrange multipliers. The epicardial and basal tags carry the Robin spring supports, and the basal tag also carries the partial Dirichlet constraint that removes the remaining rigid-body mode. The full boundary-condition treatment is given in {ref}`sec-3d-mechanics`.

The interventricular septum is defined at the cell level rather than the surface level: each finite element is tagged as belonging to the LV free wall, the RV free wall, or the septum. The native region tags come from the geometry and fibre-generation pipeline and are used for the LV and RV free-wall regions. For septal pressure-choice diagnostics, the postprocessing also constructs geometric septum masks from distances and Laplace coordinates between the LV, RV, and epicardial surfaces. This is why the results distinguish anatomical free-wall regions from the geometric septum definitions built for the proxy comparison when needed.
