"""Generate the circulation-related figures for chapters 2 and 4.

Replays each calibrated Regazzoni2020 model from `data/ukb_circ_v2/` to
periodic steady state and produces:

  fig_2_9_blanco_activation.{png,pdf}      — Blanco activation waveform
  fig_2_12_elastance.{png,pdf}              — Time-varying elastance E(t)
  fig_2_13_klotz_edpvr.{png,pdf}            — Linear vs Klotz EDPVR
  fig_4_1_targets_vs_achieved.{png,pdf}     — Calibration accuracy dotplot
  fig_4_2_pv_loops_spectrum.{png,pdf}       — LV/RV PV loops across spectrum
  fig_4_3_pressure_waveforms.{png,pdf}      — Pressure traces vs severity
  fig_4_4_parameter_trajectory.{png,pdf}    — Parameter shifts vs severity
  fig_4_5_collapses.{png,pdf}               — Three key Pearson collapses

Run from the RV/ root::

    python scripts/make_circ_figures.py
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Local helper
import sys
sys.path.insert(0, str(Path(__file__).parent))
from style import SEVERITIES, SEVERITY_LABELS, save, setup, severity_palette  # noqa: E402

from circulation.regazzoni2020 import Regazzoni2020  # noqa: E402

DATA_DIR = Path("/home/dtsteene/D1/cardiac-work/data/ukb_circ_v2")
FIG_DIR = Path(__file__).resolve().parents[1] / "figures"
NUM_BEATS = 25  # enough for venous transients to settle
DT = 1e-3
DT_EVAL = 2e-3

setup()
PALETTE = severity_palette(len(SEVERITIES))


# ---------------------------------------------------------------------------
# Replay
# ---------------------------------------------------------------------------
@dataclass
class CaseTrace:
    severity: str
    HR: float
    targets: dict
    achieved: dict
    derived: dict
    params: dict
    t: np.ndarray
    V_LV: np.ndarray
    V_RV: np.ndarray
    p_LV: np.ndarray
    p_RV: np.ndarray
    p_AR_SYS: np.ndarray
    p_AR_PUL: np.ndarray
    p_LA: np.ndarray


def replay(severity: str) -> CaseTrace:
    path = DATA_DIR / f"optimized_regazzoni_ukb_{severity}.json"
    with path.open() as f:
        d = json.load(f)
    model = Regazzoni2020(
        parameters=d["parameters"],
        initial_state=d["initial_state"],
        add_units=False,
        verbose=False,
    )
    model.solve(num_beats=NUM_BEATS, dt=DT, dt_eval=DT_EVAL)
    h = model.history
    HR = float(d["parameters"]["HR"])
    T_beat = 1.0 / HR
    t_full = h["time"]
    mask = t_full >= (t_full[-1] - T_beat - 1e-9)
    t = t_full[mask] - t_full[mask][0]
    return CaseTrace(
        severity=severity,
        HR=HR,
        targets=d["pressure_targets"],
        achieved=d["metrics_achieved"],
        derived=d["derived_hemodynamics"],
        params=d["parameters"],
        t=t,
        V_LV=h["V_LV"][mask],
        V_RV=h["V_RV"][mask],
        p_LV=h["p_LV"][mask],
        p_RV=h["p_RV"][mask],
        p_AR_SYS=h["p_AR_SYS"][mask],
        p_AR_PUL=h["p_AR_PUL"][mask],
        p_LA=h["p_LA"][mask],
    )


def replay_all() -> dict[str, CaseTrace]:
    print("Replaying calibrated circulation models...")
    cases = {}
    for sev in SEVERITIES:
        print(f"  {sev}", flush=True)
        cases[sev] = replay(sev)
    return cases


# ---------------------------------------------------------------------------
# Figure 2.9 — Blanco activation waveform
# ---------------------------------------------------------------------------
def fig_blanco_activation(case: CaseTrace) -> None:
    """Plot the Blanco activation function used in the coupled mechanics runs."""
    TC, TR, tC = 0.25, 0.40, 0.0
    T = 0.8
    t = np.linspace(0, 2 * T, 1000)

    def activation(ti):
        # Phase folded into one beat
        ti = ti % T
        if tC <= ti < tC + TC:
            return 0.5 * (1 - np.cos(np.pi * (ti - tC) / TC))
        if tC + TC <= ti < tC + TC + TR:
            return 0.5 * (1 + np.cos(np.pi * (ti - tC - TC) / TR))
        return 0.0

    a = np.array([activation(ti) for ti in t])

    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    ax.plot(t, a, color="#2b3a55", lw=1.8, label=r"LV activation $a(t)$")
    ax.axvspan(tC, tC + TC, color="#f3a2a2", alpha=0.30, label="Contraction $T_C$")
    ax.axvspan(tC + TC, tC + TC + TR, color="#a8c6e6", alpha=0.30,
               label="Relaxation $T_R$")
    # Second beat for periodicity
    ax.axvspan(T + tC, T + tC + TC, color="#f3a2a2", alpha=0.30)
    ax.axvspan(T + tC + TC, T + tC + TC + TR, color="#a8c6e6", alpha=0.30)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Activation $a(t)$")
    ax.set_xlim(0, 2 * T)
    ax.set_ylim(-0.05, 1.10)
    ax.legend(loc="upper right", framealpha=0.95)
    ax.set_title("Blanco activation function (production timing)")
    save(fig, FIG_DIR / "fig_2_9_blanco_activation")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 2.12 — Time-varying elastance E(t)
# ---------------------------------------------------------------------------
def fig_elastance(case: CaseTrace) -> None:
    lv = case.params["chambers"]["LV"]
    rv = case.params["chambers"]["RV"]
    T = 1.0 / case.HR
    t = np.linspace(0, 2 * T, 1000)

    def elastance(t_, p):
        EA, EB, TC, TR, tC = p["EA"], p["EB"], p["TC"], p["TR"], p["tC"]
        ti = t_ % T
        if tC <= ti < tC + TC:
            a = 0.5 * (1 - np.cos(np.pi * (ti - tC) / TC))
        elif tC + TC <= ti < tC + TC + TR:
            a = 0.5 * (1 + np.cos(np.pi * (ti - tC - TC) / TR))
        else:
            a = 0.0
        return EB + (EA - EB) * a

    E_lv = np.array([elastance(ti, lv) for ti in t])
    E_rv = np.array([elastance(ti, rv) for ti in t])

    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    ax.plot(t, E_lv, color="#c0392b", lw=1.8, label=r"LV $E(t)$")
    ax.plot(t, E_rv, color="#2c7fb8", lw=1.8, label=r"RV $E(t)$")
    ax.axhline(lv["EB"], color="#c0392b", lw=0.9, ls=":", alpha=0.7,
               label=r"$E_B^{\rm LV}$")
    ax.axhline(rv["EB"], color="#2c7fb8", lw=0.9, ls=":", alpha=0.7,
               label=r"$E_B^{\rm RV}$")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(r"Elastance $E(t)$  (mmHg / mL)")
    ax.set_xlim(0, 2 * T)
    ax.legend(loc="upper right", ncol=2, framealpha=0.95)
    ax.set_title("Time-varying elastance, healthy calibration")
    save(fig, FIG_DIR / "fig_2_12_elastance")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 2.13 — Klotz EDPVR comparison
# ---------------------------------------------------------------------------
def fig_klotz_edpvr(case: CaseTrace) -> None:
    """Side-by-side: linear vs nonlinear (Klotz) diastolic EDPVR.

    Shows how the exponential term decouples EDP from EDV at the operating
    point. Uses the calibrated EB, V0, kE for the LV and RV.
    """
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.6), sharey=False)
    for ax, key, color, name in [
        (axes[0], "LV", "#c0392b", "Left ventricle"),
        (axes[1], "RV", "#2c7fb8", "Right ventricle"),
    ]:
        chamber = case.params["chambers"][key]
        EB = chamber["EB"]
        V0 = chamber["V0"]
        kE = chamber.get("kE", 0.0)
        EDV = case.achieved[f"{key}_EDV"]
        EDP = case.achieved[f"{key}_EDP"]
        V = np.linspace(V0, EDV * 1.45, 400)
        dV = V - V0
        # Linear EDPVR (the old Regazzoni passive law)
        P_lin = EB * dV
        # Klotz nonlinear EDPVR (the modification)
        P_klotz = (EB / kE) * (np.exp(kE * dV) - 1.0) if kE > 0 else P_lin
        ax.plot(V, P_lin, color="#888888", lw=1.5, ls="--",
                label=fr"Linear ($k_E=0$)")
        ax.plot(V, P_klotz, color=color, lw=2.0,
                label=fr"Klotz ($k_E={kE*1000:.1f}\times10^{{-3}}$)")
        ax.scatter([EDV], [EDP], s=70, color=color, edgecolor="black",
                   zorder=5, label="Operating point")
        ax.axhline(0, color="black", lw=0.4)
        ax.set_xlabel(f"{key} volume (mL)")
        ax.set_ylabel("Diastolic pressure (mmHg)")
        ax.set_title(name)
        ax.set_ylim(-3, max(EDP * 4.0, 25))
        ax.legend(loc="upper left", framealpha=0.95)

    fig.suptitle("Klotz nonlinear EDPVR decouples end-diastolic pressure from volume",
                 y=1.02, fontsize=11)
    save(fig, FIG_DIR / "fig_2_13_klotz_edpvr")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 4.1 — Targets vs achieved hemodynamics
# ---------------------------------------------------------------------------
def fig_targets_vs_achieved(cases: dict[str, CaseTrace]) -> None:
    metrics = [
        ("LV_ESP", "LV ESP (mmHg)"),
        ("RV_ESP", "RV ESP (mmHg)"),
        ("LV_EDP", "LV EDP (mmHg)"),
        ("RV_EDP", "RV EDP (mmHg)"),
        ("Ao_DBP", "Ao DBP (mmHg)"),
        ("LA_P_MEAN", "LA mean P (mmHg)"),
    ]
    fig, axes = plt.subplots(2, 3, figsize=(9.0, 5.4), sharex=True,
                              layout="constrained")
    x = np.arange(len(SEVERITIES))
    for ax, (key, label) in zip(axes.flat, metrics):
        targets = np.array([cases[s].targets.get(key, np.nan) for s in SEVERITIES])
        achieved = np.array([cases[s].achieved.get(key, np.nan) for s in SEVERITIES])
        ax.plot(x, targets, marker="_", ms=18, lw=0, color="#888",
                mec="#444", mew=2.0, label="Target")
        ax.scatter(x, achieved, s=55, color=PALETTE,
                   edgecolor="black", linewidth=0.6, zorder=5, label="Achieved")
        ax.set_ylabel(label)
    for ax in axes[-1]:
        ax.set_xticks(x)
        ax.set_xticklabels([SEVERITY_LABELS[s] for s in SEVERITIES],
                           rotation=35, ha="right")
    # Compact legend in the first panel
    axes[0, 0].legend(loc="lower right", framealpha=0.95, fontsize=8,
                       handletextpad=0.4, borderpad=0.3)
    fig.suptitle("Calibration accuracy across the severity spectrum",
                 fontsize=11)
    save(fig, FIG_DIR / "fig_4_1_targets_vs_achieved")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 4.2 — PV loops across the spectrum
# ---------------------------------------------------------------------------
def fig_pv_loops_spectrum(cases: dict[str, CaseTrace]) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 4.2), sharey=False)
    for ax, key, name in [(axes[0], "LV", "Left ventricle"),
                          (axes[1], "RV", "Right ventricle")]:
        for sev, color in zip(SEVERITIES, PALETTE):
            c = cases[sev]
            V = c.V_LV if key == "LV" else c.V_RV
            P = c.p_LV if key == "LV" else c.p_RV
            ax.plot(V, P, color=color, lw=1.5,
                    label=SEVERITY_LABELS[sev], alpha=0.95)
        ax.set_xlabel(f"{key} volume (mL)")
        ax.set_ylabel(f"{key} pressure (mmHg)")
        ax.set_title(name)
    axes[1].legend(loc="upper right", title="Severity", fontsize=8,
                   title_fontsize=9, framealpha=0.95, labelspacing=0.25)
    fig.suptitle("Pressure–volume loops along the PAH severity spectrum",
                 y=1.02, fontsize=11)
    save(fig, FIG_DIR / "fig_4_2_pv_loops_spectrum")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 4.3 — Pressure waveforms (selected severities)
# ---------------------------------------------------------------------------
def fig_pressure_waveforms(cases: dict[str, CaseTrace]) -> None:
    selected = ["healthy", "moderate", "severe", "end_stage"]
    sel_palette = severity_palette(len(SEVERITIES))
    sel_colors = {s: sel_palette[SEVERITIES.index(s)] for s in selected}

    fig, axes = plt.subplots(2, 1, figsize=(7.0, 5.2), sharex=True)
    for ax, key, name in [
        (axes[0], "p_LV", "LV"),
        (axes[1], "p_RV", "RV"),
    ]:
        for sev in selected:
            c = cases[sev]
            arr = getattr(c, key)
            ax.plot(c.t * 1000, arr, color=sel_colors[sev], lw=1.6,
                    label=SEVERITY_LABELS[sev])
        ax.set_ylabel(f"{name} pressure (mmHg)")
        ax.set_title(f"{name} pressure waveform, last beat")
    axes[-1].set_xlabel("Time within cardiac cycle (ms)")
    axes[0].legend(loc="upper right", ncol=4, fontsize=8, framealpha=0.95)
    fig.suptitle("Ventricular pressure waveforms across the severity spectrum",
                 y=1.01, fontsize=11)
    save(fig, FIG_DIR / "fig_4_3_pressure_waveforms")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 4.4 — Parameter trajectory along severity
# ---------------------------------------------------------------------------
def fig_parameter_trajectory(cases: dict[str, CaseTrace]) -> None:
    """Show how the key driving parameters move along the severity chain."""
    def get(sev, *path):
        d = cases[sev].params
        for p in path:
            d = d[p]
        return d

    items = [
        ("R_AR_PUL", "Pulm. arterial resistance",
         lambda s: get(s, "circulation", "PUL", "R_AR")),
        ("C_AR_PUL", "Pulm. arterial compliance",
         lambda s: get(s, "circulation", "PUL", "C_AR")),
        ("RV.EA", "RV active elastance $E_A^{\\rm RV}$",
         lambda s: get(s, "chambers", "RV", "EA")),
        ("RV.kE", "RV nonlinear stiffening $k_E^{\\rm RV}$",
         lambda s: get(s, "chambers", "RV", "kE")),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(8.5, 5.6), sharex=True,
                              layout="constrained")
    x = np.arange(len(SEVERITIES))
    for ax, (key, name, fn) in zip(axes.flat, items):
        y = np.array([fn(s) for s in SEVERITIES])
        ax.plot(x, y, color="#2b3a55", lw=1.4, marker="o", ms=5.5, mec="black",
                mew=0.6)
        for xi, yi, color in zip(x, y, PALETTE):
            ax.plot(xi, yi, "o", ms=6.5, color=color, mec="black", mew=0.5)
        ax.set_title(name)
    for ax in axes[-1]:
        ax.set_xticks(x)
        ax.set_xticklabels([SEVERITY_LABELS[s] for s in SEVERITIES],
                           rotation=35, ha="right", fontsize=8)
    fig.suptitle("Calibrated parameter shifts along the severity chain",
                 fontsize=11)
    save(fig, FIG_DIR / "fig_4_4_parameter_trajectory")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 4.5 — Three key collapses (Pearson scatter plots)
# ---------------------------------------------------------------------------
def _pearson(x, y):
    x = np.asarray(x); y = np.asarray(y)
    return float(np.corrcoef(x, y)[0, 1])


def fig_collapses(cases: dict[str, CaseTrace]) -> None:
    rv_esp = np.array([cases[s].achieved["RV_ESP"] for s in SEVERITIES])
    lv_esp = np.array([cases[s].achieved["LV_ESP"] for s in SEVERITIES])
    co = np.array([cases[s].derived["CO_Lpm"] for s in SEVERITIES])
    transp = lv_esp - rv_esp

    panels = [
        ("LV ESP (mmHg)", lv_esp, "Ventricular interdependence"),
        (r"$P_{\rm LV,ES} - P_{\rm RV,ES}$  (mmHg)", transp, "Transmural collapse"),
        ("Cardiac output (L/min)", co, "Forward failure"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(9.0, 3.4))
    for ax, (ylabel, y, title) in zip(axes, panels):
        for xi, yi, color in zip(rv_esp, y, PALETTE):
            ax.scatter(xi, yi, s=65, color=color, edgecolor="black",
                       linewidth=0.6, zorder=5)
        # Linear fit
        slope, intercept = np.polyfit(rv_esp, y, 1)
        xline = np.linspace(rv_esp.min(), rv_esp.max(), 50)
        ax.plot(xline, slope * xline + intercept, color="#444", lw=1.0, ls="--",
                alpha=0.7)
        r = _pearson(rv_esp, y)
        ax.text(0.04, 0.95, fr"$r = {r:+.3f}$", transform=ax.transAxes,
                ha="left", va="top", fontsize=9,
                bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                          edgecolor="#bbb", alpha=0.95))
        ax.set_xlabel("RV ESP (mmHg)")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
    fig.suptitle("Severity-driven collapses in the calibrated spectrum",
                 y=1.04, fontsize=11)
    save(fig, FIG_DIR / "fig_4_5_collapses")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def main():
    cases = replay_all()
    healthy = cases["healthy"]
    print("Drawing figures...")
    fig_blanco_activation(healthy)
    fig_elastance(healthy)
    fig_klotz_edpvr(healthy)
    fig_targets_vs_achieved(cases)
    fig_pv_loops_spectrum(cases)
    fig_pressure_waveforms(cases)
    fig_parameter_trajectory(cases)
    fig_collapses(cases)
    print(f"Done. Wrote figures to {FIG_DIR}")


if __name__ == "__main__":
    main()
