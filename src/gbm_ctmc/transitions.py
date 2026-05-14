"""Event catalogue for the CTMC.

An Event is a (name, rate function, apply function) triple. The Gillespie loop
evaluates all rates, samples one event proportional to its rate, and applies the
state change.

v0.1 contains only basal (no-therapy) events. Therapy events will be added in
later versions following the same pattern.

References:
    Baar 2016 SI — full infinitesimal generator structure
    Blath 2023   — dormancy event rates (σ, ϱ)
    Kraut 2021   — generator formula
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from gbm_ctmc.parameters import ModelParams
from gbm_ctmc.states import State

RateFn = Callable[[np.ndarray, ModelParams], float]
ApplyFn = Callable[[np.ndarray], np.ndarray]


@dataclass(frozen=True, slots=True)
class Event:
    name: str
    rate: RateFn
    apply: ApplyFn


def _inc(state: State) -> ApplyFn:
    idx = int(state)
    def f(n: np.ndarray) -> np.ndarray:
        out = n.copy()
        out[idx] += 1
        return out
    return f


def _dec(state: State) -> ApplyFn:
    idx = int(state)
    def f(n: np.ndarray) -> np.ndarray:
        out = n.copy()
        out[idx] -= 1
        return out
    return f


def _move(src: State, dst: State) -> ApplyFn:
    i, j = int(src), int(dst)
    def f(n: np.ndarray) -> np.ndarray:
        out = n.copy()
        out[i] -= 1
        out[j] += 1
        return out
    return f


# Convenience indices
_S, _P, _D, _Q = int(State.S), int(State.P), int(State.D), int(State.Q)


def basal_events() -> list[Event]:
    """Return the 13 basal CTMC events (no therapy).

    Rate functions close over the population vector and ModelParams. They are
    pure (no side effects) and inexpensive — safe to call at every Gillespie step.
    """
    return [
        Event(
            "S_division",
            rate=lambda n, p: p.basal.lambda_S * n[_S],
            apply=_inc(State.S),
        ),
        Event(
            "S_asymmetric_division",
            rate=lambda n, p: p.switching.alpha_S * n[_S],
            apply=_inc(State.P),
        ),
        Event(
            "S_natural_death",
            rate=lambda n, p: p.basal.mu_S * n[_S],
            apply=_dec(State.S),
        ),
        Event(
            "S_competition_death",
            rate=lambda n, p: p.basal.c_S * n[_S] * n.sum() / p.K,
            apply=_dec(State.S),
        ),
        Event(
            "S_to_P_commitment",
            rate=lambda n, p: p.switching.S_to_P * n[_S],
            apply=_move(State.S, State.P),
        ),
        Event(
            "P_division",
            rate=lambda n, p: p.basal.lambda_P * n[_P],
            apply=_inc(State.P),
        ),
        Event(
            "P_natural_death",
            rate=lambda n, p: p.basal.mu_P * n[_P],
            apply=_dec(State.P),
        ),
        Event(
            "P_competition_death",
            rate=lambda n, p: p.basal.c_P * n[_P] * n.sum() / p.K,
            apply=_dec(State.P),
        ),
        Event(
            "P_to_D_differentiation",
            rate=lambda n, p: p.switching.P_to_D * n[_P],
            apply=_move(State.P, State.D),
        ),
        Event(
            "P_to_Q_dormancy",
            rate=lambda n, p: p.switching.sigma * n[_P],
            apply=_move(State.P, State.Q),
        ),
        Event(
            "D_natural_death",
            rate=lambda n, p: p.basal.mu_D * n[_D],
            apply=_dec(State.D),
        ),
        Event(
            "Q_natural_death",
            rate=lambda n, p: p.basal.mu_Q * n[_Q],
            apply=_dec(State.Q),
        ),
        Event(
            "Q_to_P_resuscitation",
            rate=lambda n, p: p.switching.rho * n[_Q],
            apply=_move(State.Q, State.P),
        ),
    ]
