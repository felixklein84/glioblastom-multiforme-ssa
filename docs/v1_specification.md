# GBM Therapy Simulation — Version 1 Specification

**Document type:** Design specification (no code)
**Version:** 1.0
**Date:** 2026-05-14
**Status:** Proposal for review

This document defines version 1 of the glioblastoma (GBM) therapy simulation. It scopes the
model, the math, the therapy modules, the parameters, the outputs, the experiments, the
plots, and the validation boundaries — before any implementation.

The guiding principle: **mechanistically meaningful, mathematically transparent,
parametrically honest.** Every quantitative claim must be reproducible from the parameter
file plus a random seed. Every assumption must be labeled.

---

## 1. Biological Scope

### 1.1 Populations included in v1

| Population | Symbol | Identity | Why included |
|------------|--------|----------|--------------|
| Stem-like | **S** | Glioma stem cell (GSC); slow-cycling; therapy-resistant | Lan 2017 fate-mapping shows GSCs are the cell-of-origin for post-therapy recurrence. Excluding them removes the central mechanism we want to study. |
| Proliferating | **P** | Fast-cycling progenitor / transit-amplifying cell | The bulk of cycling tumor mass; the population most affected by both RT and TMZ. Required for any therapy effect to be visible. |
| Differentiated | **D** | Post-mitotic tumor cell | Acts as a sink, prevents unbounded P growth, captures the realistic observation that not every tumor cell is cycling. Cheap to add. |
| Quiescent / dormant | **Q** | Cell-cycle arrested but viable | Blath 2023 result: even a small Q reservoir can cause therapy failure on standard protocols. Without Q the model cannot reproduce the *recurrence-after-remission* pattern, which is the clinical phenomenon of interest. |

**State labels are operational, not transcriptomic.** We do not claim S corresponds to a
specific marker set; it is "the slow-cycling self-renewing fraction" in the Lan 2017 sense.

### 1.2 Populations *excluded* in v1 (deliberate)

| Excluded | Reason for exclusion | Where it lives instead |
|----------|---------------------|------------------------|
| Therapy-damaged cells (separate class) | Damage repair and damage-induced death are folded into effective kill rates. Adding a separate damaged compartment would require a damage repair rate parameter for which there is no useful data. | Implicit in the kill rates per state. |
| Resistant cells as a distinct compartment | GSC resistance in Lan 2017 is pre-existing and phenotypic, not the result of a mutation acquired during therapy. v1 captures resistance via the slower kill rates in S and Q, not via a mutating subpopulation. | Implicit in S and Q kill rates. MGMT methylation is a sensitivity *parameter*, not a state. |
| Dead / removed cells | Once killed, a cell carries no further dynamics. Tracking cumulative deaths is an output metric, not a state. | Output time series (`cumulative_deaths_by_state`). |
| Migratory / invasive state ("go-or-grow") | Biologically real, but introducing migration without spatial structure is meaningless. Reserved for v2 (spatial extension). | v2 roadmap. |
| Neftel-2019 transcriptional 4-state (NPC/OPC/AC/MES) | Orthogonal classification to the Lan hierarchy. Combining them gives 16 states, none of which can be parameterized from public data. | v3+ if scRNA-seq calibration data is acquired. |
| Immune compartment | Not part of standard-of-care GBM modeling; immunotherapy is a separate scenario class. | v3 extension using Baar 2016 framework. |
| Acquired (mutational) resistance | Pre-existing resistance is dominant in Lan 2017. Adding a mutation rate parameter that we cannot calibrate would inflate model complexity without buying explanatory power. | Documented as a v2 extension. |

### 1.3 Resulting structure

Four-state compartmental model with directed transitions:

```
            S  ──S→P──▶  P  ──P→D──▶  D
            │            │
            │ (split)    │ σ        ϱ
            ▼            ▼          ▲
            P            Q ─────────┘
```

- S self-renews (S → 2S) and produces P daughters (asymmetric / commitment).
- P self-renews (P → 2P), differentiates (P → D), and enters dormancy (P → Q).
- Q resuscitates back to P. No other transitions out of Q in v1.
- D is terminal: it dies, it does not switch.

---

## 2. Mathematical Framework

### 2.1 Choice: stochastic CTMC with mean-field ODE companion

