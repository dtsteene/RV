"""Generate constitutive-law figures for the 3D mechanics chapter.

  fig_2_7_holzapfel_ogden.{png,pdf}  — stress-stretch response of the
                                       Holzapfel-Ogden constitutive law
                                       at the calibrated parameters.

Pure methodology: no simulation needed, just the closed-form derivatives
of the strain energy function. Run from RV/ root::

    python scripts/make_constitutive_figures.py
"""
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from style import save, setup  # noqa: E402

FIG_DIR = Path(__file__).resolve().parents[1] / "figures"

A, B = 2.280, 9.726
A_F, B_F = 1.685, 15.779

PHYS_LO, PHYS_HI = 0.85, 1.10


def psi_iso(lam):
    I1 = lam ** 2 + 2.0 / lam
    return (A / (2.0 * B)) * (np.exp(B * (I1 - 3.0)) - 1.0)


def psi_fiber(lam):
    arg = (lam ** 2 - 1.0) ** 2
    return (A_F / (2.0 * B_F)) * (np.exp(B_F * arg) - 1.0) * (lam >= 1.0)


def numerical_stress(psi_func, lam):
    h = 1e-5
    return (psi_func(lam + h) - psi_func(lam - h)) / (2.0 * h)


def main():
    setup()
    lam = np.linspace(0.85, 1.22, 400)

    sigma_iso = numerical_stress(psi_iso, lam)
    sigma_fiber = numerical_stress(psi_fiber, lam)
    sigma_along_fiber = sigma_iso + sigma_fiber
    sigma_transverse = sigma_iso

    fig, ax = plt.subplots(figsize=(6.0, 4.0))

    ax.axvspan(PHYS_LO, PHYS_HI, color="#dddddd", alpha=0.45, lw=0, zorder=0)
    ax.axvline(1.0, color="black", lw=0.5, alpha=0.5)
    ax.axhline(0.0, color="black", lw=0.5, alpha=0.5)

    ax.plot(lam, sigma_along_fiber, color="#c0392b", lw=2.0,
            label="Along fibre")
    ax.plot(lam, sigma_transverse, color="#666", lw=1.6, ls="--",
            label="Transverse")

    ax.set_xlabel(r"Stretch  $\lambda$")
    ax.set_ylabel(r"$\partial \Psi / \partial \lambda$  (kPa)")
    ax.set_xlim(0.85, 1.22)
    ax.set_ylim(-5, 105)
    ax.legend(loc="upper left", frameon=False)

    save(fig, FIG_DIR / "fig_2_7_holzapfel_ogden")
    plt.close(fig)
    print(f"Wrote fig_2_7_holzapfel_ogden.{{png,pdf}} to {FIG_DIR}")


if __name__ == "__main__":
    main()
