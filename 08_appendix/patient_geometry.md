(chap-appendix-patient-geometry)=
# Exploratory Patient Geometry

The fixed-anatomy production sweep deliberately holds geometry constant to isolate the pressure-assignment question. A separate exploratory comparison on a patient-specific PAH mesh provides a direction check that the fixed-anatomy result cannot do on its own. The PAH mesh is not merely the healthy mesh under a different pressure load: RV EDV is 74.2 mL rather than 94.4 mL, while total wall volume is 165.7 mL rather than 129.1 mL. These same-label PAH/healthy comparisons used the older per-case canonical tagging rather than the reference-tag protocol of the production sweep, so they are not numerically comparable case-by-case; their value is as an independent direction signal.

In the selected comparisons, the thicker PAH geometry tended to carry lower RV and septal stress-strain work density than the healthy geometry at similar or even higher RV systolic pressure. The pressure-strain proxy did not always attenuate with the stress-strain work density, especially in the RV free wall.

```{table} Exploratory same-label healthy/PAH geometry comparisons. Work densities are reported as healthy/PAH pairs. Finite-element values use stress-strain work density. Proxy values use tangent-longitudinal pressure-strain density; the RV proxy uses adjacent RV pressure, and the septal proxy uses mean LV/RV pressure.
:name: tab-app-patient-geometry-direction
:align: left

| Case | RVSP (mmHg) | RV FE (kPa) | RV proxy (kPa) | Septum FE (kPa) | Septum proxy (kPa) |
|---|---:|---:|---:|---:|---:|
| sPAP22 | 31.7 / 31.7 | 3.69 / 1.51 | 0.35 / 0.30 | 6.54 / 2.90 | 0.71 / 0.46 |
| sPAP30 | 40.5 / 34.9 | 5.05 / 1.78 | 0.48 / 0.34 | 7.01 / 3.00 | 0.83 / 0.52 |
| sPAP45 | 41.7 / 49.8 | 4.90 / 3.02 | 0.46 / 0.56 | 6.55 / 3.72 | 0.78 / 0.72 |
| sPAP55 | 57.6 / 57.8 | 5.77 / 3.19 | 0.55 / 0.63 | 5.20 / 3.48 | 0.75 / 0.66 |
| sPAP65 | 61.5 / 72.8 | 4.75 / 4.08 | 0.54 / 0.79 | 5.08 / 3.73 | 0.74 / 0.74 |
```

These runs are deliberately not promoted to main results. The healthy high-pressure sequence did not fully complete, the selected cases used end-diastolic region tagging, and the comparison changes anatomy, loading, and numerical robustness together. Their purpose is to show that the fixed UKB pressure sweep should not be read as a patient-specific PAH remodelling model.

In a thicker, remodelled geometry, RV and septal stress-strain work density can be lower at comparable RV pressure while the pressure-strain proxy may attenuate less or even increase, because the proxy does not explicitly include wall volume, curvature, passive remodelling, or reference-state changes. Together with the capped-unloading production sweep in {ref}`chap-appendix-reference-state`, this means the severe fixed-geometry RV and RV-side septal magnitudes are best read as reference-state and geometry sensitive, not as corrected PAH tissue-work estimates. The geometry-dependent relationship between the clinical pressure-strain proxy and finite-element stress-strain work density is a high-priority future-work question.
