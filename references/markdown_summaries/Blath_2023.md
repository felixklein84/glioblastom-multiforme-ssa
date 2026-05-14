# Source Summary: 2023.12.15.571717v1.full.pdf

## 1. Bibliographic Information

- **Title:** A Stochastic Population Model for the Impact of Cancer Cell Dormancy on Therapy Success — Working Paper
- **Authors:** Jochen Blath, Anna Kraut, Tobias Paul, András Tóbiás
- **Year:** 2023 (preprint, December 15, 2023)
- **Journal/Source:** bioRxiv preprint, doi: 10.1101/2023.12.15.571717
- **Status:** Working paper, not peer-reviewed at time of writing

---

## 2. Why This Source Matters

This is the most directly relevant mathematical paper for the new project. It builds a minimal stochastic CTMC model with two cancer cell states (active and dormant), drug agents, and multiple therapy protocols — precisely the structure needed for the GBM dormancy extension. The paper formalizes the distinction between spontaneous dormancy, therapy-induced dormancy, and drug-induced resuscitation as separate mechanisms with different modeling implications. It proves the many-particle ODE limit, provides explicit transition rates, and gives simulation results showing that even a small dormant subpopulation can cause therapy failure under single-drug treatment. The formal model in equations (2.1)–(2.3) can be adapted directly.

---

## 3. Biological Background

**Cancer cell dormancy:**
- Dormancy = a phenotypic switch into a non-proliferating, protected, therapy-evading cellular state.
- Can be triggered by: chemo-, immuno-, or radiation therapy stress; spontaneous/stochastic events; competition/overcrowding; environmental cues.
- Short-term dormancy (cell-cycle arrest, quiescence): modeled here.
- Long-term dormancy ("metastatic latency," years-long): explicitly excluded from this paper.

**Nomenclature clarification from the paper:**
- The authors note that "quiescence," "persistence," "latency," "tolerance," and "stemness" are all used inconsistently across the literature to describe dormancy-related phenomena.
- This paper uses "dormancy" as an umbrella term for individual cell-level non-proliferating states.

**Therapy resistance via dormancy:**
- Even a small initial population of dormant cells can cause therapy failure under classical single-drug treatment.
- Dormancy mechanisms: spontaneous switching, therapy-induced switching, competition-induced switching.
- Re-activation: spontaneous resuscitation, drug-induced resuscitation, drug-suppressed resuscitation.

**Mutation and resistance:**
- The paper includes optional resistance mutations in dormant cells.
- Mutation rate in dormant state may be lower or higher than in active state (paper notes this is unclear in the literature).

---

## 4. Therapy Relevance

**Drug model:**
- Two drugs modeled: Drug A targets active cells; Drug B targets dormant cells.
- Each drug is represented as a population of agents (particles) that decay over time and interact with cancer cells.

**Treatment protocols modeled:**
- Instantaneous drug administration: periodic injections (pulsed), with exponential decay between doses.
- Continuous drug administration: infusion modeled as an immigration process for drug agents.
- Multiple drug combinations explored systematically.

**Key findings for therapy design:**
- Single-drug treatment (targeting only active cells): fails whenever dormant population survives treatment and resuscitates.
- Adding a drug that targets dormant cells or suppresses resuscitation is critical for therapy success.
- Optimal protocol depends on the specific dormancy mechanism present: spontaneous vs. responsive switching leads to different optimal strategies.
- Reducing mutation probability is a relevant second optimization criterion alongside tumor remission.

**Radiotherapy / TMZ / GBM:** Not mentioned. Framework is generic chemotherapy. The transfer to GBM requires explicit modeling assumptions.

---

## 5. Mathematical / Modeling Relevance

**State space (equation 2.1):**
```
N(t) = (Ca(t), Cd(t), Da(t), Dd(t))
```
- `Ca(t)`: number of active cancer cells
- `Cd(t)`: number of dormant cancer cells
- `Da(t)`: number of agents of drug targeting active cells
- `Dd(t)`: number of agents of drug targeting dormant cells

This is a CTMC on ℕ₀⁴.

**Transition rates for active cells:**
- Division: rate `λ > 0`
- Natural death: rate `μ` (with `0 < μ < λ`)
- Drug-induced death: rate `μ_a^T · Da/K`
- Competition death: rate `α · Ca/K`
- Spontaneous dormancy entry: rate `σ > 0`
- Therapy-induced dormancy entry: rate `σ_T · Da/K`

**Transition rates for dormant cells:**
- Spontaneous resuscitation: rate `ϱ > 0`
- Drug-induced resuscitation: rate `ϱ_T · Dd/K` (can be positive or negative)
- Drug-induced death: rate `μ_d^T · Dd/K`

**Drug dynamics:**
- Active drug: degrades at rate `β_a`
- Dormant drug: degrades at rate `β_d`
- Pulsed dosing: instantaneous jump at periodic intervals ω

