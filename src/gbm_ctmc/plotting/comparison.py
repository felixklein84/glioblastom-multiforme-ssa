"""Multi-scenario comparison plot.

Overlays one chosen series (default: total tumor burden) across multiple
scenarios on a single axis. Trajectories are step-resampled to a uniform daily
grid so that visually adjacent lines are comparable, not jagged.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from gbm_ctmc.plotting.style import apply

# Distinct categorical palette for scenario lines
_SCENARIO_PALETTE = [
    "#444444",   # no therapy — grey
    "#1f77b4",   # RT          — blue
    "#d62728",   # TMZ         — red
    "#2ca02c",   # combined    — green
    "#9467bd",   # +TTF        — purple (future)
]


def _resample_step(times: np.ndarray, values: np.ndarray, grid: np.ndarray) -> np.ndarray:
    """Step (zero-order hold) resampling — counts are piecewise constant between events."""
    idx = np.searchsorted(times, grid, side="right") - 1
    idx = np.clip(idx, 0, len(values) - 1)
    return values[idx]


def plot_comparison(
    scenarios: dict[str, pd.DataFrame],
    out_path: str | Path,
    column: str = "total",
    title: str = "Therapy comparison — total tumor burden",
    log_y: bool = False,
    dt: float = 1.0,
) -> Path:
    """Overlay *column* across multiple scenarios on a daily grid.

    Parameters
    ----------
    scenarios:
        Mapping ``{scenario_name: trajectory_dataframe}``. Each DataFrame must
        have a ``time`` column and the requested *column*.
    out_path:
        Where to write the PNG. Parent directory is created if needed.
    column:
        Which series to plot (default ``"total"``; also ``"S"``, ``"P"``, etc.).
    """
    apply()
    fig, ax = plt.subplots()

    t_max = max(float(df["time"].iloc[-1]) for df in scenarios.values())
    grid = np.arange(0.0, t_max + dt, dt)

    for i, (name, df) in enumerate(scenarios.items()):
        times = df["time"].to_numpy()
        values = df[column].to_numpy()
        y = _resample_step(times, values, grid)
        color = _SCENARIO_PALETTE[i % len(_SCENARIO_PALETTE)]
        ax.plot(grid, y, label=name, color=color, linewidth=1.5)

    ax.set_xlabel("time (days)")
    ax.set_ylabel(column)
    ax.set_title(title)
    ax.legend(loc="best")
    if log_y:
        ax.set_yscale("symlog", linthresh=1)

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    plt.close(fig)
    return out
