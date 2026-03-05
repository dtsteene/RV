# Thesis Writing Instructions for Claude Code

This document is a guide for continuing the master thesis in `/Users/daniel/Documents/master/RV/`. It was written by a Claude Code session that spent time reading the full codebase in `/Users/daniel/Documents/master/cardiac-work/` and the existing thesis drafts. Read this entire file before touching any thesis content.

---

## The Project in Plain Terms

Daniel has built a coupled computational heart simulator. The simulator combines a three-dimensional finite element model of a biventricular heart with a zero-dimensional lumped-parameter model of the full cardiovascular circulation. The code lives in `/Users/daniel/Documents/master/cardiac-work/`. The thesis should explain what was built, why it was hard to build, what the tool revealed, and why that matters clinically.

The central scientific question is deceptively simple: when a physician uses a pressure-volume loop to estimate how much mechanical work the right ventricle did in one heartbeat, are they getting an accurate number? The hypothesis — and the main finding — is that in a diseased state like pulmonary arterial hypertension (PAH), they are not, because the shared wall between the two ventricles (the interventricular septum) is being loaded from both sides simultaneously, and the standard metric does not account for this. The transmural pressure, meaning the difference between left and right ventricular pressure, turns out to be a better proxy for the mechanical work done by the septal myocardium.

---

## Writing Style — Non-Negotiable

The single most important instruction in this document is about writing style. This thesis must read like a book, not like a list of capabilities. Specifically:

**Prose, not bullets.** Do not use bullet points for scientific content. Ever. If you find yourself wanting to write a bullet list, write a paragraph instead. Three things that go together can share a sentence. Five things that go together belong in two or three sentences. Ten things go in a paragraph. This is how good scientific writing works.

**Subheadings sparingly.** The current draft has too many subheadings. A section heading every two or three pages is appropriate. A heading every paragraph is a symptom of AI generation and will read that way. Within a chapter, let paragraphs flow. Use subheadings only when transitioning between genuinely distinct topics that cannot be bridged with a transition sentence.

**Equations belong in sentences.** An equation is not a replacement for an explanation; it is a formal statement of one. Every equation should be introduced in the prose before it appears, and the notation should be explained immediately after. Write something like: "The deformation of the tissue is described by the deformation gradient $\mathbf{F}$, which maps a material point from its reference position $\mathbf{X}$ to its current position $\mathbf{x}$, so that $\mathbf{F} = \partial \mathbf{x} / \partial \mathbf{X}$. Its determinant $J = \det \mathbf{F}$ measures the local volume change." That is correct scientific writing.

**Transitions matter.** The end of each paragraph should make the reader want to continue. The beginning of each paragraph should make sense as a continuation of the previous one. If two paragraphs do not connect, there is a missing sentence somewhere.

**First person is fine, but not constant.** "We developed..." is natural for a thesis written with supervisors involved. "I found..." is also acceptable for genuinely personal observations. Do not use passive voice to avoid the issue — passive voice is often weaker and harder to read than direct active constructions.

**No adverb padding.** Do not write "very complex" or "extremely important" or "highly sophisticated." Write what is complex, what is important, what is sophisticated. If a concept needs emphasis, the emphasis should come from where you place it in the sentence, not from an adverb.

**On the word "novel."** Every thesis claims novelty somewhere. Do not lean on this word. Describe what was done. The novelty speaks for itself if the work is good.

---

## Thesis Structure

The thesis is organized as a Jupyter Book (MyST Markdown), with the configuration in `myst.yml`. Each chapter lives in its own directory. The current structure has content in `01_the_question/` and `02_the_model/`. The plan below describes the full intended structure. Add directories and files as needed.

### Chapter 0 — Introduction (`intro.md`)

**What exists:** A short abstract and a one-paragraph framing of the core question. This is essentially a placeholder.

**What is needed:** A genuine introduction, probably 1500–2500 words, that does the following. It starts with the cardiovascular system and the clinical context — not with an equation, not with a definition, but with the observation that the right ventricle is systematically understudied and under-measured. It explains what pressure-volume loops are and why clinicians rely on them, and it explains why the RV is different from the LV in a way that makes this reliance potentially misleading. It ends by stating the research question and outlining the structure of the document.

