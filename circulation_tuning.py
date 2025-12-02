import numpy as np
import pandas as pd
import logging
import itertools
from tqdm import tqdm
from circulation.regazzoni2020 import Regazzoni2020
from circulation.units import ureg

# ==============================================================================
# 1. THE EXPERIMENTAL SPACE (4-D Search)
# ==============================================================================
search_space = {
    # Lung Resistance (Controls PA Pressure)
    # Theory: Needs to be low (~0.03-0.05) to avoid Pulmonary Hypertension.
    "R_PUL": [0.03, 0.04, 0.05, 0.06], 
    
    # Systemic Resistance (Controls BP)
    # Theory: Needs to be ~1.0, but we test wide to be sure.
    "R_SYS": [0.8, 0.9, 1.0, 1.1, 1.2, 1.3],
    
    # Contractility (Controls Stroke Volume / Pulse Pressure)
    # Default is 2.75. We test weaker hearts to prevent "Athlete" output.
    "LV_EA": [1.5, 1.8, 2.0, 2.2, 2.5, 2.75],
    
    # Initial CVP (Controls Total Blood Volume)
    # This is the knob we just fixed. We test a huge range to find the "sweet spot"
    # for filling the heart without overfilling it.
    "INIT_CVP": [5.0, 8.0, 10.0, 12.0, 15.0, 20.0]
}

# Clinical Targets (Healthy Adult)
TARGETS = {
    "BP_SYS": 120, "BP_DIA": 80, 
    "CO": 5.0,     # L/min
    "PA_MEAN": 15, # mmHg
    "LA_MEAN": 8   # mmHg (Wedge pressure)
}

# ==============================================================================
# 2. METRICS
# ==============================================================================
def get_metrics(model, history, hr_bpm=75):
    tail = 200
    
    sys_p_max = np.max(history["p_AR_SYS"][-tail:])
    sys_p_min = np.min(history["p_AR_SYS"][-tail:])
    lv_sv = np.max(history["V_LV"][-tail:]) - np.min(history["V_LV"][-tail:])
    lv_ef = (lv_sv / np.max(history["V_LV"][-tail:])) * 100
    pa_mean = np.mean(history["p_AR_PUL"][-tail:])
    la_mean = np.mean(history["p_LA"][-tail:])
    rv_max = np.max(history["p_RV"][-tail:])
    
    co = (hr_bpm * lv_sv) / 1000 
    
    # Volume Check (Sanity)
    final_vols = model.compute_volumes(model.parameters, model.state)
    total_vol = final_vols["Total"].magnitude if hasattr(final_vols["Total"], 'magnitude') else final_vols["Total"]

    return {
        "BP_Sys": int(sys_p_max),
        "BP_Dia": int(sys_p_min),
        "BP": f"{int(sys_p_max)}/{int(sys_p_min)}",
        "CO": round(co, 2),
        "PA": round(pa_mean, 1),
        "LA": round(la_mean, 1),
        "RV_Max": round(rv_max, 1),
        "EF": round(lv_ef, 1),
        "Vol": int(total_vol)
    }

