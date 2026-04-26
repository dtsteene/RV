#!/usr/bin/env python3
"""Plot the old and corrected pressure-loading paths used in the thesis."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


RV_ROOT = Path(__file__).resolve().parents[1]
CW_ROOT = RV_ROOT.parent / "cardiac-work"
OUT = RV_ROOT / "figures"
OUT.mkdir(exist_ok=True)

OLD_SUMMARY = CW_ROOT / "results" / "handover" / "handover_old" / "hemodynamic_summary.csv"
CORRECTED_ROOTS = [
    CW_ROOT / "results" / "sims" / "2026-04-23",
    CW_ROOT / "results" / "sims" / "2026-04-24",
]

CORRECTED_CASES = [
    ("sPAP22", 1047450),
    ("sPAP25", 1048194),
    ("sPAP30", 1047451),
    ("sPAP35", 1048195),
    ("sPAP45", 1047452),
    ("sPAP50", 1048196),
    ("sPAP55", 1047453),
    ("sPAP60", 1048197),
    ("sPAP65", 1047454),
    ("sPAP70", 1048198),
    ("sPAP75", 1047455),
    ("sPAP80", 1048199),
    ("sPAP85", 1047456),
    ("sPAP87", 1048200),
    ("sPAP92", 1048201),
    ("sPAP95", 1047457),
]


def load_old():
    rv, lv = [], []
    with OLD_SUMMARY.open() as f:
        for row in csv.DictReader(f):
            rv.append(float(row["RV_ESP_mmHg"]))
            lv.append(float(row["LV_ESP_mmHg"]))
    order = np.argsort(rv)
    return np.array(rv)[order], np.array(lv)[order]


def corrected_dir(run_id: int) -> Path:
    for root in CORRECTED_ROOTS:
        candidate = root / f"UKB_6beats_run_{run_id}"
        if candidate.exists():
            return candidate
    raise FileNotFoundError(run_id)


def load_corrected():
    rv, lv = [], []
    for _, run_id in CORRECTED_CASES:
        pressure = np.load(corrected_dir(run_id) / "solver" / "solver_cavity_pressure_mmHg.npy")
        beat = pressure.shape[0] // 6
        last = pressure[5 * beat :]
        lv.append(float(last[:, 0].max()))
        rv.append(float(last[:, 1].max()))
    order = np.argsort(rv)
    return np.array(rv)[order], np.array(lv)[order]


old_rv, old_lv = load_old()
new_rv, new_lv = load_corrected()

plt.rcParams.update(
    {
        "font.size": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.22,
        "grid.linewidth": 0.7,
    }
)

fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.45), dpi=220)

colors = {"old": "#9f1239", "new": "#1d4ed8"}

ax = axes[0]
ax.scatter(old_rv, old_lv, s=38, color=colors["old"], label="old handover", zorder=3)
ax.scatter(new_rv, new_lv, s=38, color=colors["new"], label="corrected", zorder=3)
for x, y, color in [(old_rv, old_lv, colors["old"]), (new_rv, new_lv, colors["new"])]:
    fit = np.poly1d(np.polyfit(x, y, 1))
    xx = np.linspace(x.min(), x.max(), 80)
    ax.plot(xx, fit(xx), color=color, linewidth=2.0, alpha=0.85)
ax.set_xlabel("Peak RV pressure (mmHg)")
ax.set_ylabel("Peak LV pressure (mmHg)")
ax.set_title("LV pressure path")
ax.legend(frameon=False, loc="lower left")

ax = axes[1]
old_trans = old_lv - old_rv
new_trans = new_lv - new_rv
ax.scatter(old_rv, old_trans, s=38, color=colors["old"], zorder=3)
ax.scatter(new_rv, new_trans, s=38, color=colors["new"], zorder=3)
for x, y, color in [(old_rv, old_trans, colors["old"]), (new_rv, new_trans, colors["new"])]:
    fit = np.poly1d(np.polyfit(x, y, 1))
    xx = np.linspace(x.min(), x.max(), 80)
    ax.plot(xx, fit(xx), color=color, linewidth=2.0, alpha=0.85)
ax.axhline(0, color="#111827", linewidth=0.8)
ax.set_xlabel("Peak RV pressure (mmHg)")
ax.set_ylabel("Peak-pressure gap (mmHg)")
ax.set_title("LV-RV pressure gap")

for ax in axes:
    ax.set_xlim(25, 92)
    ax.tick_params(length=3)

fig.suptitle("The old and corrected sweeps follow different pressure paths", y=1.04, fontsize=12)
fig.tight_layout()

for suffix in ("png", "pdf"):
    fig.savefig(OUT / f"fig_5_3b_old_new_pressure_path.{suffix}", bbox_inches="tight")
