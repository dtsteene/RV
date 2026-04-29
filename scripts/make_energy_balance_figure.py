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

    # mJ for nicer numbers
    Eint_mJ  = E_internal * 1e3
    Ebnd_mJ  = E_boundary * 1e3
    Eext_mJ  = E_external * 1e3
    Erob_mJ  = E_robin   * 1e3

    fig, (axL, axR) = plt.subplots(
        1, 2, figsize=(8.6, 3.8),
        gridspec_kw={"width_ratios": [3.2, 1.0]},
    )

    # --- Panel A: identity closure -------------------------------------------
    axL.plot(time, Eint_mJ,  color="#c0392b", lw=2.6, label=r"tensor $\int_\Omega \mathbf{S}:\dot{\mathbf{E}}\,dV$")
    axL.plot(time, Ebnd_mJ,  color="#1f77b4", lw=1.4, label=r"cavity $\oint P\,dV$")
    axL.plot(time, Eext_mJ,  color="black",   lw=1.2, ls="--", label="cavity + Robin")
    axL.set_xlabel("time (s)")
    axL.set_ylabel("cumulative work (mJ)")
    axL.legend(frameon=False, fontsize=9, loc="upper right")
    for side in ("top", "right"):
        axL.spines[side].set_visible(False)
    axL.tick_params(direction="out", length=3)

    # --- Panel B: Robin work alone, magnified --------------------------------
    axR.axhline(0, color="lightgray", lw=0.6)
    axR.plot(time, Erob_mJ, color="#444444", lw=1.6, label=r"$W_\text{Robin}(t)$")
    axR.set_xlabel("time (s)")
    axR.set_ylabel(r"$W_\text{Robin}$ (mJ)")
    axR.legend(frameon=False, fontsize=9, loc="upper left")
    for side in ("top", "right"):
        axR.spines[side].set_visible(False)
    axR.tick_params(direction="out", length=3)

    # Panel B y-limits give the Robin curve plenty of room AND make
    # the horizontal-zero a visible reference.
    rob_max = max(abs(Erob_mJ.min()), abs(Erob_mJ.max()))
    pad = max(0.02, 0.25 * rob_max)
    axR.set_ylim(-pad, rob_max + pad)

    fig.tight_layout()
    png = OUT_DIR / "fig_energy_balance_validation.png"
    pdf = OUT_DIR / "fig_energy_balance_validation.pdf"
    fig.savefig(png, dpi=180)
    fig.savefig(pdf)
    print(f"wrote {png}")
    print(f"wrote {pdf}")
    print(f"balance_err = {balance_err_J:.3e} J  ({balance_err_rel:.3e} relative)")
    print(f"end-of-cycle: tensor={Eint_mJ[-1]:+.3f} mJ  cavity={Ebnd_mJ[-1]:+.3f} mJ  "
          f"Robin={Erob_mJ[-1]:+.3f} mJ  (Robin/|tensor|={abs(Erob_mJ[-1])/abs(Eint_mJ[-1])*100:.3f}%)")


if __name__ == "__main__":
    main()
