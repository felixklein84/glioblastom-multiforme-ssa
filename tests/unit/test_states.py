"""State enum and Population container."""

import numpy as np

from gbm_ctmc.states import N_STATES, Population, State


def test_state_indices():
    assert State.S == 0
    assert State.P == 1
    assert State.D == 2
    assert State.Q == 3
    assert N_STATES == 4


def test_state_labels():
    assert State.labels() == ["S", "P", "D", "Q"]


def test_population_roundtrip():
    pop = Population(S=3, P=10, D=20, Q=1)
    arr = pop.to_array()
    assert arr.tolist() == [3, 10, 20, 1]
    assert pop.total == 34
    assert Population.from_array(arr) == pop


def test_population_from_numpy():
    arr = np.array([1, 2, 3, 4], dtype=np.int64)
    pop = Population.from_array(arr)
    assert pop == Population(1, 2, 3, 4)