**Many-particle ODE limit (equation 2.3):**
```
ċ_a = c_a(λ - μ - μ_a^T·d_a - α·c_a - σ - σ_T·d_a) + c_d(ϱ + ϱ_T·d_d)₊
ċ_d = c_a(σ + σ_T·d_a) - c_d·μ_d^T·d_d + (ϱ + ϱ_T·d_d)₊
ḋ_a = -β_a·d_a
ḋ_d = -β_d·d_d
```

This system is a logistic growth model with an additional dormancy compartment. It is the exact mean-field limit of the stochastic model.

**Gillespie algorithm:**
- Standard SSA used for simulations throughout.
- Hybrid stochastic-deterministic algorithm mentioned as an option for large populations.

**Analytical results:**
- Extinction probability in early phase (small tumor) computed analytically using branching process approximation.
- Growth rate (dominant eigenvalue) computed from linearization.

---

## 6. Parameters and Quantitative Information

The paper uses **abstract / dimensionless parameters** for illustration. No GBM-specific values are given.

| Parameter | Symbol | Role |
|---|---|---|
| Cell division rate | λ | Active cell proliferation |
| Natural death rate | μ | `0 < μ < λ` for net growth |
| Drug kill rate (active) | μ_a^T | Therapy effectiveness |
| Competition rate | α | Carrying capacity effect |
| Spontaneous dormancy rate | σ | Dormancy initiation |
| Therapy-induced dormancy | σ_T | Responsive switching |
| Spontaneous resuscitation | ϱ | Dormancy exit |
| Drug-induced resuscitation | ϱ_T | Positive or negative |
| Drug kill rate (dormant) | μ_d^T | Targeted dormant therapy |
| Drug decay rate (active) | β_a | Pharmacokinetics |
| Drug decay rate (dormant) | β_d | Pharmacokinetics |
| Carrying capacity | K | Population scaling |
| Dosing interval | ω | Pulse period |

**No explicit numerical values are calibrated to biological data.** The authors explicitly state the model is a "toy model" for illustrating mechanistic principles.

---

## 7. Assumptions and Limitations

- The model is generic cancer / generic chemotherapy — not calibrated to GBM or TMZ.
- Only individual cell dormancy (not tumor mass dormancy) is modeled.
- Only short-term dormancy (cell-cycle arrest timescale) is modeled; metastatic latency is excluded.
- No spatial structure.
- No immune system.
- No genetic heterogeneity (except optional resistance mutations treated separately).
- Drug pharmacokinetics are modeled as exponential decay — a simplified approximation.
- The paper is a **working paper** (bioRxiv preprint) and has not been peer-reviewed. Mathematical results should be treated as preliminary.
- Parameters are entirely abstract; biological transfer requires external justification.

---

## 8. Possible Use in This Project

- **Use in version 1:** The state space `(C_a, C_d)` is the minimal dormancy extension of the thesis model. The transition rates σ (spontaneous dormancy), σ_T (therapy-induced), ϱ (resuscitation) map directly to Q → (Q → P) transitions in the proposed 4-state model. The ODE limit (eq. 2.3) is the template for the deterministic approximation module. The pulsed dosing model is the template for therapy scheduling.
- **Use for documentation:** The classification of dormancy mechanisms (spontaneous, responsive, competition-induced) provides precise language for the assumptions section. The "general observations" (GOs) stated in the paper are useful as biological hypotheses to test.
- **Use for future extension:** Multiple drugs targeting both active and dormant cells, optimization of combination protocols, resistance mutation accumulation.
- **Background only:** The abstract mathematical proofs (Section 2.1 convergence theorem) and the long-term dormancy discussion.

**Analytical result — extinction probability (Section 2.4):**

For the model without competitive effects (early tumor, small population — branching process approximation):

- Probability of extinction starting from **1 active cell**: `q̄_a = μ/λ`
- Probability of extinction starting from **1 dormant cell**: `q̄_d = μ/λ`
- Both are equal to the extinction probability without dormancy.

**Key insight:** Spontaneous dormancy does NOT change the probability of tumor extinction. It only potentially delays extinction. The principal eigenvalue (exponential growth rate) is determined by the offspring mean matrix; dormancy reduces but does not eliminate the growth rate.

This is a mathematically proven result, not a simulation finding.

---

## 9. Modeling Interpretation

> **[INTERPRETATION — not a source fact]**
> This paper directly motivates adding a Quiescent/Dormant state Q to the GBM model. The transitions P → Q (therapy-induced dormancy) and Q → P (resuscitation) with distinct rates correspond exactly to σ_T and ϱ from the paper. The key modeling insight from this paper: **a drug that targets only active cells will systematically fail if the dormant subpopulation can resuscitate after treatment ends** — this is the biological rationale for why the Q state is not just decorative but changes qualitative model behavior. In the GBM context, this corresponds to TMZ killing cycling progenitors while GSCs and quiescent cells survive. The ODE limit (equation 2.3) is directly implementable as the `ode.py` module.
