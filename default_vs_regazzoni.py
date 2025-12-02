import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging
from circulation.regazzoni2020 import Regazzoni2020
from circulation.units import ureg

dt = 1e-3  # Time step for simulations
num_beats = 20 # two times that of the paper should be way more than ennough really


def get_metrics(history, label, hr_bpm):
    """
    Extracts clinical metrics from the tail of the simulation.
    Args:
        hr_bpm: MUST match the simulation HR (60 for Default, 75 for Paper).
    """
    tail_len = 1000 
    
    def get_tail(key):
        return history[key][-tail_len:]

    # Left Heart
    v_lv = get_tail("V_LV")
    lv_v_max = np.max(v_lv)
    lv_v_min = np.min(v_lv)
    lv_sv = lv_v_max - lv_v_min
    lv_ef = (lv_sv / lv_v_max) * 100
    
    # Right Heart and Pulmonary Circulation
    rv_p_max = np.max(get_tail("p_RV"))
    pa_mean = np.mean(get_tail("p_AR_PUL"))
    
    # Systemic BP
    p_ar_sys = get_tail("p_AR_SYS")
    sys_p_max = np.max(p_ar_sys)
    sys_p_min = np.min(p_ar_sys)
    
    # Cardiac Output (SV * HR)
    co = (hr_bpm * lv_sv) / 1000 # L/min
    
    # Pressures (Congestion check)
    p_LA_mean = np.mean(get_tail("p_LA"))
    p_VEN_PUL_mean = np.mean(get_tail("p_VEN_PUL"))

    return {
        "Scenario": label,
        "LV SV (mL)": round(lv_sv, 1),  
        "LV EF (%)": round(lv_ef, 1),
        "BP (mmHg)": f"{int(sys_p_max)}/{int(sys_p_min)}",
        "RV Max (mmHg)": round(rv_p_max, 1),
        "PA Mean (mmHg)": round(pa_mean, 1),
        "CO (L/min)": round(co, 1),
        "LA Mean (mmHg)": round(p_LA_mean, 1),
        "PV Mean (mmHg)": round(p_VEN_PUL_mean, 1)
    }
    
def beat_difference(beat1, beat2, model):
    """
    Computes the Normalized RMSE between two beats.
    Returns the MAX error among all state variables to detect worst-case instability.
    """
    diffs = []
    for key in model.states_names:
        v1 = beat1[key]
        v2 = beat2[key]
        
        # --- SAFETY FIX: Handle array length mismatch ---
        # Numerical time slicing can result in off-by-one errors.
        min_len = min(len(v1), len(v2))
        v1 = v1[:min_len]
        v2 = v2[:min_len]
        
        # Robust Range Calculation (Peak-to-Peak)
        norm = np.max(v1) - np.min(v1)
        
        # Handle flatlined variables (prevent division by zero)
        if norm < 1e-8:
            norm = np.abs(np.mean(v2)) + 1e-8
            
        # Root Mean Square Error
        rmse = np.sqrt(np.mean((v1 - v2) ** 2))
        
        # Normalized Error
        nrmse = rmse / norm
        diffs.append(nrmse)
        
    return np.max(diffs)

def analyze_beat_convergence(history, model):
    """
    Analyzes beat-to-beat convergence (Period 1 only).
    """
    # Handle Pint Quantity or float for Heart Rate
    hr_val = model.parameters["HR"]
    if hasattr(hr_val, "magnitude"):
        hr_hz = hr_val.to("Hz").magnitude
    else:
        hr_hz = float(hr_val)
        
    T_beat = 1.0 / hr_hz
    time_arr = history["time"]
    
    # Pre-calculate indices for speed
    num_beats = int(time_arr[-1] / T_beat)
    beat_indices = [0]
    for i in range(1, num_beats + 1):
        target_time = i * T_beat
        idx = np.searchsorted(time_arr, target_time)
        beat_indices.append(idx)
    
    diffs = []
    
    # Standard N vs N-1 comparison
    for i in range(1, len(beat_indices) - 1):
        curr_start, curr_end = beat_indices[i], beat_indices[i+1]
        prev_start, prev_end = beat_indices[i-1], beat_indices[i]
        
        # Extract slices
        beat_curr = {key: history[key][curr_start:curr_end] for key in model.states_names}
        beat_prev = {key: history[key][prev_start:prev_end] for key in model.states_names}
        
        # Check data validity
        first_key = model.states_names[0]
        if len(beat_curr[first_key]) > 0 and len(beat_prev[first_key]) > 0:
            val = beat_difference(beat_curr, beat_prev, model)
            diffs.append(val)

    return diffs

