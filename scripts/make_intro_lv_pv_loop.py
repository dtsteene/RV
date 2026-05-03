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

    v_lv = np.asarray(history["V_LV"], dtype=float)[beat]
    p_lv = np.asarray(history["p_LV"], dtype=float)[beat]
    v_rv = np.asarray(history["V_RV"], dtype=float)[beat]
    p_rv = np.asarray(history["p_RV"], dtype=float)[beat]

    fig, (ax_lv, ax_rv) = plt.subplots(1, 2, sharey=True, figsize=(8.6, 3.7))

    panels = (
        (ax_lv, v_lv, p_lv, "#1f6f9f", "Left ventricle"),
        (ax_rv, v_rv, p_rv, "#b04a3a", "Right ventricle"),
    )

    for ax, v, p, color, title in panels:
        ax.fill(v, p, color=color, alpha=0.10, lw=0)
        ax.plot(v, p, color=color, lw=2.0)
        add_arrow(ax, v, p, 0.55, color)
        ax.set_title(title)
        ax.set_xlabel("Volume (mL)")
        ax.text(
            float(np.mean(v)), float(np.mean(p)), "stroke work",
            ha="center", va="center", fontsize=10, color="#24475a",
        )
        ax.grid(False)

    ax_lv.set_ylabel("Pressure (mmHg)")
    ax_lv.set_ylim(0, max(p_lv.max(), p_rv.max()) + 12)

    v_min = min(v_lv.min(), v_rv.min()) - 12
    v_max = max(v_lv.max(), v_rv.max()) + 12
    for ax in (ax_lv, ax_rv):
        ax.set_xlim(v_min, v_max)

    save(fig, FIGURES / "fig_1_0_pv_loops_regazzoni_default")

    sw_lv = -np.trapezoid(p_lv, v_lv) * MMHG_ML_TO_J
    sw_rv = -np.trapezoid(p_rv, v_rv) * MMHG_ML_TO_J
    print(f"LV: SW={sw_lv:.3f} J, peak P={p_lv.max():.0f} mmHg, "
          f"EDV={v_lv.max():.0f} mL, ESV={v_lv.min():.0f} mL")
    print(f"RV: SW={sw_rv:.3f} J, peak P={p_rv.max():.0f} mmHg, "
          f"EDV={v_rv.max():.0f} mL, ESV={v_rv.min():.0f} mL")


if __name__ == "__main__":
    main()