The existing abstract question — "do standard RV pressure-volume loops accurately reflect the mechanical work generated by the RV myocardium?" — is exactly right. The introduction should build toward that question from first principles, not announce it in the first sentence.

**Key content to include:** The clinical relevance of RV dysfunction in PAH. The anatomical argument for why the septum complicates standard RV work estimation (it is a shared wall loaded by LV pressure from one side and RV pressure from the other). A brief preview of the computational approach. A one-sentence summary of the main result (transmural pressure tracks septal work better than LV pressure alone).

### Chapter 1 — The Scientific Question (`01_the_question/The Scientific Question.md`)

**What exists:** A reasonable first draft explaining the PV-loop formulation $W = \oint P \, dV$ and the "Hidden Hero" hypothesis. The tone is already decent — it is written as prose with equations. But the admonition boxes (`::: admonition`) make it feel like documentation, not a thesis. Consider removing them and integrating their content into flowing prose.

**What is needed:** Expand the section on *why* the septum creates ambiguity. The key mechanism is this: during systole in a healthy heart, the LV generates roughly five times higher pressure than the RV. This pressure difference loads the septum such that it bows into the RV cavity. The RV effectively "free-rides" on this septal motion — the LV is doing work that shows up as RV volume ejection. In PAH, the RV pressure rises toward LV levels. The septum flattens and may even bow into the LV, a sign clinicians call the "D-sign." In this state, the standard assumption that LV pressure alone drives septal mechanics breaks down completely.

**Mathematical content:** The quantity being compared is the mechanical work done by the septal myocardium, computed as $W_\text{sep} = \int_\Omega \mathbf{S} : \dot{\mathbf{E}} \, dV$ where $\mathbf{S}$ is the second Piola-Kirchhoff stress tensor and $\mathbf{E}$ is the Green-Lagrange strain. This integral over the septal domain gives the ground-truth internal elastic work. The clinical proxy for this would ordinarily be the area enclosed in a pressure-strain loop, $W_\text{PS} \approx \oint P \, d\epsilon_\text{ff}$ where $\epsilon_\text{ff}$ is the fiber strain and $P$ is the chamber pressure. The question is: which $P$ do you use for the septum, and does it matter?

### Chapter 2 — The Computational Model (`02_the_model/`)

This chapter is the largest and most technical. The existing files in `02_the_model/` contain good drafts of individual components. The task is to unify them into a coherent narrative. The files are: `overview.md`, `geometry.ipynb`, `fibers.md`, `3D_mechanics.md`, `active_contaction.md`, `0D_circulation.md`.

Note the typo: `active_contaction.md` should be renamed to `active_contraction.md` in the filesystem and updated in `myst.yml`.

#### Section: Geometry and Fiber Architecture

**What exists:** `geometry.ipynb` describes the truncated ellipsoid geometry. `fibers.md` describes the LDRB algorithm and helix angles. These are well-written.

**What is needed:** A connecting narrative. The geometry chapter should open by motivating the choice of idealized geometry (control over shape parameters, reproducibility, no need for patient-specific imaging at this stage). It should then describe the biventricular ellipsoid concretely — dimensions, wall thicknesses, the way the RV is attached to the LV as a crescent-shaped cavity. The LDRB section should follow naturally, framed as: once you have the geometry, you need to assign the microstructure. The equations in `fibers.md` are correct — keep them but surround them with better prose explaining *why* fiber angles vary transmurally (it is related to the mechanical efficiency of the "wringing" motion during systole).

**Technical details from code:** In `geometry_generator.py`, fiber angles are `alpha_endo_lv=60, alpha_epi_lv=-60` for the LV, and `alpha_endo_rv=90, alpha_epi_rv=-25` for the RV. The RV has shallower angles to reflect its different wrapping geometry. The mesh resolution is approximately 5 mm characteristic element length for the UKB synthetic mesh, producing around 45,000 tetrahedra. For patient-specific meshes (healthy and PAH cases), the count rises to 60,000–80,000.

Three function spaces are used for the fiber fields: a sixth-order quadrature space for the solver (where integration accuracy matters most), a DG0 space for assigning spatially varying active tension by region, and a DG1 space for visualization.

