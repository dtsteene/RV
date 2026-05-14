(chap-results)=
# Results

The results are easiest to understand if two questions are kept separate. First: within a single simulation, does the pressure-strain proxy get the regional work differences right? Second: when the circulation changes while geometry is held fixed, does the proxy rank the loading cases in the same order as the finite-element stress-strain work density?

A proxy can rank a pressure sweep well and still give the wrong regional balance within a single patient, so the chapter starts with the regional ratio analysis. The ratio test is the cleaner mechanics check: it does not depend on whether the hemodynamic axis chosen for the sweep is clinically typical. The pressure sweep then comes in as a controlled loading experiment, asking whether the same proxies rank the cases consistently with the finite-element reference.

A note before the visual. The reader should read {numref}`fig-cascade-loops-sweep` and {numref}`fig-septum-pressure-choices` for **loop areas only** — the proxy quantity is signed loop area, and these figures are intended as a qualitative orientation to what the rest of the chapter compares quantitatively. The top row of {numref}`fig-cascade-loops-sweep` is the fiber-direction projection $S_{ff}\,\dot E_{ff}$, which is the dominant component of the full tensor contraction $\mathbf{S}:\dot{\mathbf{E}}$ but not the literal full work; cross-fiber, sheet, and sheet-normal contributions are smaller but not zero. Loop shapes, timing, and other geometric features beyond signed area are not the focus.

{numref}`fig-cascade-loops-sweep` puts the FE reference and the clinical pressure-strain proxy side by side across the sixteen cases: the top row is fiber-direction stress-strain loops $S_{ff}$ vs $E_{ff}$, the bottom row is the proxy $p_\text{cav}$ vs longitudinal strain $\varepsilon_{ll}$. The visible question is whether the bottom-row areas preserve the top-row regional balance, and whether they do so consistently as RV pressure rises. The free-wall proxy uses adjacent cavity pressure; the septum is shown with $p_\text{LV}$ as a default, but which pressure should drive the septal proxy is itself one of the chapter's open questions. {numref}`fig-septum-pressure-choices` shows the same septum loops under four candidate pressures: $p_\text{LV}$, $p_\text{RV}$, mean, and transmural.

```{figure} ../figures/fig_5_0c_cascade_loops_sweep.png
:name: fig-cascade-loops-sweep
:width: 100%

Top row: fiber-direction stress-strain loops $S_{ff}$ vs $E_{ff}$ for the LV free wall, RV free wall, and septum across the sixteen capped-reference sweep cases (last simulated beat). Bottom row: clinical pressure-strain proxy ($p_\text{LV}$ for LV and septum, $p_\text{RV}$ for RV) against tangent-longitudinal strain $\varepsilon_{ll}$. Each line is one simulation. Colour: achieved peak RV systolic pressure (mmHg).
```

```{figure} ../figures/fig_5_0d_septum_pressure_choices.png
:name: fig-septum-pressure-choices
:width: 100%

Septum pressure-strain loops across the sixteen cases under four candidate pressures: $p_\text{LV}$, $p_\text{RV}$, mean $(p_\text{LV}+p_\text{RV})/2$, and transmural $p_\text{LV}-p_\text{RV}$. All panels share the same septal longitudinal strain on the x-axis. Each line is one simulation; colour is achieved peak RV systolic pressure (mmHg). Loop area is the proxy work density $w_\text{PS}$ for the chosen pressure; the chapter quantifies the consequences of each choice in {numref}`tab-septum-proxies` and {numref}`fig-septum-ratio-headline`.
```

Unless stated otherwise, the results use the capped-reference pressure-loading sweep defined in {ref}`chap-calibration`: sixteen cases on a shared biventricular reference mesh ($n=8070$ cells). Geometry, material model, fibre architecture, and end-diastolic mesh target are held fixed; only the 0D circulation varies to raise RV pressure across the cases. The RV end-diastolic pressure used during inverse unloading is capped at 5 mmHg.

The sixteen cases share the same region tag set (1269 geometric septum cells in every case; see {ref}`sec-shared-mask-tagging`), so regional integrals are case-comparable cell-by-cell. Reported pressures, correlations, and proxies use the cavity Lagrange-multiplier pressure from the coupled mechanics solve.

