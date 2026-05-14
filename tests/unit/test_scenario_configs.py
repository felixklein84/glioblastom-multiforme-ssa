"""All shipped scenario configs load and validate."""

from pathlib import Path

import pytest

from gbm_ctmc.parameters import ModelParams


SCENARIOS_DIR = Path(__file__).resolve().parents[2] / "configs" / "scenarios"
SCENARIOS = ["no_therapy", "radiotherapy", "tmz", "stupp"]


@pytest.mark.parametrize("name", SCENARIOS)
def test_scenario_config_loads(name: str):
    p = ModelParams.from_yaml(SCENARIOS_DIR / f"{name}.yaml")
    p.validate()


def test_no_therapy_config_has_type_none():
    p = ModelParams.from_yaml(SCENARIOS_DIR / "no_therapy.yaml")
    assert p.therapy.type == "none"


def test_radiotherapy_config_has_rt_params():
    p = ModelParams.from_yaml(SCENARIOS_DIR / "radiotherapy.yaml")
    assert p.therapy.type == "radiotherapy"
    assert p.therapy.radiotherapy.n_fractions == 30


def test_stupp_config_has_both_modules():
    p = ModelParams.from_yaml(SCENARIOS_DIR / "stupp.yaml")
    assert p.therapy.type == "stupp"
    assert p.therapy.radiotherapy.n_fractions == 30
    assert p.therapy.tmz.adjuvant_cycles == 6


def test_extends_overlay_preserves_defaults(tmp_path: Path):
    """A scenario that only overrides therapy must retain default basal rates."""
    base = tmp_path / "base.yaml"
    base.write_text("K: 1234\nbasal:\n  lambda_P: 0.11\n")
    child = tmp_path / "child.yaml"
    child.write_text(
        "extends: base.yaml\ntherapy:\n  type: tmz\n"
    )
    p = ModelParams.from_yaml(child)
    assert p.K == 1234
    assert p.basal.lambda_P == pytest.approx(0.11)
    assert p.therapy.type == "tmz"
