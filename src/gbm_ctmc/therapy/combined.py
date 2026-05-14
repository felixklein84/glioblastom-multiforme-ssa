"""Combined therapy — composition of multiple Therapy implementations.

``StuppTherapy`` is the canonical combination: RT + TMZ following the Stupp 2005
protocol. ``CombinedTherapy`` is the general form — any number of therapies are
delegated to in turn for events, breakpoints, and pulses.

This module contains no biology of its own. All effects come from the
constituent therapies. There is no synergy multiplier in v0.2 — combined effects
are strictly additive (extra events from each therapy are concatenated; pulses
from each fire independently).
"""

from __future__ import annotations

from typing import Sequence

import numpy as np

from gbm_ctmc.parameters import ModelParams
from gbm_ctmc.therapy.base import Therapy
from gbm_ctmc.transitions import Event


class CombinedTherapy:
    """Generic combination of multiple therapies."""

    def __init__(self, *therapies: Therapy):
        if not therapies:
            raise ValueError("CombinedTherapy requires at least one therapy")
        self.therapies: tuple[Therapy, ...] = tuple(therapies)
        self.name = "+".join(t.name for t in self.therapies)

    def extra_events_at(self, t: float) -> list[Event]:
        events: list[Event] = []
        for therapy in self.therapies:
            events.extend(therapy.extra_events_at(t))
        return events

    def breakpoints(self, t_lo: float, t_hi: float) -> list[float]:
        bps: list[float] = []
        for therapy in self.therapies:
            bps.extend(therapy.breakpoints(t_lo, t_hi))
        return bps

    def pulse_at(
        self,
        t: float,
        n: np.ndarray,
        params: ModelParams,
        rng: np.random.Generator,
    ) -> np.ndarray | None:
        """Apply each therapy's pulse in declaration order; return the composed
        result, or None if no constituent therapy fires a pulse at *t*."""
        result: np.ndarray | None = None
        current = n
        for therapy in self.therapies:
            updated = therapy.pulse_at(t, current, params, rng)
            if updated is not None:
                current = updated
                result = updated
        return result


class StuppTherapy(CombinedTherapy):
    """RT + TMZ in the Stupp 2005 schedule."""

    def __init__(self, rt: Therapy, tmz: Therapy):
        super().__init__(rt, tmz)
        self.name = "stupp"
