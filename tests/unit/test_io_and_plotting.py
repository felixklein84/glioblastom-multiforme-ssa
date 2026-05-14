"""CSV round-trip and plot file creation."""

from pathlib import Path

import numpy as np

from gbm_ctmc.io.results import (
    load_trajectory_csv,
    save_trajectory_csv,
    trajectory_to_dataframe,
)
from gbm_ctmc.parameters import ModelParams
from gbm_ctmc.plotting.trajectory import plot_trajectory
from gbm_ctmc.simulation import run_baseline


def _short_traj():
    p = ModelParams.defaults()
    p.run.seed = 42
    p.run.t_end = 20.0
    return run_baseline(p)


def test_trajectory_to_dataframe_columns():
    df = trajectory_to_dataframe(_short_traj())
    assert list(df.columns) == ["time", "S", "P", "D", "Q", "total"]
    assert (df["total"] == df[["S", "P", "D", "Q"]].sum(axis=1)).all()
    assert df["time"].iloc[0] == 0.0


def test_save_and_load_csv(tmp_path: Path):
    traj = _short_traj()
    csv_path = tmp_path / "traj.csv"
    save_trajectory_csv(traj, csv_path)
    assert csv_path.exists() and csv_path.stat().st_size > 0

    df_back = load_trajectory_csv(csv_path)
    df_orig = trajectory_to_dataframe(traj)
    assert list(df_back.columns) == list(df_orig.columns)
    assert len(df_back) == len(df_orig)
    assert np.allclose(df_back["time"], df_orig["time"])


def test_plot_trajectory_creates_png(tmp_path: Path):
    df = trajectory_to_dataframe(_short_traj())
    out = plot_trajectory(df, tmp_path / "fig.png")
    assert out.exists()
    assert out.stat().st_size > 0