#### Section: Three-Dimensional Continuum Mechanics

**What exists:** `3D_mechanics.md` is the best-written section in the existing draft. The kinematics are clearly described. The Holzapfel-Ogden model is laid out correctly.

**What is needed:** The existing draft describes the passive mechanics well. It needs a clearer explanation of why the volumetric term uses a penalty formulation rather than strict incompressibility, and why this was necessary. The heart muscle is nearly incompressible but not perfectly so, and the FEniCSx implementation uses a slightly compressible formulation to avoid numerical locking. This connects to a critical bug discovered during development, which is described below in the implementation section.

The **active stress formulation** (`active_contaction.md`) needs expansion. The existing draft describes $\mathbf{S}_\text{total} = \mathbf{S}_\text{passive} + T_a (\mathbf{f}_0 \otimes \mathbf{f}_0)$ but does not explain the calcium-driven dynamics of $T_a(t)$. In the code, the Blanco ventricular activation model is used: the active tension rises from zero at end-diastole, peaks around 250 ms into systole, then decays exponentially during the relaxation phase. The total beat duration is calibrated to 75 beats per minute, giving a cycle length of 0.8 seconds. The LV and RV have a maximum active tension of approximately 100 kPa, while the septum is given 70 kPa to reflect its thinner and less dominant role.

**The spatially varying activation** is one of the more subtle aspects of the implementation. Three distinct activation zones are defined — the LV free wall, the septum, and the RV free wall — each with its own scaling of the activation waveform. This heterogeneity is assigned via a DG0 function, where cell tags (generated by the LDRB process and manually refined using `septum_editor.py`) determine which activation amplitude a given element receives.

**Material parameters:** $a = 0.33$ kPa, $b = 8.0$, $a_f = 0.876$ kPa, $b_f = 7.46$, $a_s = 0.485$ kPa, $b_s = 8.41$, $a_{fs} = 0.216$ kPa, $b_{fs} = 5.98$, bulk modulus $\kappa = 10$ kPa.

#### Section: The Zero-Dimensional Circulation Model

**What exists:** `0D_circulation.md` describes the Windkessel concept and the 3D-0D coupling interface well. The electrical analogy table is actually a decent didactic device but should probably be prose instead.

**What is needed:** A clearer description of the Regazzoni (2020) model specifically — what it models (four cardiac chambers with valve dynamics, systemic and pulmonary circulations as three-element Windkessel networks), and why this particular model was chosen. The coupling strategy — the volume ratio approach — deserves careful explanation because it is one of the less obvious engineering choices in the project.

**The volume ratio coupling:** When a patient-specific mesh is used, the cavity volume of the FEM mesh (the volume enclosed by the LV endocardium, for example) does not match the end-diastolic volume that the 0D model was calibrated for. Rather than rescaling the 0D model or reshaping the geometry, a ratio is computed between the mesh cavity volume and the 0D model's end-diastolic volume at steady state. During the simulation, when the 0D model requests a particular volume from the ventricle, the FEM model delivers that volume scaled by this ratio. This allows the 0D pressure dynamics to be physiologically correct even when the mesh geometry differs from the clinical measurements used to tune the 0D model. This is expressed as:
$$V_\text{FEM}(t) = \frac{V_\text{mesh,ED}}{V_\text{0D,ED}} \cdot V_\text{0D}(t)$$
where $V_\text{mesh,ED}$ is the cavity volume measured from the unloaded mesh and $V_\text{0D,ED}$ is the end-diastolic volume at steady state in the 0D simulation.

---

### Chapter 3 — Implementation and Challenges

This is arguably the most important chapter for demonstrating the real difficulty of the work. It is also the chapter most likely to be omitted from a typical thesis, which is a mistake. The challenges described below are genuine scientific contributions — they represent lessons learned about the limitations of existing software and the subtle ways that numerical methods can produce physically misleading results.

**Write this chapter as a narrative of discovery.** Not "we encountered bug X and fixed it by doing Y." Rather: here is what we expected, here is what we observed, here is the reasoning process that led to the diagnosis, and here is the resolution. This is how science actually works and how thesis readers learn to do it themselves.

