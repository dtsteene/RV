# Source Reading Notes

Working notes for sources that have local PDFs and have been checked for the claims used in the thesis. This file is not thesis text.

## Regional Work / Pressure-Strain Origin

### `forrester1974pressure_length`

Local PDF: `/home/dtsteene/citations/01_work_loop_foundations/forrester1974_pressure_length_loops.pdf`

Forrester et al. introduce the pressure-length loop as a way to compare segmental and whole-heart function. This supports the thesis claim that the regional-loop idea predates Russell and was originally a pressure-for-force/stress approximation, not an exact local mechanics identity.

### `tyberg1974segmental`

Local PDF: `/home/dtsteene/citations/01_work_loop_foundations/tyberg1974_segmental_work_pressure_length.pdf`

Tyberg et al. use pressure-length loops in an ischemia experiment. The useful thesis point is the loop-orientation/work interpretation: ischemic segments can move from positive loop area toward zero or negative area, meaning that the segment is no longer contributing active work in the same way.

### `urheim2005regional`

Local PDF: `/home/dtsteene/citations/01_work_loop_foundations/urheim2005_regional_myocardial_work_pressure_strain.pdf`

Urheim et al. combine LV pressure with strain Doppler to define regional myocardial work as pressure-strain loop area. They compare strain Doppler with sonomicrometry and report a good correlation for regional work index. They also state the core limitation clearly: regional wall stress would require transmural pressure, wall thickness, and local curvature, so LV pressure is a substitute for stress rather than the stress itself.

### `russell2012novel`

Local PDF: `/home/dtsteene/citations/02_pressure_strain_clinical/russell2012_noninvasive_pressure_strain_work.pdf`

Russell et al. make the pressure-strain method clinically usable by estimating LV pressure non-invasively from valve timing and cuff pressure. Their validation has two parts: comparison against invasive pressure/sonomicrometry in dogs and comparison against invasive pressure in patients; they also compare regional loop area with FDG-PET glucose metabolism in a small patient subset. The glucose result supports pressure-strain area as a marker of regional metabolic demand, but it does not remove the pressure-for-stress approximation.

### `voigt2015definitions`

Local PDF: `/home/dtsteene/citations/02_pressure_strain_clinical/voigt2015_2d_speckle_tracking_definitions_consensus.pdf`

Voigt et al. define the standard 2D speckle-tracking strain components as longitudinal, circumferential, and radial components relative to the cardiac image contour, not as myocardial fibre strain. The document recommends that global strain be calculated from the full myocardial line or equivalent segmental averaging and lists longitudinal strain as an apical-view quantity. This supports the thesis wording that clinical speckle tracking gives a scalar image/anatomical strain component rather than the fibre-projected strain used in the finite-element mechanics.

### `sade2023current`

Local PDF: `/home/dtsteene/citations/02_pressure_strain_clinical/sade2023_eacvi_ste_clinical_use_survey.pdf`

Sade et al. surveyed contemporary EACVI practice. Among LV speckle-tracking users, global longitudinal strain from the three apical views was the dominant measurement, and GLS was by far the most commonly used clinical strain assessment. For RV applications, the relevant clinical quantities are also longitudinal, especially RV free-wall longitudinal strain. Use this as current-practice support for making the thesis proxy primarily longitudinal-strain based.

### `abawi2022noninvasive`

Local PDF: `/home/dtsteene/citations/02_pressure_strain_clinical/abawi2022_noninvasive_myocardial_work_review.pdf`

Abawi et al. describe the clinical myocardial-work workflow as combining LV global/segmental longitudinal strain from standard apical echocardiographic views with an estimated LV pressure curve. The strain curve is differentiated and multiplied by instantaneous pressure before integration over time. This is the cleanest review source for the statement that clinical myocardial work is a pressure-longitudinal-strain construction.

### `thomas2025clinical`

Local PDF: `/home/dtsteene/citations/02_pressure_strain_clinical/thomas2026_strain_echocardiography_consensus.pdf`

The ASE/EACVI clinical consensus endorses LV global longitudinal strain and RV free-wall longitudinal strain across several clinical settings, including pulmonary hypertension, while myocardial work is generally listed as not currently endorsed or not supported by enough evidence for routine clinical use. It also states that 3D strain is still developing and radial strain is not endorsed clinically. This is important thesis nuance: GLS/RVFWLS are established clinical strain measures, but pressure-strain myocardial work, especially RV myocardial work, remains less settled.