**Primary framework:** Continuous-time Markov chain (CTMC) on $\mathbb{N}_0^4$, simulated
exactly via Gillespie's stochastic simulation algorithm (SSA).

**Why CTMC and not ODEs only:** Cure vs. recurrence in GBM is fundamentally a stochastic
question. After therapy, tumor populations are small (10⁰ – 10³ cells); whether a single
surviving GSC restarts growth or randomly dies is exactly the type of event ODEs cannot
represent. Kraut 2021 makes this point explicitly: "even when the cell division rate exceeds
the death rate, it can happen that cells randomly die before they can divide, and the tumor
goes extinct."

**Why ODE companion:** For large populations (pre-treatment, early recurrence) the ODE
mean-field is faster, smoother, and useful as a sanity check. The Ethier–Kurtz theorem
(Baar 2016, Kraut 2021) guarantees that the rescaled CTMC converges to the ODE as the
carrying capacity $K \to \infty$. Implementing both serves dual purposes:

- Validation: SSA and ODE must agree in the large-K limit (or there is a bug).
- Performance: ODE is acceptable for parameter sweeps; SSA is reserved for extinction
  probability and small-population regimes.

**Hybrid solver:** Mentioned in Kraut 2021 but **deferred to v2**. v1 will not switch between
SSA and ODE dynamically; the user picks one.

**Not chosen for v1, and why:**

| Framework | Reason deferred |
|-----------|----------------|
| PDE (spatial) | Requires imaging data (MRI segmentation), advection-diffusion-reaction calibration, mesh handling. Scope-wise: not feasible without spatial data. Roadmapped via Conte & Surulescu 2021. |
| Agent-based model | Adds simulation cost (10⁴–10⁶× slower) without adding a question we cannot ask in CTMC for v1. Roadmapped if spatial mechanisms become important. |
| Branching process (analytical only) | Cannot represent competition / carrying capacity, which is needed to bound tumor growth. Useful as an analytical reference (extinction probability) but not as the primary simulator. |

### 2.2 State vector

$$\mathbf{N}(t) = (n_S(t),\; n_P(t),\; n_D(t),\; n_Q(t)) \in \mathbb{N}_0^4$$

Counts are integers. The total $n_{\text{tot}}(t) = n_S + n_P + n_D + n_Q$ is the tumor
burden.

**Carrying capacity $K$:** Population-scale parameter. Competition rates are scaled by $1/K$
(Baar 2016 convention). In the ODE limit, $\bar{n}_x = n_x / K$ are bounded; in SSA, counts
are unbounded but competition death increases linearly in total population.

### 2.3 Transition events

The CTMC has 13 basal events. Each is exponentially clocked with the rate given.

| # | Event | Rate | Notes |
|---|-------|------|-------|
| 1 | S division (symmetric) | $\lambda_S \cdot n_S$ | Self-renewal of GSCs |
| 2 | S asymmetric division | $\alpha_S \cdot n_S$ | Produces a P daughter, S unchanged |
| 3 | S natural death | $\mu_S \cdot n_S$ | |
| 4 | S competition death | $c_S \cdot n_S \cdot n_{\text{tot}} / K$ | Carrying-capacity feedback |
| 5 | S → P commitment | $s_{SP} \cdot n_S$ | Irreversible |
| 6 | P division | $\lambda_P \cdot n_P$ | |
| 7 | P natural death | $\mu_P \cdot n_P$ | |
| 8 | P competition death | $c_P \cdot n_P \cdot n_{\text{tot}} / K$ | |
| 9 | P → D differentiation | $s_{PD} \cdot n_P$ | Irreversible |
| 10 | P → Q spontaneous dormancy | $\sigma \cdot n_P$ | Blath 2023 σ |
| 11 | D natural death | $\mu_D \cdot n_D$ | |
| 12 | Q natural death | $\mu_Q \cdot n_Q$ | |
| 13 | Q → P resuscitation | $\varrho \cdot n_Q$ | Blath 2023 ϱ |

Therapy adds further events (Section 3).

### 2.4 Time and population units

- **Time unit:** day. All rates have units of day⁻¹.
- **Population unit:** absolute cell count (integer). The ODE companion uses rescaled
  $\bar{n}_x = n_x / K$.
