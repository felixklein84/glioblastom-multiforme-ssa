"""Therapy modules — RT, TMZ, combined Stupp protocol, no-therapy baseline.

All therapies implement the :class:`Therapy` protocol. The segmented simulation
engine consumes ``extra_events_at``, ``breakpoints``, and ``pulse_at`` to drive
the Gillespie loop across schedule boundaries.

All kill rates and therapy-induced dormancy rates in v0.2 are **placeholders**
(``ASM``) unless individually marked ``LIT``. No clinical prediction is implied.
"""

from gbm_ctmc.parameters import ModelParams
from gbm_ctmc.therapy.base import Therapy
from gbm_ctmc.therapy.combined import StuppTherapy, CombinedTherapy
from gbm_ctmc.therapy.none import NoTherapy
from gbm_ctmc.therapy.radiotherapy import RadiotherapyTherapy
from gbm_ctmc.therapy.temozolomide import TemozolomideTherapy

__all__ = [
    "Therapy",
    "NoTherapy",
    "RadiotherapyTherapy",
    "TemozolomideTherapy",
    "CombinedTherapy",
    "StuppTherapy",
    "build_therapy",
]


def build_therapy(params: ModelParams) -> Therapy:
    """Factory: construct the Therapy implementation named by ``params.therapy.type``."""
    t = params.therapy.type
    if t == "none":
        return NoTherapy()
    if t == "radiotherapy":
        return RadiotherapyTherapy(params.therapy.radiotherapy)
    if t == "tmz":
        return TemozolomideTherapy(params.therapy.tmz)
    if t == "stupp":
        return StuppTherapy(
            RadiotherapyTherapy(params.therapy.radiotherapy),
            TemozolomideTherapy(params.therapy.tmz),
        )
    raise ValueError(f"Unknown therapy type: {t!r}")
