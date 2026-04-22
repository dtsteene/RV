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

# Holzapfel-Ogden parameters used in the thesis (kPa for the a's)
A, B = 0.33, 8.0
A_F, B_F = 0.876, 7.46
A_S, B_S = 0.485, 8.41
A_FS, B_FS = 0.216, 5.98
KAPPA = 10.0  # bulk modulus (kPa)


def stress_uniaxial_along(direction: str, lam: np.ndarray) -> np.ndarray:
    """First Piola stress along a given direction for an isochoric uniaxial stretch.

    For a stretch λ in the chosen direction with isochoric compensation
    (1/√λ in the orthogonal directions), C = diag(λ², 1/λ, 1/λ) when stretched
    along the first axis.  We compute the contribution of the isotropic and
    direction-specific anisotropic terms.
    """
    I1 = lam ** 2 + 2.0 / lam
    # Isotropic stress along the loading direction (Holzapfel-Ogden iso term)
    # dPsi_iso/dC = (a/2) exp(b(I1-3))
    # S_iso = 2 dPsi/dC, then convert to Cauchy/PK1 along the load direction.
    # For the simple display purpose we report the engineering stress
    # σ_eng = ∂Psi/∂λ in the loaded direction.
    # Use a small numerical derivative for clarity and generality.
    return None  # we use closed forms below for individual terms


def psi_iso(lam):
    I1 = lam ** 2 + 2.0 / lam
    return (A / (2.0 * B)) * (np.exp(B * (I1 - 3.0)) - 1.0)


def psi_fiber(lam):
    """Fiber loading: I_4f = lam^2."""
    arg = (lam ** 2 - 1.0) ** 2
    return (A_F / (2.0 * B_F)) * (np.exp(B_F * arg) - 1.0) * (lam >= 1.0)


def psi_sheet(lam):
    arg = (lam ** 2 - 1.0) ** 2
    return (A_S / (2.0 * B_S)) * (np.exp(B_S * arg) - 1.0) * (lam >= 1.0)


def numerical_stress(psi_func, lam):
    """First-order finite-difference stress dPsi/dlam (engineering stress)."""
    h = 1e-5
    return (psi_func(lam + h) - psi_func(lam - h)) / (2.0 * h)


def main():
    setup()
    lam = np.linspace(0.85, 1.30, 400)

    sigma_iso = numerical_stress(psi_iso, lam)
    sigma_fiber = numerical_stress(psi_fiber, lam)
    sigma_sheet = numerical_stress(psi_sheet, lam)
    # Total along fiber direction = isotropic + fiber anisotropic
    sigma_along_fiber = sigma_iso + sigma_fiber
    sigma_along_sheet = sigma_iso + sigma_sheet
    sigma_perp = sigma_iso  # isotropic-only response transverse to anisotropy

    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.plot(lam, sigma_along_fiber, color="#c0392b", lw=2.0,
            label=r"Along fiber  ($\Psi_{\rm iso} + \Psi_{f}$)")
    ax.plot(lam, sigma_along_sheet, color="#2c7fb8", lw=2.0,
            label=r"Along sheet  ($\Psi_{\rm iso} + \Psi_{s}$)")
    ax.plot(lam, sigma_perp, color="#888", lw=2.0, ls="--",
            label=r"Isotropic only  ($\Psi_{\rm iso}$)")
    ax.axvline(1.0, color="black", lw=0.5, alpha=0.5)
    ax.axhline(0.0, color="black", lw=0.5, alpha=0.5)
    ax.set_xlabel(r"Stretch  $\lambda$")
    ax.set_ylabel(r"Engineering stress  $\partial \Psi / \partial \lambda$  (kPa)")
    ax.set_xlim(0.85, 1.30)
    ax.set_ylim(-3, 35)
    ax.legend(loc="upper left", framealpha=0.95)
    ax.set_title("Holzapfel--Ogden response at the calibrated parameters")

    # Annotate the calibrated parameters in a small box
    ptext = (
        rf"$a={A}$ kPa, $b={B}$" "\n"
        rf"$a_f={A_F}$ kPa, $b_f={B_F}$" "\n"
        rf"$a_s={A_S}$ kPa, $b_s={B_S}$"
    )
    ax.text(0.97, 0.05, ptext, transform=ax.transAxes,
            ha="right", va="bottom", fontsize=8,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                      edgecolor="#bbb", alpha=0.95))

    save(fig, FIG_DIR / "fig_2_7_holzapfel_ogden")
    plt.close(fig)
    print(f"Wrote fig_2_7_holzapfel_ogden.{{png,pdf}} to {FIG_DIR}")


if __name__ == "__main__":
    main()
