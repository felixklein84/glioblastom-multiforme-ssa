"""Same seed → identical trajectory. Different seed → different trajectory."""

import numpy as np

from gbm_ctmc.parameters import ModelParams
from gbm_ctmc.simulation import run_baseline


def _run_with_seed(seed: int):
    p = ModelParams.defaults()
    p.run.seed = seed
    p.run.t_end = 30.0
    return run_baseline(p)


def test_same_seed_reproduces_trajectory():
    a = _run_with_seed(123)
    b = _run_with_seed(123)
    ta, sa = a.to_arrays()
    tb, sb = b.to_arrays()
    assert ta.shape == tb.shape
    assert np.array_equal(sa, sb)
    assert np.allclose(ta, tb)


def test_different_seed_changes_trajectory():
    a = _run_with_seed(1)
    b = _run_with_seed(2)
    ta, sa = a.to_arrays()
    tb, sb = b.to_arrays()
    # Either different number of events, or different sequence of states
    if ta.shape == tb.shape:
        assert not np.array_equal(sa, sb)