### `delhaas1994regional`

Local PDF: `/home/dtsteene/citations/01_work_loop_foundations/delhaas1994_regional_fibre_stress_strain_area.pdf`

Delhaas et al. estimate fibre stress and fibre strain area in canine LV experiments and compare it with regional blood flow/oxygen demand. This is useful background for why fibre stress-strain area is a more mechanical regional-work estimate than chamber pressure-strain area, but it is still an LV/canine validation setting, not a biventricular septal pressure-assignment study.

### `suga1979total`

Local PDF: `/home/dtsteene/citations/01_work_loop_foundations/suga1979_total_energy_cardiac_oxygen.pdf`

Suga is best used as whole-ventricle energetic background. Pressure-volume area relates to oxygen consumption in the ventricle model, but the thesis should not present Suga as proof that regional pressure-strain loops measure biological energy directly. The cleaner thesis reason to care about tensor work is the mechanical energy balance between boundary PV work and internal stress-strain work.

## Direct Computational Predecessor

### `finsberg2019assessment`

Local PDF: `/home/dtsteene/citations/01_work_loop_foundations/finsberg2019_assessment_regional_myocardial_work.pdf`

Finsberg et al. compare pressure-strain loops, fibre stress-strain loops, and model-resolved work in personalised LV mechanics models for one healthy case and one LBBB case. The thesis can safely use it for three points: pressure-strain loops can preserve useful relative regional information, pressure-strain work is much smaller in absolute magnitude than model-resolved stress-strain work, and septal signs/orientations can disagree in dyssynchronous mechanics. It is not a biventricular pressure-assignment study.

### `regazzoni2022cardiac`

Local final PDF: `/home/dtsteene/citations/03_computational_cardiac_mechanics/regazzoni2022_jcp_closed_loop_final.pdf`

Regazzoni et al. support the broad modelling claim that a 3D cardiac mechanics model can be coupled to a closed-loop 0D circulation through volume consistency and energy-consistent boundary conditions. Use this as the modern mathematical formulation of the coupling and energy-balance viewpoint, not as the historical origin of the general idea.

### `kerckhoffs2007coupling`

Local PDF: `/home/dtsteene/citations/03_computational_cardiac_mechanics/kerckhoffs2007_coupling_fe_lumped_circulation.pdf`

This is the best historical anchor found so far for coupling finite-element ventricular mechanics to a closed-loop lumped circulation. The key idea is simple: the FE model and circulation model each predict a ventricular cavity volume, and the ventricular pressures are iterated until those volumes agree. Use it when explaining where the 3D-0D volume-consistency idea comes from. Do not present Regazzoni as inventing the general coupling idea.

### `piersanti2022closed`

Local final PDF: `/home/dtsteene/citations/03_computational_cardiac_mechanics/piersanti2022_cma_biventricular_3d0d_final.pdf`

This is a Regazzoni/Quarteroni-line biventricular extension of the 3D-0D closed-loop electromechanics framework. It explicitly couples a 3D biventricular electromechanics model to a 0D closed-loop circulation using volume conservation constraints, with LV and RV pressures acting as Lagrange multipliers. Use it to support the statement that this type of coupling has been applied to biventricular models, not just LV models.

### `finsberg2019computational`

Local HTML: `/home/dtsteene/citations/03_computational_cardiac_mechanics/finsberg2019computational_pmc.html`

This paper supports the claim that patient-specific biventricular finite-element models have been used in pulmonary hypertension. It estimates patient-specific ventricular mechanics in control and PAH groups and reports changes in RV wall thickness, volumes, strain, passive stiffness, and regional fibre stress. Use it to avoid overstating novelty: this thesis is not the first biventricular PAH mechanics model; its narrower contribution is testing pressure-strain proxy choices against model-resolved tensor work in a biventricular setting.

### `finsberg2018efficient`

Local HTML: `/home/dtsteene/citations/03_computational_cardiac_mechanics/finsberg2018efficient_pmc.html`

This paper supports the claim that personalised biventricular mechanics models have been used to estimate mechanical function and myofiber stress. Use it together with `finsberg2019computational` when writing the novelty statement: the gap is not "no biventricular FEM exists", but "pressure-strain proxy validation and septal pressure assignment have not been tested in this biventricular way."

