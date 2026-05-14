"""Schedule primitives shared by therapy modules."""

from __future__ import annotations

from typing import Iterable


def is_in_any_window(t: float, windows: Iterable[tuple[float, float]]) -> bool:
    """True iff *t* lies in any half-open window [start, end)."""
    return any(start <= t < end for start, end in windows)


def window_breakpoints_in(
    windows: Iterable[tuple[float, float]],
    t_lo: float,
    t_hi: float,
) -> list[float]:
    """Edges of *windows* (both start and end) lying in (t_lo, t_hi]."""
    edges: list[float] = []
    for start, end in windows:
        if t_lo < start <= t_hi:
            edges.append(start)
        if t_lo < end <= t_hi:
            edges.append(end)
    return edges


def pulse_breakpoints_in(
    times: Iterable[float],
    t_lo: float,
    t_hi: float,
) -> list[float]:
    """Pulse times in (t_lo, t_hi]."""
    return [float(t) for t in times if t_lo < t <= t_hi]