The comparisons should be read as tests of simplification. The finite-element stress-strain work density is the model-side reference, not patient-level ground truth. The question is how much of that reference survives when regional mechanics are reduced first to a scalar pressure scale and then to one longitudinal strain component.

The ratio tests use simple formulas. For two regions $A$ and $B$, the finite-element work-density ratio is

$$
R_\text{FE}(A,B) = \frac{w_\text{int}(A)}{w_\text{int}(B)},
\qquad
w_\text{int}(A)=\frac{W_\text{int}[\Omega_A]}{|\Omega_{A,0}|},
$$

and the clinical-style proxy ratio is

$$
R_\text{proxy}(A,B) = \frac{w_\text{PS}(A)}{w_\text{PS}(B)}.
$$

Here $W_\text{int}[\Omega_A]$ is the volume-integrated stress-strain work over region $\Omega_A$, and $|\Omega_{A,0}|$ is that region's reference volume. Both $w_\text{int}$ and the pressure-strain loop area $w_\text{PS}$ are density-like quantities with units of pressure: J/m$^3$ = Pa, reported here in kPa. The pressure-strain proxy is already treated as a density-like index, so it has no additional regional volume factor. All pressure-strain proxies are computed cellwise — per-cell loop area against the cell's assigned pressure — and then volume-integrated over the region; for spatially varying septal pressure choices (nearest-side and through-wall weighted), pressure varies cell-by-cell within the septum.

The free-wall ratio $R = w_\text{LV}/w_\text{RV}$ sits above one across the sweep, so we report the absolute error $|R_\text{proxy}-R_\text{FE}|$, averaged over the sixteen cases.

The septum produces two ratios per case — septum/LV-free-wall and septum/RV-free-wall — that straddle unity, since the septum sits below the LV free wall and above the thinner RV free wall. Absolute differences would weigh "twice too high" and "twice too low" unequally, so we use the mean absolute log-ratio

$$
\eta_\text{ratio}
= \left\langle \left| \log \frac{R_\text{proxy}}{R_\text{FE}} \right| \right\rangle ,
$$

averaged across both ratios and all sixteen cases. The scale is multiplicative: $\eta_\text{ratio} = 0$ is exact and $\eta_\text{ratio} = 0.18$ corresponds to a typical ratio error of about $\exp(0.18)-1 \approx 20\%$.

Throughout the chapter, the longitudinal-strain proxy uses the tangent-longitudinal definition from {ref}`sec-work-definitions`. The raw apico-basal direction is projected into the local wall tangent plane before evaluating $\varepsilon_{ll}$, so the proxy does not count the through-wall component of the LDRB apex-gradient field as longitudinal strain. Fibre-aligned diagnostics use the model-side Green-Lagrange fibre strain $E_{ff}=\mathbf{E}:(\mathbf{f}_0\otimes\mathbf{f}_0)$ and are treated as mechanical checks rather than competing clinical proxies.

These ratios are tested first in the free walls, where pressure assignment is simple, and then in the septum, where it is not. The conceptual asymmetry between the two cases is the one introduced in {numref}`fig-freewall-septum-schematic`.

## Numerical Reference Quality

The FE stress-strain work density is treated as reliable on three bounded checks. Across the sixteen cases the coupled simulation reaches near-periodic state by beat 5, with beat-to-beat changes between beats 5 and 6 at most 1.5% on peak cavity pressures and 1.8% on stroke volumes ({ref}`sec-app-periodic-convergence`). The per-cell stress-strain work integral matches the boundary work to relative tolerance $10^{-5}$ to $10^{-4}$ ({numref}`fig-energy-balance`). Mesh sensitivities at the production 5 mm resolution stay below about 3% on free-wall work-density ratios and 6% on severe-case septal quantities; the full summary is in {numref}`tab-numerical-robustness-summary` at the end of the chapter and the detailed account in {ref}`chap-appendix-numerical`. These numerical floors are an order of magnitude smaller than the proxy errors reported below.

The central finding is summarised before the detailed analyses below, free walls first, then septum.