- **Simulated horizon:** v1 default is 365 days (one year). User-configurable.

### 2.5 Stochastic assumptions

- All inter-event times are exponentially distributed (Markov assumption). Real cell-cycle
  durations are log-normal / gamma; this is a deliberate simplification, standard in this
  literature. Flagged as a limitation (Section 8).
- Events are conditionally independent given the current state (no event memory).
- Single random seed reproduces a single trajectory exactly. Independent trajectories use
  independent seeds (or `numpy.random.SeedSequence` spawning).

---

## 3. Therapy Modules

Each scenario layers additional events on top of the basal CTMC. Therapy is always defined
by a *schedule* (when it is on) and a set of *rate modifications* (what changes while it is
on).

### 3.0 Common conventions

- **Schedule:** explicit list of treatment intervals, in days from $t=0$. v1 hard-codes the
  Stupp protocol; later versions can read schedules from YAML.
- **Compliance:** modeled only for TTF (continuous fields, real-world compliance ~75%). RT
  and TMZ are assumed perfectly delivered in v1.
- **Repair / recovery:** v1 does NOT model sublethal damage and repair as a separate
  process. Repair is folded into the *effective* kill rate per state. This is the standard
  approach in low-complexity stochastic tumor models.

### 3.1 No therapy (baseline)

Only events 1–13 are active. Used for:

- Calibrating doubling times and S/P/D/Q steady-state fractions.
- Establishing pre-treatment tumor size.
- Sanity-checking that the model produces unbounded growth without competition and bounded
  growth with competition.

### 3.2 Radiotherapy (RT)

**Schedule:** Stupp protocol. 30 fractions × 2 Gy, weekday-only in reality, simplified to
daily for v1 (30 consecutive days starting at $t = 0$).

**Mechanism:** RT causes acute DNA damage; cells die at the next mitotic attempt. v1 models
RT as a *discrete fractional kill* at the time of each fraction:

$$n_x(t_k^+) = n_x(t_k^-) - \text{Binomial}(n_x(t_k^-),\; \kappa_x^{\text{RT}})$$

This is not a CTMC event — it is a deterministic-time Binomial draw, applied as a hook into
the SSA. The CTMC handles continuous dynamics between fractions.

**Kill probability per fraction per state:** $\kappa_S = 0.03$, $\kappa_P = 0.20$,
$\kappa_D = 0.10$, $\kappa_Q = 0.01$. All `[ASSUMPTION]`. Rationale: cycling cells
maximally radio-sensitive (4 Rs of radiobiology); quiescent and slow-cycling cells protected.

**Therapy-induced dormancy:** After each fraction, a fraction $\sigma_T^{\text{RT}}$ of
surviving P cells move to Q. Captures the well-documented BMP-driven RT-induced quiescence
in GBM. `[ASSUMPTION for magnitude]`.

**Repair / sublethal damage:** Not modeled as a separate state in v1. Folded into the kill
probability (a "fraction of fraction-induced lethal damage").

**Resistant survival:** Implicit. Cells in S and Q states have inherently low $\kappa_x$
because they cycle rarely; these are the cells that survive RT in the model.

### 3.3 Drug therapy — Temozolomide (TMZ)

**Schedule:** Stupp protocol.
- **Concomitant phase:** day 0 – day 41, daily TMZ at 75 mg/m².
- **Recovery gap:** day 42 – day 48.
- **Adjuvant phase:** 6 cycles × 5 days on / 23 days off, starting day 49.

v1 does not model mg/m² → intracellular concentration. Schedule is binary: "TMZ active" or
"TMZ inactive."

**Mechanism:** TMZ alkylates DNA; methylated lesions are cytotoxic only at the next DNA
replication. Hence kill rates are low for non-replicating cells (D, Q) and high for cycling
cells (P).

**While TMZ is active**, add continuous death events:

| State | Extra death rate (day⁻¹) |
|-------|--------------------------|
| S | $\delta_S^{\text{TMZ}} = 0.03$ |
| P | $\delta_P^{\text{TMZ}} = 0.20$ |
| D | $\delta_D^{\text{TMZ}} = 0.05$ |
| Q | $\delta_Q^{\text{TMZ}} = 0.01$ |

