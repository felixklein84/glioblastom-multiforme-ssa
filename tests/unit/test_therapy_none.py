"""NoTherapy: trivial pass-through; engine-with-NoTherapy ≡ run_baseline."""

import numpy as np

from gbm_ctmc.parameters import ModelParams
from gbm_ctmc.simulation import run_baseline, run_simulation
from gbm_ctmc.therapy import NoTherapy


def test_none_returns_empty():
    nt = NoTherapy()
    assert nt.extra_events_at(0.0) == []
    assert nt.breakpoints(0.0, 100.0) == []
    n = np.array([5, 50, 100, 2], dtype=np.int64)
    rng = np.random.default_rng(0)
    p = ModelParams.defaults()
    assert nt.pulse_at(10.0, n, p, rng) is None


def test_engine_with_none_matches_run_baseline():
    """run_simulation(params, NoTherapy()) must be identical to run_baseline(params)
    given the same seed — same RNG, same events, no schedule breakpoints."""
    p = ModelParams.defaults()
    p.run.seed = 1234
    p.run.t_end = 20.0

    baseline = run_baseline(p)
    via_engine = run_simulation(p, NoTherapy())

    tb, sb = baseline.to_arrays()
    te, se = via_engine.to_arrays()
    assert tb.shape == te.shape
    assert np.array_equal(sb, se)
    assert np.allclose(tb, te)
