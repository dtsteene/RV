# Geometry and Simulation Cases

(sec-geometry-anatomical-model)=
## The Anatomical Model Used In This Study

The analyses reported in this thesis use one biventricular geometry: a synthetic baseline derived from the UK Biobank statistical shape model {cite}`mauger2019right`. The atlas was constructed by Mauger et al. from cardiovascular magnetic resonance images of 4,329 participants in the UK Biobank study, fitting a subdivision surface template to each scan using diffeomorphic registration. A reference sub-cohort of 630 participants with no cardiovascular risk factors was used to define normal reference morphology, and the mean shape of this sub-cohort serves as the baseline geometry here. {numref}`fig-mesh-regions` walks from the atlas surface down to the tagged finite-element mesh used in this thesis, and gives the reader a concrete object to anchor the geometric and constitutive description that follows.

```{figure} ../figures/fig_2_1_mesh_regions.png
:name: fig-mesh-regions
:width: 90%

From UK Biobank atlas to the simulation mesh. Top-left: the UKB mean atlas surface (red), with the clipped ventricular bulk (gray) shown beneath the parts of the atlas that this thesis discards — the atria, valves, and outflow tracts above the basal plane. Top-right: the resulting tetrahedral myocardial volume mesh, shown in short-axis cut so the LV cavity (right), the RV cavity (left), and the wall thickness are visible. Bottom-left: the boundary surface tags used in the mechanics solve and in the LDRB fibre algorithm — LV endocardium, RV endocardium, epicardium, and the basal cap. Bottom-right: the cell-level volume tags that partition the myocardium into LV free wall, RV free wall, and interventricular septum (the colours used here are reused everywhere region-resolved quantities are shown later in this thesis).
```

The geometry is a clipped ventricular mesh rather than a full anatomical heart. The atria, valves, and outflow tracts above the valve plane are not represented spatially; they belong to the circulation model described in {ref}`sec-0d-circulation`. What remains is the ventricular myocardium between the apex and one planar base: the LV free wall, RV free wall, and interventricular septum. The LV and RV endocardial surfaces, the epicardial surface, and the basal cap are retained as boundary labels on this myocardial solid.

Making the finite-element domain the ventricular myocardium is a modelling choice, but a standard one in ventricular mechanics. The ventricular myocardium is the mechanically active, fibre-reinforced bulk tissue of the wall. Experimental and constitutive studies treat it as a nonlinear, nearly incompressible, direction-dependent material whose response is organized by local fibre and sheet architecture {cite}`holzapfel2009constitutive`. In contrast, the endocardium and epicardium are thin lining or covering layers. They matter here as surfaces: blood pressure acts on the endocardial cavity boundaries, epicardial springs support the outer boundary, and both surfaces help define transmural coordinates for fibre assignment. They are not given separate thicknesses or separate constitutive laws in this model.

This ventricular truncation is common in finite-element ventricular mechanics models {cite}`finsberg2018efficient,pluijmert2017determinants`, but it is not anatomically neutral. In this geometry, the RV loses proportionally far more cavity volume above the basal plane than the LV, because its inflow and outflow geometry is more extended near the base. Closed-cavity volumes computed on the original UKB atlas before clipping give 119.6 mL for the LV and 128.7 mL for the RV. After the basal clip, the LV cavity drops to 111.5 mL — a 6.8% loss — while the RV cavity drops to 76.9 mL, a 40% loss. {numref}`fig-volume-clipped` shows the discarded material directly: the unclipped atlas surface (red) sits on top of the simulation mesh (gray), and the asymmetry between the two outflow caps is visible at a glance. The 3D--0D coupling in {ref}`sec-3d-0d-coupling` compensates for this mismatch with a fixed mesh-to-circulation volume scaling. The underlying spatial model, however, remains the clipped crescent-shaped RV shown in {numref}`fig-mesh-regions`, which should be kept in mind when interpreting RV-side quantities.

