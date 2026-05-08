(sec-fibers)=
# Myocardial Fibre Architecture

The mechanical anisotropy of the myocardium makes the spatial arrangement of fibres one of the most important inputs to the simulation. The fibre direction is the direction in which the passive material is stiffest, and in the active-stress model it is also the direction along which active tension is applied during contraction. In the real heart, muscle fibres wrap around the ventricular walls in a complex helical pattern: near the endocardium, fibres run in a right-handed helix when viewed from the apex, while near the epicardium they run in a left-handed helix, with a continuous rotation of the helix angle across the wall thickness {cite}`streeter1969fiber,bayer2012novel`. This arrangement is mechanically important because fibre shortening is converted into wall thickening, torsion, and ejection rather than pure one-dimensional shortening {cite}`pluijmert2017determinants`.

Assigning realistic fibre orientations to an idealized mesh requires a systematic method that can work on arbitrary geometries without relying on patient-specific imaging of the fibre structure. The approach used here is the Laplace-Dirichlet Rule-Based (LDRB) algorithm of Bayer et al. {cite}`bayer2012novel`. The core idea is to define a local coordinate system at every point in the myocardium by solving a series of Laplace equations on the mesh with Dirichlet boundary conditions that encode anatomical information. Three coordinate fields are needed: a transmural coordinate $d$ that varies from zero at the endocardium to one at the epicardium, an apico-basal coordinate that runs from apex to base, and a circumferential coordinate orthogonal to the other two. Each of these is obtained as the solution to a Laplace equation with appropriate boundary conditions on the endocardial, epicardial, and basal surfaces of the mesh. {numref}`fig-apex-laplace` shows the apico-basal solution $\phi_\text{ab}$ as one concrete example; the transmural solution $\phi_\text{epi}$ has the same character with the boundary conditions moved to the endocardial and epicardial surfaces.

```{figure} ../figures/fig_2_4_apex_laplace.png
:name: fig-apex-laplace
:width: 60%

The apico-basal Laplace solution $\phi_\text{ab}$ on the production mesh, used as one of three coordinate fields in the LDRB algorithm. The scalar field is harmonic on the myocardium with $\phi_\text{ab}=1$ at the apex (bright spot, lower right) and $\phi_\text{ab}=0$ on the base (top, dark red). The gradient $\nabla\phi_\text{ab}$, taken at every integration point, defines the local apico-basal direction used to orient the fibres.
```

Once this local coordinate system is established at every integration point, the fibre direction $\mathbf{f}_0$ is determined by rotating the circumferential direction through the helix angle $\alpha$, which varies linearly with the transmural coordinate:

$$
\alpha(d) = \alpha_\text{endo}(1 - d) + \alpha_\text{epi}\, d.
$$

For the left ventricular free wall, we use $\alpha_\text{endo} = +60^\circ$ and $\alpha_\text{epi} = -60^\circ$, a standard rule-based choice used to reproduce the transmural helix-angle rotation of ventricular myocardium {cite}`bayer2012novel`. The resulting variation produces the characteristic double-helical structure: fibres at the endocardium run in a steep right-handed helix, transition to nearly circumferential at mid-wall, and continue to a left-handed helix at the epicardium.

The right ventricular free wall has a different architecture. Because the RV wall is much thinner and wraps around the outside of the LV in a crescent shape, the fibre angles tend to be shallower, with less transmural rotation. In the model, the RV uses prescribed LDRB angles $\alpha_\text{endo} = +90^\circ$ and $\alpha_\text{epi} = -25^\circ$, giving a more nearly transverse fibre orientation at the endocardium. This separate RV rule follows biventricular rule-based fibre models that treat the RV and septum differently from the LV free wall {cite}`doste2019rulebased`. To apply the two helix-angle conventions, every cell must first be classified as LV-side or RV-side. {numref}`fig-lv-rv-partition` shows this cell-level partition, defined by the sign of $\phi_\text{lv}-\phi_\text{rv}$, where $\phi_\text{lv}$ and $\phi_\text{rv}$ are two further Laplace solutions, harmonic with Dirichlet value 1 on the LV and RV endocardial surfaces respectively.

```{figure} ../figures/fig_2_5_lv_rv_partition.png
:name: fig-lv-rv-partition
:width: 60%

LV/RV cell partition used to apply distinct helix-angle conventions. Each cell is classified by the sign of $\phi_\text{lv}-\phi_\text{rv}$, with cells closer to the LV endocardial surface coloured blue and cells closer to the RV endocardial surface coloured red. The transition through the septum is visible as the smooth colour gradient running from blue to red along the central wall.
```

In addition to the fibre direction $\mathbf{f}_0$, the full fibre-sheet description defines a sheet direction $\mathbf{s}_0$, which is perpendicular to the fibre direction and lies in the plane of the local fibre-sheet laminae. The sheet normal $\mathbf{n}_0 = \mathbf{f}_0 \times \mathbf{s}_0$ completes an orthonormal frame at each point. The LDRB algorithm assigns all three directions simultaneously as part of the same coordinate rotation procedure. The passive material parameters used in this thesis are transversely isotropic: one direction, the fibre direction, is mechanically distinguished, while directions in the plane transverse to the fibre are treated the same by the passive law. The sheet and sheet-normal directions remain useful for diagnostics and for decomposing stress-strain work into directional components.

For the model description, the important output of the fibre-generation step is the local orthonormal frame $(\mathbf{f}_0,\mathbf{s}_0,\mathbf{n}_0)$ attached to the reference mesh. Different numerical representations of these fields are used later for stress integration, activation storage, and visualization, but those are implementation details. {ref}`sec-3d-mechanics` uses $\mathbf{f}_0$ both in the passive material law and in the active-stress term $T_a(t)(\mathbf{f}_0\otimes\mathbf{f}_0)$; {ref}`chap-results` uses the same frame to decompose stress-strain work into fibre, sheet, normal, and cross terms.

The fibre architecture is also where the model and the clinical proxy begin to differ. The active stress and the anisotropic passive stiffness are defined in the local fibre-sheet frame, whereas echocardiographic pressure-strain work is normally based on longitudinal strain {cite}`russell2012novel,voigt2015definitions,abawi2022noninvasive`. The comparison in this thesis therefore tests not only a pressure-for-stress substitution, but also the loss incurred when tensorial fibre-based mechanics is viewed through a single clinically measurable strain direction. {numref}`fig-fiber-field` shows the resulting fibre architecture on the UK Biobank baseline mesh, with the helical rotation visible across the wall.

```{figure} ../figures/fig_2_2_fiber_field.png
:name: fig-fiber-field
:width: 70%

LDRB-generated fibre field $\mathbf{f}_0$ on the biventricular UK Biobank mesh, oblique view, coloured by helix angle $\alpha$. The right-handed endocardial helix on the LV outer wall is visible transitioning to a left-handed helix at the epicardium, and the much shallower rotation across the thinner RV free wall is seen at right. The helix-angle range follows the standard LDRB convention used in this thesis ($+60^\circ$ at LV endocardium to $-60^\circ$ at LV epicardium; $+90^\circ$ to $-25^\circ$ across the thinner RV wall).
```
