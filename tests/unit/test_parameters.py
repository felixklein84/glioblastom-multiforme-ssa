"""Parameter dataclasses and YAML loading."""

from pathlib import Path

import pytest

from gbm_ctmc.parameters import ModelParams


def test_defaults_are_self_consistent():
    p = ModelParams.defaults()
    p.validate()
    assert p.K > 0
    assert p.basal.lambda_P > p.basal.mu_P, "P should have net growth at low density"
    assert p.run.t_end > 0


def test_yaml_loader_round_trip(tmp_path: Path):
    yaml_content = """
K: 500
basal:
  lambda_S: 0.015
  lambda_P: 0.18
switching:
  sigma: 0.004
  rho: 0.025
initial:
  S: 3
  P: 30
  D: 60
  Q: 1
run:
  t_end: 90.0
  seed: 7
"""
    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(yaml_content)

    p = ModelParams.from_yaml(cfg_path)
    assert p.K == 500
    assert p.basal.lambda_S == pytest.approx(0.015)
    assert p.basal.lambda_P == pytest.approx(0.18)
    assert p.switching.sigma == pytest.approx(0.004)
    assert p.switching.rho == pytest.approx(0.025)
    assert p.initial.P == 30
    assert p.run.t_end == pytest.approx(90.0)
    assert p.run.seed == 7


def test_yaml_loader_rejects_unknown_keys(tmp_path: Path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("basal:\n  not_a_real_param: 0.1\n")
    with pytest.raises(ValueError, match="Unknown basal parameter"):
        ModelParams.from_yaml(bad)


def test_validate_rejects_bad_values():
    p = ModelParams.defaults()
    p.K = -1
    with pytest.raises(ValueError):
        p.validate()


def test_to_dict_is_jsonable():
    p = ModelParams.defaults()
    d = p.to_dict()
    assert d["K"] == p.K
    assert d["basal"]["lambda_S"] == p.basal.lambda_S
    assert d["initial"]["S"] == p.initial.S


def test_default_config_file_loads():
    """The repo's shipped default config must load and validate."""
    root = Path(__file__).resolve().parents[2]
    cfg = root / "configs" / "default.yaml"
    p = ModelParams.from_yaml(cfg)
    p.validate()
