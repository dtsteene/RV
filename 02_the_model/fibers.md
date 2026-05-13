(sec-fibers)=
# Myocardial Fibre Architecture

The myocardium is direction-dependent, so the spatial arrangement of fibres is one of the simulation's primary inputs. The fibre direction is the axis along which the passive material is stiffest and along which active tension is applied during contraction. In the real heart, muscle fibres wrap around the ventricular walls in a helical pattern: near the endocardium they run in a right-handed helix when viewed from the apex, near the epicardium in a left-handed helix, with the helix angle rotating continuously across the wall thickness {cite}`streeter1969fiber,bayer2012novel`. This arrangement is mechanically important because fibre shortening produces wall thickening, torsion, and ejection rather than pure one-dimensional shortening {cite}`pluijmert2017determinants`.

Assigning realistic fibre orientations to an idealized mesh, without per-patient imaging of the fibre structure, needs a method that adapts to the geometry. The Laplace-Dirichlet Rule-Based (LDRB) algorithm {cite}`bayer2012novel` does this by solving a small number of simple boundary-value problems on the mesh and reading directions off their gradients.

Each of those problems has the same form: a Laplace equation with Dirichlet boundary conditions — the *Laplace-Dirichlet* in LDRB. Fix a scalar field $\phi$ to value 0 on one chosen patch of the mesh boundary and to 1 on another, then ask for the smoothest extension into the interior:

$$\nabla^2 \phi = 0 \text{ on } \Omega, \quad \phi = 0 \text{ on } \Gamma_0, \quad \phi = 1 \text{ on } \Gamma_1.$$

Such solutions are *harmonic*: at every interior point, $\phi$ equals the average of values in any small neighbourhood. This gives a smooth transition from $0$ to $1$ between the two boundary patches $\Gamma_0$ and $\Gamma_1$, conforming to the geometry of the wall even on irregular shapes. Its gradient $\nabla\phi$ points perpendicular to the level sets of $\phi$, from $\Gamma_0$ toward $\Gamma_1$ at every interior point, giving a direction "from the 0-boundary to the 1-boundary". Which direction it encodes depends on where the 0 and 1 boundary patches are placed.

For the LDRB construction we need three direction fields: an apico-basal direction from apex to base, a transmural direction from endocardium to epicardium, and a circumferential direction perpendicular to both. The first two come from Laplace solutions: one with $\phi=0$ at the apex and $\phi=1$ at the base, and one with $\phi=0$ on the endocardia and $\phi=1$ on the epicardium. The third — the circumferential direction — is built from these two and is defined formally below. The two Laplace solutions are shown in {numref}`fig-apex-laplace` and {numref}`fig-transmural-laplace`.

```{figure} ../figures/fig_2_4_apex_laplace.png
:name: fig-apex-laplace
:width: 70%

The apico-basal Laplace solution $\phi_\text{ab}$: $\phi=0$ at the apex (blue) and $\phi=1$ on the base (red). The gradient $\nabla\phi_\text{ab}$ defines the local apico-basal direction at every interior point.
```

```{figure} ../figures/fig_2_4b_transmural_laplace.png
:name: fig-transmural-laplace
:width: 70%

The transmural Laplace solution $\phi_\text{epi}$: $\phi=0$ on the LV and RV endocardial surfaces (blue, inside the cavities) and $\phi=1$ on the epicardium (red, outer wall). The gradient $\nabla\phi_\text{epi}$ defines the local transmural direction at every interior point.
```

The helix angle $\alpha$ is the angle between a fibre and the local circumferential direction. When $\alpha = 0$ the fibre runs purely circumferentially, like a horizontal line drawn on a cylinder. Positive $\alpha$ tilts the fibre toward the apex, producing a right-handed helix; negative $\alpha$ tilts toward the base, producing a left-handed helix. At $\alpha = \pm 90^\circ$ the fibre would point straight along the apex-to-base axis.

To compute that rotation at every point, the LDRB algorithm builds a local coordinate frame from the Laplace gradients and tilts the circumferential axis by $\alpha$ within the wall's tangent plane (the plane spanned by circumferential and apico-basal). The angle varies linearly with the transmural coordinate $d$:

$$
\alpha(d) = \alpha_\text{endo}(1 - d) + \alpha_\text{epi}\, d.
$$

For the left ventricular free wall, we use $\alpha_\text{endo} = +60^\circ$ and $\alpha_\text{epi} = -60^\circ$, the standard rule-based choice {cite}`bayer2012novel`. The formula then gives $\alpha = +60^\circ$ at the endocardium ($d=0$), passes through $0^\circ$ at mid-wall ($d=0.5$), and reaches $-60^\circ$ at the epicardium ($d=1$). A fibre on the inner wall surface therefore starts as a steep right-handed helix, rotates smoothly to purely circumferential halfway through the wall, and continues to a steep left-handed helix on the outer wall — the characteristic double-helical structure of ventricular myocardium.

The right ventricular free wall has a different architecture. The RV wall is thinner than the LV free wall (about 0.4 the LV thickness in the simulation mesh; see {ref}`sec-geometry-anatomical-model`) and wraps around the outside of the LV in a crescent, so its fibres are shallower with less transmural rotation. The model uses prescribed LDRB angles $\alpha_\text{endo} = +90^\circ$ and $\alpha_\text{epi} = -25^\circ$, so the RV fibre points almost straight along the long axis at the endocardium and tilts only modestly the other way at the epicardium. This separate RV rule follows biventricular rule-based fibre models that treat the RV and septum differently from the LV free wall {cite}`doste2019rulebased`.