{numref}`fig-freewall-ratio-headline` shows the free-wall result. The adjacent-pressure proxy (using $p_\text{LV}$ for the LV wall and $p_\text{RV}$ for the RV wall) clusters tightly along the identity line, with mean absolute error 0.16 (raw $|R_\text{proxy}-R_\text{FE}|$) across the sweep. Free-wall LV/RV work-density ratios are preserved.

```{figure} ../figures/fig_5_0_freewall_headline.png
:name: fig-freewall-ratio-headline
:width: 70%

LV/RV free-wall work-density ratio across the sixteen capped-reference sweep cases. Each marker is one simulation; the dashed grey line is the identity $y=x$. The adjacent-pressure proxy ($p_\text{LV}$ for the LV wall, $p_\text{RV}$ for the RV wall) clusters along the identity line.
```

The septum picture is different. {numref}`fig-septum-ratio-headline` shows the septum/LV-free-wall and septum/RV-free-wall ratios for three septal pressure choices. Transmural pressure departs from the identity line in every one of the sixteen cases — the proxy is systematically too small because $p_\text{LV}-p_\text{RV}$ is a small number relative to either cavity pressure alone — while LV pressure and mean pressure stay closer. The combined septum log-ratio errors $\eta_\text{ratio}$ are 0.805 for LV pressure, 0.969 for mean pressure, and 2.075 for transmural pressure: transmural is more than twice as bad as the next-worst single-pressure choice.

```{figure} ../figures/fig_5_0_septum_headline.png
:name: fig-septum-ratio-headline
:width: 100%

Septum / LV-free-wall (left) and septum / RV-free-wall (right) work-density ratios across the sixteen capped-reference sweep cases, for three septal pressure choices. Each marker is one simulation; the dashed grey line is the identity $y=x$. Transmural pressure (red diamonds, visually emphasised) departs from identity in every case; $p_\text{LV}$ (blue circles) and mean pressure (green triangles) stay much closer. Inset values are the log-ratio error $\eta_\text{ratio}$ per pressure choice and panel; the per-panel values straddle the chapter's combined septum log-ratio errors of $0.805$ ($p_\text{LV}$), $0.969$ (mean), and $2.075$ (transmural).
```

These three observations — adjacent pressure preserves the free-wall ratio, transmural pressure fails the septum ratio, no single-pressure choice resolves the septum cleanly — are the core result of the chapter. The rest of the analyses below test them by case-ranking correlations, by strain-direction sensitivity, and by pressure-mixture diagnostics.

The mechanical reason for the free-wall/septum asymmetry visible in the two headline figures is shown in {numref}`fig-work-components`. In the local fibre-sheet-normal basis, the stress-strain contraction decomposes into fibre, sheet, sheet-normal, and cross terms, each reported as a signed fraction of the net regional work density.

Across the primary sweep this decomposition is strongly fibre-dominated in the free walls — about 89% of LV and 94% of RV work density on average — but less one-dimensional in the septum, where fibre is still the largest component at about 80% but sheet-normal and cross-axis contributions are substantially larger. The free walls are mechanically close to a single-fibre problem, so a single-direction strain proxy is reasonable; the septum is not, and a single strain direction misses more of its mechanical accounting.

```{figure} ../figures/fig_5_0b_work_components_vs_rvsp.png
:name: fig-work-components
:width: 95%

Component breakdown of finite-element stress-strain work density across the primary capped-reference pressure-loading sweep. Work density is decomposed in the local fibre-sheet-normal basis. Fibre work dominates the free-wall trends, while the septum has a larger sheet-normal and cross-axis contribution. This is the first warning that a one-direction pressure-strain proxy is mechanically cleaner in the free walls than in the septum.
```

(sec-results-freewalls)=
## Free Walls

The simplest case is the comparison between the LV free wall and the RV free wall, with the septum excluded from both. Each free wall faces one cavity, so the pressure assignment is mechanically natural: $p_\text{LV}$ for the LV free wall and $p_\text{RV}$ for the RV free wall. This is the cleanest setting for the pressure assignment, but whether a single cavity pressure scaled against a single longitudinal strain component recovers the free-wall stress-strain work density is still an empirical question, not an identity; failure here would point to a more basic limitation than septal pressure ambiguity.