All `[ASSUMPTION]`. The contrast $\delta_P \gg \delta_S, \delta_Q$ encodes the central
biological mechanism: TMZ selects pre-existing resistant slow/non-cycling cells (Lan 2017).

**Therapy-induced dormancy:** Continuous event during TMZ at rate
$\sigma_T^{\text{TMZ}} \cdot n_P$. (P → Q.)

**Resistance selection vs. emergence:**
- **Selection (modeled):** Pre-existing S and Q cells have low TMZ kill rate; they are
  enriched as the bulk P dies. This is the Lan 2017 mechanism.
- **Emergence (not modeled in v1):** De novo TMZ-resistant clones arising from genetic
  mutation are not implemented. Documented as a v2 extension.

**Repair interpretation:** MGMT-mediated repair is captured by a single multiplier on the
TMZ kill rates: methylated MGMT → ~2× kill (or equivalently, unmethylated MGMT → ~0.5×
kill). The multiplier is a sensitivity *parameter*, not a fixed model value.

### 3.4 Combined therapy (Stupp)

Concomitant RT + TMZ during days 0–41 (both modules active simultaneously), then recovery,
then adjuvant TMZ alone.

**Avoiding double-counting:**
- RT kills are applied at *discrete fraction times* (Binomial draws).
- TMZ kills are *continuous CTMC events* (exponentially clocked).
- Because the two mechanisms act on different time grids (one discrete, one continuous),
  they cannot collide on the same event. The probability that a given cell is killed in any
  small interval is well-defined as the sum/product of independent kill mechanisms.
- Therapy-induced dormancy from RT and TMZ are *both* active during the concomitant phase.
  This is a deliberate modeling choice: empirically, GBM cells become quiescent under
  combined stress, and both stressors contribute additively to the σ_T rate.

**Synergy assumption:** v1 assumes **additive** effects on death rate (no positive or
negative synergy multiplier). Documented as a limitation; clinical Stupp evidence suggests
additive-to-mildly-synergistic, but no clean quantification.

### 3.5 Stupp + Tumor Treating Fields (TTF)

TTF (Optune) adds a continuous low-rate kill event throughout the entire simulation (or
from a user-defined start time), scaled by a compliance parameter (default 0.75 from
EF-14 trial median).

| State | $c_{\text{comp}} \cdot \delta_x^{\text{TTF}}$ (day⁻¹) |
|-------|-------------------------------------------------------|
| S | $0.75 \times 0.005 = 0.00375$ |
| P | $0.75 \times 0.08 = 0.06$ |
| D | $0.75 \times 0.002 = 0.0015$ |
| Q | $0.75 \times 0.002 = 0.0015$ |

TTF disrupts mitosis, so the P kill rate dominates. No therapy-induced dormancy from TTF
in v1.

---

## 4. Parameters

Evidence-level legend:

- **LIT** — directly cited from a paper in `references/markdown_summaries/`
- **THE** — from the bachelor thesis (must be re-checked when thesis code is consulted)
- **ASM** — biologically motivated assumption / order-of-magnitude estimate
- **FIT** — fitted to a target output (none in v1)
- **UNK** — unknown; treated as free parameter

**YAML?** = exposed in `config/default_params.yaml` and overridable per run.

### 4.1 Population scaling

| Parameter | Meaning | Unit | Default | Evidence | YAML? |
|-----------|---------|------|---------|----------|-------|
| $K$ | Carrying capacity / population scale | cells | 1000 | UNK | yes |
| $n_S(0)$ | Initial GSC count | cells | 5 | ASM | yes |
| $n_P(0)$ | Initial progenitor count | cells | 50 | ASM | yes |
| $n_D(0)$ | Initial differentiated count | cells | 100 | ASM | yes |
| $n_Q(0)$ | Initial dormant count | cells | 2 | ASM | yes |

### 4.2 Basal proliferation and death