To apply the two angle conventions, every cell must first be classified as LV-side or RV-side. The classification uses a further Laplace solution, the *LV-to-RV scalar* $\lambda$, with Dirichlet value 1 on the LV endocardium and 0 on the RV endocardium. {numref}`fig-lv-rv-partition` shows the field: cells with $\lambda > 0.5$ form the LV side and $\lambda \leq 0.5$ the RV side for the helix-angle assignment. The same smooth $\lambda$ is reused later in the thesis as the weight in the through-wall septum pressure choice ({ref}`sec-work-definitions`) and as the LV-side/RV-side split in the simplification-cascade diagnostic ({ref}`sec-simplification-cascade`). This LV/RV partition is distinct from the geometric LV/RV/septum partition in {numref}`fig-mesh-regions`, which is used for region integration throughout the thesis.

```{figure} ../figures/fig_2_5_lv_rv_partition.png
:name: fig-lv-rv-partition
:width: 70%

The LV-to-RV scalar $\lambda$: Laplace solution with $\lambda = 1$ on the LV endocardium (blue) and $\lambda = 0$ on the RV endocardium (red). LDRB thresholds at $\lambda = 0.5$ to pick the helix-angle rule per cell; the smooth field is reused as a pressure weight in the septum-proxy choices of {ref}`sec-work-definitions`.
```

The circumferential direction is the cross product of the apico-basal and transmural gradients:
$$
\mathbf{e}_\text{circ} \;=\; \frac{\nabla\phi_\text{ab}\times\nabla\phi_\text{epi}}{\lVert\nabla\phi_\text{ab}\times\nabla\phi_\text{epi}\rVert}.
$$
By construction it is perpendicular to both inputs, so it lies in the wall's tangent plane and points counter-clockwise around the long axis when viewed from the apex. {numref}`fig-circ-alpha` shows it as one arrow per cell, with each arrow coloured by the helix angle $\alpha$ that the rule above prescribes for that cell.

```{figure} ../figures/fig_2_5b_circ_alpha.png
:name: fig-circ-alpha
:width: 70%

The circumferential direction $\mathbf{e}_\text{circ}$ shown as one arrow per cell, all flat in the wall's tangent plane. The colour is the prescribed helix angle $\alpha$ at that cell — red toward $+90^\circ$, blue toward $-60^\circ$. At this stage the arrows only carry colour, not yet tilt. Notice that the LV and RV are visibly different: the LV cycles smoothly between $+60^\circ$ and $-60^\circ$ across the wall, while the RV reaches deep red on its endocardial side, all the way to the prescribed $+90^\circ$.
```

The fibre direction $\mathbf{f}_0$ is what we get when each of those flat arrows is rotated within the apico-basal–circumferential plane by its own $\alpha$. An arrow with $\alpha=0$ stays parallel to $\mathbf{e}_\text{circ}$; positive $\alpha$ tilts it upward toward the apex; negative $\alpha$ tilts it downward toward the base. So in {numref}`fig-fibers-alpha`, deep red ($\alpha=+90^\circ$) points straight up the long axis, and deep blue ($\alpha=-60^\circ$) points down toward the base. The colour assigned to each cell in {numref}`fig-circ-alpha` is exactly the rotation that turns its flat arrow into the tilted fibre arrow in {numref}`fig-fibers-alpha`.

```{figure} ../figures/fig_2_5_fibers_alpha.png
:name: fig-fibers-alpha
:width: 70%

The fibre field $\mathbf{f}_0$ on the same mesh and colour scale. The right-handed-inner / left-handed-outer double helix of the LV is visible on the left of the cut, and the flatter, more apex-aligned RV endocardial pattern on the right.
```

One last subtlety. The rule above prescribes one $\alpha$ inside the LV region and a different one inside the RV region, so naively the fibre direction would jump across the LV/RV interface — a visible seam, most obviously on the epicardium where RV and LV free walls meet. The LDRB algorithm avoids that seam by interpolating the LV-side and RV-side fibre frames in quaternion space, sliding along the shorter arc of the unit sphere with a weight set by the LV/RV scalars in {numref}`fig-lv-rv-partition`. This *bidirectional spherical linear interpolation* (bislerp) {cite}`bayer2012novel` is what keeps the colour pattern continuous across the interface in {numref}`fig-circ-alpha` and {numref}`fig-fibers-alpha`.

The LDRB algorithm assigns three directions at once: the fibre direction $\mathbf{f}_0$, a sheet direction $\mathbf{s}_0$ perpendicular to it within the local fibre-sheet laminae, and the sheet normal $\mathbf{n}_0 = \mathbf{f}_0 \times \mathbf{s}_0$. The passive material law used here is transversely isotropic — only $\mathbf{f}_0$ is mechanically distinguished — but the full frame $(\mathbf{f}_0,\mathbf{s}_0,\mathbf{n}_0)$ is what {ref}`chap-results` uses to decompose stress-strain work into fibre, sheet, normal, and cross terms. {ref}`sec-3d-mechanics` uses $\mathbf{f}_0$ in the passive law and in the active-stress term $T_a(t)(\mathbf{f}_0\otimes\mathbf{f}_0)$.