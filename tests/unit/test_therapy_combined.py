"""Combined / Stupp therapy — composition correctness and config wiring."""

import numpy as np

from gbm_ctmc.parameters import ModelParams, RadiotherapyParams, TemozolomideParams
from gbm_ctmc.simulation import run_simulation
from gbm_ctmc.therapy import (
    CombinedTherapy,
    RadiotherapyTherapy,
    StuppTherapy,
    TemozolomideTherapy,
    build_therapy,
)


def test_combined_extra_events_unions_constituents():
    rt = RadiotherapyTherapy(RadiotherapyParams())
    tmz = TemozolomideTherapy(TemozolomideParams())
    stupp = StuppTherapy(rt, tmz)

    # Inside TMZ window: 0 (RT continuous) + 5 (TMZ continuous) = 5
    assert len(stupp.extra_events_at(10.0)) == 5
    # Outside any TMZ window: 0 + 0 = 0
    assert len(stupp.extra_events_at(46.0)) == 0


def test_combined_breakpoints_union_of_constituents():
    rt = RadiotherapyTherapy(RadiotherapyParams(start_day=1.0, n_fractions=3,
                                                 interval_days=1.0))
    tmz = TemozolomideTherapy(TemozolomideParams())
    stupp = StuppTherapy(rt, tmz)

    bps = set(stupp.breakpoints(0.0, 60.0))
    # RT fractions
    for ft in (1.0, 2.0, 3.0):
        assert ft in bps
    # TMZ window edges
    for edge in (42.0, 49.0, 54.0):
        assert edge in bps


def test_combined_pulse_delegates_to_rt():
    """At an RT fraction time the pulse fires; at non-fraction times no pulse."""
    rt_params = RadiotherapyParams(start_day=1.0, n_fractions=2, interval_days=1.0,
                                    kappa_P=0.5, sigma_T_per_fraction=0.0)
    rt = RadiotherapyTherapy(rt_params)
    tmz = TemozolomideTherapy(TemozolomideParams())
    stupp = StuppTherapy(rt, tmz)

    n = np.array([10, 100, 50, 5], dtype=np.int64)
    rng = np.random.default_rng(0)
    p = ModelParams.defaults()

    assert stupp.pulse_at(1.5, n, p, rng) is None
    out = stupp.pulse_at(1.0, n, p, rng)
    assert out is not None
    assert out[1] <= n[1]  # P reduced by RT kill


def test_combined_name_composes_constituents():
    rt = RadiotherapyTherapy(RadiotherapyParams())
    tmz = TemozolomideTherapy(TemozolomideParams())
    c = CombinedTherapy(rt, tmz)
    assert c.name == "radiotherapy+tmz"
    s = StuppTherapy(rt, tmz)
    assert s.name == "stupp"


def test_build_therapy_factory_dispatches_on_type():
    p = ModelParams.defaults()
    p.therapy.type = "none"
    assert build_therapy(p).name == "none"
    p.therapy.type = "radiotherapy"
    assert build_therapy(p).name == "radiotherapy"
    p.therapy.type = "tmz"
    assert build_therapy(p).name == "tmz"
    p.therapy.type = "stupp"
    assert build_therapy(p).name == "stupp"


def test_stupp_run_reduces_burden_relative_to_baseline():
    p_no = ModelParams.defaults()
    p_no.run.seed = 21
    p_no.run.t_end = 50.0
    p_no.therapy.type = "none"
    traj_no = run_simulation(p_no)
    final_total_no = int(traj_no.states[-1].sum())

    p_st = ModelParams.defaults()
    p_st.run.seed = 21
    p_st.run.t_end = 50.0
    p_st.therapy.type = "stupp"
    # Aggressive combined kill to ensure the single-run effect is detectable
    p_st.therapy.radiotherapy.kappa_P = 0.4
    p_st.therapy.tmz.delta_P = 0.4
    traj_st = run_simulation(p_st)
    final_total_st = int(traj_st.states[-1].sum())

    assert final_total_st < final_total_no, (
        f"Aggressive Stupp should reduce total burden "
        f"(no_therapy={final_total_no}, stupp={final_total_st})"
    )


def test_combined_pulse_is_none_when_no_constituent_pulses():
    """At a time with no RT fraction, neither RT nor TMZ should produce a pulse."""
    rt = RadiotherapyTherapy(RadiotherapyParams(start_day=1.0, n_fractions=2,
                                                 interval_days=1.0))
    tmz = TemozolomideTherapy(TemozolomideParams())
    stupp = StuppTherapy(rt, tmz)

    n = np.array([5, 50, 100, 2], dtype=np.int64)
    rng = np.random.default_rng(0)
    p = ModelParams.defaults()
    assert stupp.pulse_at(20.0, n, p, rng) is None
