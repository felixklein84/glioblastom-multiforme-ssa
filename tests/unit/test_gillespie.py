"""Gillespie SSA: mechanics, monotonicity, termination."""

import numpy as np

from gbm_ctmc.gillespie import simulate
from gbm_ctmc.parameters import ModelParams
from gbm_ctmc.transitions import basal_events


def _short_run(seed: int = 0, t_end: float = 30.0):
    p = ModelParams.defaults()
    rng = np.random.default_rng(seed)
    n0 = np.array([5, 50, 100, 2], dtype=np.int64)
    return simulate(n0, p, basal_events(), t_end=t_end, rng=rng, max_steps=200_000)


def test_simulate_returns_trajectory_with_initial_state():
    traj = _short_run()
    assert len(traj.times) >= 1
    assert traj.times[0] == 0.0
    assert traj.states[0].tolist() == [5, 50, 100, 2]


def test_times_monotone_non_decreasing():
    traj = _short_run()
    times = np.asarray(traj.times)
    assert (np.diff(times) >= 0).all()


def test_counts_non_negative():
    traj = _short_run()
    _, states = traj.to_arrays()
    assert (states >= 0).all()


def test_simulate_respects_t_end():
    traj = _short_run(seed=1, t_end=10.0)
    assert traj.times[-1] <= 10.0 + 1e-12


def test_each_step_changes_total_by_at_most_one():
    traj = _short_run(seed=2, t_end=15.0)
    _, states = traj.to_arrays()
    totals = states.sum(axis=1)
    deltas = np.diff(totals)
    assert set(deltas.tolist()).issubset({-1, 0, 1}), (
        f"Single-event SSA must change total by -1/0/1, got deltas {set(deltas)}"
    )


def test_extinction_on_zero_initial_state():
    p = ModelParams.defaults()
    rng = np.random.default_rng(0)
    n0 = np.zeros(4, dtype=np.int64)
    traj = simulate(n0, p, basal_events(), t_end=10.0, rng=rng)
    assert traj.is_extinct
    assert len(traj.times) == 1  # only the initial state