## Broader FEM Regional-Work Literature

### `wang2012myocardial`

Local HTML: `/home/dtsteene/citations/03_computational_cardiac_mechanics/wang2012_myocardial_contractility_regional_work_springer.html`

Wang et al. used LV finite-element models with in-vivo MRI tagging and LV pressure recordings to estimate active fibre stress in five canine hearts. The abstract explicitly says that regional distributions of fibre stretch, stress, and myocardial work were examined. Use this as evidence that FEM regional work predates and is broader than the Finsberg pressure-strain comparison.

### `namani2020effects`

Local HTML: `/home/dtsteene/citations/03_computational_cardiac_mechanics/namani2020_regional_coronary_perfusion.html`

Namani et al. coupled an LV finite-element mechanics model, systemic circulation, and coronary microcirculation. They define regional myocardial work as area under the myofiber stress-strain curve and use it as a regional demand measure when comparing with coronary perfusion. Useful for showing that stress-strain regional work is a modelling quantity used outside the pressure-strain validation literature.

### `pluijmert2017determinants`

Local HTML: `/home/dtsteene/citations/03_computational_cardiac_mechanics/pluijmert2017_determinants_biventricular.html`

Pluijmert et al. used a biventricular finite-element mechanics model to test sensitivity to geometry and myofiber orientation. They report changes in both local myofiber work and global pump work, including a roughly 18% increase in local myofiber work after adaptive myofiber reorientation. Useful for avoiding the false claim that only LV geometry has been studied.

### `ahmadbakir2018multiphysics`

Local HTML: `/home/dtsteene/citations/03_computational_cardiac_mechanics/ahmad_bakir2018_multiphysics_biventricular_lvad.html`

Ahmad Bakir et al. developed an idealized biventricular electromechanics/fluid model and extracted 2nd Piola-Kirchhoff stress and Green-Lagrange strain components from the LV free wall, septum, and RV free wall. They generated stress-strain loops to assess regional work. This is directly useful for the intro nuance: biventricular stress-strain regional work has been examined, but not as the same septal pressure-assignment test.

### `craine2024successful`

Local HTML: `/home/dtsteene/citations/03_computational_cardiac_mechanics/successful_crt_negative_septal_work_2024.html`

Craine et al. used patient-specific models of dyssynchronous heart failure and CRT to compute regional myocardial work from stress-strain loops, including negative septal work. They also tested simplified work estimates using ventricular pressure as a stress surrogate and Laplace-style wall stress estimates. This is a very relevant modern source for saying pressure-based simplifications are actively studied, while keeping the thesis claim narrower than "we are first to look at regional work."

### `bayer2012novel`

Local HTML: `/home/dtsteene/citations/05_coordinates_geometry/bayer2012novel_pmc.html`

This is the source for the Laplace-Dirichlet rule-based fibre assignment idea. It supports the fibre chapter's claim that the local cardiac coordinate system and fibre field can be built from Laplace problems with anatomical boundary conditions.

### `bols2013computational`

Local accepted-manuscript PDF: `/home/dtsteene/citations/03_computational_cardiac_mechanics/bols2013computational_accepted.pdf`

This supports the backward displacement / prestress description. The relevant idea is that an in-vivo image geometry is already loaded, so treating it as stress-free gives wrong stress and deformation; the backward displacement method iteratively updates an unloaded reference geometry by solving forward loaded problems.

### `blanco2010computational`

Local PDF: `/home/dtsteene/citations/03_computational_cardiac_mechanics/blanco2010computational.pdf`

This is useful background for coupled 3D-1D-0D cardiovascular modelling and the general closed-loop-circulation idea. In this thesis it is mainly used for the activation/circulation model context, not as direct evidence for the pressure-strain proxy result.

### `akiba2019optuna`

Local arXiv PDF: `/home/dtsteene/citations/03_computational_cardiac_mechanics/akiba2019optuna_arxiv.pdf`

This supports the description of Optuna as a hyperparameter-optimization framework with define-by-run search spaces and sampling/pruning machinery. The thesis only needs it for the software/method citation.

### `hansen2001completely`

Local PDF: `/home/dtsteene/citations/03_computational_cardiac_mechanics/hansen2001cmaes.pdf`

This supports the description of CMA-ES as an evolution strategy that adapts a covariance matrix / mutation distribution from successful search steps. The thesis should not over-explain CMA-ES beyond what is needed to justify why it worked better than coordinate-wise sampling here.

