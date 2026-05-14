# GBM CTMC — Formal Model Specification (v1)

**Version:** 1.0  
**Date:** 2026-05-14  
**Status:** Draft — not peer-reviewed

This document defines the mathematical model used in the GBM CTMC simulation project. It is
intended to be self-contained for a reader with graduate-level mathematics and no prior GBM
biology background. Biological claims are sourced; modeling assumptions are labeled explicitly.

**Evidence level labels used throughout:**
- `[LITERATURE]` — directly supported by a cited source
- `[ASSUMPTION]` — biologically motivated estimate; must be varied in sensitivity analysis
- `[FREE PARAMETER]` — uncalibrated; chosen for illustrative purposes only
- `[INTERPRETATION]` — logical inference from cited sources, not a direct quote

---

## 1. Biological Background

### 1.1 Glioblastoma (GBM)

Glioblastoma (WHO grade IV, IDH wild-type) is the most aggressive primary brain tumor. Median
overall survival is approximately 15 months with standard treatment; 5-year survival is ~5%
`[LITERATURE: Alfonso et al. 2017]`. The primary cause of treatment failure is recurrence,
driven by a small population of therapy-resistant glioma stem cells (GSCs).

### 1.2 Cell State Hierarchy

Lan et al. (2017, *Nature*) used fate mapping of patient-derived GBM xenografts to establish a
3-state proliferative hierarchy `[LITERATURE: Lan et al. 2017]`:

| State | Label | Biological Identity |
|-------|-------|---------------------|
| S | GSC (slow-cycling) | Glioma stem cell; self-renewing; slow division; therapy-resistant |
| P | Progenitor (fast-cycling) | Transit-amplifying cell; rapid proliferation; therapy-sensitive |
| D | Differentiated | Post-mitotic; no self-renewal; no proliferation |

**Direction:** S → P (irreversible commitment), P → D (irreversible differentiation).  
**Self-renewal:** S can divide symmetrically (S → 2S) or asymmetrically (S → S + P).  
`[INTERPRETATION: hierarchy inferred from Lan 2017 fate-mapping; exact symmetric/asymmetric
fractions are modeled as a free parameter]`

A fourth state is added based on Blath et al. (2023):

| State | Label | Biological Identity |
|-------|-------|---------------------|
| Q | Quiescent/Dormant | Cell-cycle arrested; non-proliferating; therapy-evading |

**Q entry:** From P under therapy stress or spontaneously.  
**Q exit (resuscitation):** Spontaneous, or upon drug washout.  
`[LITERATURE: Blath et al. 2023 for dormancy mechanism; Q state in GBM supported by 2022
GBM-specific literature on BMP-driven quiescence]`

### 1.3 Therapy Resistance Mechanisms Modeled

- **Pre-existing GSC resistance:** TMZ selects pre-existing resistant GSCs, not de novo mutations `[LITERATURE: Lan 2017]`
- **Dormancy-induced failure:** Cycling cells enter Q state under therapy; survive; resuscitate after treatment ends `[LITERATURE: Blath 2023]`
- **MGMT methylation:** Primary TMZ resistance biomarker; implemented as a kill-rate multiplier `[LITERATURE: reviewed]`

**Explicitly excluded from v1:**
- Neftel 2019 four transcriptional states (NPC/OPC/AC/MES-like) — orthogonal classification; 16-state combination is unparameterizable `[DELIBERATE SIMPLIFICATION]`
- Spatial structure, go-or-grow phenotype switching — v2 extension
- Immune response — v3 extension using Baar 2016 framework
- Genetic resistance mutations — excluded; focus is on phenotypic plasticity

---

## 2. State Space

### 2.1 Cancer Cell Population

The cancer cell population at time *t* is described by:

$$\mathbf{N}(t) = \bigl(n_S(t),\; n_P(t),\; n_D(t),\; n_Q(t)\bigr) \in \mathbb{N}_0^4$$