#### The Deviatoric Stress Bug

The first major implementation challenge came from the fenicsx-pulse library's compressible material implementation. When computing stresses using compressible hyperelastic models, the stress tensor should be computed from the full Green-Lagrange strain tensor $\mathbf{E}$. However, early versions of the implementation were only passing the deviatoric component of $\mathbf{E}$ to the stress calculation routines. Since the volumetric component of the strain is responsible for a significant fraction of the stress — particularly in the stiff fiber directions — this caused the computed stresses to be systematically too low by a substantial factor. The symptoms were subtle: the model converged, the pressure-volume loops looked plausible in shape, but the stress magnitudes were far below what would be expected for cardiac tissue at these pressures. The fix required tracing through the FEniCSx computation graph to identify where the full strain was being silently replaced by its deviatoric part, then patching the library code.

#### Prestressing and the Unloading Problem

The geometry is generated as a mesh representing the heart at some natural shape. But in reality, the heart at end-diastole is already under significant pressure — the LV end-diastolic pressure is typically 8–12 mmHg and the RV is at 4–8 mmHg. If one simply applies these pressures to the reference mesh, the resulting deformation is computed relative to an already-stressed state, and the stress-free reference configuration is never realized. This introduces errors in the stress field throughout the simulation.

The solution is inverse elasticity, also called prestressing: given a deformed configuration (the mesh) and the loads applied to it, find the reference (stress-free) configuration by solving an inverse problem. The method used here is the approach of Gee et al., which iteratively updates the reference coordinates. Once the stress-free reference is found, the simulation begins from this configuration and deforms forward under the imposed end-diastolic pressures, recovering the original mesh shape and then continuing through systole and diastole.

This prestressing step is numerically delicate. The boundary conditions must be carefully chosen — a Robin condition on the epicardium with springs of stiffness $k_\text{epi} = 10^5$ Pa/m and a Dirichlet condition fixing the base prevent rigid body motion while allowing physiological deformation. The inverse problem typically requires 10–15 iterations to converge to a sufficiently stress-free reference.

#### Metrics Calculation and the DG1 Projection Problem

A significant amount of time was spent debugging what appeared to be a catastrophic energy imbalance in the simulation results. The computed internal mechanical work was returning values roughly three times lower than the external work done by the pressure forces — a violation of the first law of thermodynamics that seemed to indicate a fundamental flaw in the simulation.

The source of this discrepancy was a subtle numerical artifact in how quantities were being projected between function spaces for post-processing. The stress $\mathbf{S}$ and strain $\mathbf{E}$ are computed at quadrature points inside each element. When these fields were projected to a first-order discontinuous Galerkin (DG1) space for storage and visualization, the projection introduced oscillations at the interfaces between elements. The DG1 projection assigns nodal values, and for the thin septum in particular — where steep gradients exist between the LV and RV sides — these oscillations were severe enough to cause sign changes in the integrand of the work calculation. Integrating an oscillating field over a thin region can produce a result with the wrong sign and wildly incorrect magnitude.

The fix was to use a piecewise-constant DG0 projection instead, where each cell in the mesh is assigned a single average value. This eliminates the oscillations entirely. The trade-off is spatial resolution, but for integrated quantities like total regional work, the DG0 approach is actually more accurate because it does not introduce spurious gradients.

---

### Chapter 4 — Tuning the Circulation Model

The 0D circulation model contains dozens of parameters representing the mechanical properties of vessels, valves, and chamber wall stiffnesses across the systemic and pulmonary circulations. For the healthy baseline, these parameters were adapted from the literature and the Regazzoni (2020) reference. For the PAH case, they needed to be substantially modified to reflect the elevated pulmonary vascular resistance and altered chamber geometry that characterizes the disease.

This chapter describes the parameter identification problem and the sequence of optimization methods applied to solve it.

**Framing the problem:** A parameter vector $\boldsymbol{\theta} \in \mathbb{R}^n$ determines the behavior of the 0D model. The objective is to find $\boldsymbol{\theta}^*$ such that the model output — pressure waveforms, flow rates, ejection fractions, end-diastolic volumes — matches clinical target values derived from patient measurements and literature. The cost function is a weighted sum of squared deviations from these targets:
$$\mathcal{L}(\boldsymbol{\theta}) = \sum_i w_i \left(\frac{y_i(\boldsymbol{\theta}) - y_i^\text{target}}{y_i^\text{target}}\right)^2$$