| Parameter | Meaning | Unit | Default | Evidence | YAML? |
|-----------|---------|------|---------|----------|-------|
| $\lambda_S$ | S division rate | day⁻¹ | 0.02 | LIT (upper bound from Lan 2017) | yes |
| $\lambda_P$ | P division rate | day⁻¹ | 0.20 | ASM | yes |
| $\mu_S$ | S natural death | day⁻¹ | 0.005 | ASM | yes |
| $\mu_P$ | P natural death | day⁻¹ | 0.02 | ASM | yes |
| $\mu_D$ | D natural death | day⁻¹ | 0.05 | ASM | yes |
| $\mu_Q$ | Q natural death | day⁻¹ | 0.003 | ASM | yes |
| $c_S, c_P, c_D, c_Q$ | Competition coefficients | day⁻¹ | 0.005 each | ASM | yes |

### 4.3 Phenotypic switching

| Parameter | Meaning | Unit | Default | Evidence | YAML? |
|-----------|---------|------|---------|----------|-------|
| $\alpha_S$ | S asymmetric division → P | day⁻¹ | 0.01 | ASM | yes |
| $s_{SP}$ | S → P commitment | day⁻¹ | 0.01 | ASM | yes |
| $s_{PD}$ | P → D differentiation | day⁻¹ | 0.05 | ASM | yes |
| $\sigma$ | Spontaneous dormancy P → Q | day⁻¹ | 0.005 | LIT (structure from Blath 2023) | yes |
| $\varrho$ | Resuscitation Q → P | day⁻¹ | 0.02 | LIT (structure from Blath 2023) | yes |

### 4.4 Radiotherapy

| Parameter | Meaning | Unit | Default | Evidence | YAML? |
|-----------|---------|------|---------|----------|-------|
| $n_{\text{frac}}$ | Number of fractions | — | 30 | LIT (Stupp) | yes |
| $d_{\text{frac}}$ | Dose per fraction | Gy | 2.0 | LIT (Stupp) | yes (informational) |
| $\Delta t_{\text{frac}}$ | Interval between fractions | day | 1.0 | LIT (simplified) | yes |
| $\kappa_S, \kappa_P, \kappa_D, \kappa_Q$ | Kill probability per fraction | — | 0.03 / 0.20 / 0.10 / 0.01 | ASM | yes |
| $\sigma_T^{\text{RT}}$ | RT-induced dormancy fraction | — | 0.10 | ASM | yes |

### 4.5 Temozolomide

| Parameter | Meaning | Unit | Default | Evidence | YAML? |
|-----------|---------|------|---------|----------|-------|
| Concomitant duration | days 0–41 | day | 42 | LIT (Stupp) | yes |
| Adjuvant cycles | Number of 28-day cycles | — | 6 | LIT (Stupp) | yes |
| Treatment days per cycle | "On" days per 28-day cycle | day | 5 | LIT (Stupp) | yes |
| $\delta_S, \delta_P, \delta_D, \delta_Q$ | TMZ kill rate per day | day⁻¹ | 0.03 / 0.20 / 0.05 / 0.01 | ASM | yes |
| $\sigma_T^{\text{TMZ}}$ | TMZ-induced dormancy rate | day⁻¹ | 0.10 | ASM | yes |
| $f_{\text{MGMT}}$ | MGMT methylation kill multiplier | — | 2.0 | ASM | yes (sensitivity) |

### 4.6 Tumor Treating Fields

| Parameter | Meaning | Unit | Default | Evidence | YAML? |
|-----------|---------|------|---------|----------|-------|
| $c_{\text{comp}}$ | Compliance | — | 0.75 | LIT (EF-14) | yes |
| $\delta_S^{\text{TTF}}, ..., \delta_Q^{\text{TTF}}$ | TTF kill rate per day | day⁻¹ | 0.005 / 0.08 / 0.002 / 0.002 | ASM | yes |

### 4.7 Simulation control

| Parameter | Meaning | Unit | Default | Evidence | YAML? |
|-----------|---------|------|---------|----------|-------|
| `t_end` | Simulation horizon | day | 365 | — | yes |
| `seed` | RNG seed (None → random) | — | None | — | yes |
| `n_replicates` | Independent trajectories per experiment | — | 100 | — | yes |
| `solver` | "ssa" / "ode" | — | "ssa" | — | yes |

> **Honesty clause for the documentation:** No paper in our reference set provides
> calibrated CTMC transition rates for human GBM. All defaults above marked ASM are
> order-of-magnitude estimates chosen so that (a) the no-therapy baseline produces
> visible tumor growth on a 6-month horizon, and (b) the Stupp protocol produces visible
> tumor reduction followed by recurrence. They are NOT clinically predictive values.

