"""Radiotherapy module — pulse breakpoints, kill mechanics, end-to-end run."""

import numpy as np

from gbm_ctmc.parameters import ModelParams, RadiotherapyParams
from gbm_ctmc.simulation import run_simulation
from gbm_ctmc.therapy import RadiotherapyTherapy
from gbm_ctmc.therapy.radiotherapy import apply_rt_fraction


def test_fraction_times_match_schedule():
    rt = RadiotherapyParams(start_day=1.0, n_fractions=5, interval_days=2.0)
    assert rt.fraction_times == [1.0, 3.0, 5.0, 7.0, 9.0]


def test_breakpoints_are_fraction_times_in_range():
    rt = RadiotherapyTherapy(RadiotherapyParams(start_day=1.0, n_fractions=5,
                                                interval_days=1.0))
    bps = rt.breakpoints(0.0, 10.0)
    assert bps == [1.0, 2.0, 3.0, 4.0, 5.0]


def test_no_continuous_events():
    rt = RadiotherapyTherapy(RadiotherapyParams())
    assert rt.extra_events_at(0.0) == []
    assert rt.extra_events_at(1.5) == []


def test_pulse_fires_only_at_fraction_times():
    rt_params = RadiotherapyParams(start_day=2.0, n_fractions=3, interval_days=1.0,
                                    kappa_S=0.5, kappa_P=0.5, kappa_D=0.5, kappa_Q=0.5,
                                    sigma_T_per_fraction=0.0)
    rt = RadiotherapyTherapy(rt_params)
    n = np.array([10, 10, 10, 10], dtype=np.int64)
    p = ModelParams.defaults()
    rng = np.random.default_rng(0)

    # No pulse at a non-fraction time
    assert rt.pulse_at(1.5, n, p, rng) is None
    # Pulse at fraction time
    out = rt.pulse_at(2.0, n, p, rng)
    assert out is not None
    assert out.sum() <= n.sum()


def test_apply_rt_fraction_kills_with_p1():
    """κ=1.0 should kill all cells in that state deterministically."""
    rt = RadiotherapyParams(kappa_S=1.0, kappa_P=1.0, kappa_D=1.0, kappa_Q=1.0,
                            sigma_T_per_fraction=0.0)
    n = np.array([10, 20, 30, 5], dtype=np.int64)
    out = apply_rt_fraction(n, rt, np.random.default_rng(0))
    assert out.tolist() == [0, 0, 0, 0]


def test_apply_rt_fraction_no_kill_with_p0():
    """κ=0 leaves population unchanged (modulo dormancy transfer)."""
    rt = RadiotherapyParams(kappa_S=0.0, kappa_P=0.0, kappa_D=0.0, kappa_Q=0.0,
                            sigma_T_per_fraction=0.0)
    n = np.array([10, 20, 30, 5], dtype=np.int64)
    out = apply_rt_fraction(n, rt, np.random.default_rng(0))
    assert out.tolist() == n.tolist()


def test_apply_rt_fraction_dormancy_transfers_only_p_to_q():
    """sigma_T=1, κ=0 → all P move to Q; S, D unchanged."""
    rt = RadiotherapyParams(kappa_S=0.0, kappa_P=0.0, kappa_D=0.0, kappa_Q=0.0,
                            sigma_T_per_fraction=1.0)
    n = np.array([10, 20, 30, 5], dtype=np.int64)
    out = apply_rt_fraction(n, rt, np.random.default_rng(0))
    assert out[0] == 10              # S unchanged
    assert out[1] == 0                # all P moved
    assert out[2] == 30              # D unchanged
    assert out[3] == 25               # 5 + 20


def test_rt_run_reduces_p_relative_to_baseline():
    """Run a short scenario: RT should reduce final P relative to no therapy."""
    p_no = ModelParams.defaults()
    p_no.run.seed = 7
    p_no.run.t_end = 40.0
    p_no.therapy.type = "none"
    traj_no = run_simulation(p_no)
    final_p_no = int(traj_no.states[-1][1])

    p_rt = ModelParams.defaults()
    p_rt.run.seed = 7
    p_rt.run.t_end = 40.0
    p_rt.therapy.type = "radiotherapy"
    # Aggressive RT to make the effect detectable in a single run
    p_rt.therapy.radiotherapy.kappa_P = 0.5
    p_rt.therapy.radiotherapy.n_fractions = 20
    traj_rt = run_simulation(p_rt)
    final_p_rt = int(traj_rt.states[-1][1])

    assert final_p_rt < final_p_no, (
        f"Aggressive RT should reduce P (no_therapy={final_p_no}, RT={final_p_rt})"
    )
