from __future__ import annotations

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from circulation.regazzoni2020 import Regazzoni2020
from style import save, setup


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
MMHG_ML_TO_J = 133.322e-6


def last_beat(history: dict[str, list[float]], heart_rate_hz: float) -> slice:
    time = np.asarray(history["time"], dtype=float)
    cycle_length = 1.0 / heart_rate_hz
    start = time[-1] - cycle_length
    i0 = int(np.searchsorted(time, start, side="left"))
    return slice(i0, len(time))


def add_arrow(ax, x: np.ndarray, y: np.ndarray, frac: float, color: str) -> None:
    i = int(frac * (len(x) - 2))
    ax.annotate(
        "",
        xy=(x[i + 1], y[i + 1]),
        xytext=(x[i], y[i]),
        arrowprops={"arrowstyle": "->", "lw": 1.6, "color": color},
    )


def main() -> None:
    logging.getLogger("circulation").setLevel(logging.WARNING)
    setup()

    model = Regazzoni2020(add_units=False, verbose=False)
    history = model.solve(num_beats=10)
    beat = last_beat(history, float(model.parameters["HR"]))

    volume = np.asarray(history["V_LV"], dtype=float)[beat]
    pressure = np.asarray(history["p_LV"], dtype=float)[beat]

    pump_work = -np.trapezoid(pressure, volume) * MMHG_ML_TO_J
    edv = float(volume.max())
    esv = float(volume.min())
    sv = edv - esv
    ef = 100.0 * sv / edv

    fig, ax = plt.subplots(figsize=(5.2, 3.7))
    color = "#1f6f9f"

    ax.fill(volume, pressure, color=color, alpha=0.10, lw=0)
    ax.plot(volume, pressure, color=color, lw=2.0)
    add_arrow(ax, volume, pressure, 0.55, color)

    ax.text(0.50, 0.43, "stroke work", transform=ax.transAxes, ha="center", va="center", fontsize=10, color="#24475a")

    ax.set_xlabel("LV volume (mL)")
    ax.set_ylabel("LV pressure (mmHg)")
    ax.set_xlim(esv - 12, edv + 12)
    ax.set_ylim(0, max(pressure) + 12)
    ax.grid(False)

    save(fig, FIGURES / "fig_1_0_lv_pv_loop_regazzoni_default")
    print(f"LV EDV={edv:.1f} mL, ESV={esv:.1f} mL, SV={sv:.1f} mL, EF={ef:.1f}%, work={pump_work:.3f} J")


if __name__ == "__main__":
    main()