where $n_x(t)$ is the number of cells in state $x \in \{S, P, D, Q\}$ at time $t$.

### 2.2 Drug Compartments (Therapy Scenarios)

For therapy scenarios, drug concentrations are tracked as separate state variables. Following
Blath et al. (2023) `[LITERATURE]`, drug agents are modeled as a particle count decaying
exponentially:

$$\mathbf{N}(t) = \bigl(n_S, n_P, n_D, n_Q, n_{\mathrm{tmz}}\bigr) \in \mathbb{N}_0^5$$

where $n_{\mathrm{tmz}}(t)$ is the current TMZ agent count (pulsed dosing: injected at fixed
intervals, decays at rate $\beta_{\mathrm{tmz}}$). Radiotherapy is modeled as instantaneous
fractional kill events rather than a continuous drug compartment.

### 2.3 Carrying Capacity Scaling

Following Baar et al. (2016) `[LITERATURE]`, all competition terms are scaled by a carrying
capacity parameter $K \in \mathbb{N}$. The rescaled process $\bar{\mathbf{n}}(t) = \mathbf{N}(t)/K$
converges to the ODE mean-field limit as $K \to \infty$ (Ethier–Kurtz theorem). In simulations,
$K$ is a free parameter controlling the effective tumor size at which stochastic fluctuations
become negligible `[FREE PARAMETER]`.

---

## 3. Transition Rates (Q-matrix)

This section defines all events in the continuous-time Markov chain. The infinitesimal generator
(Q-matrix) is defined by the off-diagonal transition rates listed below. The diagonal entries are
$q_{ii} = -\sum_{j \neq i} q_{ij}$.

### 3.1 Notation

Let $\mathbf{n} = (n_S, n_P, n_D, n_Q)$ denote the current state. Let $\delta_x$ be the unit
vector increasing state $x$ by 1. Rates are given in units of day$^{-1}$ unless noted.

### 3.2 Basal Events (No Therapy)

#### S state — GSC

| Event | State change | Rate | Evidence |
|-------|-------------|------|----------|
| S division (symmetric) | $\mathbf{n} \to \mathbf{n} + \delta_S$ | $\lambda_S \cdot n_S$ | `[ASSUMPTION]` |
| S asymmetric division | $\mathbf{n} \to \mathbf{n} + \delta_P$ | $\alpha_S \cdot n_S$ | `[ASSUMPTION]` |
| S natural death | $\mathbf{n} \to \mathbf{n} - \delta_S$ | $\mu_S \cdot n_S$ | `[ASSUMPTION]` |
| S competition death | $\mathbf{n} \to \mathbf{n} - \delta_S$ | $c_S \cdot n_S \cdot n_{\mathrm{tot}} / K$ | `[ASSUMPTION]` based on `[LITERATURE: Baar 2016]` |
| S → P commitment | $\mathbf{n} \to \mathbf{n} - \delta_S + \delta_P$ | $s_{SP} \cdot n_S$ | `[ASSUMPTION]` |

where $n_{\mathrm{tot}} = n_S + n_P + n_D + n_Q$ is the total cell count.

#### P state — Progenitor

| Event | State change | Rate | Evidence |
|-------|-------------|------|----------|
| P division | $\mathbf{n} \to \mathbf{n} + \delta_P$ | $\lambda_P \cdot n_P$ | `[ASSUMPTION]` |
| P natural death | $\mathbf{n} \to \mathbf{n} - \delta_P$ | $\mu_P \cdot n_P$ | `[ASSUMPTION]` |
| P competition death | $\mathbf{n} \to \mathbf{n} - \delta_P$ | $c_P \cdot n_P \cdot n_{\mathrm{tot}} / K$ | `[ASSUMPTION]` |
| P → D differentiation | $\mathbf{n} \to \mathbf{n} - \delta_P + \delta_D$ | $s_{PD} \cdot n_P$ | `[ASSUMPTION]` |
| P → Q (spontaneous dormancy) | $\mathbf{n} \to \mathbf{n} - \delta_P + \delta_Q$ | $\sigma \cdot n_P$ | `[LITERATURE: Blath 2023, σ]` |

