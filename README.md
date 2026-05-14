# Glioblastoma Therapy Simulation (gbm-ctmc)

Stochastic simulation of glioblastoma cell-state dynamics using a continuous-time
Markov chain (CTMC) on a 4-state hierarchy: **S** (glioma stem cell), **P**
(progenitor), **D** (differentiated), **Q** (quiescent / dormant).

**Status:** v0.2 — adds the three therapy modules (radiotherapy, temozolomide,
combined Stupp) on top of the v0.1 baseline. See
[`docs/v1_specification.md`](docs/v1_specification.md) for the full model spec.

> **Scientific caution.** This is a **mechanistic toy model**. All therapy kill
> probabilities and dormancy rates shipped in this repo are **placeholders**
> (tagged `ASM` in the configs) — they are not calibrated against patient data
> and the simulation makes **no clinical predictions**. The protocol *schedules*
> (Stupp 30×2 Gy RT and the 5/28-day TMZ adjuvant cycles) are taken from Stupp
> 2005 (`LIT`); the *kill rates* are order-of-magnitude assumptions.

---

## Installation

Python ≥ 3.10.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Scripts and tests also work without installing — they patch `sys.path` against
the source tree.

---

## Quick start

### Baseline (no therapy)

```bash
python scripts/run_baseline.py
```

Writes `outputs/baseline/trajectory.{csv,png}`.

### Therapy comparison (4 scenarios)

```bash
python scripts/run_comparison.py --t-end 200 --seed 42
```

Runs the no-therapy / RT / TMZ / Stupp scenarios under the same seed and writes:

- `outputs/comparison/<scenario>/trajectory.csv` — full SSA trajectory per scenario
- `outputs/comparison/summary.csv` — one row per scenario with nadir, final state, runtime
- `outputs/comparison/comparison_total.png` — total burden overlay (linear y)
- `outputs/comparison/comparison_total_log.png` — same, symlog y
- `outputs/comparison/comparison_{S,P,D,Q}.png` — per-state overlays

> A full 365-day Stupp run takes ~3 minutes in pure-Python SSA. Use `--t-end`
> to shorten while iterating.

### Single scenario

```bash
python scripts/run_baseline.py --config configs/scenarios/stupp.yaml --out outputs/stupp_demo
```

---

## Therapy modules

| Therapy | Module | How it modifies the CTMC |
|---|---|---|
| None | `gbm_ctmc.therapy.none.NoTherapy` | No-op; engine ≡ baseline |
| Radiotherapy | `.radiotherapy.RadiotherapyTherapy` | Discrete Binomial fractional-kill pulses at deterministic fraction times. No continuous CTMC events. |
| Temozolomide | `.temozolomide.TemozolomideTherapy` | Adds 5 extra CTMC events (4 per-state kills + P→Q dormancy) when *t* is inside a treatment window. |
| Combined (Stupp) | `.combined.StuppTherapy` | Composes RT + TMZ. Extra events are concatenated; pulses fire in declaration order. No synergy multiplier. |

All four implement the same `Therapy` protocol (see
[`src/gbm_ctmc/therapy/base.py`](src/gbm_ctmc/therapy/base.py)):

```python
class Therapy(Protocol):
    name: str
    def extra_events_at(self, t: float) -> list[Event]: ...      # CTMC events
    def breakpoints(self, t_lo: float, t_hi: float) -> list[float]: ...
    def pulse_at(self, t, n, params, rng) -> np.ndarray | None: ...
```

The segmented engine in `simulation.engine.run_simulation` walks across the
sorted breakpoints, swaps the active event list each segment, applies any pulse
at the boundary, and continues — single Gillespie loop, no duplication of
simulation code across therapies.

---

## Configuration

Each scenario is a small YAML in `configs/scenarios/` that `extends:` the
top-level [`configs/default.yaml`](configs/default.yaml):

```yaml
# configs/scenarios/stupp.yaml
extends: ../default.yaml
therapy:
  type: stupp
  radiotherapy:
    n_fractions: 30       # LIT — Stupp 2005
    kappa_P: 0.20         # ASM — placeholder, NOT clinically calibrated
    ...
  tmz:
    concomitant_end: 42.0 # LIT — Stupp 2005
    delta_P: 0.20         # ASM
    ...
```

The loader deep-merges the parent into the child so each scenario file lists
only its overrides. Unknown keys raise `ValueError` at load time.

---

## Run the tests

```bash
pytest
```

62 tests in v0.2 — all unit tests, ~3 min total in pure-Python SSA. Covers:

- `test_states.py`, `test_parameters.py` — state enum, dataclasses, YAML loader, `extends`
- `test_transitions.py` — basal event catalogue invariants
- `test_gillespie.py` — SSA monotone time, non-negative counts, single-event mass change
- `test_reproducibility.py` — same seed ⇒ identical trajectory
- `test_io_and_plotting.py` — CSV round-trip, PNG creation
- `test_therapy_schedule.py` — window/pulse helpers
- `test_therapy_none.py` — `run_simulation` ≡ `run_baseline` under `NoTherapy`
- `test_therapy_radiotherapy.py` — fraction times, Binomial kill at κ=0/1, P→Q dormancy
- `test_therapy_tmz.py` — Stupp 7-window schedule, event activation inside/outside windows
- `test_therapy_combined.py` — composition correctness, factory dispatch
- `test_scenario_configs.py` — every shipped scenario YAML loads and validates

---

## Project structure (v0.2)

```
glioblastoma-therapy-simulation/
├── src/gbm_ctmc/
│   ├── states.py / parameters.py / transitions.py / gillespie.py
│   ├── simulation/engine.py        # run_baseline, run_simulation (segmented)
│   ├── therapy/
│   │   ├── base.py                 # Therapy protocol
│   │   ├── schedule.py             # window / pulse helpers
│   │   ├── none.py / radiotherapy.py / temozolomide.py / combined.py
│   ├── io/results.py               # CSV writer
│   └── plotting/
│       ├── trajectory.py           # single-run line plot
│       └── comparison.py           # multi-scenario overlay
├── configs/
│   ├── default.yaml
│   └── scenarios/{no_therapy,radiotherapy,tmz,stupp}.yaml
├── scripts/{run_baseline,run_comparison}.py
├── tests/unit/                     # pytest suite
├── outputs/                        # generated, gitignored
├── docs/                           # spec + architecture
└── references/                     # literature summaries
```

---

## What's next (not in v0.2)

- **v0.3** — Tumor Treating Fields (TTF / Optune) as a fifth scenario.
- **v0.4** — Batch experiments: *n* independent replicates per scenario, aggregate metrics (extinction probability, time-to-recurrence, quantile bands).
- **v0.5** — ODE mean-field companion + SSA/ODE agreement test.
- **v0.6** — Sensitivity analysis (tornado plot).
- **v1.0** — All five scenarios calibrated to qualitative literature patterns, Sphinx docs, demo GIF.

See [`docs/v1_specification.md`](docs/v1_specification.md) for the full roadmap.

---

## Performance note

The current pure-Python SSA executes ~8 kevents/s. A full 365-day Stupp run is
~3 minutes. This is acceptable for v0.2 (single trajectories) but will become
the bottleneck once v0.4 introduces 100+ replicates per scenario. Rate-array
vectorisation is the planned first optimisation.
