"""Single-trajectory simulation runners.

``run_baseline`` is the no-therapy convenience function (kept for v0.1 callers).
``run_simulation`` is the general entry point: it takes a ``Therapy`` and walks
the Gillespie SSA across schedule breakpoints, applying pulses at the boundaries.
"""

from __future__ import annotations

import numpy as np

from gbm_ctmc.gillespie import Trajectory, simulate
from gbm_ctmc.parameters import ModelParams
from gbm_ctmc.therapy import Therapy, build_therapy
from gbm_ctmc.transitions import basal_events


def _initial_state(params: ModelParams) -> np.ndarray:
    return np.array(
        [params.initial.S, params.initial.P, params.initial.D, params.initial.Q],
        dtype=np.int64,
    )


def run_baseline(params: ModelParams) -> Trajectory:
    """Run a no-therapy baseline. Equivalent to ``run_simulation`` with NoTherapy."""
    rng = np.random.default_rng(params.run.seed)
    n0 = _initial_state(params)
    return simulate(
        n0=n0,
        params=params,
        events=basal_events(),
        t_end=params.run.t_end,
        rng=rng,
        max_steps=params.run.max_steps,
    )


def run_simulation(
    params: ModelParams,
    therapy: Therapy | None = None,
) -> Trajectory:
    """Run one trajectory under the given (or YAML-derived) therapy.

    The horizon is split into segments at therapy breakpoints; the SSA runs
    inside each segment with the active event list, and any pulse at the
    boundary is applied between segments. Reproducible from ``params.run.seed``.
    """
    if therapy is None:
        therapy = build_therapy(params)

    rng = np.random.default_rng(params.run.seed)
    t_end = float(params.run.t_end)
    max_steps = params.run.max_steps

    n = _initial_state(params)
    t = 0.0
    full = Trajectory()
    full.append(t, n)

    # Sorted, deduplicated, in-range breakpoints + the final time
    raw_bps = therapy.breakpoints(0.0, t_end)
    boundaries = sorted({round(b, 9) for b in raw_bps if 0.0 < b <= t_end})
    boundaries.append(t_end)

    for next_t in boundaries:
        if next_t <= t:
            continue

        events = basal_events() + list(therapy.extra_events_at(t))
        segment = simulate(
            n0=n,
            params=params,
            events=events,
            t_end=next_t,
            rng=rng,
            max_steps=max_steps,
            t_start=t,
        )
        # Append everything from the segment except its first point (== t, n)
        for ts, ns in zip(segment.times[1:], segment.states[1:]):
            full.append(ts, ns)

        n = segment.states[-1].copy()
        t = next_t

        if int(n.sum()) == 0:
            break

        # Apply any pulse exactly at the breakpoint
        pulsed = therapy.pulse_at(t, n, params, rng)
        if pulsed is not None:
            n = pulsed
            full.append(t, n)
            if int(n.sum()) == 0:
                break

    return full