#### D state — Differentiated

| Event | State change | Rate | Evidence |
|-------|-------------|------|----------|
| D natural death | $\mathbf{n} \to \mathbf{n} - \delta_D$ | $\mu_D \cdot n_D$ | `[ASSUMPTION]` |

No division for D. `[LITERATURE: Lan 2017 — differentiated cells have no self-renewal]`

#### Q state — Quiescent

| Event | State change | Rate | Evidence |
|-------|-------------|------|----------|
| Q natural death | $\mathbf{n} \to \mathbf{n} - \delta_Q$ | $\mu_Q \cdot n_Q$ | `[ASSUMPTION]` |
| Q → P (spontaneous resuscitation) | $\mathbf{n} \to \mathbf{n} - \delta_Q + \delta_P$ | $\varrho \cdot n_Q$ | `[LITERATURE: Blath 2023, ϱ]` |

### 3.3 Total Rate and Gillespie Step

The total event rate is:
$$R(\mathbf{n}) = \sum_e r_e(\mathbf{n})$$

At each Gillespie step:
1. Generate waiting time $\tau \sim \mathrm{Exp}(R(\mathbf{n}))$
2. Advance time: $t \to t + \tau$
3. Select event $e$ with probability $r_e(\mathbf{n}) / R(\mathbf{n})$
4. Apply state change $\mathbf{n} \to \mathbf{n} + v_e$

`[LITERATURE: Kraut 2021 — clearest algorithmic description]`

---

## 4. Therapy Modifications

Therapy is modeled as additional kill events layered onto the basal CTMC. Each therapy module
activates specific rates. The following subsections describe each of the four therapy scenarios
in version 1.

### 4.1 Scenario 0: No Therapy (Baseline)

Basal rates only. Used to calibrate tumor growth dynamics and establish pre-treatment equilibrium.

### 4.2 Scenario 1: Radiotherapy (RT)

**Stupp RT protocol:** 30 fractions × 2 Gy = 60 Gy total, delivered Monday–Friday over 6 weeks.
`[LITERATURE: Stupp et al. 2005]`

**Modeling approach:** Discrete fractional kill events, not continuous kill rate. At each RT
fraction event (modeled as a Dirac pulse at time $t_k$):

$$n_x \to n_x - \mathrm{Binomial}(n_x,\; \kappa_x^{\mathrm{RT}})$$

where $\kappa_x^{\mathrm{RT}} \in [0,1]$ is the per-fraction kill probability for state $x$.

**Rationale for discrete model:** RT acts acutely at the time of dose delivery; exponential decay
between fractions is fast (sub-day); modeling as instantaneous fractional kill is a valid
approximation for daily fractions `[INTERPRETATION]`.

**Kill probability by state:**

| State | $\kappa_x^{\mathrm{RT}}$ | Rationale |
|-------|--------------------------|-----------|
| S | 0.03 | GSC radio-resistance; slow-cycling → reduced RT sensitivity `[ASSUMPTION]` |
| P | 0.20 | Fast-cycling; maximal DNA damage during S/G2/M phase `[ASSUMPTION]` |
| D | 0.10 | Post-mitotic but DNA accessible `[ASSUMPTION]` |
| Q | 0.01 | Cell-cycle arrested; deeply radio-resistant `[ASSUMPTION]` |

**Therapy-induced dormancy (RT):** RT induces quiescence in a fraction of surviving P cells:
$$n_P \to n_P - k,\quad n_Q \to n_Q + k, \quad k \sim \mathrm{Binomial}(n_P^{\mathrm{surviving}},\; \sigma_T^{\mathrm{RT}})$$
`[ASSUMPTION: σ_T^RT, magnitude informed by Blath 2023]`

