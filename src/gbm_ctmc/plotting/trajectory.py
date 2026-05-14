"""Trajectory line plot — counts of S/P/D/Q + total over time."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from gbm_ctmc.plotting.style import STATE_COLORS, TOTAL_COLOR, apply
from gbm_ctmc.states import State


def plot_trajectory(
    df: pd.DataFrame,
    out_path: str | Path,
    title: str = "GBM CTMC baseline trajectory",
    log_y: bool = False,
) -> Path:
    """Plot a single trajectory as line counts per state + total.

    Expects columns: time, S, P, D, Q, total (as produced by
    `gbm_ctmc.io.results.trajectory_to_dataframe`).
    """
    apply()
    fig, ax = plt.subplots()

    for label in State.labels():
        ax.plot(df["time"], df[label], label=label, color=STATE_COLORS[label], linewidth=1.2)
    ax.plot(df["time"], df["total"], label="total", color=TOTAL_COLOR,
            linewidth=1.8, linestyle="--")

    ax.set_xlabel("time (days)")
    ax.set_ylabel("cell count")
    ax.set_title(title)
    ax.legend(loc="upper left", ncols=5)
    if log_y:
        ax.set_yscale("symlog", linthresh=1)

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    plt.close(fig)
    return out
