(chap-results)=
# Results

The results are easiest to understand if two questions are kept separate. First: within a single simulation, does the pressure-strain proxy get the regional work differences right? Second: when the circulation changes while geometry is held fixed, does the proxy rank the loading cases in the same order as the finite-element stress-strain work density?

A proxy can rank a pressure sweep correctly and still get the regional balance wrong within a single case, so the chapter starts with the regional ratio analysis. The ratio test is a within-case mechanics check: each simulation gives an independent answer to whether the proxy preserves the relative magnitude of work across regions, so the conclusion is not tied to which loading axis was swept. The pressure sweep then comes in as a controlled loading experiment, asking whether the same proxies rank the cases consistently with the finite-element reference.

A note before the figures. {numref}`fig-cascade-loops-sweep` and {numref}`fig-septum-pressure-choices` should be read for loop areas only — the proxy quantity is loop area, and these figures are a qualitative orientation to what the rest of the chapter compares quantitatively. {numref}`fig-cascade-loops-sweep` places the FE reference and the clinical pressure-strain proxy side by side across the sixteen cases: the top row is fiber-direction stress-strain loops $S_{ff}$ vs $E_{ff}$, the bottom row is the proxy $p_\text{cav}$ vs longitudinal strain $\varepsilon_{ll}$. The top-row projection $S_{ff}\,\dot E_{ff}$ is the dominant component of the full tensor contraction $\mathbf{S}:\dot{\mathbf{E}}$ but not the literal full work; cross-fiber, sheet, and sheet-normal contributions are smaller but not zero. Loop shapes, timing, and other geometric features beyond loop area are not the focus. Loop area is signed in principle — work done by the cavity on the tissue would flip the sign — but every loop here goes the same way, so areas are positive throughout.

The visible question is whether the bottom-row areas preserve the top-row regional balance, and whether they do so consistently as RV pressure rises. The free-wall proxy uses adjacent cavity pressure; the septum is shown with $p_\text{LV}$ as a default, but which pressure should drive the septal proxy is itself one of the chapter's open questions. {numref}`fig-septum-pressure-choices` shows the same septum loops under four candidate pressures: $p_\text{LV}$, $p_\text{RV}$, mean, and transmural.

```{figure} ../figures/fig_5_0c_cascade_loops_sweep.png
:name: fig-cascade-loops-sweep
:width: 100%

Top row: fiber-direction stress-strain loops $S_{ff}$ vs $E_{ff}$ for the LV free wall, RV free wall, and septum across the sixteen capped-reference sweep cases (last simulated beat). Bottom row: clinical pressure-strain proxy ($p_\text{LV}$ for LV and septum, $p_\text{RV}$ for RV) against tangent-longitudinal strain $\varepsilon_{ll}$. Each line is one simulation. Colour: achieved peak RV systolic pressure (mmHg).
```

```{figure} ../figures/fig_5_0d_septum_pressure_choices.png
:name: fig-septum-pressure-choices
:width: 100%

Septum pressure-strain loops across the sixteen cases under four candidate pressures: $p_\text{LV}$, $p_\text{RV}$, mean $(p_\text{LV}+p_\text{RV})/2$, and transmural $p_\text{LV}-p_\text{RV}$. All panels share the same septal longitudinal strain on the x-axis. Each line is one simulation; colour is achieved peak RV systolic pressure (mmHg).
```

The results use the capped-reference pressure-loading sweep defined in {ref}`chap-calibration`: sixteen cases on a shared biventricular reference mesh ($n=8070$ cells). Geometry, material model, fibre architecture, and end-diastolic mesh target are held fixed; only the 0D circulation varies to raise RV pressure across the cases. The RV end-diastolic pressure used during inverse unloading is capped at 5 mmHg.

The sixteen cases share the same region tag set (1269 geometric septum cells in every case; see {ref}`sec-shared-mask-tagging`), so regional integrals are case-comparable cell-by-cell.

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

