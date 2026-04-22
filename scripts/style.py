"""Shared matplotlib styling for thesis figures.

Usage::

    from style import setup, severity_palette, save

    setup()
    fig, ax = plt.subplots(figsize=(6, 4))
    # ... plot ...
    save(fig, "figures/fig_4_2_pv_loops_spectrum")
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

# Canonical severity ordering used throughout the thesis, from lightest to
# darkest. Internal keys match the archived JSON filenames in
# `data/ukb_circ_v2/`; the display labels are remapped to reflect the
# ACHIEVED hemodynamic classification under ESC 2022 thresholds, not the
# original optimization targets (see tuning.md "Calibration honesty").
#
# Notes on the remapping:
#   - `healthy_low` is shown as "Upper normal" (achieved mPAP 18.9, below
#     the ESC PH threshold of 20).
#   - `healthy` is shown as "Borderline PH" (achieved mPAP 20.7, just above
#     the threshold). The original "healthy" calibration does not reach
#     Kovacs-normal hemodynamics once the RV EDV target from the UKB mean
#     mesh is enforced; the optimizer defends EDV at the expense of RV ESP.
#   - The old `borderline` key (target mPAP 20.3, achieved 20.6) was
#     hemodynamically indistinguishable from the renamed `healthy` and
#     has been dropped from the spectrum. The JSON remains on disk as an
#     archival artifact.
SEVERITIES = [
    "healthy_low",
    "healthy",
    "mild",
    "moderate",
    "moderate_severe",
    "severe",
    "very_severe",
    "end_stage",
]

SEVERITY_LABELS = {
    "healthy_low": "Upper normal",
    "healthy": "Borderline PH",
    "mild": "Mild",
    "moderate": "Moderate",
    "moderate_severe": "Mod--severe",
    "severe": "Severe",
    "very_severe": "Very severe",
    "end_stage": "End-stage",
}


def setup() -> None:
    """Apply thesis-wide matplotlib defaults."""
    mpl.rcParams.update({
        # Typography — match MyST/LaTeX serif body text
        "font.family": "serif",
        "font.serif": ["DejaVu Serif", "Computer Modern Roman", "Times New Roman"],
        "mathtext.fontset": "cm",
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "figure.titlesize": 12,
        # Lines and markers
        "lines.linewidth": 1.6,
        "lines.markersize": 5,
        "axes.linewidth": 0.8,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        # Layout
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.linestyle": ":",
        "grid.linewidth": 0.5,
        "grid.alpha": 0.6,
        "figure.dpi": 100,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.facecolor": "white",
        "figure.facecolor": "white",
    })


def severity_palette(n: int = 8) -> list:
    """Return n perceptually ordered colors for severity levels."""
    cmap = mpl.colormaps["plasma"]
    # Avoid the very-bright endpoints
    return [cmap(0.10 + 0.75 * i / max(n - 1, 1)) for i in range(n)]


def save(fig: plt.Figure, stem: str | Path) -> None:
    """Save figure as PNG (for MyST web build) and PDF (for print)."""
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(stem.with_suffix(".png"))
    fig.savefig(stem.with_suffix(".pdf"))