def get_convergence_stats(diffs, threshold=5e-2):
    """
    Classifies convergence into Stable, Slow Drift, or Unstable.
    Removes specific checks for Alternans.
    """
    if not diffs:
        return {"status": "Unstable", "converged": False, "beats_to_fix": np.inf, "final_error": 1.0}
    
    arr = np.array(diffs)
    final_err = arr[-1]
    
    # --- 1. STABLE (Green Light) ---
    if final_err < threshold:
        # Find when it first settled under the line
        violations = np.where(arr >= threshold)[0]
        beats_to_fix = violations[-1] + 2 if len(violations) > 0 else 1
        return {
            "status": "Stable", 
            "converged": True, 
            "beats_to_fix": beats_to_fix, 
            "final_error": final_err
        }

    # --- 2. SLOW DRIFT (Yellow Light) ---
    # Error is above threshold, but consistently decreasing.
    tail_len = 5
    if len(arr) > tail_len:
        recent_trend = arr[-tail_len:]
        # Check if every step is an improvement (strictly negative slope)
        is_improving = np.all(np.diff(recent_trend) < 0)
        
        if is_improving:
             return {
                 "status": "Slow Drift", 
                 "converged": True, # Marked True for your pipeline 
                 "beats_to_fix": len(arr), 
                 "final_error": final_err
             }

    # --- 3. UNSTABLE (Red Light) ---
    return {
        "status": "Unstable", 
        "converged": False, 
        "beats_to_fix": np.inf, 
        "final_error": final_err
    }

def plot_convergence(beat_diffs, threshold=5e-2):
    """
    Plots the convergence metric over beat numbers on a log scale.
    """
    beats = np.arange(1, len(beat_diffs) + 1)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(beats, beat_diffs, 'o-', color='tab:blue', linewidth=2, label='Max Normalized RMSE')
    
    # Add tolerance threshold line
    ax.axhline(threshold, color='tab:green', linestyle='--', label=f'Tolerance ({threshold})')
    
    # Styling
    ax.set_yscale('log')
    ax.set_xlabel('Beat Number')
    ax.set_ylabel('Convergence Error (Log Scale)')
    ax.set_title('Simulation Convergence Speed')
    ax.grid(True, which="both", ls="-", alpha=0.2)
    ax.legend()
    
    # Annotate final value
    if len(beat_diffs) > 0:
        final_err = beat_diffs[-1]
        status = "Converged" if final_err < threshold else "Not Converged"
        color = "green" if final_err < threshold else "red"
        ax.text(0.95, 0.95, f"Status: {status}\nFinal Error: {final_err:.2e}", 
                transform=ax.transAxes, ha='right', va='top', 
                bbox=dict(boxstyle="round", facecolor='white', edgecolor=color))
    
    plt.tight_layout()
    plt.show()
    
    
