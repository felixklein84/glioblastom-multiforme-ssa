"""Radiotherapy module — Stupp-style fractionated RT.

Modelled as **discrete fractional kill pulses** at deterministic times:
    n_x(t_k^+) = n_x(t_k^-) - Binomial(n_x(t_k^-), κ_x)

After each fraction a Binomial fraction ``sigma_T_per_fraction`` of surviving P
cells moves to Q (therapy-induced dormancy).

There are no continuous CTMC events for RT in v0.2 — RT acts only at fraction
times. Continuous post-irradiation effects (sublethal damage repair, mitotic
delay) are folded into the per-fraction kill probability.

All kill probabilities are **placeholders** (ASM). No clinical prediction.
"""

from __future__ import annotations

import numpy as np

from gbm_ctmc.parameters import ModelParams, RadiotherapyParams
from gbm_ctmc.therapy.schedule import pulse_breakpoints_in
from gbm_ctmc.transitions import Event


class RadiotherapyTherapy:
    """Fractionated RT therapy. Pulse-only — no continuous CTMC events."""

    name: str = "radiotherapy"

    def __init__(self, params: RadiotherapyParams):
        self.rt = params
        self._fraction_times = list(params.fraction_times)
        self._fraction_set = {round(t, 9) for t in self._fraction_times}

    def extra_events_at(self, t: float) -> list[Event]:
        return []

    def breakpoints(self, t_lo: float, t_hi: float) -> list[float]:
        return pulse_breakpoints_in(self._fraction_times, t_lo, t_hi)

    def pulse_at(
        self,
        t: float,
        n: np.ndarray,
        params: ModelParams,
        rng: np.random.Generator,
    ) -> np.ndarray | None:
        if round(t, 9) not in self._fraction_set:
            return None
        return apply_rt_fraction(n, self.rt, rng)


def apply_rt_fraction(
    n: np.ndarray,
    rt: RadiotherapyParams,
    rng: np.random.Generator,
) -> np.ndarray:
    """Apply one RT fraction: per-state Binomial kill + P→Q dormancy on survivors.

    Pure function — exported so tests can call it directly.
    """
    out = n.astype(np.int64, copy=True)
    kill_probs = (rt.kappa_S, rt.kappa_P, rt.kappa_D, rt.kappa_Q)
    for i, kappa in enumerate(kill_probs):
        if out[i] > 0 and kappa > 0:
            killed = int(rng.binomial(int(out[i]), float(kappa)))
            out[i] -= killed
    # Therapy-induced dormancy on surviving P cells
    sigma_T = max(0.0, min(1.0, float(rt.sigma_T_per_fraction)))
    if out[1] > 0 and sigma_T > 0:
        dormant = int(rng.binomial(int(out[1]), sigma_T))
        out[1] -= dormant
        out[3] += dormant
    return out
