# Conclusion and Future Work

## Conclusion

Pressure-strain work is most reliable in the setting it implicitly assumes: a myocardial wall loaded mainly by one adjacent cavity. In the simulations presented here, the LV and RV free-wall work-density ratio was captured reasonably well by the adjacent-pressure longitudinal proxy, making the RV free wall a meaningful part of the study rather than only a control case. The septum was different. It behaved as shared tissue between two pressure-loaded cavities, and septal work-density magnitudes were better preserved by two-sided pressure choices than by transmural pressure alone.

The pressure sweep adds an important caution. Proxy rankings based on correlation across a loading path can flip when the loading path changes. The old and corrected simulations demonstrated this directly. The safest conclusion is therefore not a universal pressure prescription for the septum, but a mechanical reading: free walls are closest to the adjacent-pressure assumption; septal tissue behaves as a two-sided wall; and any single-pressure septal proxy should be interpreted with care.

The study should also be read for what it is. It is not a clinical PAH cohort and it does not claim to reproduce disease progression. It is a controlled mechanics test of a common pressure-for-stress simplification. That controlled setting is useful: if the proxy behaves well in the free walls but becomes pressure-choice dependent in the septum even when the model is known exactly, then the septal ambiguity is not just an imaging problem. It is already present in the mechanics.

## Future Work

The most immediate extension is to run the same free-wall and septal ratio analysis on the patient-specific meshes. This would test whether the free-wall result survives changes in wall thickness and chamber size, and whether RV hypertrophy moves the proxy error in the direction predicted by Laplace-type reasoning. A useful design would separate geometry and loading as much as possible: healthy geometry with healthy and high-RV-pressure circulations, PAH or thickened geometry with the same two circulations, and possibly an artificially thickened RV wall to isolate wall thickness from all other patient-specific differences.

A second extension is a higher-resolution septal study. The septum could be treated as an engineering object in its own right: a curved wall with two pressure boundaries, active fibres, and mechanical constraints from both ventricles. With enough through-wall resolution, one could test whether the best local pressure scale truly moves from LV pressure on the LV side toward RV pressure on the RV side, and whether mean pressure is only a coarse average of that local behaviour.

A third extension is clinical validation. The model suggests that free-wall pressure-strain work indices are relatively robust, while septal indices are pressure-choice dependent in RV pressure overload. Testing this clinically would require CMR geometry, reliable RV pressure estimates, and pressure-strain work from echocardiography or feature tracking in the same patients. Without measured hemodynamics, assigning patient-specific circulation parameters from anatomy alone would introduce a new source of uncertainty.