For the lowest-pressure UKB baseline case in the primary sweep, the finite-element stress-strain work density in the LV free wall was 3.75 times the RV free-wall value. The tangent-longitudinal proxy using adjacent cavity pressure gave an LV/RV ratio of 3.88, close to the finite-element reference. Assigning the same pressure to both free walls lost the balance: LV pressure everywhere gave a ratio of 1.85, and RV pressure everywhere gave 1.09. Replacing the pressure magnitude with the same pressure trace scaled to unit peak, $\hat p(t)=p(t)/\max_t |p(t)|$, so that the proxy reduces to $\oint \hat p\,d\varepsilon$ — keeping the time shape but dropping the magnitude — also collapsed the LV/RV balance. The same pattern holds across the primary pressure-loading sweep. The mean absolute error in the free-wall LV/RV ratio (raw $|R_\text{proxy}-R_\text{FE}|$) was 0.16 for the adjacent-pressure tangent-longitudinal proxy, compared with 0.68 for LV pressure everywhere and 0.87 for RV pressure everywhere. The sweep result is shown in {numref}`fig-freewall-spectrum`. Adjacent cavity pressure remains the best of the tested longitudinal pressure assignments for the free-wall ratio.

```{figure} ../figures/fig_5_2_freewall_ratio_spectrum.png
:name: fig-freewall-spectrum
:width: 95%

Free-wall LV/RV work-density ratio across the primary capped-reference pressure-loading sweep. The adjacent-pressure longitudinal proxy follows the finite-element stress-strain work-density ratio better than the alternatives. The pressure-normalized waveform-only index preserves timing information but not work-density magnitude.
```

A scatter view of the same comparison is shown in {numref}`fig-freewall-ratio-scatter`. This makes the difference between correlation and magnitude easier to see. Several pressure choices rank the cases in a similar order, but the adjacent-pressure points lie closest to the identity line.

```{figure} ../figures/fig_5_2c_freewall_ratio_scatter.png
:name: fig-freewall-ratio-scatter
:width: 95%

Scatter comparison between pressure-strain proxy LV/RV ratios and finite-element stress-strain LV/RV ratios in the primary capped-reference sweep. Each panel shows one longitudinal pressure assignment. The solid line is a least-squares regression, the dashed line is the identity line, and colour denotes achieved RV systolic pressure. A high correlation alone is not enough; the useful proxy should also lie near the identity line.
```

The free-wall ratio test asks whether the proxy preserves regional magnitudes. The next question is whether pressure-strain also ranks loading cases better than pressure or strain alone.

This within-region ranking test is shown for both free walls in {numref}`fig-rv-lakatos-bridge`. The RV panel connects the model to the recent clinical validation by Lakatos et al. {cite}`lakatos2024right`: their endpoint was invasive RV contractility, whereas the endpoint here is finite-element RV free-wall stress-strain work density, so the comparison is not a reproduction of their pressure-volume analysis. It is instead the finite-element analogue of the same pressure-correction idea. The LV panel should be read more simply as the symmetric free-wall check, because LV pressure-strain work already has a larger clinical literature {cite}`urheim2005regional,russell2012novel,abawi2022noninvasive`.

Across the sweep, the adjacent-pressure longitudinal proxy correlated strongly with finite-element work density in both walls: $r=0.994$ in the LV and $r=0.967$ in the RV. The single-component comparators in {numref}`tab-freewall-correlations` show why combining pressure and strain matters. In the LV, $p_\text{LV}$ is nearly constant across the sweep and falls the wrong way as the RV expands, while longitudinal strain alone carries little ranking signal. In the RV, $p_\text{RV}$ alone carries most of the ranking but longitudinal shortening alone carries none.

One potential challenge: swapping in non-adjacent $p_\text{LV}$ on the RV side gives a slightly higher correlation ($r=0.992$). This reflects co-variation of achieved $p_\text{LV}$ and $p_\text{RV}$ along the capped-reference path, so ranking alone cannot tell adjacent from non-adjacent pressure here. The magnitude analysis above settles it: non-adjacent $p_\text{LV}$ on the RV side inflates the RV proxy and collapses the LV/RV ratio.

Wall-adjacent pressure paired with longitudinal strain is therefore both correlation-strong and magnitude-stable, with the clearest added value on the RV side.

