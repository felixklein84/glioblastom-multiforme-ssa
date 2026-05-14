"""Cell state definitions and population vector type.

4-state hierarchy (Lan 2017 + Blath 2023):
    S — Glioma stem cell (slow-cycling, therapy-resistant)
    P — Progenitor (fast-cycling, therapy-sensitive)
    D — Differentiated (post-mitotic)
    Q — Quiescent / dormant (cell-cycle arrested)
"""

from __future__ import annotations

from enum import IntEnum
from typing import NamedTuple

import numpy as np


class State(IntEnum):
    S = 0
    P = 1
    D = 2
    Q = 3

    @classmethod
    def labels(cls) -> list[str]:
        return [s.name for s in cls]


N_STATES = len(State)


class Population(NamedTuple):
    """Immutable snapshot of cell counts."""

    S: int
    P: int
    D: int
    Q: int

    def to_array(self) -> np.ndarray:
        return np.array([self.S, self.P, self.D, self.Q], dtype=np.int64)

    @classmethod
    def from_array(cls, arr: np.ndarray) -> "Population":
        return cls(int(arr[0]), int(arr[1]), int(arr[2]), int(arr[3]))

    @property
    def total(self) -> int:
        return self.S + self.P + self.D + self.Q