### `baratta2023dolfinx`

Local PDF: `/home/dtsteene/citations/03_computational_cardiac_mechanics/baratta2023dolfinx.pdf`

This supports the FEniCSx/DOLFINx software description: DOLFINx is the next-generation FEniCS problem-solving environment and provides the finite-element infrastructure used by fenicsx-pulse.

### `holzapfel2009constitutive`

Local PDF: `/home/dtsteene/citations/03_computational_cardiac_mechanics/holzapfel2009constitutive.pdf`

Holzapfel and Ogden review passive myocardium as an orthotropic material with locally identifiable fibre, sheet, and sheet-normal directions. The paper develops a structurally based constitutive framework that accounts for the muscle fibre direction and myocyte sheet structure. This supports the thesis use of the Holzapfel-Ogden law as the passive constitutive model, but it should not be used to claim that the chosen parameters are patient-specific.

### `klotz2006single`

Local PDF: `/home/dtsteene/citations/04_pulmonary_hypertension/klotz2006single.pdf`

Klotz et al. show that normalized end-diastolic pressure-volume relationships from different hearts have a similar underlying shape and propose estimating a whole EDPVR from one measured end-diastolic pressure-volume point. This supports the calibration chapter's use of a Klotz-style nonlinear EDPVR to decouple end-diastolic pressure and volume. In this thesis it is used as a practical pressure-volume curve shape, not as a patient-specific stiffness measurement.

## PAH / Calibration Sources Already Local

### `humbert2022esc`

Local PDF: `/home/dtsteene/citations/04_pulmonary_hypertension/humbert2022_esc_ers_ph_guidelines.pdf`

Use for PH/PAH definitions, risk table guardrails, and the point that the thesis pressure sweep should not be advertised as a published severity ladder.

### `kovacs2009pulmonary`

Local PDF: `/home/dtsteene/citations/04_pulmonary_hypertension/kovacs2009_pulmonary_pressure_ranges.pdf`

Use for normal pulmonary pressure values at rest and exercise. Good source for low-pressure anchors.

### `tello2019tapse`

Local PDF: `/home/dtsteene/citations/04_pulmonary_hypertension/tello2019_tapse_pasp_ph.pdf`

Use for severe PH hemodynamic values and RV-arterial coupling context.

### `baggen2016cmr`

Local PDF: `/home/dtsteene/citations/04_pulmonary_hypertension/baggen2016_cmr_pah_mortality_review.pdf`

Use for CMR prognostic/remodelling context in PAH, especially when discussing what changes in real patients beyond pressure alone.

### `benza2010reveal`

Local PDF: `/home/dtsteene/citations/04_pulmonary_hypertension/benza2010_reveal_predicting_survival_pah.pdf`

Use for REVEAL registry prognosis framing and for avoiding a simplistic pressure-only PAH severity ladder.

## Geometry / Current RV Pressure-Strain Literature

### `mauger2019right`

Local PDF: `/home/dtsteene/citations/05_coordinates_geometry/mauger2019right.pdf`

Mauger et al. constructed a biventricular shape atlas from 4,329 UK Biobank CMR studies, using a subdivision surface mesh fitted by diffeomorphic registration. They defined a healthy reference sub-cohort of 630 participants. This supports the thesis statement that the synthetic baseline geometry is derived from a UK Biobank biventricular statistical shape model.

### `wang2022apply`

Local PDF: `/home/dtsteene/citations/02_pressure_strain_clinical/wang2022apply.pdf`

Wang et al. apply non-invasive pressure-strain loop myocardial work analysis to pulmonary hypertension, including RV work indices. This supports the modest claim that recent clinical studies have begun using pressure-strain loops for RV work in PH. It should not be used as a tensor-work validation source.

### `lakatos2024right`

Local PDF: `/home/dtsteene/citations/02_pressure_strain_clinical/lakatos2024_rv_pressure_strain_work_validation.pdf`

Lakatos et al. validate an RV pressure-strain myocardial-work index against invasive pressure-volume analysis. The deformation input is global longitudinal strain, and the method builds RV pressure-strain loops from RV pressure and differentiated strain curves. This is useful because it shows that the current RV extension of myocardial work is still longitudinal-strain based, not fibre-strain based, and that RV myocardial work is being evaluated as a contractility-related clinical index.