```{table} Pearson correlations between candidate predictors and finite-element free-wall stress-strain work density across the primary capped-reference sweep. The adjacent pressure-strain index combines the cavity pressure on the corresponding side with regional longitudinal strain.
:name: tab-freewall-correlations
:align: left

| Side | Predictor | $r$ |
|---|---|---:|
| LV | $p_\text{LV}\times\varepsilon_{ll}$ (adjacent proxy) | 0.994 |
| LV | $p_\text{LV}$ alone | -0.798 |
| RV | $p_\text{RV}\times\varepsilon_{ll}$ (adjacent proxy) | 0.967 |
| RV | $p_\text{RV}$ alone | 0.909 |
| RV | Longitudinal shortening $\varepsilon_{ll}$ alone | -0.09 |
| RV | RV ejection fraction (FEM cavity) | -0.717 |
| RV | $p_\text{LV}\times\varepsilon_{ll}$ (non-adjacent) | 0.992 |
```

```{figure} ../figures/fig_5_2b_rv_lakatos_bridge.png
:name: fig-rv-lakatos-bridge
:width: 95%

Free-wall bridge between adjacent pressure-longitudinal-strain proxies and finite-element stress-strain work density in the primary capped-reference sweep. Left: LV free wall. Right: RV free wall, the model-side analogue of the Lakatos et al. RV pressure-strain argument. The main scatter in each panel uses the adjacent pressure-strain proxy; the inset reports Pearson correlations, with PS denoting the adjacent pressure-strain proxy. Colour denotes achieved RV systolic pressure.
```

This result is important because it prevents an over-broad conclusion. Cavity pressure still carries useful mechanical information as a work-density proxy. In the free walls, where the one-wall/one-pressure assumption is closest to valid, adjacent pressure preserves regional work-density magnitudes reasonably well. The difficulty appears when tissue is shared between the two cavities.

(sec-results-septum)=
## The Septum

The septum is not a free wall. It is a shared internal wall with LV pressure on one side and RV pressure on the other, so the pressure assignment is qualitatively different. A free wall has one comparatively unambiguous pressure scale; the septum has six plausible ones.

Four are uniform across the septal volume: $p_\text{LV}$ (the usual clinical convention), $p_\text{RV}$ (the pressure on the opposite septal face), the transmural difference $p_\text{LV}-p_\text{RV}$ (net pressure across the wall), and the mean $(p_\text{LV}+p_\text{RV})/2$ (septal tissue loaded from both sides). Two more vary across the septum's thickness: a nearest-side pressure that assigns $p_\text{LV}$ to cells on the LV side and $p_\text{RV}$ to cells on the RV side, and a through-wall weighted pressure that interpolates smoothly between the two using a transventricular coordinate. Formal definitions are in {ref}`sec-work-definitions`.

The distinction matters because pressure difference and tissue loading are not the same thing. The pressure difference is the natural quantity for net septal force, curvature, and the clinical D-sign in RV pressure overload {cite}`ryan1985echocardiographic,vonk2013right`. If RV pressure rises toward LV pressure, the septum flattens because the pressure difference across it is reduced. Myocardial work density, however, is local stress times local strain. A septum compressed and constrained by two pressurized cavities can still carry substantial tissue work density even when the pressure difference is small. Transmural pressure is therefore mechanically meaningful, but it is not automatically the best scalar stress scale for septal work density.

To test this directly, the septal pressure choices for the longitudinal pressure-strain proxy were compared in two ways. First, their correlations with septal stress-strain work density were computed across the pressure sweep. Second, their ability to preserve septum/free-wall work-density ratios was measured. The ratio test is the more direct magnitude test: it asks whether the proxy gives the correct amount of septal work density relative to the LV and RV free walls in the same simulation.

Across the sweep, every single-pressure choice except transmural carried a positive ranking correlation with septal stress-strain work density. LV pressure gave the smallest septum/free-wall magnitude error among them. Transmural pressure failed both tests — the only negative ranking correlation and the largest magnitude error. This is the central septal warning: the pressure difference across the septum is not the same as the scalar stress scale needed to preserve septal tissue-work density.

