(sec-geometry-anatomical-model)=
# Geometry

The main production analyses in this thesis run on one biventricular geometry, built in three steps. The shape comes from the UK Biobank statistical atlas of Mauger et al. {cite}`mauger2019right`, at end-diastole, taking the mean of a healthy sub-cohort of 630 cardiac MR scans as the baseline. The atlas is then cut at a single flat plane below the valves so that the basal boundary of the simulation domain is one planar surface rather than the irregular valve-annulus geometry — a standard simplification in finite-element ventricular mechanics {cite}`finsberg2018efficient,pluijmert2017determinants`.

What remains is meshed and labelled by `cardiac-geometries` {cite}`cardiac_geometries`, which tags the endocardial (inner, cavity-facing) and epicardial (outer) surfaces along with the basal cap. These are thin lining layers, not separate volumetric materials in the model; they matter here as surfaces. The endocardium carries the cavity pressure load, the epicardium carries Robin support springs, and both surfaces define transmural coordinates for fibre assignment. {numref}`fig-surface-tags` shows the four boundary surfaces that carry these roles.

```{figure} ../figures/fig_2_6_surface_tags.png
:name: fig-surface-tags
:width: 65%

Boundary surface tags on the clipped biventricular mesh: LV endocardium (deep blue), RV endocardium (light teal), epicardial surface (orange-tan), basal cap (red rim).
```

The septum is defined directly from the surface tags. For an interior point $x$, write $d_\text{LV}(x)$, $d_\text{RV}(x)$, $d_\text{epi}(x)$ for the Euclidean distances from $x$ to the LV endocardium, the RV endocardium, and the epicardium. The septum is the set of points for which both endocardial surfaces are closer than the epicardium:

$$
\Omega_\text{sept} \;=\; \{\, x \in \Omega \;:\; \max(d_\text{LV}(x),\, d_\text{RV}(x)) < d_\text{epi}(x) \,\}.
$$

The remaining cells are LV free wall (closer to the LV endocardium) or RV free wall (closer to the RV endocardium). The red region in {numref}`fig-mesh-regions` is exactly $\Omega_\text{sept}$.

```{figure} ../figures/fig_2_1_mesh_regions.png
:name: fig-mesh-regions
:width: 70%

Cell-level region tags on the clipped biventricular UK Biobank baseline mesh, short-axis cut through mid-ventricle: LV free wall (blue), RV free wall (pale yellow), septum (red); LV cavity at right, RV cavity at left. The same colour mapping is reused for all region-resolved quantities in this thesis.
```

The basal clip is not symmetric: the RV cavity loses far more than the LV, because the RV outflow geometry extends further toward the base. The RV cavity drops by 40% (128.7 → 76.9 mL), while the LV cavity drops by only 6.8% (119.6 → 111.5 mL). {numref}`fig-volume-clipped` shows the discarded material directly — outflow tracts, valve regions, atria, great vessels — sitting on top of the simulation mesh.

```{figure} ../figures/fig_2_3_volume_clipped.png
:name: fig-volume-clipped
:width: 95%

Basal clipping in three panels. *Left:* the full UK Biobank atlas, with the four valve openings (mitral, aortic, tricuspid, pulmonary) visible as colour-tagged rings on the red epicardial surface. *Middle:* the same atlas (red) sitting on top of the retained ventricular bulk (gray) — the basal-plane cut is the boundary between them. *Right:* the simulation mesh used in the rest of this thesis. Grayish patches in the middle panel are a rendering glitch along the basal cut, not actual overlap.
```

```{figure} ../figures/fig_2_3b_side_views.png
:name: fig-volume-clipped-side
:width: 90%

Side views of the full UK Biobank atlas (*left*) and the simulation mesh (*right*). The RV cavity reaches well above the basal plane into the pulmonary outflow tract, while the LV cavity tapers earlier.
```

The RV cavity surface in the simulation mesh is not exactly the RV surface in the atlas. The UKB atlas exports the RV cavity as two separately segmented pieces — septum-side and free-wall-side endocardia — and the meshing pipeline merges them and applies a Laplacian smoothing pass (100 iterations, relaxation 0.1) before tetrahedralization. The unsmoothed atlas surface in the left panel of {numref}`fig-volume-clipped-side` looks fine as a render, but the volume tetrahedra that have to fit between the cavity and epicardial surfaces degrade at the seam between the two atlas pieces unless the seam is smoothed first.

The smoothing displaces the RV endocardial surface by 0.9 mm on average (up to about 7 mm locally near the seam) and thickens the RV wall against the unchanged epicardium by 1.2 mm on average. The LV endocardium and the epicardium are single-piece atlas surfaces and are not smoothed, so the LV wall thickness is exactly what the atlas defines.

On the production mesh this leaves an end-diastolic free-wall thickness of about 2.9 mm at the RV and 6.8 mm at the LV (median vertex-to-epicardium distance), so the RV/LV thickness ratio in the simulation is roughly 0.4. The RV is therefore still the thinner free wall, and the qualitative asymmetry that motivates the separate RV fibre rule and the lower RV pressure scale is preserved. The smoothed RV nevertheless sits at the upper edge of healthy adult anatomical ratios (typically 0.3–0.5), so quantitative RV-versus-LV thickness contrasts inferred from these simulations should be read as a mild underestimate of the in-vivo asymmetry rather than an exact reproduction of it.

Mesh generation is handled by `cardiac_geometries.mesh.ukb()` from the `cardiac-geometries` library {cite}`cardiac_geometries`, which calls the `ukb-atlas` pipeline described above and tetrahedralizes the resulting closed surface with `gmsh`. The production mesh uses a target element edge length of 5 mm, giving 8070 tetrahedral cells; a finer convergence check at 3.75 mm (around 15000 cells) is also run as an endpoint comparison. At the production resolution the mesh resolves the LV free wall, RV free wall, and septum as integration regions, but it is not designed to resolve detailed septal transmural layers — a limitation that matters for the through-wall septal diagnostics in {ref}`chap-results`.
