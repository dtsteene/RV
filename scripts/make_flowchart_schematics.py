"""Create flowchart-style schematic figures for the model chapter."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, RegularPolygon

from style import save, setup


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"

EDGE = "#2f3b43"
TEXT = "#263238"
BLUE = "#e8edf7"
RED = "#f5e7eb"
GREEN = "#e7f0ef"
YELLOW = "#f6efd9"
ORANGE = "#fff3e0"
GREY = "#eeeeee"
LINE = "#546e7a"


def card(
    ax,
    xy,
    wh,
    title: str,
    body: str = "",
    facecolor: str = GREY,
    *,
    title_size: float = 9.2,
    body_size: float = 7.4,
    lw: float = 1.1,
):
    x, y = xy
    w, h = wh
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.012,rounding_size=0.020",
        linewidth=lw,
        edgecolor=EDGE,
        facecolor=facecolor,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h * (0.62 if body else 0.50),
        title,
        ha="center",
        va="center",
        fontsize=title_size,
        fontweight="bold",
        color=TEXT,
        linespacing=1.12,
    )
    if body:
        ax.text(
            x + w / 2,
            y + h * 0.30,
            body,
            ha="center",
            va="center",
            fontsize=body_size,
            color=TEXT,
            linespacing=1.16,
        )
    return patch


def arrow(
    ax,
    start,
    end,
    *,
    label: str | None = None,
    color: str = LINE,
    lw: float = 1.6,
    rad: float = 0.0,
    label_offset=(0.0, 0.0),
    label_size: float = 7.8,
    ms: int = 12,
):
    patch = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=ms,
        linewidth=lw,
        color=color,
        connectionstyle=f"arc3,rad={rad}",
        shrinkA=4,
        shrinkB=4,
    )
    ax.add_patch(patch)
    if label:
        ax.text(
            (start[0] + end[0]) / 2 + label_offset[0],
            (start[1] + end[1]) / 2 + label_offset[1],
            label,
            ha="center",
            va="center",
            fontsize=label_size,
            color=color,
            bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none", alpha=0.96),
        )
    return patch


def valve(ax, xy, label: str, facecolor: str = "#ffffff") -> None:
    patch = RegularPolygon(
        xy,
        numVertices=4,
        radius=0.031,
        orientation=0.785,
        facecolor=facecolor,
        edgecolor=EDGE,
        linewidth=1.0,
    )
    ax.add_patch(patch)
    ax.text(xy[0], xy[1], label, ha="center", va="center", fontsize=6.7, fontweight="bold", color=TEXT)


def setup_axes(figsize=(7.8, 4.4)):
    setup()
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def make_0d_network() -> None:
    fig, ax = setup_axes((8.4, 4.5))

    ax.text(0.5, 0.94, "Closed-loop 0D circulation", ha="center", va="center", fontsize=12, fontweight="bold", color=TEXT)

    chamber_w, chamber_h = 0.15, 0.12
    branch_w, branch_h = 0.24, 0.17

    la = (0.10, 0.69)
    lv = (0.38, 0.69)
    sys = (0.67, 0.61)
    ra = (0.72, 0.25)
    rv = (0.42, 0.25)
    pul = (0.10, 0.25)

    card(ax, la, (chamber_w, chamber_h), "LA", "time-varying\nelastance", BLUE)
    card(ax, lv, (chamber_w, chamber_h), "LV", "time-varying\nelastance", BLUE)
    card(ax, ra, (chamber_w, chamber_h), "RA", "time-varying\nelastance", BLUE)
    card(ax, rv, (chamber_w, chamber_h), "RV", "time-varying\nelastance", BLUE)

    card(
        ax,
        sys,
        (branch_w, branch_h),
        "systemic Windkessel",
        "arterial / venous\nR, C, L elements",
        GREEN,
        title_size=8.8,
        body_size=7.2,
    )
    card(
        ax,
        pul,
        (branch_w, branch_h),
        "pulmonary Windkessel",
        "arterial / venous\nR, C, L elements",
        YELLOW,
        title_size=8.8,
        body_size=7.2,
    )

    # Forward-flow path around the closed loop.
    arrow(ax, (0.25, 0.75), (0.38, 0.75), label="MV", label_offset=(0.0, 0.037), color="#1f77b4")
    valve(ax, (0.315, 0.75), "MV")
    arrow(ax, (0.53, 0.75), (0.67, 0.70), label="AV", label_offset=(0.005, 0.040), color="#1f77b4")
    valve(ax, (0.600, 0.725), "AV")
    arrow(ax, (0.79, 0.61), (0.79, 0.37), label="systemic\nreturn", label_offset=(0.075, 0.0), color="#2e7d32", label_size=7.3)
    arrow(ax, (0.72, 0.31), (0.57, 0.31), label="TV", label_offset=(0.0, -0.040), color="#c0392b")
    valve(ax, (0.645, 0.31), "TV")
    arrow(ax, (0.42, 0.31), (0.34, 0.31), label="PV", label_offset=(0.0, -0.040), color="#c0392b")
    valve(ax, (0.380, 0.31), "PV")
    arrow(ax, (0.22, 0.42), (0.18, 0.69), label="pulmonary\nreturn", label_offset=(-0.090, 0.0), color="#8a6d00", label_size=7.3)

    ax.text(0.50, 0.11, "Valves set direction; vascular RCL branches set afterload, compliance, and inertance.", ha="center", va="center", fontsize=8.2, color=TEXT)

    save(fig, FIGURES / "fig_2_10_0d_network")
    plt.close(fig)


def make_coupling_schematic() -> None:
    fig, ax = setup_axes((8.4, 4.5))

    ax.text(0.5, 0.94, "Bidirectional 3D-0D coupling at one time step", ha="center", va="center", fontsize=12, fontweight="bold", color=TEXT)

    card(ax, (0.06, 0.56), (0.24, 0.16), "0D circulation", "advance valves,\nvessels, chambers", BLUE, title_size=10.2, body_size=7.8)
    card(ax, (0.385, 0.58), (0.23, 0.12), "volume scaling", r"$\mathcal{V}^*_\mathrm{FEM}=s\,\mathcal{V}^*_\mathrm{0D}$", GREEN, title_size=9.2, body_size=7.8)
    card(ax, (0.70, 0.56), (0.24, 0.16), "3D mechanics", "solve equilibrium\nwith cavity constraints", RED, title_size=10.2, body_size=7.8)

    card(ax, (0.70, 0.24), (0.24, 0.12), "active tension", "Blanco waveform\nfixed peak tension", ORANGE, title_size=8.8, body_size=7.2)
    card(ax, (0.40, 0.24), (0.22, 0.12), "checkpoint", "displacement and\npressure multipliers", GREY, title_size=8.8, body_size=7.0)
    card(ax, (0.08, 0.24), (0.22, 0.12), "metrics", "stress, strain,\nwork density", GREY, title_size=8.8, body_size=7.0)

    arrow(ax, (0.30, 0.64), (0.385, 0.64), label="target volumes", color="#1f77b4", lw=2.0, label_offset=(0.0, 0.060), label_size=7.5)
    arrow(ax, (0.615, 0.64), (0.70, 0.64), label="scaled targets", color="#1f77b4", lw=2.0, label_offset=(0.0, 0.060), label_size=7.5)
    arrow(ax, (0.70, 0.505), (0.30, 0.505), label=r"$p_\mathrm{LV},p_\mathrm{RV}$ from Lagrange multipliers", color="#c0392b", lw=2.0, label_offset=(0.0, -0.055), label_size=7.3)
    arrow(ax, (0.82, 0.36), (0.82, 0.56), color="#ef8a00", lw=1.8, label="drive", label_offset=(0.055, 0.0), label_size=7.4)
    arrow(ax, (0.73, 0.56), (0.58, 0.36), color="#607d8b", lw=1.5)
    arrow(ax, (0.40, 0.30), (0.30, 0.30), color="#607d8b", lw=1.5)

    arrow(ax, (0.18, 0.56), (0.18, 0.72), color="#455a64", rad=-0.20, lw=1.3, ms=10)
    ax.text(0.18, 0.76, "next step", ha="center", va="center", fontsize=7.5, color="#455a64")

    ax.text(0.5, 0.10, "The mechanics solve is volume controlled; the returned pressures are the multipliers that enforce the cavity volumes.", ha="center", va="center", fontsize=7.8, color=TEXT)

    save(fig, FIGURES / "fig_2_11_coupling_schematic")
    plt.close(fig)


def make_boundary_conditions() -> None:
    fig, ax = setup_axes((8.4, 4.5))

    ax.text(0.5, 0.94, "Boundary and cavity conditions", ha="center", va="center", fontsize=12, fontweight="bold", color=TEXT)

    # Central model body.
    body = FancyBboxPatch(
        (0.38, 0.37),
        0.24,
        0.25,
        boxstyle="round,pad=0.018,rounding_size=0.080",
        linewidth=1.5,
        edgecolor=EDGE,
        facecolor="#f8fafc",
    )
    ax.add_patch(body)
    ax.text(0.50, 0.505, "biventricular\nmechanics", ha="center", va="center", fontsize=10.2, fontweight="bold", color=TEXT, linespacing=1.15)
    ax.text(0.50, 0.425, r"$\mathbf{u},\ p_\mathrm{LV},\ p_\mathrm{RV}$", ha="center", va="center", fontsize=9.2, color=TEXT)

    card(ax, (0.06, 0.61), (0.25, 0.15), "LV endocardium", r"$\mathcal{V}_\mathrm{LV}=\mathcal{V}_\mathrm{LV}^*$" + "\n" + r"returns $p_\mathrm{LV}$", BLUE, title_size=9.2, body_size=7.6)
    card(ax, (0.69, 0.61), (0.25, 0.15), "RV endocardium", r"$\mathcal{V}_\mathrm{RV}=\mathcal{V}_\mathrm{RV}^*$" + "\n" + r"returns $p_\mathrm{RV}$", BLUE, title_size=9.2, body_size=7.6)
    card(ax, (0.06, 0.20), (0.26, 0.15), "epicardium", "Robin spring\nnormal direction only", GREEN, title_size=9.2, body_size=7.6)
    card(ax, (0.68, 0.20), (0.26, 0.15), "base", "base-normal/global-x fixed\nRobin support", YELLOW, title_size=8.8, body_size=7.0)

    arrow(ax, (0.31, 0.665), (0.39, 0.555), color="#1f77b4", lw=1.8, label="constraint", label_offset=(-0.015, 0.035))
    arrow(ax, (0.69, 0.665), (0.61, 0.555), color="#1f77b4", lw=1.8, label="constraint", label_offset=(0.015, 0.035))
    arrow(ax, (0.32, 0.295), (0.39, 0.425), color="#2e7d32", lw=1.8, label="support", label_offset=(-0.028, -0.010))
    arrow(ax, (0.68, 0.295), (0.61, 0.425), color="#8a6d00", lw=1.8, label="stabilize", label_offset=(0.030, -0.010))

    # Small visual cue for tangential sliding.
    arrow(ax, (0.72, 0.145), (0.90, 0.145), color="#78909c", lw=1.3, label="tangential sliding remains", label_offset=(0.0, -0.032), label_size=7.1, ms=10)

    ax.text(0.50, 0.08, "Cavity constraints impose volumes; scalar pressures enter as Lagrange multipliers. Robin terms are included in the energy budget.", ha="center", va="center", fontsize=7.6, color=TEXT)

    save(fig, FIGURES / "fig_2_8_boundary_conditions")
    plt.close(fig)


def main() -> None:
    make_0d_network()
    make_coupling_schematic()
    make_boundary_conditions()


if __name__ == "__main__":
    main()