Here $W_\text{int}[\Omega_A]$ is the volume-integrated stress-strain work over region $\Omega_A$, and $|\Omega_{A,0}|$ is that region's reference volume. Both $w_\text{int}$ and the pressure-strain loop area $w_\text{PS}$ are density-like quantities with units of pressure: J/m$^3$ = Pa, reported here in kPa. $w_\text{PS}$ is already in those units. All pressure-strain proxies are computed cellwise — per-cell loop area against the cell's assigned pressure — and then volume-averaged over the region; for spatially varying septal pressure choices (nearest-side and through-wall weighted), pressure varies cell-by-cell within the septum.

The free-wall ratio $R = w_\text{LV}/w_\text{RV}$ sits above one across the sweep, so we report the absolute error $|R_\text{proxy}-R_\text{FE}|$, averaged over the sixteen cases.

The septum produces two ratios per case: septum/LV-free-wall (below 1) and septum/RV-free-wall (above 1). Absolute differences would weigh "twice too high" and "twice too low" unequally, so we use the mean absolute log-ratio

$$
\eta_\text{ratio}
= \left\langle \left| \log \frac{R_\text{proxy}}{R_\text{FE}} \right| \right\rangle ,
$$

averaged across both ratios and all sixteen cases. The scale is multiplicative: $\eta_\text{ratio} = 0$ is exact and $\eta_\text{ratio} = 0.18$ corresponds to a typical ratio error of about $\exp(0.18)-1 \approx 20\%$.

The numerical floors on the FE reference — periodic-state convergence, energy-balance closure, and mesh sensitivity at 5 mm — sit an order of magnitude below the proxy errors reported below; full details are in {numref}`tab-numerical-robustness-summary` at the end of the chapter and in {ref}`chap-appendix-numerical`.

The central finding is summarised below, free walls first, then septum.

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

(sec-results-freewalls)=
## Free Walls

The simplest case is the comparison between the LV free wall and the RV free wall, with the septum excluded from both. Each free wall faces one cavity, so the pressure assignment is mechanically natural: $p_\text{LV}$ for the LV free wall and $p_\text{RV}$ for the RV free wall. This is the cleanest setting for the pressure assignment, but whether a single cavity pressure scaled against a single longitudinal strain component recovers the free-wall stress-strain work density is still an empirical question, not an identity; failure here would point to a more basic limitation than septal pressure ambiguity.

The adjacent-pressure tangent-longitudinal proxy tracks the finite-element LV/RV free-wall work-density ratio across the primary sweep, shown in {numref}`fig-freewall-spectrum`. Mean absolute error (raw $|R_\text{proxy}-R_\text{FE}|$) was 0.16 for the adjacent-pressure proxy, compared with 0.68 for $p_\text{LV}$ everywhere and 0.87 for $p_\text{RV}$ everywhere — pressure misassignment to either wall collapses the balance.

A separate test asked whether pressure magnitude matters at all, or whether the time-shape of the pressure trace is enough on its own. Each cavity's waveform was rescaled to unit peak, $\hat p(t)=p(t)/\max_t |p(t)|$, with the LV proxy using $\hat p_\text{LV}$ and the RV proxy using $\hat p_\text{RV}$. The free-wall proxy then reduces to $\oint \hat p\,d\varepsilon$ — same timing, no peak-pressure scale. The LV/RV balance also collapsed, so magnitude is carrying real information, not just shape.

Adjacent cavity pressure remains the best of the tested longitudinal pressure assignments for the free-wall ratio.

```{figure} ../figures/fig_5_2_freewall_ratio_spectrum.png
:name: fig-freewall-spectrum
:width: 95%

Free-wall LV/RV work-density ratio across the primary capped-reference pressure-loading sweep. The adjacent-pressure longitudinal proxy follows the finite-element stress-strain work-density ratio better than the alternatives. The pressure-normalized waveform-only index preserves timing information but not work-density magnitude.
```