{numref}`tab-septum-proxies` reports the per-pressure values. The table is restricted to the longitudinal-strain proxy because that is the clinical pressure-strain quantity tested by the thesis; a fibre-aligned diagnostic, also computed as a model-side check, is taken up below.

```{table} Septal longitudinal pressure-strain proxy performance in the primary capped-reference pressure-loading sweep. Correlation tests case ranking across the sweep; ratio error tests preservation of septum/free-wall magnitude within each case.
:name: tab-septum-proxies
:align: left

| Pressure choice | Ranking correlation $r$ | Magnitude ratio error |
|---|---:|---:|
| $p_\text{LV}$ | 0.540 | 0.805 |
| $p_\text{RV}$ | 0.527 | 1.171 |
| $p_\text{LV}-p_\text{RV}$ | -0.331 | 2.075 |
| Mean pressure | 0.535 | 0.969 |
| Nearest-side pressure | 0.547 | 0.999 |
| Through-wall weighted pressure | 0.540 | 0.970 |
```

The correlation part of the table is shown as scatter plots in {numref}`fig-septum-correlation-scatter`. The plot makes two points visible. First, transmural pressure is visually the wrong trend for this primary sweep: high-RV-pressure cases have low transmural pressure but high septal stress-strain work density, so the proxy moves opposite to the reference and the correlation becomes negative. Second, the LV, mean, nearest-side, and through-wall weighted choices are not identical, but they all keep the septum inside the two-cavity loading picture rather than treating it as a pure pressure-difference wall.

```{figure} ../figures/fig_5_3a_septum_proxy_correlation_scatter.png
:name: fig-septum-correlation-scatter
:width: 95%

Septal pressure-choice correlations in the primary capped-reference sweep. Each panel compares a longitudinal pressure-strain proxy with finite-element septal stress-strain work density. The solid line is a least-squares regression and colour denotes achieved RV systolic pressure. Transmural pressure is mechanically meaningful for net septal pressure difference, but it is not a good scalar work-density pressure in this analysis.
```

The geometric septum mask used here was also stress-tested by shrinking and expanding it near the LV/RV junction. This changes exactly the part of the definition that is hardest to draw: how much junctional tissue belongs to the shared wall. The central result did not depend on the exact cutoff. A very tight septal core can make transmural pressure rank the cases better, but it still gives the worst septum/free-wall magnitude error. This is why the main septal result gives more weight to regional ratios than to correlation alone; details are in {ref}`sec-app-septum-epi-envelope`.

(sec-results-septum-strain-direction)=
### Strain Direction in the Septum

The pressure-assignment failure above explains only part of the septal difficulty. Pairing the same pressure choices with the model-side fibre strain $E_{ff}$ instead of longitudinal strain transforms the picture, shown in {numref}`fig-septum-strain-direction-diagnostic`. Two-sided pressure choices (mean, nearest-side, through-wall weighted) become tightly aligned with septal stress-strain work density (correlations near 0.97, magnitude errors near 0.07), and LV pressure also improves substantially. Transmural pressure remains poor on both tests. Part of the septal difficulty is therefore a strain-direction limitation of longitudinal strain, not only a pressure-assignment limitation.

```{figure} ../figures/fig_5_3b_septum_strain_direction_diagnostic.png
:name: fig-septum-strain-direction-diagnostic
:width: 95%

Model-side septal fibre diagnostic in the primary capped-reference sweep. Left: correlations with finite-element septal stress-strain work density. Right: septum/free-wall magnitude preservation. Fibre-aligned strain strongly favours two-sided pressure choices, while transmural pressure still performs poorly.
```

{numref}`tab-principal-strain-alignment` reports principal-shortening alignment in all three regions. For each cell in the replayed displacement field, the Green-Lagrange strain tensor was diagonalised and its most-compressive eigenvector compared with the fibre, longitudinal, radial, and circumferential directions. Fibre is the best-aligned candidate everywhere: mean angle 30–32 degrees, best-aligned in 60% of regional volume. Longitudinal alignment is markedly weaker — 48° in the LV free wall, 54° in the RV free wall, 50° in the septum.

