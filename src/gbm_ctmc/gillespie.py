"""Gillespie Stochastic Simulation Algorithm (SSA).

Algorithm (Kraut 2021, Baar 2016):
    1. Compute total rate R = Σ_e r_e(n)
    2. If R == 0: system is absorbed; stop
    3. Draw waiting time τ ~ Exp(R)
    4. Select event e with probability r_e(n) / R
    5. Apply event and advance time
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

import numpy as np

from gbm_ctmc.parameters import ModelParams
from gbm_ctmc.transitions import Event


@dataclass
class Trajectory:
    """Time-stamped sequence of population states."""

    times: list[float] = field(default_factory=list)
    states: list[np.ndarray] = field(default_factory=list)

    def append(self, t: float, n: np.ndarray) -> None:
        self.times.append(t)
        self.states.append(n.copy())

    def to_arrays(self) -> tuple[np.ndarray, np.ndarray]:
        return np.asarray(self.times), np.asarray(self.states)

    @property
    def is_extinct(self) -> bool:
        return len(self.states) > 0 and int(self.states[-1].sum()) == 0


def simulate(
    n0: np.ndarray,
    params: ModelParams,
    events: Sequence[Event],
    t_end: float,
    rng: np.random.Generator,
    max_steps: int = 10_000_000,
    t_start: float = 0.0,
) -> Trajectory:
    """Run the Gillespie SSA from *n0* at *t_start* to absolute time *t_end*.

    The trajectory always includes the initial state and the final state at the
    moment of termination (extinction, absorption, or t_end reached).

    Setting *t_start* lets callers stitch together piecewise SSA segments — the
    segmented engine uses this to swap the active event list across therapy
    schedule boundaries.
    """
    n = n0.astype(np.int64, copy=True)
    t = float(t_start)
    traj = Trajectory()
    traj.append(t, n)

    rates = np.empty(len(events), dtype=np.float64)

    for _ in range(max_steps):
        for i, e in enumerate(events):
            rates[i] = e.rate(n, params)

        R = float(rates.sum())
        if R <= 0.0:
            break  # absorbed (all-zero rates ⇒ all-zero state or fixed point)

        tau = rng.exponential(1.0 / R)
        t_next = t + tau
        if t_next > t_end:
            # Record the final state at t_end (state unchanged since last event)
            traj.append(t_end, n)
            return traj

        t = t_next
        idx = int(rng.choice(len(events), p=rates / R))
        n = events[idx].apply(n)
        traj.append(t, n)

        if int(n.sum()) == 0:
            break

    return traj
