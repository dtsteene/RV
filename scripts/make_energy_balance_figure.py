"""Generate the energy-balance validation figure for Chapter 1.

Extracts Panel 5 of `plot_loops.plot_engineering_debug` into a standalone figure
showing that the tensor stress power integral matches the sum of cavity PV-work
and Robin boundary work to numerical precision.

Usage:
    python make_energy_balance_figure.py

Input: metrics_downsample_1.npy from a completed simulation.
Output: figures/fig_energy_balance.{png,pdf} in the thesis root.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

# --- paths -------------------------------------------------------------------
METRICS = Path(
    "/global/D1/homes/dtsteene/cardiac-work/results/sims/2026-04-07/"
    "UKB_6beats_run_1017003/analysis/last_beat/metrics_downsample_1.npy"
)
OUT_DIR = Path(__file__).resolve().parent.parent / "figures"
OUT_DIR.mkdir(exist_ok=True)


def get_safe(metrics: dict, keys: list[str], n: int) -> np.ndarray:
    """Return first available key from `keys` or zeros of length `n`."""
    for k in keys:
        if k in metrics:
            return np.asarray(metrics[k])
    return np.zeros(n)


def main() -> None:
    metrics = np.load(METRICS, allow_pickle=True).item()
    time = np.asarray(metrics["time"])
    n = len(time)

    w_active = get_safe(metrics, ["work_active_Whole"], n)
    w_passive = get_safe(metrics, ["work_passive_Whole"], n)
    w_comp = get_safe(metrics, ["work_comp_Whole"], n)
    w_boundary = get_safe(metrics, ["work_boundary_exact_LV"], n) + get_safe(
        metrics, ["work_boundary_exact_RV"], n
    )
    w_robin = get_safe(metrics, ["work_robin_epi"], n) + get_safe(
        metrics, ["work_robin_base"], n
    )

    # align lengths defensively
    m = min(len(time), len(w_active), len(w_passive), len(w_comp), len(w_boundary), len(w_robin))
    time = time[:m]
    E_internal = np.cumsum(w_active[:m] + w_passive[:m] + w_comp[:m])
    E_boundary = np.cumsum(w_boundary[:m])
    E_robin = np.cumsum(w_robin[:m])
    E_external = E_boundary + E_robin

    balance_err_J = float(E_internal[-1] - E_external[-1])
    balance_err_rel = balance_err_J / max(abs(E_internal[-1]), 1e-30)

    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.plot(time, E_internal, color="#c0392b", lw=2.4, label="tensor work")
    ax.plot(time, E_external, color="black", lw=1.4, ls="--", label="boundary + Robin")

    ax.set_xlabel("time (s)")
    ax.set_ylabel("cumulative work (J)")
    ax.legend(frameon=False, fontsize=10, loc="upper right")

    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(direction="out", length=3)

    fig.tight_layout()
    png = OUT_DIR / "fig_energy_balance_validation.png"
    pdf = OUT_DIR / "fig_energy_balance_validation.pdf"
    fig.savefig(png, dpi=180)
    fig.savefig(pdf)
    print(f"wrote {png}")
    print(f"wrote {pdf}")
    print(f"balance_err = {balance_err_J:.3e} J  ({balance_err_rel:.3e} relative)")


if __name__ == "__main__":
    main()