Longitudinal alignment is not noticeably worse in the septum than in the free walls. The free-wall proxy therefore does not work because strain happens to align with longitudinal there; it works because adjacent cavity pressure tracks the FE work driving each cavity. The septum-specific failure of transmural pressure is consequently a pressure-assignment problem, not a strain-direction one.

```{table} Alignment of candidate directions with principal shortening in each region of the primary capped-reference sweep. Values are volume-weighted within each case and averaged across the 16 capped cases.
:name: tab-principal-strain-alignment
:align: left

| Region | Candidate direction | Mean angle to principal shortening | Mean $\lvert\cos\theta\rvert$ | Best-aligned volume fraction |
|---|---|---:|---:|---:|
| LV free wall | Fibre | 30.4 deg | 0.808 | 0.59 |
| LV free wall | Longitudinal | 48.3 deg | 0.622 | 0.21 |
| LV free wall | Radial | 59.7 deg | 0.469 | 0.13 |
| LV free wall | Circumferential | 63.5 deg | 0.424 | 0.07 |
| RV free wall | Fibre | 32.4 deg | 0.782 | 0.59 |
| RV free wall | Longitudinal | 54.5 deg | 0.547 | 0.14 |
| RV free wall | Radial | 56.4 deg | 0.515 | 0.16 |
| RV free wall | Circumferential | 60.0 deg | 0.478 | 0.11 |
| Septum | Fibre | 30.0 deg | 0.810 | 0.60 |
| Septum | Longitudinal | 50.2 deg | 0.598 | 0.20 |
| Septum | Radial | 57.0 deg | 0.505 | 0.15 |
| Septum | Circumferential | 64.2 deg | 0.415 | 0.06 |
```

Substituting the most-compressive principal-shortening direction at each cell — which requires the full local strain tensor — also fails to identify a single best pressure. Mean pressure was strongest for case ranking ($r=0.83$), RV pressure preserved the septum/free-wall ratio best ($\eta_\text{ratio}=0.11$), and neither matched the fibre-aligned result where two-sided pressures dominated both tests.

Principal shortening is the most-compressive direction at each cell by construction, so it also bounds what any other single-direction strain scalar — including a fitted linear combination of anatomical-axis strains with globally fixed weights — could achieve on these cells. Improvements beyond this point require either a spatially-varying strain direction (which the fibre-aligned diagnostic above uses within the model) or a proxy that includes shear strain components. Resolving the septal proxy therefore needs three-dimensional strain information: the full local tensor, or as a clinical compromise a combination of longitudinal, circumferential, and radial strains, rather than a different single scalar component.

(sec-results-pressure-mixtures)=
## Pressure Mixtures As A Diagnostic

The fixed candidates can be extended into a one-parameter family,

$$
p_\lambda = \lambda p_\text{LV} + (1-\lambda)p_\text{RV},
$$

so that $\lambda=0$ gives RV pressure, $\lambda=0.5$ mean pressure, $\lambda=1$ LV pressure, and values outside $[0,1]$ extrapolate beyond the physical LV--RV pressure interval. This is not proposed as a fitted clinical proxy; it asks where on the LV--RV axis the data place the septum. For the tangent-longitudinal proxy in the primary sweep, the best correlation with septal stress-strain work density occurred at $\lambda=1.60$, and the best septum/free-wall ratio preservation drifted to the upper boundary of the scan ($\lambda\geq 5$, with the magnitude objective still monotonically decreasing at the scan edge). Both optima sit well outside $[0,1]$, which means no linear mixture of the two cavity pressures matches the septal stress-strain reference without negative weight on RV pressure. {numref}`fig-septum-lambda` shows the split. The scan is the signature of the septum behaving as shared tissue: the single-pressure reduction is being asked to absorb geometry, stress redistribution, and strain-direction error, and there is no in-bounds $\lambda$ that absorbs them well.

```{figure} ../figures/fig_5_4_septum_lambda_scan.png
:name: fig-septum-lambda
:width: 95%

Diagnostic scan of the septal pressure mixture $p_\lambda=\lambda p_\text{LV}+(1-\lambda)p_\text{RV}$ in the primary capped-reference sweep. The best value of $\lambda$ depends on whether the target is correlation across the pressure sweep or preservation of septum/free-wall work-density ratios. Both optima sit outside the physical $[0,1]$ interval, which is why no fitted single septal pressure would be honest.
```

