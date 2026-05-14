"""Model parameters: typed dataclasses + YAML loader.

Evidence-level convention (informational tags carried in YAML comments):
    LIT — literature-supported
    ASM — biologically motivated assumption (placeholder; not clinically calibrated)
    UNK — uncalibrated / free parameter

Therapy parameters in v0.2 (RT, TMZ) are **all placeholders** unless tagged LIT.
No clinical prediction is implied.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

import yaml


# ── Basal / switching / population / run ───────────────────────────────────────

@dataclass
class BasalRates:
    lambda_S: float = 0.02   # LIT upper bound (Lan 2017: GSC doubling > 24 h)
    lambda_P: float = 0.20   # ASM
    mu_S: float = 0.005      # ASM
    mu_P: float = 0.02       # ASM
    mu_D: float = 0.05       # ASM
    mu_Q: float = 0.003      # ASM
    c_S: float = 0.005       # ASM
    c_P: float = 0.01        # ASM
    c_D: float = 0.005       # ASM
    c_Q: float = 0.001       # ASM


@dataclass
class SwitchingRates:
    alpha_S: float = 0.01    # ASM — S asymmetric division → P daughter
    S_to_P: float = 0.01     # ASM
    P_to_D: float = 0.05     # ASM
    sigma: float = 0.005     # LIT structure (Blath 2023 σ); ASM magnitude
    rho: float = 0.02        # LIT structure (Blath 2023 ϱ); ASM magnitude


@dataclass
class InitialPopulation:
    S: int = 5
    P: int = 50
    D: int = 100
    Q: int = 2


@dataclass
class RunControls:
    t_end: float = 365.0
    seed: int | None = 42
    max_steps: int = 10_000_000


# ── Therapy parameters ─────────────────────────────────────────────────────────

@dataclass
class RadiotherapyParams:
    """Stupp RT protocol. All kill probabilities are PLACEHOLDERS (ASM)."""

    start_day: float = 1.0
    n_fractions: int = 30
    interval_days: float = 1.0
    # Per-fraction kill probability — [ASSUMPTION] (no clinical calibration)
    kappa_S: float = 0.03
    kappa_P: float = 0.20
    kappa_D: float = 0.10
    kappa_Q: float = 0.01
    # Per-fraction fraction of surviving P cells that enter Q — [ASSUMPTION]
    sigma_T_per_fraction: float = 0.10

    @property
    def fraction_times(self) -> list[float]:
        return [self.start_day + i * self.interval_days for i in range(self.n_fractions)]


@dataclass
class TemozolomideParams:
    """Stupp TMZ protocol. Schedule from Stupp 2005; kill rates are PLACEHOLDERS."""

    # Schedule — LIT (Stupp 2005)
    concomitant_start: float = 0.0
    concomitant_end: float = 42.0
    adjuvant_start: float = 49.0
    adjuvant_cycles: int = 6
    cycle_length_days: float = 28.0
    treatment_days: float = 5.0

    # Per-day extra death rate during active TMZ — [ASSUMPTION]
    delta_S: float = 0.03
    delta_P: float = 0.20
    delta_D: float = 0.05
    delta_Q: float = 0.01
    # Per-day P→Q transition rate during active TMZ — [ASSUMPTION]
    sigma_T: float = 0.10

    def windows(self) -> list[tuple[float, float]]:
        wins: list[tuple[float, float]] = []
        if self.concomitant_end > self.concomitant_start:
            wins.append((self.concomitant_start, self.concomitant_end))
        for c in range(self.adjuvant_cycles):
            start = self.adjuvant_start + c * self.cycle_length_days
            wins.append((start, start + self.treatment_days))
        return wins


@dataclass
class TherapyParams:
    """Top-level therapy selector. ``type`` chooses which module is instantiated."""

    type: str = "none"   # one of: none | radiotherapy | tmz | stupp
    radiotherapy: RadiotherapyParams = field(default_factory=RadiotherapyParams)
    tmz: TemozolomideParams = field(default_factory=TemozolomideParams)


# ── Top-level container + loader ───────────────────────────────────────────────

_KNOWN_THERAPY_TYPES = {"none", "radiotherapy", "tmz", "stupp"}


@dataclass
class ModelParams:
    K: int = 1000
    basal: BasalRates = field(default_factory=BasalRates)
    switching: SwitchingRates = field(default_factory=SwitchingRates)
    initial: InitialPopulation = field(default_factory=InitialPopulation)
    run: RunControls = field(default_factory=RunControls)
    therapy: TherapyParams = field(default_factory=TherapyParams)

    @classmethod
    def defaults(cls) -> "ModelParams":
        return cls()

    @classmethod
    def from_yaml(cls, path: str | Path) -> "ModelParams":
        raw = _load_yaml_with_extends(Path(path))
        return cls._from_dict(raw)

    @classmethod
    def _from_dict(cls, raw: dict[str, Any]) -> "ModelParams":
        p = cls()
        if "K" in raw:
            p.K = int(raw["K"])

        _apply_floats(p.basal, raw.get("basal", {}), "basal")
        _apply_floats(p.switching, raw.get("switching", {}), "switching")
        _apply_ints(p.initial, raw.get("initial", {}), "initial")

        if "run" in raw:
            for k, v in raw["run"].items():
                if not hasattr(p.run, k):
                    raise ValueError(f"Unknown run parameter: {k}")
                if k == "t_end":
                    setattr(p.run, k, float(v))
                elif k == "seed":
                    setattr(p.run, k, None if v is None else int(v))
                else:
                    setattr(p.run, k, int(v))

        if "therapy" in raw:
            _load_therapy(p.therapy, raw["therapy"])

        p.validate()
        return p

    def validate(self) -> None:
        if self.K <= 0:
            raise ValueError(f"K must be positive, got {self.K}")
        for name in ("lambda_S", "lambda_P", "mu_S", "mu_P", "mu_D", "mu_Q"):
            v = getattr(self.basal, name)
            if v < 0:
                raise ValueError(f"basal.{name} must be non-negative, got {v}")
        if self.run.t_end <= 0:
            raise ValueError(f"run.t_end must be positive, got {self.run.t_end}")
        if self.therapy.type not in _KNOWN_THERAPY_TYPES:
            raise ValueError(
                f"Unknown therapy.type {self.therapy.type!r}; "
                f"expected one of {sorted(_KNOWN_THERAPY_TYPES)}"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "K": self.K,
            "basal": asdict(self.basal),
            "switching": asdict(self.switching),
            "initial": asdict(self.initial),
            "run": asdict(self.run),
            "therapy": {
                "type": self.therapy.type,
                "radiotherapy": asdict(self.therapy.radiotherapy),
                "tmz": asdict(self.therapy.tmz),
            },
        }


# ── Helpers ────────────────────────────────────────────────────────────────────

def _apply_floats(target: Any, src: dict[str, Any], section: str) -> None:
    for k, v in src.items():
        if not hasattr(target, k):
            raise ValueError(f"Unknown {section} parameter: {k}")
        setattr(target, k, float(v))


def _apply_ints(target: Any, src: dict[str, Any], section: str) -> None:
    for k, v in src.items():
        if not hasattr(target, k):
            raise ValueError(f"Unknown {section} parameter: {k}")
        setattr(target, k, int(v))


_INT_FIELDS = {"n_fractions", "adjuvant_cycles"}


def _load_therapy(target: TherapyParams, src: dict[str, Any]) -> None:
    if "type" in src:
        target.type = str(src["type"])
    for sub_name, sub_target in (("radiotherapy", target.radiotherapy),
                                 ("tmz", target.tmz)):
        if sub_name not in src:
            continue
        for k, v in src[sub_name].items():
            if not hasattr(sub_target, k):
                raise ValueError(f"Unknown therapy.{sub_name} parameter: {k}")
            cast = int if k in _INT_FIELDS else float
            setattr(sub_target, k, cast(v))


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursive dict merge: override wins, but nested dicts merge field-wise."""
    result: dict[str, Any] = dict(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def _load_yaml_with_extends(
    path: Path, _seen: Iterable[Path] = ()
) -> dict[str, Any]:
    """Load YAML, recursively resolving 'extends:' references relative to the file."""
    path = path.resolve()
    if path in _seen:
        raise ValueError(f"Cyclic extends detected at {path}")
    with open(path) as f:
        raw: dict[str, Any] = yaml.safe_load(f) or {}
    if "extends" in raw:
        ext = raw.pop("extends")
        base_path = (path.parent / ext).resolve()
        base = _load_yaml_with_extends(base_path, _seen=(*_seen, path))
        raw = _deep_merge(base, raw)
    return raw
