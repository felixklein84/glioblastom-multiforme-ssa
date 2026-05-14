"""Temozolomide therapy — continuous kill rate during treatment windows.

Modelled as extra CTMC death events (per state) and an extra P→Q dormancy event
active while *t* falls in any TMZ treatment window. Outside treatment windows
the therapy contributes no events.

The Stupp schedule (LIT) is concomitant phase [0, 42 d) followed by 6 adjuvant
cycles of 5/28-day on/off, starting at day 49. Kill rates are placeholders (ASM)
unless individually calibrated.
"""

from __future__ import annotations

import numpy as np

from gbm_ctmc.parameters import ModelParams, TemozolomideParams
from gbm_ctmc.states import State
from gbm_ctmc.therapy.schedule import is_in_any_window, window_breakpoints_in
from gbm_ctmc.transitions import Event

_S, _P, _D, _Q = int(State.S), int(State.P), int(State.D), int(State.Q)


class TemozolomideTherapy:
    name: str = "tmz"

    def __init__(self, params: TemozolomideParams):
        self.tmz = params
        self._windows = params.windows()

    def extra_events_at(self, t: float) -> list[Event]:
        if not is_in_any_window(t, self._windows):
            return []
        return _tmz_events()

    def breakpoints(self, t_lo: float, t_hi: float) -> list[float]:
        return window_breakpoints_in(self._windows, t_lo, t_hi)

    def pulse_at(self, t, n, params, rng):
        return None


def _move_p_to_q(n: np.ndarray) -> np.ndarray:
    out = n.copy()
    out[_P] -= 1
    out[_Q] += 1
    return out


def _dec(idx: int):
    def f(n: np.ndarray) -> np.ndarray:
        out = n.copy()
        out[idx] -= 1
        return out
    return f


def _tmz_events() -> list[Event]:
    """The 5 extra events active while TMZ is on."""
    return [
        Event(
            "S_tmz_kill",
            rate=lambda n, p: p.therapy.tmz.delta_S * n[_S],
            apply=_dec(_S),
        ),
        Event(
            "P_tmz_kill",
            rate=lambda n, p: p.therapy.tmz.delta_P * n[_P],
            apply=_dec(_P),
        ),
        Event(
            "D_tmz_kill",
            rate=lambda n, p: p.therapy.tmz.delta_D * n[_D],
            apply=_dec(_D),
        ),
        Event(
            "Q_tmz_kill",
            rate=lambda n, p: p.therapy.tmz.delta_Q * n[_Q],
            apply=_dec(_Q),
        ),
        Event(
            "P_to_Q_tmz_induced",
            rate=lambda n, p: p.therapy.tmz.sigma_T * n[_P],
            apply=_move_p_to_q,
        ),
    ]