---

## 5. Outputs

### 5.1 Per-run outputs (one simulation trajectory)

| Output | Type | Shape | Notes |
|--------|------|-------|-------|
| `times` | array, days | (n_steps,) | Event times for SSA; uniform grid for ODE |
| `counts` | array, integers | (n_steps, 4) | Columns: S, P, D, Q |
| `total_burden` | array | (n_steps,) | $n_S + n_P + n_D + n_Q$ |
| `resistant_fraction` | array | (n_steps,) | $(n_S + n_Q) / n_{\text{tot}}$ — "phenotypically protected" fraction |
| `cycling_fraction` | array | (n_steps,) | $(n_S + n_P) / n_{\text{tot}}$ |
| `cumulative_deaths_by_state` | array | (n_steps, 4) | Tracks therapy + natural mortality |
| `cumulative_deaths_by_cause` | array | (n_steps, n_causes) | Splits death by RT vs TMZ vs TTF vs natural vs competition |
| `extinct` | bool | scalar | True if $n_{\text{tot}}$ reaches 0 |
| `time_to_extinction` | float \| None | scalar | First time at which $n_{\text{tot}} = 0$, or None |
| `time_to_recurrence` | float \| None | scalar | First time after nadir at which $n_{\text{tot}}$ re-exceeds the initial total |
| `nadir_burden` | int | scalar | Minimum tumor burden over the trajectory |
| `nadir_time` | float | scalar | Time of nadir |
| `progression_proxy` | array | (n_steps,) | Log10(total_burden) clipped at 0; surrogate for "tumor signal" |

### 5.2 Metadata stamped on every run

- `parameters`: full ModelParams snapshot (so the run is reproducible from this alone)
- `scenario`: one of `none | rt | tmz | stupp | stupp_ttf`
- `seed`: integer used for the RNG
- `solver`: `ssa` or `ode`
- `git_commit`: hash of the code at run time
- `runtime_seconds`: wall-clock duration

### 5.3 Per-experiment outputs (n_replicates trajectories per scenario)

- `extinction_probability`: empirical fraction of replicates with `extinct == True`
- `median_time_to_recurrence`: with bootstrap 95% CI
- `quantile_trajectories`: 5th / 50th / 95th percentile of total_burden over time
- `final_burden_distribution`: histogram of total_burden at t_end
- `resistant_fraction_at_t_end`: distribution across replicates

All outputs are stored as Parquet (numeric) + JSON (metadata) — single file per run,
single directory per experiment.

---

## 6. Experiments

Each experiment is a script in `experiments/` that produces a deterministic directory of
output files. The same experiment script must always produce the same plots given the
same seed.

### 6.1 Experiment 1 — Baseline growth (no therapy)

**Goal:** Confirm tumor grows from initial state, reaches a competition-limited plateau,
and the S/P/D/Q steady-state fractions are biologically plausible.

**Setup:** scenario = `none`, t_end = 365, n_replicates = 100, default params.

**Pass criteria:** Median final burden > 5× initial; resistant fraction settles to a stable
value < 1; no replicate exhibits unbounded growth above 10K (carrying capacity active).

### 6.2 Experiment 2 — Therapy comparison

**Goal:** Compare nadir, recurrence time, and extinction probability across the five
scenarios (none / RT / TMZ / Stupp / Stupp+TTF).

**Setup:** t_end = 365, n_replicates = 100 per scenario, default params.

**Output:** A 5-scenario panel plot showing median trajectory + 5–95% band per scenario,
and a summary table (extinction prob, median nadir, median recurrence time).

### 6.3 Experiment 3 — Timing comparison

**Goal:** Does delaying TMZ start by 1 / 2 / 4 weeks change outcomes?

**Setup:** Stupp scenario, TMZ start offset in {0, 7, 14, 28} days. 100 replicates per
condition.

**Pass criteria for the experiment being well-posed:** Output is monotone or has a clear
optimum — not random noise (which would indicate the noise floor exceeds the effect).

### 6.4 Experiment 4 — Resistant-fraction dynamics (no de novo resistance)