A scatter view of the same comparison is shown in {numref}`fig-freewall-ratio-scatter`. This makes the difference between correlation and magnitude easier to see. Several pressure choices rank the cases in a similar order, but the adjacent-pressure points lie closest to the identity line.

```{figure} ../figures/fig_5_2c_freewall_ratio_scatter.png
:name: fig-freewall-ratio-scatter
:width: 95%

Scatter comparison between pressure-strain proxy LV/RV ratios and finite-element stress-strain LV/RV ratios in the primary capped-reference sweep. Each panel shows one longitudinal pressure assignment. The solid line is a least-squares regression, the dashed line is the identity line, and colour denotes achieved RV systolic pressure. Panel titles report the Pearson correlation $r$ between proxy and FE ratios and the mean absolute error $\text{MAE}=\langle|R_\text{proxy}-R_\text{FE}|\rangle$. A high $r$ alone is not enough; the useful proxy should also lie near the identity line, captured by a small MAE.
```

The free-wall ratio test asks whether the proxy preserves regional magnitudes. The next question is whether pressure-strain also ranks loading cases better than pressure or strain alone.

The ranking test is shown for both free walls in {numref}`fig-rv-lakatos-bridge`.

Across the sweep, the adjacent-pressure longitudinal proxy correlated strongly with finite-element work density in both walls: $r=0.994$ in the LV and $r=0.967$ in the RV. The single-component comparators in {numref}`tab-freewall-correlations` show why combining pressure and strain matters. In the LV, $p_\text{LV}$ is nearly constant across the sweep and falls the wrong way as the RV expands, while longitudinal strain alone carries little ranking signal. In the RV, $p_\text{RV}$ alone carries most of the ranking but longitudinal shortening alone carries none.

One potential challenge: swapping in non-adjacent $p_\text{LV}$ on the RV side gives a slightly higher correlation ($r=0.992$). This reflects co-variation of achieved $p_\text{LV}$ and $p_\text{RV}$ along the capped-reference path, so ranking alone cannot tell adjacent from non-adjacent pressure here. The magnitude analysis above settles it: non-adjacent $p_\text{LV}$ on the RV side inflates the RV proxy and collapses the LV/RV ratio.

Wall-adjacent pressure paired with longitudinal strain is therefore both correlation-strong and magnitude-stable.

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

Adjacent pressure-longitudinal-strain proxies versus finite-element stress-strain work density in the primary capped-reference sweep. Left: LV free wall. Right: RV free wall. The main scatter in each panel uses the adjacent pressure-strain proxy; the inset reports Pearson correlations, with PS denoting the adjacent pressure-strain proxy. Colour denotes achieved RV systolic pressure.
```

(sec-results-septum)=
## The Septum

The septum is not a free wall. It is a shared internal wall with LV pressure on one side and RV pressure on the other, so the pressure assignment is qualitatively different. A free wall has one comparatively unambiguous pressure scale; for the septum we test six candidates.

Four are uniform across the septal volume: $p_\text{LV}$ (the usual clinical convention), $p_\text{RV}$ (the pressure on the opposite septal face), the transmural difference $p_\text{LV}-p_\text{RV}$ (net pressure across the wall), and the mean $(p_\text{LV}+p_\text{RV})/2$ (septal tissue loaded from both sides). Two more vary across the septum's thickness: a nearest-side pressure that assigns $p_\text{LV}$ to cells on the LV side and $p_\text{RV}$ to cells on the RV side, and a through-wall weighted pressure that interpolates smoothly between the two using a transventricular coordinate. Formal definitions are in {ref}`sec-work-definitions`.

Across the sweep, every single-pressure choice except transmural carried a positive ranking correlation with septal stress-strain work density. LV pressure gave the smallest septum/free-wall magnitude error among them. Transmural pressure failed both tests — the only negative ranking correlation and the largest magnitude error.

{numref}`tab-septum-proxies` reports the per-pressure values. The table is restricted to the longitudinal-strain proxy; a fibre-aligned diagnostic is taken up below.

```{table} Septal longitudinal pressure-strain proxy performance in the primary capped-reference pressure-loading sweep. Correlation tests case ranking across the sweep; the log-ratio error $\eta_\text{ratio}$ (defined above) tests preservation of septum/free-wall magnitude within each case.
:name: tab-septum-proxies
:align: left