### 4.3 Scenario 2: Temozolomide (TMZ)

**Stupp TMZ protocol:**
- Concomitant phase (weeks 1–6): 75 mg/m² daily, concurrent with RT
- Adjuvant phase: 6 cycles × 5/28-day schedule, 150–200 mg/m²
`[LITERATURE: Stupp et al. 2005]`

**Modeling approach:** TMZ kill is applied as a continuous daily kill rate during treatment days,
implemented as additional per-cell death events in the CTMC.

Additional death rates during active TMZ (per cell per day):

| State | $\delta_x^{\mathrm{TMZ}}$ | Rationale |
|-------|---------------------------|-----------|
| S | 0.03 | Pre-existing resistance via MGMT or other mechanisms `[LITERATURE: Lan 2017, ASSUMPTION for rate]` |
| P | 0.20 | Cycling cells maximally sensitive to alkylating damage `[ASSUMPTION]` |
| D | 0.05 | `[ASSUMPTION]` |
| Q | 0.01 | Non-replicating; alkylation damage not converted to lethal DSBs `[ASSUMPTION]` |

**Therapy-induced dormancy (TMZ):** TMZ induces P → Q transitions at rate $\sigma_T^{\mathrm{TMZ}}$
during active treatment. `[LITERATURE: Blath 2023, σ_T]`

**MGMT methylation:** If MGMT is methylated, multiply all TMZ kill rates by factor $f_{\mathrm{MGMT}} \approx 2$. This is implemented as a sensitivity analysis parameter, not a fixed model constant.
`[ASSUMPTION for magnitude; MGMT mechanism is LITERATURE]`

### 4.4 Scenario 3: Combined (Stupp Protocol)

Sequential combination of Scenarios 1 + 2 following the Stupp protocol timeline:

```
Week 1–6:   RT (30 fractions) + concomitant TMZ (75 mg/m², daily)
Week 7–10:  Recovery (no therapy)
Week 11+:   Adjuvant TMZ (6 cycles, 5/28-day)
```

During the concomitant phase, both the RT fractional kill events and the TMZ continuous kill
rates are active simultaneously.

### 4.5 Scenario 4: Stupp + Tumor Treating Fields (TTF)

TTF (Optune) adds a continuous kill effect targeting mitotic cells, modeled as an additional
death rate active continuously (overlapping with all therapy phases and recovery):

| State | $\delta_x^{\mathrm{TTF}}$ | Rationale |
|-------|---------------------------|-----------|
| S | 0.005 | Slow-cycling; rarely in mitosis `[ASSUMPTION]` |
| P | 0.08 | Cycling cells disrupted in metaphase by alternating electric fields `[ASSUMPTION]` |
| D | 0.002 | Post-mitotic; TTF negligible `[ASSUMPTION]` |
| Q | 0.002 | Non-cycling; TTF negligible `[ASSUMPTION]` |

**Compliance scaling:** Effective kill rate = $c_{\mathrm{comp}} \cdot \delta_x^{\mathrm{TTF}}$,
where $c_{\mathrm{comp}} = 0.75$ (default, based on EF-14 trial median compliance `[LITERATURE]`).

---

## 5. Mean-Field ODE Limit

### 5.1 Derivation Principle

By the Ethier–Kurtz (1986) law of large numbers for individual-based Markov processes
`[LITERATURE: Kraut 2021]`, the rescaled process $\bar{n}_x(t) = n_x(t)/K$ converges almost
surely to the solution of the following ODE system as $K \to \infty$:

$$\frac{d}{dt}\bar{n}_x = \sum_{e \in E} (v_e)_x \cdot r_e\bigl(\bar{\mathbf{n}}\bigr)$$

where $v_e$ is the state-change vector of event $e$ and $r_e$ is its rate.

### 5.2 Basal ODE System (No Therapy)