```{figure} ../figures/fig_2_3_volume_clipped.png
:name: fig-volume-clipped
:width: 70%

Volume lost to basal clipping. The unclipped UK Biobank atlas surface (red) is overlaid on the clipped ventricular mesh actually used by the simulation (gray). The red caps above the basal plane are the parts that the simulation does not represent spatially: the atria, the atrioventricular valves, the LV outflow tract above the aortic valve, and the longer RV outflow tract reaching the pulmonary valve. Closed-cavity integrals quantify the loss as 8.1 mL (6.8%) of the LV cavity and 51.8 mL (40%) of the RV cavity — most of the asymmetry concentrates on the RV side, which is the side the central thesis question depends on. This volume loss is reabsorbed by the mesh-to-circulation volume scaling described in {ref}`sec-3d-0d-coupling`.
```

Using one geometry is a deliberate restriction. It lets the longitudinal pressure-strain proxy be tested under controlled loading changes without simultaneously changing wall thickness, cavity size, septal curvature, or patient-specific segmentation details. This makes the interpretation cleaner: when the proxy changes across the sweep, the change comes from the imposed circulation and the resulting deformation, not from a different anatomy. The cost is that the sweep should not be read as a real PAH disease trajectory. Real PAH remodelling changes geometry and material properties together with pressure {cite}`vonk2013right,vonk2017relationship,humbert2022esc`. Patient-specific healthy and PAH meshes are available in the wider project and are discussed only as preliminary geometry-sensitivity checks and future-work motivation, not as part of the main result set reported in this thesis.

(sec-mesh-generation)=
## Mesh Generation

Mesh generation is handled by the `cardiac-geometries` library {cite}`cardiac_geometries`. For the UK Biobank case, the function `cardiac_geometries.mesh.ukb()` generates a tetrahedral volume mesh directly from the mean atlas surface geometry, parametrized by a target characteristic element length. The production mesh uses a characteristic length of 5 mm, giving approximately 8000 tetrahedral cells. At this resolution, the mesh resolves the anatomical regions used for integration — LV free wall, RV free wall, and septum — but it is not designed to resolve detailed septal transmural layers. That limitation matters for the through-wall septal diagnostics in {ref}`chap-results`.

```{table} Mesh and unit conventions used in the production simulations.
:name: tab-mesh-units
:align: left

| Quantity | Convention |
|---|---|
| Production mesh size | characteristic length 5 mm, approximately 8070 tetrahedral cells |
| Finer endpoint check | characteristic length 3.75 mm, approximately 15000 tetrahedral cells |
| Coordinates in generated mesh | mm |
| Coordinates in mechanics solve | m |
| Hemodynamic pressure | mmHg |
| Stress and work-density output | kPa, equivalent to kJ m$^{-3}$ |
| Total work output | J or mJ |
```

All meshes are generated with node coordinates in millimeters and scaled by a factor of $10^{-3}$ to meters before any finite element computation. The mechanics solve uses this SI length scale, with material stresses and work densities reported in kPa, hemodynamic pressures reported in mmHg, and total work reported in J or mJ after unit conversion. Since work density has units J/m$^3$, it is equivalent to Pa and is converted to kPa for presentation. The meshes are rotated after generation so that the outward normal to the basal plane is aligned with the positive $x$-axis, a convention that simplifies the application of the out-of-plane Dirichlet constraint at the base.

The boundary surfaces of the mesh are labeled with integer tags that distinguish the left ventricular endocardium, the right ventricular endocardium, the epicardial surface, and the basal plane. These tags serve multiple purposes downstream. The LV and RV endocardial tags define the cavity surfaces whose volumes are constrained in the coupled mechanics solve; the corresponding pressures are returned by the solver as Lagrange multipliers. The epicardial and basal tags define the Robin spring supports, and the basal tag also defines the partial Dirichlet constraint used to remove the remaining rigid-body mode. The same boundary tags provide the Dirichlet data for the Laplace problems used by the LDRB fibre-assignment algorithm in {ref}`sec-fibers`.

The interventricular septum is defined at the cell level rather than the surface level: each finite element is tagged as belonging to the LV free wall, the RV free wall, or the septum. The native region tags come from the geometry and fibre-generation pipeline and are used for the LV and RV free-wall regions. For septal pressure-choice diagnostics, the postprocessing also constructs geometric septum masks from distances and Laplace coordinates between the LV, RV, and epicardial surfaces. This is why the results distinguish anatomical free-wall regions from diagnostic septal masks when needed.
