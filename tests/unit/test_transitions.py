"""Event catalogue: rate non-negativity, zero conditions, structural invariants."""

import numpy as np

from gbm_ctmc.parameters import ModelParams
from gbm_ctmc.transitions import basal_events


def test_basal_has_13_events():
    assert len(basal_events()) == 13


def test_rates_non_negative():
    p = ModelParams.defaults()
    n = np.array([5, 50, 100, 2], dtype=np.int64)
    for e in basal_events():
        assert e.rate(n, p) >= 0.0, e.name


def test_zero_state_zero_rates():
    p = ModelParams.defaults()
    n = np.zeros(4, dtype=np.int64)
    for e in basal_events():
        assert e.rate(n, p) == 0.0, e.name


def test_d_state_has_no_division_or_switching():
    """D cells should only undergo natural death — no division or switching events."""
    p = ModelParams.defaults()
    n_d_only = np.array([0, 0, 100, 0], dtype=np.int64)
    for e in basal_events():
        if e.name != "D_natural_death":
            assert e.rate(n_d_only, p) == 0.0, f"{e.name} should be zero with only D cells"


def test_q_state_only_dies_or_resuscitates():
    """Q cells: only natural death or Q→P resuscitation."""
    p = ModelParams.defaults()
    n_q_only = np.array([0, 0, 0, 50], dtype=np.int64)
    allowed = {"Q_natural_death", "Q_to_P_resuscitation"}
    for e in basal_events():
        if e.name not in allowed:
            assert e.rate(n_q_only, p) == 0.0, f"{e.name} should be zero with only Q cells"


def test_event_application_changes_total_by_at_most_one():
    """A single event changes total population by exactly -1, 0, or +1."""
    n = np.array([5, 50, 100, 2], dtype=np.int64)
    initial_total = int(n.sum())
    for e in basal_events():
        n_after = e.apply(n)
        delta = int(n_after.sum()) - initial_total
        assert delta in (-1, 0, 1), f"{e.name} changed total by {delta}"
        # Sanity: original vector untouched
        assert int(n.sum()) == initial_total


def test_event_application_preserves_non_negativity_when_source_present():
    """When applied to a state where the source cell exists, counts remain non-negative."""
    n = np.array([5, 50, 100, 2], dtype=np.int64)
    for e in basal_events():
        n_after = e.apply(n)
        assert (n_after >= 0).all(), f"{e.name} produced negative counts: {n_after}"