Let $s = \bar{n}_S$, $p = \bar{n}_P$, $d = \bar{n}_D$, $q = \bar{n}_Q$,
$n = s + p + d + q$.

$$\dot{s} = \lambda_S s - \mu_S s - c_S s n - s_{SP} s$$

$$\dot{p} = \alpha_S s + s_{SP} s + \lambda_P p - \mu_P p - c_P p n - s_{PD} p - \sigma p + \varrho q$$

$$\dot{d} = s_{PD} p - \mu_D d$$

$$\dot{q} = \sigma p - \varrho q - \mu_Q q$$

**Interpretation:**
- $s$ grows via S division ($\lambda_S$), decays via death ($\mu_S$), competition ($c_S n$), and commitment ($s_{SP}$)
- $p$ receives input from S asymmetric division ($\alpha_S s$) and S→P commitment, gains from P division, loses to differentiation and dormancy entry, gains from resuscitation
- $d$ is a sink: gains from P→D, loses to death
- $q$ cycles between dormant and active via $\sigma$ and $\varrho$

### 5.3 Therapy ODE Modifications

**RT (between fractions):** Continuous kill rates are zero; fractional kill is applied as
instantaneous resets at fraction times $t_k$:
$$\bar{n}_x(t_k^+) = \bar{n}_x(t_k^-) \cdot (1 - \kappa_x^{\mathrm{RT}})$$

**TMZ (active days):** Add kill terms to each state's ODE:
$$\dot{x}\big|_{\mathrm{TMZ}} = \dot{x}\big|_{\mathrm{basal}} - \delta_x^{\mathrm{TMZ}} \cdot \bar{n}_x$$

**TTF (continuous):**
$$\dot{x}\big|_{\mathrm{TTF}} = \dot{x}\big|_{\mathrm{prev}} - c_{\mathrm{comp}} \cdot \delta_x^{\mathrm{TTF}} \cdot \bar{n}_x$$

---

## 6. Analytical Results

### 6.1 Extinction Probability (Early Tumor)

For the minimal active/dormant sub-model (ignoring S and D), the extinction probability starting
from a single active (P) or dormant (Q) cell satisfies, in the branching process approximation
(small population, no competition):

$$\bar{q}_P = \bar{q}_Q = \frac{\mu_P}{\lambda_P}$$

`[LITERATURE: Blath et al. 2023, Section 2.4 — proved rigorously]`

**Key insight:** Spontaneous dormancy does NOT change the extinction probability. It may delay
extinction but cannot prevent it if $\mu_P < \lambda_P$ (net growth). The growth rate
(principal eigenvalue) is determined by the offspring mean matrix; dormancy reduces but does
not eliminate it.

### 6.2 Basic Reproduction Number

The net growth condition for the active population without therapy:
$$\lambda_P - \mu_P - s_{PD} - \sigma > 0 \quad \Longleftrightarrow \quad \text{tumor grows}$$

This is the threshold condition for exponential growth in the linearized system.

---

## 7. Parameter Summary

All parameters with default values and evidence levels are maintained in
`config/default_params.yaml`. Here is a condensed overview.

### 7.1 Parameters with Any Literature Support

| Symbol | Meaning | Default | Evidence |
|--------|---------|---------|----------|
| $\kappa_S^{\mathrm{RT}}$ / $\kappa_P^{\mathrm{RT}}$ | RT kill fraction per 2 Gy fraction | 0.03 / 0.20 | `[ASSUMPTION]`, order from RT biology |
| Number of RT fractions | Stupp protocol | 30 | `[LITERATURE: Stupp 2005]` |
| RT dose per fraction | Stupp protocol | 2 Gy | `[LITERATURE: Stupp 2005]` |
| TMZ concomitant dose | Stupp | 75 mg/m² | `[LITERATURE: Stupp 2005]` |
| TMZ adjuvant cycles | Stupp | 6 | `[LITERATURE: Stupp 2005]` |
| TMZ adjuvant schedule | Stupp | 5/28 days | `[LITERATURE: Stupp 2005]` |
| TTF compliance | EF-14 median | 0.75 | `[LITERATURE: EF-14 trial]` |
| $\sigma$ | Spontaneous dormancy rate | 0.005 | `[ASSUMPTION]` (Blath 2023 structure) |
| $\varrho$ | Spontaneous resuscitation rate | 0.02 | `[ASSUMPTION]` (Blath 2023 structure) |
| GSC doubling time | Lan 2017 lower bound | > 24 h → $\lambda_S < 0.03$ | `[LITERATURE: Lan 2017]` |