**Goal:** Show that the resistant fraction $(n_S + n_Q)/n_{\text{tot}}$ rises under
therapy and falls during recovery — pure selection dynamics from pre-existing heterogeneity.

**Setup:** Stupp scenario, 50 replicates. Track resistant_fraction over time.

**Interpretation:** This is the model's qualitative reproduction of the Lan 2017 result.
A rising resistant fraction under therapy is the model's signature.

### 6.5 Experiment 5 — Sensitivity analysis

**Goal:** Identify which assumption parameters most affect the recurrence outcome.

**Setup:** One-at-a-time variation of high-priority assumption parameters (see
`docs/assumptions.md` priority HIGH list): $\sigma$, $\varrho$, $\sigma_T^{\text{TMZ}}$,
$\kappa_S^{\text{RT}}$, $\delta_P^{\text{TMZ}}$, $f_{\text{MGMT}}$.

Each varied across {0.25×, 0.5×, 1×, 2×, 4×} default. 50 replicates per condition.

**Output:** Tornado plot of effect-on-median-recurrence-time per parameter.

### 6.6 Experiment 6 — Stochastic ensemble for extinction probability

**Goal:** For each therapy scenario, estimate the cure probability (= P[extinction by
day 365]) and compare to the analytical branching-process bound $\mu_P / \lambda_P$
(Blath 2023).

**Setup:** Small initial tumor (n_S=1, n_P=5, n_D=0, n_Q=0). 1000 replicates per
scenario.

**Pass criteria for implementation validation:** Without therapy, the empirical
extinction probability must approach $\mu_P / \lambda_P$ within statistical uncertainty.
This is a built-in correctness check, not just an experiment.

### 6.7 Experiment 7 — SSA vs. ODE agreement (validation only)

**Goal:** Verify SSA mean trajectory converges to ODE solution as K increases.

**Setup:** No therapy. K ∈ {100, 1000, 10000, 100000}. 200 SSA replicates each;
compare mean trajectory to ODE solution.

**Pass criteria:** At K = 10⁴, ‖mean(SSA) − ODE‖ / max(ODE) < 5% on every state.

---

## 7. Plots and Demo

All plots produced by `experiments/<name>.py`, saved into `experiments/<name>/figures/`.

### 7.1 Trajectory plot

Single-replicate time series. One line per state (S, P, D, Q), one for total. Therapy
windows shaded in the background. Log-y axis for the total, linear for fractions.

### 7.2 Stacked population plot

Stacked area chart of S/P/D/Q over time, for a single representative trajectory or median
across replicates. Communicates *composition*: when therapy ends, what is the tumor made
of?

### 7.3 Therapy overlay plot

Overlay of 5 scenarios' median trajectory (with 5–95% band) on the same axes. The
headline visual.

### 7.4 Sensitivity plot

Tornado plot from Experiment 5: bars showing positive/negative effect on median
recurrence time for each parameter at ±factor variation.

### 7.5 Distribution across runs

Per scenario at $t = $ end: histogram of total_burden across replicates, with extinction
fraction shown as a separate bar at zero.

### 7.6 Demo GIF

20-second animation showing two trajectories side by side — Stupp vs. Stupp+TTF —
animating tumor composition (stacked area) as time progresses. Treatment windows shaded.
Counter showing days elapsed.

Format: matplotlib `FuncAnimation` → MP4 → GIF. Stored at
`05_PORTFOLIO_ASSETS/gifs/gbm_demo.gif`. Resolution target: 800×450, ≤ 5 MB.

---

## 8. Validation and Limitations

### 8.1 What the v1 model CAN show

- **Qualitative mechanism comparison.** Whether dormancy + GSC pre-existing resistance
  reproduces the recurrence-after-remission pattern. Yes, by construction, but the
  *strength* of the effect across parameter assumptions is an honest output.
- **Relative ordering of therapy scenarios.** Median nadir and recurrence time should rank
  no-therapy < monotherapy < Stupp < Stupp+TTF. If they do not, the parameters are wrong
  or the model is wrong.
- **Stochastic cure probability** in a small-population regime.
- **Selection dynamics** of phenotypically resistant subpopulations.
- **Sensitivity rankings** — which assumption parameters most affect qualitative outcomes.

### 8.2 What the v1 model CANNOT show

