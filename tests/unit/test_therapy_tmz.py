"""Temozolomide module — windows, event activation, end-to-end run."""

import numpy as np

from gbm_ctmc.parameters import ModelParams, TemozolomideParams
from gbm_ctmc.simulation import run_simulation
from gbm_ctmc.therapy import TemozolomideTherapy


def test_stupp_schedule_windows_count():
    """Concomitant + 6 adjuvant cycles = 7 windows."""
    tmz = TemozolomideParams()
    wins = tmz.windows()
    assert len(wins) == 1 + tmz.adjuvant_cycles
    assert wins[0] == (0.0, 42.0)
    assert wins[1] == (49.0, 54.0)
    assert wins[-1] == (49.0 + 5 * 28.0, 49.0 + 5 * 28.0 + 5.0)


def test_extra_events_inside_and_outside_windows():
    tmz = TemozolomideTherapy(TemozolomideParams())
    assert len(tmz.extra_events_at(10.0)) == 5    # inside concomitant
    assert len(tmz.extra_events_at(45.0)) == 0    # in recovery gap
    assert len(tmz.extra_events_at(51.0)) == 5    # inside adjuvant cycle 1
    assert len(tmz.extra_events_at(54.0)) == 0    # at window edge (half-open)


def test_tmz_breakpoints_contain_window_edges():
    tmz = TemozolomideTherapy(TemozolomideParams())
    bps = tmz.breakpoints(0.0, 60.0)
    # Concomitant end and adjuvant cycle 1 start/end must appear
    for expected in (42.0, 49.0, 54.0):
        assert expected in bps


def test_no_pulse_for_tmz():
    tmz = TemozolomideTherapy(TemozolomideParams())
    n = np.array([5, 50, 100, 2], dtype=np.int64)
    p = ModelParams.defaults()
    assert tmz.pulse_at(10.0, n, p, np.random.default_rng(0)) is None


def test_tmz_event_rates_zero_outside_window_when_not_appended():
    """Sanity: tmz extra_events list is empty outside windows → engine adds nothing extra."""
    tmz = TemozolomideTherapy(TemozolomideParams())
    assert tmz.extra_events_at(46.0) == []


def test_tmz_run_reduces_p_relative_to_baseline():
    p_no = ModelParams.defaults()
    p_no.run.seed = 11
    p_no.run.t_end = 45.0
    p_no.therapy.type = "none"
    traj_no = run_simulation(p_no)
    final_p_no = int(traj_no.states[-1][1])

    p_tmz = ModelParams.defaults()
    p_tmz.run.seed = 11
    p_tmz.run.t_end = 45.0
    p_tmz.therapy.type = "tmz"
    p_tmz.therapy.tmz.delta_P = 0.5  # aggressive kill for a detectable single-run effect
    traj_tmz = run_simulation(p_tmz)
    final_p_tmz = int(traj_tmz.states[-1][1])

    assert final_p_tmz < final_p_no, (
        f"Aggressive TMZ should reduce P (no_therapy={final_p_no}, TMZ={final_p_tmz})"
    )