(sec-results-numerical)=
## Numerical Robustness Checks

The detailed numerical checks behind the interpretation are collected in {ref}`chap-appendix-numerical` and summarised in {numref}`tab-numerical-robustness-summary`. Only the implications for the present chapter are picked out below.

The primary capped-reference sweep is complete: all 16 cases have solver pressure histories, metrics files, per-cell work data, and finite numeric arrays on the shared 5 mm reference mesh ($n=8070$ cells). The capped production set was not rerun at 10 mm, so the earlier h=10-to-h=5 comparison is treated as numerical-method support rather than as a direct convergence proof for the capped reference-state choice. Against the 3.75 mm mesh-convergence endpoints in the related production setup, peak pressures and end-diastolic volumes differed by less than 0.8% at 5 mm, and free-wall work-density ratios differed by less than about 3%. Septal quantities were more sensitive, especially at high RV pressure: the observed difference between the 5 mm and 3.75 mm meshes was about 5-7% for severe-case septal stress-strain work and septal longitudinal-proxy quantities. Across all sixteen cases the geometric septum is 1269 cells and the tag-3 septum is 1266 cells, a 0.1% difference shared by every case, so the primary septal region is not a non-canonical mask artefact.

In postprocessing-only replay tests, DG1 state storage changed integrated regional stress-strain work by at most about 1.2% relative to Quadrature6, whereas DG0 suppressed high-pressure septal work. The basal support should be read as a stabilizing modelling choice: the production setup fixes only the base-normal/global-x displacement component, tangential sliding remains, and the no-Dirichlet variants did not converge during end-diastolic inflation. Net Robin work was below 0.2% of cavity boundary work in the checked endpoint cases. These checks support the main regional conclusions, with the septum appropriately treated as the numerically more sensitive region.

(sec-results-reference-state)=
## Reference-State Sensitivity

Beyond mesh and function-space resolution, the largest caveat on the absolute work-density numbers in this chapter is the unloaded reference configuration. The inverse-unloading step uses the same fixed UKB geometry for all pressure cases. In severe RV loading, this can make the inferred unloaded RV reference too small because the model has no RV hypertrophy, curvature remodelling, or regional material adaptation with which to carry the higher end-diastolic pressure. The primary capped-reference sweep keeps the end-diastolic mesh target unchanged but caps the RV end-diastolic pressure used during inverse unloading at 5 mmHg. This is more constrained than arbitrary passive-stiffness tuning, because it changes only the questionable RV prestress target while keeping the circulation, anatomy, and material law otherwise comparable.

Regional stiffness checks, fixed-reference acute-loading pilots, and an exploratory healthy/PAH patient-geometry comparison all supported the same central concern: RV and RV-side septal absolute work-density magnitudes are reference-state and geometry sensitive, and the direction of the bias is not captured by a simple one-sided correction. The reference-state checks are given in {ref}`sec-app-reference-remodeling-sensitivity`; the patient-geometry direction check is given in {ref}`chap-appendix-patient-geometry`. The pressure-proxy comparisons remain useful as controlled fixed-geometry tests, but severe-case RV and RV-side septal magnitudes should not be treated as corrected PAH tissue-work estimates.


The fixed-geometry pressure sweep should therefore be read carefully. It is not a simulation of PAH progression in a patient. Real PAH changes pressure, volume, wall thickness, curvature, stiffness, activation, and contractility together. The sweep isolates one part of that system by changing the circulation while holding the anatomy and material model fixed. That isolation is useful, because it exposes how pressure choices for the longitudinal proxy respond to loading changes. It is not the same as a clinical cohort, and its severe RV and RV-side septal density magnitudes should not be treated as corrected PAH tissue-work estimates.

This distinction gives the thesis a more conservative and more useful result. The model does not prove that one septal pressure formula is clinically best. It shows where the pressure-strain idea is mechanically reasonable, where it becomes ambiguous, and why the septum is the difficult case. The narrow recommendation that survives is concrete: use adjacent cavity pressure for free-wall pressure-strain work; avoid transmural pressure as a septal work-density proxy in RV pressure overload; treat any single-pressure septal formula as a modelling choice rather than a measurement.