- **Clinical predictions for individual patients.** No patient-specific calibration; no
  imaging input; no genomic profile.
- **Quantitative survival estimates.** No mapping from cell count to clinical endpoints
  (OS, PFS).
- **Spatial dynamics.** Invasion, infiltrative growth, MRI-visible margin progression.
  These require PDE / spatial models.
- **Acquired mutational resistance.** Genetic drift, MGMT-promoter methylation gain/loss,
  TERT mutation effects — all absent.
- **Immune effects.** No T-cell infiltration, no immunotherapy response.
- **Drug pharmacokinetics.** No PK/PD model; TMZ is a binary on/off.
- **Tumor heterogeneity beyond 4 states.** Neftel transcriptional plasticity, single-cell
  trajectories.

### 8.3 What real clinical prediction would require

- Patient-specific calibration of growth rates and resistance fractions from longitudinal
  imaging.
- Spatial component for invasion (PDE on segmented MRI, or 3D ABM).
- Pharmacokinetic / pharmacodynamic model linking dose to intracellular concentration to
  damage.
- Molecular biomarkers as inputs (MGMT methylation, IDH status, TERT, EGFR amplification).
- Validation against held-out patient cohorts with documented treatment outcomes.
- Regulatory-grade software lifecycle (V&V, traceability, change control).

### 8.4 How to phrase limitations honestly

In the README and any portfolio materials, the framing should be:

> This is a **mechanistic stochastic toy model** for studying how cell-state heterogeneity
> and dormancy interact with standard GBM therapies. It is calibrated to qualitatively
> reproduce known clinical patterns (recurrence after Stupp, modest TTF benefit) using
> parameters that are biologically motivated but not patient-specific. It is **not a
> clinical decision-support tool** and makes no quantitative predictions for individual
> patients. The model's value is pedagogical and exploratory — it makes the consequences
> of stochastic dormancy and phenotypic selection mathematically transparent.

Anywhere a default parameter is shown, the evidence tag (LIT / ASM / UNK) must travel with
it. The phrase "predicts" should be reserved for "predicts under the stated assumptions";
never "predicts in patients."

---

## 9. Open Decisions (review needed before implementation locks in)

1. **K interpretation.** Is K an absolute cell count or an arbitrary scaling parameter?
   v1 treats it as scaling; alternative is to set K = clinically observed peak tumor cell
   count (~10⁹ cells), in which case the simulation cost becomes prohibitive.
2. **σ_T^RT additive vs. fixed-fraction.** Currently the spec says "a Binomial fraction of
   surviving P cells move to Q after each fraction." An alternative is a continuous CTMC
   event activated only on RT days. The Binomial is closer to the biological mechanism;
   the continuous variant is closer to Blath 2023's formulation. Pick one.
3. **Initial population composition.** The defaults (5/50/100/2) are pulled from the air.
   Worth deriving them from a no-therapy steady-state run to make them internally
   consistent.
4. **Thesis parameter integration.** Once the bachelor thesis code is consulted, any
   parameters carried over should be tagged THE in the parameter table.

---

## 10. Out-of-Scope Pointers (acknowledged, deferred)

- **Spatial extension (v2):** PDE-based invasion model, Conte & Surulescu 2021 roadmap.
- **Immune extension (v3):** T-cell compartment, Baar 2016 framework.
- **RL-based therapy optimization (research extension):** Once v1 is stable, the simulator
  becomes the environment for a reinforcement-learning agent that designs personalized
  schedules.
- **Calibration against published trial data:** Possible if synthetic-cohort calibration
  against EF-14 or Stupp Kaplan–Meier curves is performed; requires a survival-mapping
  layer not in v1.

---

## 11. Document Status

This specification is the source-of-truth for v1 design. Code in `src/gbm_ctmc/` (already
written as a skeleton) must be checked against this spec before being considered v1-ready.
Any deviation must either be reflected back into this document or fixed in the code.

| Section | Reviewer | Date | Sign-off |
|---------|----------|------|----------|
| 1 — Biological scope | | | |
| 2 — Mathematical framework | | | |
| 3 — Therapy modules | | | |
| 4 — Parameters | | | |
| 5 — Outputs | | | |
| 6 — Experiments | | | |
| 7 — Plots | | | |
| 8 — Validation & limitations | | | |