The difficulty is that the cost landscape is non-convex, has multiple local minima, and each evaluation of $\mathcal{L}$ requires running the 0D model to a periodic steady state, which can take tens of seconds.

**Nelder-Mead:** The first approach was the Nelder-Mead simplex method, a gradient-free local optimizer that explores parameter space by reflecting and contracting a simplex of $n+1$ points. It worked for the healthy baseline because a reasonable starting point was available from literature values. For the PAH case, the parameter changes are large enough that Nelder-Mead consistently converged to poor local minima.

**Differential evolution:** The second approach was differential evolution, a population-based global optimizer that maintains a population of candidate solutions and generates new candidates by combining elements from the current population with random perturbations. This is effective at escaping local minima and proved better at exploring the large parameter shifts required for PAH. The result from differential evolution was then passed to Nelder-Mead as a warm start for local refinement.

**Bayesian optimization with Optuna:** The third and most successful approach was Bayesian optimization using the Optuna library. Optuna maintains a probabilistic surrogate model of the cost function and uses it to intelligently select the next evaluation point — focusing on regions that are both promising (low predicted cost) and uncertain (few previous evaluations nearby). The Tree-structured Parzen Estimator (TPE) sampler used by Optuna proved effective here. Because each evaluation is expensive, the ability to extract maximum information from each run is critical, and Bayesian methods are specifically designed for this regime.

---

### Chapter 5 — Results

This chapter presents the simulation results for the three test cases: the UKB synthetic baseline, the patient-specific healthy anatomy, and the patient-specific PAH anatomy.

#### Hemodynamics Validation

Before examining work estimates, the simulated hemodynamics must be shown to be physiologically realistic. Present pressure-volume loops for both LV and RV from all three cases. The healthy cases should show LV peak pressures of approximately 120 mmHg and RV peak pressures of approximately 25 mmHg, with LV stroke volumes around 70 mL. The PAH case should show elevated RV pressures (>50 mmHg) and reduced RV stroke volume.

#### Work Decomposition

The internal elastic work of the septum is decomposed into fiber, cross-fiber (sheet), and wall-normal components. Results show that fiber shortening contributes approximately 35% of the total internal work in the LV, with the sheet direction contributing around 45% and the wall-normal direction accounting for the remainder. For the RV, the fiber fraction is higher at around 53%. This decomposition reveals that standard clinical work proxies, which implicitly assume that all myocardial work comes from fiber shortening, miss a substantial fraction of the true energetic expenditure.

#### Proxy Comparison: Healthy vs. PAH

This is the central result. For the interventricular septum, three pressure proxies are compared against the ground-truth internal work:

The **left ventricular pressure** alone ($P_\text{LV}$) as the driving pressure for septal deformation.
The **right ventricular pressure** alone ($P_\text{RV}$).
The **transmural pressure** ($P_\text{LV} - P_\text{RV}$), which captures the net pressure difference across the septal wall.

In healthy physiology, $P_\text{LV}$ and $P_\text{LV} - P_\text{RV}$ perform similarly, with correlation coefficients $R^2 \approx 0.94$ and $0.93$ respectively. This makes sense: in health, $P_\text{RV}$ is small compared to $P_\text{LV}$, so the transmural pressure is nearly identical to the LV pressure. The septum is effectively an LV structure mechanically.

In PAH, the picture changes substantially. The $P_\text{LV}$ proxy shows degraded correlation ($R^2 \approx 0.81$), while the transmural pressure proxy improves to $R^2 \approx 0.87$. The $P_\text{LV}$ proxy overestimates septal work in PAH because it does not account for the opposing pressure on the RV side of the septum, which the elevated RV pressure provides. The net mechanical load on the septum is the pressure difference, not the LV pressure alone.

**This is the thesis's key result.** It suggests that clinical work estimation using echocardiographic pressure-strain loops should use transmural pressure (which can be estimated from combined echocardiographic and Doppler measurements) rather than LV pressure when assessing septal mechanics in the context of RV pressure overload.

