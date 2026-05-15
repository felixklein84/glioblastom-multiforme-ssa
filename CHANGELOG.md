# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Parameter default changes — even though defaults are not part of the public API
— are called out in their own `Parameters` subsection because they can change
scientific results.

---

## [Unreleased]

### Planned

- v0.3 — Tumor Treating Fields (TTF / Optune) scenario.
- v0.4 — Batch experiments: *n* independent replicates per scenario; aggregate
  metrics (extinction probability, time-to-recurrence, quantile bands).
- v0.5 — ODE mean-field companion + SSA/ODE agreement test.
- v0.6 — Sensitivity analysis (tornado plot).
- v1.0 — All five scenarios; Sphinx docs deployed; demo GIF; CI green.

---

## [0.2.0] — 2026-05-15

### Added

- Therapy package `gbm_ctmc.therapy` with the `Therapy` protocol.
- `NoTherapy`, `RadiotherapyTherapy`, `TemozolomideTherapy`, `StuppTherapy`,
  generic `CombinedTherapy` (composition).
- Segmented simulation engine `run_simulation(params, therapy)`: walks across
  schedule breakpoints, swaps active event list, applies discrete pulses at
  boundaries — single Gillespie loop, no duplicated simulation code.
- `extends:` mechanism in the YAML loader for DRY scenario configs
  (recursive deep-merge with cycle detection).
- Therapy parameter dataclasses: `RadiotherapyParams`, `TemozolomideParams`,
  `TherapyParams`.
- Scenario configs `configs/scenarios/{no_therapy,radiotherapy,tmz,stupp}.yaml`.
- Comparison script `scripts/run_comparison.py` — runs all 4 scenarios under a
  shared seed; writes per-scenario CSVs + summary.csv + 6 overlay PNGs.
- `plotting.comparison.plot_comparison()` — multi-scenario overlay with
  step-resampling onto a uniform daily grid.
- Demo GIF script `scripts/make_demo_gif.py` — 2-panel animated stacked
  composition (no-therapy vs Stupp) with Stupp treatment windows shaded.
- Sphinx documentation scaffold under `docs/source/`: index, getting started,
  quickstart, configs, model overview, therapy, limitations, references, API,
  changelog. Theme: `furo`. MyST markdown parser.
- `CITATION.cff` and MIT `LICENSE`.
- Tests: 38 new (62 total). Per-therapy modules, schedule helpers, composition,
  scenario-config loading, `extends:` overlay correctness.

### Changed

- `gillespie.simulate()` accepts a `t_start` parameter so segments can be
  stitched into a continuous trajectory across schedule boundaries.
  Backwards-compatible: defaults to `0.0`.
- `parameters.ModelParams` now has a top-level `therapy: TherapyParams` field.
  Backwards-compatible: defaults to `type: "none"`.
- README rewritten to cover therapy modules, comparison run, demo GIF, and the
  scientific caution about placeholder kill rates.

### Removed

- `docs/model_specification.md` (older draft superseded by
  `docs/v1_specification.md`).

### Parameters

- All therapy kill rates and dormancy rates shipped with v0.2 are
  **placeholders** tagged `ASM`. They reproduce qualitative literature patterns
  (RT reduces P, TMZ extends nadir, Stupp accelerates debulking) but are
  **not** clinically calibrated.

---

## [0.1.0] — 2026-05-14

### Added

- Core package skeleton `gbm_ctmc/` with `states.py`, `parameters.py`,
  `transitions.py`, `gillespie.py`.
- 4-state cell hierarchy: S (GSC), P (progenitor), D (differentiated),
  Q (quiescent).
- Thirteen basal CTMC events (Lan 2017 hierarchy + Blath 2023 dormancy).
- Gillespie SSA `simulate()` and `Trajectory` container.
- `ModelParams` dataclass + YAML loader with validation.
- `simulation.engine.run_baseline()` — single no-therapy trajectory.
- `io.results` — CSV writers for trajectories.
- `plotting.trajectory` — line plot of S/P/D/Q + total.
- `scripts/run_baseline.py` — CLI runner with `--config`, `--seed`, `--out`.
- `configs/default.yaml` with evidence-level tags.
- 28 unit tests: states, parameters, transitions, Gillespie mechanics,
  reproducibility, I/O, plotting.
- README with run instructions.
- `docs/v1_specification.md` and `docs/assumptions.md` (carried over from
  earlier exploratory work).

### Notes

- The pure-Python SSA executes ~8 k events/s. A 180-day baseline takes ~50 s.
  Vectorising the rate computation is the planned first optimisation when
  batch experiments arrive in v0.4.
