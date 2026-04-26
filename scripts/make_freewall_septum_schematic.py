#!/usr/bin/env python3
"""Create a minimal schematic for the free-wall versus septum pressure choice."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle


OUT = Path(__file__).resolve().parents[1] / "figures"
OUT.mkdir(exist_ok=True)


def arrow(ax, start, end, label, color="#1d4ed8"):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=2.0,
            color=color,
        )
    )
    mx = 0.5 * (start[0] + end[0])
    my = 0.5 * (start[1] + end[1])
    ax.text(mx, my + 0.08, label, ha="center", va="bottom", fontsize=11, color=color)


def setup(ax, title):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=13, pad=10, weight="bold")


fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.4), dpi=220)

setup(axes[0], "Free wall")
axes[0].add_patch(Rectangle((0.12, 0.18), 0.34, 0.64, facecolor="#dbeafe", edgecolor="none"))
axes[0].add_patch(Rectangle((0.46, 0.18), 0.22, 0.64, facecolor="#d1d5db", edgecolor="#4b5563", linewidth=1.4))
axes[0].add_patch(Rectangle((0.68, 0.18), 0.20, 0.64, facecolor="#f8fafc", edgecolor="none"))
axes[0].text(0.29, 0.50, "cavity", ha="center", va="center", fontsize=11, color="#1e3a8a")
axes[0].text(0.57, 0.50, "wall", ha="center", va="center", fontsize=11, color="#111827")
arrow(axes[0], (0.26, 0.72), (0.48, 0.72), r"$P_\mathrm{cav}$")
axes[0].text(0.50, 0.08, "one obvious pressure scale", ha="center", va="center", fontsize=10)

setup(axes[1], "Septum")
axes[1].add_patch(Rectangle((0.08, 0.18), 0.30, 0.64, facecolor="#dbeafe", edgecolor="none"))
axes[1].add_patch(Rectangle((0.38, 0.18), 0.24, 0.64, facecolor="#d1d5db", edgecolor="#4b5563", linewidth=1.4))
axes[1].add_patch(Rectangle((0.62, 0.18), 0.30, 0.64, facecolor="#e0f2fe", edgecolor="none"))
axes[1].text(0.23, 0.50, "LV", ha="center", va="center", fontsize=11, color="#1e3a8a")
axes[1].text(0.50, 0.50, "septum", ha="center", va="center", fontsize=11, color="#111827")
axes[1].text(0.77, 0.50, "RV", ha="center", va="center", fontsize=11, color="#075985")
arrow(axes[1], (0.22, 0.72), (0.40, 0.72), r"$P_\mathrm{LV}$")
arrow(axes[1], (0.78, 0.30), (0.60, 0.30), r"$P_\mathrm{RV}$", color="#0369a1")
axes[1].text(0.50, 0.08, "shared tissue, two-sided loading", ha="center", va="center", fontsize=10)

fig.subplots_adjust(wspace=0.20, left=0.04, right=0.98, top=0.84, bottom=0.12)

for suffix in ("png", "pdf"):
    fig.savefig(OUT / f"fig_5_0_freewall_vs_septum_schematic.{suffix}", bbox_inches="tight")

