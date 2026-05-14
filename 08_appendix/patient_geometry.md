(chap-appendix-patient-geometry)=
# Exploratory Patient Geometry

The fixed-anatomy production sweep deliberately holds geometry constant to isolate the pressure-assignment question. A separate exploratory comparison on patient-specific healthy and PAH meshes provides a direction check that the fixed-anatomy result cannot do on its own. The PAH mesh is not merely the healthy mesh under a different pressure load: RV EDV is 74.2 mL rather than 94.4 mL, while total wall volume is 165.7 mL rather than 129.1 mL.

The updated check uses the same capped inverse-unloading convention as the production sweep and fixed reference tags within each patient geometry. The healthy and PAH meshes cannot share a cell-by-cell reference tag set because their anatomy is different, so the table is still not a controlled case-by-case validation. Its value is directional: it asks whether a remodelled, thicker PAH geometry changes the relation between pressure-strain proxy values and finite-element stress-strain work density.

```{table} Exploratory cap=5 healthy/PAH geometry comparisons. Work densities are reported as healthy/PAH pairs. Finite-element values use stress-strain work density. Proxy values use tangent-longitudinal pressure-strain density; the RV proxy uses adjacent RV pressure, and the septal proxy uses mean LV/RV pressure.
:name: tab-app-patient-geometry-direction
:align: left

| Case | RVSP (mmHg) | RV FE (kPa) | RV proxy (kPa) | Septum FE (kPa) | Septum proxy (kPa) |
|---|---:|---:|---:|---:|---:|
| sPAP22 | 32.1 / 33.4 | 3.81 / 1.74 | 0.28 / 0.25 | 5.83 / 3.08 | 0.31 / 0.15 |
| sPAP65 | 65.7 / 78.5 | 5.60 / 4.93 | 0.56 / 0.68 | 5.73 / 4.41 | 0.44 / 0.32 |
| sPAP95 | 89.2 / 113.0 | 4.29 / 6.61 | 0.53 / 0.99 | 5.50 / 4.98 | 0.45 / 0.41 |
```

The table should be read pairwise, not as a new correlation analysis. With only three nominal pressure levels, and with achieved pressures differing between the two geometries, a Pearson correlation would mostly describe the selected cases and would have a very wide uncertainty. The useful signal is simpler: the raw magnitudes, and whether the finite-element work density and the pressure-strain proxy move in the same direction when the geometry is changed.

These runs are deliberately not promoted to main results. The comparison changes anatomy, loading, cavity-volume scaling, and the inferred reference state together, and the two geometries cannot be brought onto one common cellwise atlas in the way the fixed-geometry production sweep can. Their purpose is narrower: they are a warning about extrapolating fixed-geometry magnitudes, not an independent validation of the production sweep. They show that the fixed UKB pressure sweep should not be read as a patient-specific PAH remodelling model.

The septal direction is consistent across the three selected levels: the PAH geometry gives lower septal stress-strain work density than the healthy geometry despite similar or higher RV systolic pressure. The RV free wall is less one-directional: PAH is lower at low and mid pressure, but the severe PAH case exceeds the healthy case because the achieved RV systolic pressure is much higher. The pressure-strain proxy does not attenuate in the same way as the finite-element work density; it continues to follow pressure and longitudinal shortening more directly. Together with the capped-unloading production sweep in {ref}`chap-appendix-reference-state`, this means the severe fixed-geometry RV and RV-side septal magnitudes are best read as reference-state and geometry sensitive, not as corrected PAH tissue-work estimates. The geometry-dependent relationship between the clinical pressure-strain proxy and finite-element stress-strain work density is a high-priority future-work question.