### 7.2 Parameters That Are Entirely Free

All proliferation rates ($\lambda_S$, $\lambda_P$), natural death rates ($\mu_x$), competition
coefficients ($c_x$), phenotypic switching rates ($s_{SP}$, $s_{PD}$, $\sigma_T$), and
therapy-induced dormancy rates are **free parameters** with no published GBM-specific CTMC
calibration.

> **Scientific honesty note:** No paper in the reference set provides CTMC transition rates
> calibrated to human GBM. All numerical values in `config/default_params.yaml` are
> order-of-magnitude assumptions. Version 1 results are intended as qualitative illustrations
> of mechanistic effects, not quantitative clinical predictions.

---

## 8. Assumptions and Limitations

### 8.1 Structural Assumptions

1. **Well-mixed population.** No spatial structure; all cells compete equally. `[SIMPLIFICATION]`
2. **Exponential waiting times.** All inter-event times are exponentially distributed (CTMC). Real
   cell-cycle time distributions are not exponential (typically log-normal or gamma).
3. **Finite type space.** Only S, P, D, Q states; no continuous trait evolution.
4. **No immune response.** Innate and adaptive immunity are not modeled.
5. **Homogeneous drug exposure.** All cells experience the same drug concentration regardless of
   their location in the tumor.

### 8.2 Biological Simplifications

6. **No de novo resistance mutations.** Resistance is modeled via pre-existing state heterogeneity
   only (Lan 2017 justification). `[DELIBERATE]`
7. **Irreversible hierarchy S → P → D.** In reality, de-differentiation has been reported. `[SIMPLIFICATION]`
8. **Neftel transcriptional states excluded.** The NPC/OPC/AC/MES classification is orthogonal
   and incompatible with the Lan hierarchy at v1 complexity.

### 8.3 Parameter Limitations

9. **No calibrated GBM CTMC parameters exist in the literature.** All transition rates are
   assumptions. Sensitivity analysis is required for any quantitative claim.
10. **MGMT multiplier is an order-of-magnitude estimate.** Exact ratio of TMZ sensitivity between
    methylated and unmethylated MGMT is context-dependent and dose-dependent.

---

## 9. References

| Citation | Used for |
|----------|----------|
| Lan et al. 2017, *Nature*, doi:10.1038/nature23666 | 3-state hierarchy S/P/D; GSC selection by TMZ |
| Blath et al. 2023, *bioRxiv*, doi:10.1101/2023.12.15.571717 | Q state; σ, ϱ, σ_T rates; ODE limit (eq. 2.3); extinction probability |
| Baar et al. 2016, *Sci. Reports* | CTMC framework; K scaling; competition terms; ODE limit |
| Baar et al. 2016 SI | Full infinitesimal generator; clock rate formulas |
| Kraut 2021, *DMV* | Gillespie algorithm; ODE generator formula; hybrid approach |
| Alfonso et al. 2017, *J.R. Soc. Interface* | GBM clinical background; go-or-grow biology |
| Stupp et al. 2005, *NEJM* | Standard-of-care RT + TMZ protocol |
| EF-14 trial (Stupp et al. 2017) | TTF compliance data |

Full summaries of the reference PDFs are in `references/markdown_summaries/`.

---

## 10. Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-14 | Initial draft; 4-state model; 4+1 therapy scenarios |
