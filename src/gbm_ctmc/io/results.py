"""CSV writers and readers for trajectories.

v0.1 uses CSV for simplicity and human-readability. Parquet may be adopted later
for large batch experiments (see architecture doc §13).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from gbm_ctmc.gillespie import Trajectory
from gbm_ctmc.states import State


def trajectory_to_dataframe(traj: Trajectory) -> pd.DataFrame:
    """Convert a Trajectory to a pandas DataFrame."""
    times, states = traj.to_arrays()
    df = pd.DataFrame(states, columns=State.labels())
    df.insert(0, "time", times)
    df["total"] = df[State.labels()].sum(axis=1)
    return df


def save_trajectory_csv(traj: Trajectory, path: str | Path) -> Path:
    """Write a trajectory to CSV. Creates parent directory if needed."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    df = trajectory_to_dataframe(traj)
    df.to_csv(p, index=False)
    return p


def load_trajectory_csv(path: str | Path) -> pd.DataFrame:
    """Read a trajectory CSV back into a DataFrame."""
    return pd.read_csv(path)