#### The Energy Ratio

Across all three cases, a consistent ratio of approximately 0.32 is observed between the integrated internal work and the external PV-loop work. That is, the tensor stress-strain integral returns about one-third of what the $\oint P \, dV$ calculation gives. This discrepancy is not yet fully resolved and should be discussed honestly. Possible contributions include: the absorption of energy by the Robin boundary springs (though this was tested and found to be small), numerical errors in the work calculation related to how the stress and strain tensors are projected between function spaces, and the genuine physical interpretation of work in a constrained mechanical system.

---

### Chapter 6 — Discussion

The discussion should interpret the main result in clinical context, address the limitations honestly, and suggest future directions.

**On the clinical implication:** The finding that transmural pressure outperforms LV pressure as a proxy for septal work in PAH has a potential clinical application. Myocardial work imaging — using speckle-tracking echocardiography to estimate strain and combining this with noninvasive pressure estimates — is increasingly used in clinical cardiology. Current implementations typically use LV pressure even for septal segments. If RV pressure can be estimated (e.g., from tricuspid regurgitation jet velocity), the transmural correction described here could improve accuracy in patients with RV pressure overload.

**On the energy paradox:** Address the W_int ≈ 0.32 × W_ext finding directly. Explain what is known and what remains uncertain. This is not a weakness — it is honest science. Computational studies of cardiac mechanics regularly encounter this kind of discrepancy when comparing different work measures, and the literature contains several papers grappling with the same issue.

**On limitations:** The geometry is idealized (truncated ellipsoid), which means that the realistic curvatures and thicknesses of the real septum are not captured. The active contraction model is simplified — the Blanco model does not reproduce the full calcium dynamics of individual sarcomeres. The boundary conditions (Robin springs on the epicardium) impose an artificial stiffness that may influence the results. Only one PAH patient is considered.

---

### Chapter 7 — Conclusion

The conclusion should be brief. It restates the main finding in concrete terms, describes what the computational approach contributed that could not have been done with clinical data alone, and identifies the most important open questions.

---

## Current State of Each File (Updated After Writing Session, March 2026)

- `intro.md`: **WRITTEN.** Full ~1400-word introduction. Builds from RV's clinical neglect → PAH → PV loops → septal ambiguity → the study → main result → structure.
- `01_the_question/The Scientific Question.md`: **WRITTEN.** Admonition boxes removed. Mechanistic argument expanded. $W_\text{int}$ and $W_\text{PS}$ both defined. Precise statement of hypothesis at end.
- `02_the_model/overview.md`: **WRITTEN.** Flows as prose, describes why both 3D and 0D are needed and how they're coupled.
- `02_the_model/geometry.ipynb`: **UNTOUCHED.** Reference notebook. Key content should eventually be extracted to a `.md` geometry section.
- `02_the_model/fibers.md`: **WRITTEN.** Prose-first description of LDRB, double-helix architecture, LV vs RV fiber angles, the three function spaces.
- `02_the_model/3D_mechanics.md`: **WRITTEN.** Full kinematics → HO model → weak form → BCs. Compressible formulation choice explained. Bold definition-list style removed.
- `02_the_model/active_contraction.md`: **WRITTEN** (file renamed from typo `active_contaction.md`). Active stress decomposition, Blanco activation model, spatially varying peak tension per zone.
- `02_the_model/0D_circulation.md`: **WRITTEN.** Table removed. Prose description of Regazzoni model, Windkessel, volume ratio coupling, callback structure.
- `03_implementation/implementation.md`: **WRITTEN.** New file. Covers prestressing, the deviatoric stress bug, DG1 projection error, heart rate calibration.
- `myst.yml`: **FIXED.** Removed deleted `meeting.md`, fixed `active_contraction.md` name, fixed bib reference to `refrences.bib`, added `03_implementation/implementation.md`.

## What Still Needs to Be Created