| Pressure choice | Ranking correlation $r$ | Log-ratio error $\eta_\text{ratio}$ |
|---|---:|---:|
| $p_\text{LV}$ | 0.540 | 0.805 |
| $p_\text{RV}$ | 0.527 | 1.171 |
| $p_\text{LV}-p_\text{RV}$ | -0.331 | 2.075 |
| Mean pressure | 0.535 | 0.969 |
| Nearest-side pressure | 0.547 | 0.999 |
| Through-wall weighted pressure | 0.540 | 0.970 |
```

The correlation part of the table is shown as scatter plots in {numref}`fig-septum-correlation-scatter`. The plot makes two points visible. First, transmural pressure is visually the wrong trend for this primary sweep: high-RV-pressure cases have low transmural pressure but high septal stress-strain work density, so the proxy moves opposite to the reference and the correlation becomes negative. Second, the $p_\text{LV}$, $p_\text{RV}$, mean, nearest-side, and through-wall weighted choices are not identical, but they all assign the septum a cavity pressure rather than a pressure difference.

```{figure} ../figures/fig_5_3a_septum_proxy_correlation_scatter.png
:name: fig-septum-correlation-scatter
:width: 95%

Septal pressure-choice correlations in the primary capped-reference sweep. Each panel compares a longitudinal pressure-strain proxy with finite-element septal stress-strain work density. The solid line is a least-squares regression and colour denotes achieved RV systolic pressure.
```

The geometric septum mask used here was also stress-tested by shrinking and expanding it near the LV/RV junction, where the shared-wall boundary is hardest to define. This sensitivity check did not rescue transmural pressure as a septal work-density proxy. In a very tight central-septum core, transmural pressure can regain a positive case-ranking correlation, but the same mask gives the largest septum/free-wall magnitude error in the sweep. This is why the main septal result gives more weight to regional ratios than to correlation alone; details are in {ref}`sec-app-septum-epi-envelope`.

(sec-results-septum-strain-direction)=
### Strain Direction in the Septum

The pressure-assignment failure above explains only part of the septal difficulty. Pairing the same pressure choices with the model-side fibre strain $E_{ff}$ instead of longitudinal strain transforms the picture, shown in {numref}`fig-septum-strain-direction-diagnostic`. Two-sided pressure choices (mean, nearest-side, through-wall weighted) become tightly aligned with septal stress-strain work density (correlations near 0.97, magnitude errors near 0.07), and LV pressure also improves substantially. Transmural pressure remains poor on both tests. Part of the septal difficulty is therefore a strain-direction limitation of longitudinal strain, not only a pressure-assignment limitation.

```{figure} ../figures/fig_5_3b_septum_strain_direction_diagnostic.png
:name: fig-septum-strain-direction-diagnostic
:width: 70%

Model-side septal fibre diagnostic in the primary capped-reference sweep. Top: correlations with finite-element septal stress-strain work density. Bottom: septum/free-wall magnitude preservation.
```

{numref}`tab-principal-strain-alignment` reports the angle between each candidate strain direction and the cell-local principal-shortening direction, volume-weighted within each region. Fibre is the best-aligned candidate everywhere (~30°), and longitudinal is similarly misaligned across all three regions (48° LV, 54° RV, 50° septum). The septum is not uniquely poorly served by longitudinal strain.

Combined with the fibre-aligned diagnostic above, this isolates the septum-specific failure: pressure choice, not strain direction. Switching strain direction helps every region similarly in pure alignment terms; the reason the fibre substitution looks dramatic for the septum is that the two-sided pressure choices were already the right pressure scale, and giving them the right strain magnitude on top rescues a proxy that was failing for pressure-related reasons.

```{table} Alignment of candidate strain directions with principal shortening in each region of the primary capped-reference sweep. For each cell, the Green-Lagrange strain tensor is diagonalised and its most-compressive eigenvector compared with the fibre and longitudinal directions. Values are volume-weighted within each case and averaged across the 16 capped cases.
:name: tab-principal-strain-alignment
:align: left

