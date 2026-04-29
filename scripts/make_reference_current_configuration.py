from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Polygon

from style import save, setup


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"


def blob(cx: float, cy: float, sx: float, sy: float, phase: float = 0.0) -> tuple[np.ndarray, np.ndarray]:
    theta = np.linspace(0, 2 * np.pi, 240)
    r = 1.0 + 0.10 * np.sin(3 * theta + phase) + 0.06 * np.cos(5 * theta - 0.4 * phase)
    return cx + sx * r * np.cos(theta), cy + sy * r * np.sin(theta)


def add_blob(ax: plt.Axes, cx: float, cy: float, sx: float, sy: float, color: str, phase: float = 0.0) -> None:
    x, y = blob(cx, cy, sx, sy, phase)
    ax.fill(x, y, color=color, alpha=0.18, lw=0)
    ax.plot(x, y, color=color, lw=1.8)


def main() -> None:
    setup()
    fig, ax = plt.subplots(figsize=(7.0, 3.0))
    ax.set_axis_off()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)

    ref_color = "#3f6f8f"
    cur_color = "#9a6234"

    add_blob(ax, 2.0, 2.05, 1.25, 0.95, ref_color, phase=0.2)
    add_blob(ax, 8.0, 2.05, 1.50, 0.78, cur_color, phase=1.1)

    ax.text(2.0, 3.45, "Reference configuration", ha="center", va="center", fontsize=11, weight="bold")
    ax.text(2.0, 3.17, r"$\mathcal{B}_0$: fixed mesh", ha="center", va="center", fontsize=10)
    ax.text(8.0, 3.45, "Current configuration", ha="center", va="center", fontsize=11, weight="bold")
    ax.text(8.0, 3.17, r"$\mathcal{B}_t$: deformed body", ha="center", va="center", fontsize=10)

    arrow = FancyArrowPatch((3.55, 2.15), (6.45, 2.15), arrowstyle="->", mutation_scale=18, lw=1.5, color="#333333")
    ax.add_patch(arrow)
    ax.text(5.0, 2.48, r"$\mathbf{x}=\boldsymbol{\varphi}(\mathbf{X},t)$", ha="center", va="center", fontsize=11)

    ax.plot([1.75], [2.28], marker="o", color=ref_color, ms=5)
    ax.text(1.58, 2.52, r"$\mathbf{X}$", ha="center", va="center", fontsize=11, color=ref_color)
    ax.plot([7.82], [2.34], marker="o", color=cur_color, ms=5)
    ax.text(7.62, 2.60, r"$\mathbf{x}$", ha="center", va="center", fontsize=11, color=cur_color)

    ref_patch = Polygon([[2.25, 1.62], [2.64, 1.62], [2.64, 1.97], [2.25, 1.97]], closed=True, facecolor="white", edgecolor=ref_color, lw=1.3)
    cur_patch = Polygon([[8.20, 1.55], [8.68, 1.67], [8.58, 1.98], [8.10, 1.86]], closed=True, facecolor="white", edgecolor=cur_color, lw=1.3)
    ax.add_patch(ref_patch)
    ax.add_patch(cur_patch)
    ax.text(2.45, 1.42, r"$dV$", ha="center", va="center", fontsize=10, color=ref_color)
    ax.text(8.40, 1.36, r"$dv$", ha="center", va="center", fontsize=10, color=cur_color)

    ax.text(2.0, 0.70, r"work density: $\mathbf{S}:\dot{\mathbf{E}}$", ha="center", va="center", fontsize=10)
    ax.text(8.0, 0.70, r"work density: $\boldsymbol{\sigma}:\mathbf{d}$", ha="center", va="center", fontsize=10)
    ax.text(
        5.0,
        0.25,
        r"same stress power: $\boldsymbol{\sigma}:\mathbf{d}\,dv = \mathbf{S}:\dot{\mathbf{E}}\,dV$",
        ha="center",
        va="center",
        fontsize=10,
    )

    save(fig, FIGURES / "fig_intro_reference_current_configuration")


if __name__ == "__main__":
    main()