# ==============================================================================
# 3. RUNNER
# ==============================================================================
def run_experiment(r_p, r_s, ea, cvp):
    logging.basicConfig(level=logging.ERROR)
    
    params = Regazzoni2020.default_parameters()
    init = Regazzoni2020.default_initial_conditions()
    
    # --- CONSTANTS (Structural) ---
    params["circulation"]["SYS"]["C_VEN"] = 60.0 * ureg("mL/mmHg") # Regazzoni Table 3
    params["HR"] = 1.25 * ureg("Hz") # 75 BPM
    
    # Timings (Regazzoni Table 3)
    params["chambers"]["LV"]["TC"] = 0.34 * ureg("s"); params["chambers"]["LV"]["TR"] = 0.17 * ureg("s")
    params["chambers"]["RV"]["TC"] = 0.272 * ureg("s"); params["chambers"]["RV"]["TR"] = 0.12 * ureg("s")
    params["chambers"]["LA"]["tC"] = 0.60 * ureg("s"); params["chambers"]["LA"]["TC"] = 0.104 * ureg("s")
    params["chambers"]["RA"]["tC"] = 0.56 * ureg("s"); params["chambers"]["RA"]["TC"] = 0.064 * ureg("s")

    # --- VARIABLES ---
    params["circulation"]["PUL"]["R_AR"] = r_p * ureg("mmHg * s / mL")
    params["circulation"]["PUL"]["R_VEN"] = r_p * ureg("mmHg * s / mL")
    params["circulation"]["SYS"]["R_AR"] = r_s * ureg("mmHg * s / mL")
    params["chambers"]["LV"]["EA"] = ea * ureg("mmHg / mL")
    
    # --- INITIALIZATION ---
    # We set these to guide the solver, but 'p_VEN_SYS' is the main volume knob
    init["p_VEN_SYS"] = cvp * ureg("mmHg") 
    init["p_AR_SYS"] = 90.0 * ureg("mmHg") 
    init["p_AR_PUL"] = 15.0 * ureg("mmHg")
    init["p_VEN_PUL"] = 8.0 * ureg("mmHg")

    # Initialize
    model = Regazzoni2020(parameters=params)
    
    # Run with FIX (Passing init to solve)
    # We use fewer beats (8) to speed up the massive search. 
    # Steady state is usually close enough by then for ranking.
    hist = model.solve(num_beats=8, initial_state=init) 
    
    return get_metrics(model, hist)

# ==============================================================================
# 4. EXECUTION
# ==============================================================================
if __name__ == "__main__":
    grid = list(itertools.product(
        search_space["R_PUL"], 
        search_space["R_SYS"], 
        search_space["LV_EA"],
        search_space["INIT_CVP"]
    ))
    
    print(f"Starting Massive Grid Search ({len(grid)} simulations)...")
    results = []
    
    for r_p, r_s, ea, cvp in tqdm(grid):
        try:
            m = run_experiment(r_p, r_s, ea, cvp)
            
            # --- SCORING ALGORITHM ---
            # 1. BP Deviation (Target 120/80)
            err_sys = abs(m["BP_Sys"] - TARGETS["BP_SYS"])
            err_dia = abs(m["BP_Dia"] - TARGETS["BP_DIA"])
            
            # 2. CO Deviation (Target 5.0) - Heavily Weighted
            # We want to punish "Athlete" (7.0) and "Failure" (3.0) equally
            err_co  = abs(m["CO"] - TARGETS["CO"]) * 20 
            
            # 3. PA Pressure (Target 15)
            err_pa = abs(m["PA"] - TARGETS["PA_MEAN"]) * 2
            
            # 4. LA Pressure (Target 8) - Prevent Congestion
            err_la = abs(m["LA"] - TARGETS["LA_MEAN"]) * 2

            score = err_sys + err_dia + err_co + err_pa + err_la
            
            results.append({
                "R_PUL": r_p, "R_SYS": r_s, "EA": ea, "CVP": cvp,
                "BP": m["BP"], "CO": m["CO"], "PA": m["PA"], "LA": m["LA"],
                "RV": m["RV_Max"], "Vol": m["Vol"],
                "Score": round(score, 1)
            })
        except Exception:
            pass # Skip crashes

    # Sort & Display
    if results:
        df = pd.DataFrame(results).sort_values(by="Score")
        print("\n--- TOP 20 HEALTHY CANDIDATES ---")
        print(df.head(20).to_string(index=False))
        
        # Save to CSV for offline analysis
        df.to_csv("grid_search_results.csv", index=False)
        print("\nFull results saved to 'grid_search_results.csv'")
    else:
        print("CRITICAL FAIL: No simulations succeeded.")