- `04_tuning/tuning.md` — Chapter on 0D model optimization (Nelder-Mead → differential evolution → Bayesian / Optuna). See content description in chapter plan above.
- `05_results/results.md` — Results chapter: hemodynamics validation, work decomposition, proxy comparison healthy vs PAH.
- `06_discussion/discussion.md` — Discussion: clinical implication of transmural pressure result, energy ratio, limitations.
- A brief conclusion section (can live in the discussion file or standalone).
- Figures copied from `_build/` into a `figures/` directory and referenced in the text.
- Geometry section extracted from `02_the_model/geometry.ipynb` into a proper `.md` file.

The `myst.yml` ToC needs entries for chapters 04–06 as they are created.

---

## Key References — Status

The bib file (`refrences.bib`) has been substantially expanded. Current entries:

**Added:**
- `finsberg2019assessment` — Finsberg et al. paper (direct predecessor, LV-only FEM work)
- `balaban2017high` — Balaban et al. 2017 (data assimilation framework)
- `holzapfel2009constitutive` — Holzapfel & Ogden 2009 (full entry now present)
- `holzapfel2000nonlinear` — Holzapfel textbook
- `bayer2012novel` — Bayer et al. 2012 (LDRB algorithm)
- `streeter1969fiber` — Streeter et al. 1969 (fiber orientation experimental basis)
- `bols2013computational` — Bols et al. 2013 (backward displacement prestressing)
- `gee2010computational` — Gee et al. 2010 (alternate prestressing method)
- `russell2012novel` — Russell et al. 2012 (non-invasive myocardial work, pressure-strain loops)
- `delhaas1994regional` — Delhaas et al. 1994 (fiber stress-strain and O2 demand)
- `suga1979total` — Suga 1979 (PV area and O2 consumption)
- `galie2015esc` — Galié et al. 2015 (ESC/ERS PAH guidelines)
- `vonk2013right` — Vonk-Noordegraaf et al. 2013 (RV adaptation in PAH)
- `logg2012automated` — FEniCS book

**Still needed:**
- Regazzoni 2020: the actual paper behind the 0D circulation model. The `circulation` software
  citation exists but the underlying paper needs to be identified and added. Search the
  `circulation` library GitHub README for the reference.
- Blanco ventricular activation model: find the exact paper for the activation waveform.
- Optuna paper (Akiba et al., 2019) if Bayesian optimization chapter goes into detail.

**Broken cite keys fixed:**
- `{cite}main_pdf` in 3D_mechanics.md → replaced with `{cite}holzapfel2000nonlinear`
- `{cite}holzapfel2009constitutive` was in text but not in bib → now in bib

---

## Technical Notes for Writing Code Blocks and Equations

The MyST Markdown format supports LaTeX math via `$$` blocks and inline `$`. Use this consistently. Do not use code blocks to display equations.

When referring to code for context, a brief code snippet is acceptable in the implementation chapter, but keep them short and always surround them with explanatory prose. The thesis is not a software manual.

For figures, the `_build/` directory contains many generated plots from simulation runs. Key figures to include:
- `biv_fibers_*.png` — fiber orientation visualization
- `pv_loop_last_beat_*.png` — PV loops for both ventricles
- `pressure_strain_loop_*.png` — pressure-strain proxy loops
- `stress_strain_loops_*.png` — stress-strain loops
- `energy_analysis_dual_*.png` — work decomposition
- `work_comparison_bars_*.png` — proxy comparison bar charts

These need to be copied from `_build/` into an appropriate `figures/` directory and referenced using MyST figure syntax.

---

## How to Continue Writing

When picking up this project, start by reading this file, then read the existing chapter files to understand what tone has been established. Before writing a new chapter, read the relevant sections of `complete_cycle.py`, `metrics_calculator.py`, and any other code files that the chapter describes. The comments in the code are a valuable source of technical detail.

Write in long paragraphs first, then go back and add the equations. It is easier to identify where an equation belongs once the prose argument is complete. The math should feel like a consequence of the text, not a replacement for it.

If you are unsure about a technical detail, note it with a `<!-- TODO: verify -->` comment and move on. Do not invent numbers or equations. Everything numerical should come from the code or the literature.

The thesis is being built in MyST Markdown and rendered with Jupyter Book. Test the build periodically using `jupyter-book build .` from the RV directory to catch broken cross-references and missing figures early.
