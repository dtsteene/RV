"""Create the end-to-end simulation pipeline overview figure."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from style import save, setup


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"


EDGE = "#2f3b43"
TEXT = "#263238"


def card(
    ax,
    xy,
    wh,
    title: str,
    body: str,
    facecolor: str,
    *,
    title_size: float = 9.0,
    body_size: float = 7.2,
):
    """Draw a rounded process card with a short title and body."""
    x, y = xy
    w, h = wh
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.012,rounding_size=0.020",
        linewidth=1.1,
        edgecolor=EDGE,
        facecolor=facecolor,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h * 0.62,
        title,
        ha="center",
        va="center",
        fontsize=title_size,
        fontweight="bold",
        color=TEXT,
    )
    ax.text(
        x + w / 2,
        y + h * 0.30,
        body,
        ha="center",
        va="center",
        fontsize=body_size,
        color=TEXT,
        linespacing=1.2,
    )
    return patch


def label_card(ax, xy, wh, text: str, facecolor: str, *, size: float = 8.2):
    x, y = xy
    w, h = wh
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        linewidth=1.1,
        edgecolor=EDGE,
        facecolor=facecolor,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=size,
        fontweight="bold",
        color=TEXT,
        linespacing=1.2,
    )
    return patch


def arrow(
    ax,
    start,
    end,
    *,
    color: str = "#546e7a",
    lw: float = 1.8,
    rad: float = 0.0,
    label: str | None = None,
    label_offset=(0.0, 0.0),
):
    patch = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=12,
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
            fontsize=8.0,
            color=color,
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.95),
        )


def main() -> None:
    setup()
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})

    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    colors = {
        "geom": "#e7f0ef",
        "fiber": "#f6efd9",
        "circ": "#e8edf7",
        "mech": "#f5e7eb",
        "prep": "#edf2df",
        "active": "#fff3e0",
        "out": "#eeeeee",
    }

    ax.text(
        0.5,
        0.93,
        "Preparation",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color=TEXT,
    )

    y_top, h_top, w_top = 0.73, 0.13, 0.14
    xs = [0.055, 0.25, 0.445, 0.64, 0.805]
    top_cards = [
        ("Geometry", "mesh\nlabels", colors["geom"]),
        ("Fibres", "LDRB\nframe", colors["fiber"]),
        ("0D warm-up", "periodic\ncycle", colors["circ"]),
        ("Scale", "match\nvolumes", colors["prep"]),
        ("Prestress", "loaded ED\nstate", colors["mech"]),
    ]
    for x, (title, body, color) in zip(xs, top_cards):
        card(ax, (x, y_top), (w_top, h_top), title, body, color, title_size=8.7, body_size=7.2)

    for start, end in zip(xs[:-1], xs[1:]):
        arrow(
            ax,
            (start + w_top + 0.004, y_top + h_top / 2),
            (end - 0.004, y_top + h_top / 2),
            lw=1.6,
        )

    ax.text(
        0.5,
        0.62,
        "Coupled solve at each time step",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color=TEXT,
    )

    card(
        ax,
        (0.08, 0.29),
        (0.31, 0.17),
        "0D circulation",
        "advance circuit\nrequest target volumes",
        colors["circ"],
        title_size=10.5,
        body_size=8.5,
    )
    card(
        ax,
        (0.61, 0.29),
        (0.31, 0.17),
        "3D mechanics",
        "solve equilibrium\nreturn cavity pressures",
        colors["mech"],
        title_size=10.5,
        body_size=8.5,
    )

    label_card(
        ax,
        (0.63, 0.10),
        (0.25, 0.095),
        "Active tension\nBlanco waveform",
        colors["active"],
        size=8.5,
    )
    label_card(
        ax,
        (0.66, 0.50),
        (0.23, 0.075),
        "Record metrics\nstress, strain, work density",
        colors["out"],
        size=7.0,
    )

    arrow(
        ax,
        (0.39, 0.395),
        (0.61, 0.395),
        color="#1f77b4",
        lw=2.2,
        label="target volumes",
        label_offset=(0.0, 0.042),
    )
    arrow(
        ax,
        (0.61, 0.345),
        (0.39, 0.345),
        color="#c0392b",
        lw=2.2,
        label="pressures",
        label_offset=(0.0, -0.042),
    )
    arrow(ax, (0.755, 0.195), (0.755, 0.29), color="#ef8a00", lw=1.9)
    arrow(ax, (0.755, 0.46), (0.755, 0.50), color="#607d8b", lw=1.7)

    save(fig, FIGURES / "fig_2_0_pipeline_overview")


if __name__ == "__main__":
    main()
