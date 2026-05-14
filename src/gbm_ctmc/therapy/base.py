"""The Therapy protocol.

A therapy is a stateless object that tells the simulation engine three things:

1. Which extra CTMC events are active at any time *t* (e.g. TMZ kill rates during
   a treatment window).
2. The set of "breakpoints" — times in the simulation horizon where the active
   event list changes or a discrete pulse fires. The engine stops the SSA at
   each breakpoint, swaps event lists, applies any pulse, and resumes.
3. Whether a discrete pulse fires at a specific time, and if so how to apply it
   to the current population (e.g. RT fractional kill is a Binomial draw).

Basal events are added by the engine, not by the therapy — this keeps
composition (Stupp = RT + TMZ) free of duplicate basal events.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

import numpy as np

from gbm_ctmc.parameters import ModelParams
from gbm_ctmc.transitions import Event


@runtime_checkable
class Therapy(Protocol):
    """Interface implemented by every therapy module."""

    name: str

    def extra_events_at(self, t: float) -> list[Event]:
        """CTMC events active at time *t*, **excluding** basal events.

        The engine concatenates this with ``basal_events()`` before running an
        SSA segment.
        """
        ...

    def breakpoints(self, t_lo: float, t_hi: float) -> list[float]:
        """Sorted times in (*t_lo*, *t_hi*] where the event list changes or a
        pulse fires. The engine schedules SSA segments between consecutive
        breakpoints, applies any pulse at the breakpoint, and re-evaluates
        ``extra_events_at`` for the next segment.
        """
        ...

    def pulse_at(
        self,
        t: float,
        n: np.ndarray,
        params: ModelParams,
        rng: np.random.Generator,
    ) -> np.ndarray | None:
        """If a discrete pulse fires exactly at *t*, return the new population
        vector. Otherwise return None.

        Distinct from CTMC events: pulses fire at deterministic times (e.g. RT
        fractions) and apply non-incremental changes (e.g. Binomial kill).
        """
        ...