def plot_comparative_convergence(results_dict, threshold):
    """
    Plots multiple convergence curves on a single figure
    Args:
        results_dict: dict { "Scenario Label": beat_diffs_list }
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for label, diffs in results_dict.items():
        beats = np.arange(1, len(diffs) + 1)
        ax.plot(beats, diffs, 'o-', linewidth=2, label=label, alpha=0.8, markersize=4)

    ax.axhline(threshold, color='k', linestyle='--', alpha=0.5, label=f'Threshold ({threshold})')
    
    ax.set_yscale('log')
    ax.set_xlabel('Beat Number')
    ax.set_ylabel('Max NRMSE (Log Scale)')
    ax.set_title('Convergence Comparison')
    ax.grid(True, which="both", ls="-", alpha=0.2)
    ax.legend()
    plt.tight_layout()
    plt.savefig("convergence_comparison.png", dpi=300)
    plt.show()
    



def apply_paper_timings(parameters):
    """Applies the specific chamber timings from Regazzoni 2022 Table 3."""
    # Atrial Relaxation (Critical for filling)
    parameters["chambers"]["LA"]["TR"] = 0.68 * ureg("s")
    parameters["chambers"]["RA"]["TR"] = 0.64 * ureg("s")
    
    # Atrial Contraction Timings
    parameters["chambers"]["LA"]["tC"] = 0.60 * ureg("s") 
    parameters["chambers"]["LA"]["TC"] = 0.104 * ureg("s")
    parameters["chambers"]["RA"]["tC"] = 0.56 * ureg("s") 
    parameters["chambers"]["RA"]["TC"] = 0.064 * ureg("s")

    # RV (Shorter systole in paper)
    parameters["chambers"]["RV"]["TC"] = 0.272 * ureg("s")
    parameters["chambers"]["RV"]["TR"] = 0.12 * ureg("s")
    
    return parameters

def main():
    print("\n" + "="*60)
    print("ANALYSIS: DEFAULT PACKAGE VS. REGAZZONI 2022 PAPER")
    print("="*60)
    
    logging.basicConfig(level=logging.WARNING)
    
    #=============================================================================
    #default parameters
    params_def = Regazzoni2020.default_parameters()
    init_def = Regazzoni2020.default_initial_conditions()
    
    model_def = Regazzoni2020(initial_state=init_def, parameters=params_def)
    hist_def = model_def.solve(num_beats=num_beats, initial_state=init_def)

    metrics_def = get_metrics(hist_def, "Default Package", hr_bpm=60)
    #==============================================================================


    #=============================================================================
    #paper parameters    
    params_paper = Regazzoni2020.default_parameters()
    
    params_paper["circulation"]["SYS"]["C_VEN"] = 60.0 * ureg("mL/mmHg") 
    
    params_paper = apply_paper_timings(params_paper)
    
    params_paper["HR"] = 1.25 * ureg("Hz")
    
    init_paper = Regazzoni2020.default_initial_conditions()
    
    print(f"Running Paper Simulation ({num_beats} beats) to extract Limit Cycle...")
    model_paper = Regazzoni2020(initial_state=init_paper, parameters=params_paper)
    hist_paper = model_paper.solve(num_beats=num_beats, initial_state=init_paper, dt = dt) 
    
    metrics_paper = get_metrics(hist_paper, "Regazzoni Paper (Table 3)", hr_bpm=75)
    #=============================================================================
    
    
    #paper parameters but bpm of 60 
    params_paper_60bpm = Regazzoni2020.default_parameters()
    params_paper_60bpm["circulation"]["SYS"]["C_VEN"] = 60.0 * ureg("mL/mmHg") 
    params_paper_60bpm = apply_paper_timings(params_paper_60bpm)
    params_paper_60bpm["HR"] = 1.0 * ureg("Hz") # 60 BPM
    init_paper_60bpm = Regazzoni2020.default_initial_conditions()
    model_paper_60bpm = Regazzoni2020(initial_state=init_paper_60bpm, parameters=params_paper_60bpm)
    print(f"Running Paper Simulation ({num_beats} beats) @ 60 BPM to extract Limit Cycle...")
    hist_paper_60bpm = model_paper_60bpm.solve(num_beats=num_beats, initial_state=init_paper_60bpm, dt = dt) 
    metrics_paper_60bpm = get_metrics(hist_paper_60bpm, "Regazzoni Paper (Table 3) @ 60 BPM", hr_bpm=60)
  
    metrics_ref = {
        "Scenario": "Healthy Reference",
        "LV SV (mL)": "65-80", "LV EF (%)": "50-70", 
        "BP (mmHg)": "120/80", "RV Max (mmHg)": "< 25", "PA Mean (mmHg)": "< 19",
        "CO (L/min)": "4.5-6.0", "LA Mean (mmHg)": "5-10", "PV Mean (mmHg)": "> LA"
    }
    
    df = pd.DataFrame([metrics_ref, metrics_def, metrics_paper, metrics_paper_60bpm])
    print("\n--- DISCREPANCY TABLE ---")
    print(df.to_string(index=False))
    

    
    final_state_raw = {key: hist_paper[key][-1] for key in init_paper.keys()}
    
    print("\n" + "="*60)
    print("RECOMMENDED INITIAL CONDITIONS FOR PR (COPY-PASTE BELOW)")
    print("="*60)
    print("default_initial_conditions = {")
    for k, v in final_state_raw.items():
        # Heuristic to assign units based on variable name
        if "V_" in k:
            unit = "mL"
        elif "p_" in k:
            unit = "mmHg"
        elif "Q_" in k:
            unit = "mL/s"
        else:
            unit = ""
            
        print(f'    "{k}": {v:.4f} * ureg("{unit}"),')
    print("}")
    
    # Save final state to csv
    df_final = pd.DataFrame(final_state_raw, index=[0])
    df_final.to_csv("final_state_paper_simulation.csv", index=False)
    print(f"\nSaved limit cycle state to 'final_state_paper_simulation.csv'")

    fig, ax = plt.subplots(2, 2, figsize=(14, 10))
    
    # Helper for plotting (Direct access)
    def plot_loop(axis, hist, p_label, v_label, style, label):
        vol = hist[v_label]
        press = hist[p_label]
        axis.plot(vol[-1000:], press[-1000:], style, label=label, linewidth=2)

    def plot_all(axis, hist, p_label, v_label, style, label):
        vol = hist[v_label]
        press = hist[p_label]
        axis.plot(vol, press, style, label=label, alpha=0.6, linewidth=1)
        
    
    plot_loop(ax[0, 0], hist_def, "p_LV", "V_LV", 'r:', "Default (Floppy Veins)")
    plot_loop(ax[0, 0], hist_paper, "p_LV", "V_LV", 'b-', "Paper (Table 3)")
    plot_loop(ax[0, 0], hist_paper_60bpm, "p_LV", "V_LV", 'g--', "Paper (Table 3) @ 60 BPM")
    ax[0, 0].set_title("Left Ventricle (Stable Loop)")
    ax[0, 0].set_xlabel("Volume [mL]"); ax[0, 0].set_ylabel("Pressure [mmHg]"); ax[0, 0].legend()
    ax[0, 0].grid(True)
    
    #=============================================================================
    
    plot_loop(ax[0, 1], hist_def, "p_RV", "V_RV", 'r:', "Default")
    plot_loop(ax[0, 1], hist_paper, "p_RV", "V_RV", 'b-', "Paper (PH)")
    plot_loop(ax[0, 1], hist_paper_60bpm, "p_RV", "V_RV", 'g--', "Paper (Table 3) @ 60 BPM")
    ax[0, 1].set_title("Right Ventricle (Stable Loop)")
    ax[0, 1].set_xlabel("Volume [mL]"); ax[0, 1].legend()
    ax[0, 1].grid(True)
    
    #=============================================================================
    plot_all(ax[1, 0], hist_def, "p_LV", "V_LV", 'r:', "Default")
    plot_all(ax[1, 0], hist_paper, "p_LV", "V_LV", 'b-', "Paper")
    plot_all(ax[1, 0], hist_paper_60bpm, "p_LV", "V_LV", 'g--', "Paper (Table 3) @ 60 BPM")
    ax[1, 0].set_title("Left Ventricle (Convergence History)")
    ax[1, 0].set_xlabel("Volume [mL]"); ax[1, 0].set_ylabel("Pressure [mmHg]")
    ax[1, 0].grid(True)
    #=============================================================================
    
    
    plot_all(ax[1, 1], hist_def, "p_RV", "V_RV", 'r:', "Default")
    plot_all(ax[1, 1], hist_paper, "p_RV", "V_RV", 'b-', "Paper")
    plot_all(ax[1, 1], hist_paper_60bpm, "p_RV", "V_RV", 'g--', "Paper (Table 3) @ 60 BPM")
    ax[1, 1].set_title("Right Ventricle (Convergence History)")
    ax[1, 1].set_xlabel("Volume [mL]")
    ax[1, 1].grid(True)
    
    plt.suptitle("Regazzoni 2022 Reproduction: Default vs Paper Parameters", fontsize=16)
    plt.tight_layout()
    plt.savefig("pv_loops_default_vs_paper.png", dpi=300)
    
    
    print("\n" + "="*60)
    print("HARD CONVERGENCE METRICS (SIMPLIFIED)")
    print("="*60)

    # 1. Compute differences (Now returns single list)
    diffs_def = analyze_beat_convergence(hist_def, model_def)
    diffs_paper = analyze_beat_convergence(hist_paper, model_paper)
    diffs_60 = analyze_beat_convergence(hist_paper_60bpm, model_paper_60bpm)

    # 2. Get Hard Stats
    THRESHOLD = 5e-2 # 5% mild threshold
    
    stats_def = get_convergence_stats(diffs_def, threshold=THRESHOLD)
    stats_paper = get_convergence_stats(diffs_paper, threshold=THRESHOLD)
    stats_60 = get_convergence_stats(diffs_60, threshold=THRESHOLD)

    # 3. Create Summary Table
    convergence_summary = [
        {
            "Scenario": "Default", 
            "Status": stats_def["status"],
            "Beats to Fix": stats_def["beats_to_fix"],
            "Final Error": f"{stats_def['final_error']:.2e}"
        },
        {
            "Scenario": "Paper (75bpm)", 
            "Status": stats_paper["status"],
            "Beats to Fix": stats_paper["beats_to_fix"],
            "Final Error": f"{stats_paper['final_error']:.2e}"
        },
        {
            "Scenario": "Paper (60bpm)", 
            "Status": stats_60["status"],
            "Beats to Fix": stats_60["beats_to_fix"],
            "Final Error": f"{stats_60['final_error']:.2e}"
        }
    ]
    
    df_conv = pd.DataFrame(convergence_summary)
    print(df_conv.to_string(index=False))

    # 4. Clean Comparative Plotting
    results_map = {
        "Default": diffs_def,
        "Paper (75bpm)": diffs_paper,
        "Paper (60bpm)": diffs_60
    }
    
    plot_comparative_convergence(results_map, threshold=THRESHOLD)
    

if __name__ == "__main__":
    main()