| Region | Candidate direction | Mean angle to principal shortening | Mean $\lvert\cos\theta\rvert$ | Best-aligned volume fraction |
|---|---|---:|---:|---:|
| LV free wall | Fibre | 30.4 deg | 0.808 | 0.59 |
| LV free wall | Longitudinal | 48.3 deg | 0.622 | 0.21 |
| RV free wall | Fibre | 32.4 deg | 0.782 | 0.59 |
| RV free wall | Longitudinal | 54.5 deg | 0.547 | 0.14 |
| Septum | Fibre | 30.0 deg | 0.810 | 0.60 |
| Septum | Longitudinal | 50.2 deg | 0.598 | 0.20 |
```

Substituting the most-compressive principal-shortening direction at each cell — which requires the full local strain tensor — also fails to identify a single best pressure. Mean pressure was strongest for case ranking ($r=0.83$), RV pressure preserved the septum/free-wall ratio best ($\eta_\text{ratio}=0.11$), and neither matched the fibre-aligned result where two-sided pressures dominated both tests.

(sec-results-pressure-mixtures)=
## Pressure Mixtures As A Diagnostic

The fixed candidates can be extended into a one-parameter family,

$$
p_\lambda = \lambda p_\text{LV} + (1-\lambda)p_\text{RV},
$$

with $\lambda$ a single scalar applied uniformly across the septum (distinct from the spatially varying $\lambda(\mathbf{X})$ used in the through-wall weighted choice). $\lambda=0$ gives RV pressure, $\lambda=0.5$ mean, $\lambda=1$ LV pressure. This is not a fitted clinical proxy; it asks where on the LV--RV axis the data place the septum. For the tangent-longitudinal proxy in the primary sweep, the best correlation with septal stress-strain work density occurred at $\lambda=1.60$, and the best septum/free-wall ratio preservation drifted to the upper boundary of the scan ($\lambda\geq 5$, with the magnitude objective still monotonically decreasing at the scan edge). Both optima require negative weight on RV pressure — no weighted average of the two cavity pressures matches the septal stress-strain reference. {numref}`fig-septum-lambda` shows the split.

```{figure} ../figures/fig_5_4_septum_lambda_scan.png
:name: fig-septum-lambda
:width: 95%

Diagnostic scan of the septal pressure mixture $p_\lambda=\lambda p_\text{LV}+(1-\lambda)p_\text{RV}$ in the primary capped-reference sweep. Two objectives are scanned: correlation across the pressure sweep, and septum/free-wall ratio preservation.
```

(sec-results-numerical)=
## Numerical Robustness Checks

The mesh-convergence study against a 3.75 mm reference (full details in {ref}`chap-appendix-numerical`) gave hemodynamic differences below 0.8% and free-wall work-density ratio differences below 3% at the production 5 mm resolution. Septal quantities were more sensitive at high RV pressure, with 5–7% differences for severe-case stress-strain work and longitudinal-proxy quantities. Postprocessing-only replay showed DG1 state storage within 1.2% of the production Quadrature6 setup. Net Robin (boundary support) work was below 0.2% of cavity boundary work. The geometric and tag-3 septum masks differ by 0.1% across all sixteen cases, so the primary septal region is not a tagging artefact. The full summary is in {numref}`tab-numerical-robustness-summary`.

