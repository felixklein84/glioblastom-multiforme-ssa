"""No-therapy baseline implementation of the Therapy protocol."""

from __future__ import annotations

import numpy as np

from gbm_ctmc.parameters import ModelParams
from gbm_ctmc.transitions import Event


class NoTherapy:
    name: str = "none"

    def extra_events_at(self, t: float) -> list[Event]:
        return []

    def breakpoints(self, t_lo: float, t_hi: float) -> list[float]:
        return []

    def pulse_at(
        self,
        t: float,
        n: np.ndarray,
        params: ModelParams,
        rng: np.random.Generator,
    ) -> np.ndarray | None:
        return None
