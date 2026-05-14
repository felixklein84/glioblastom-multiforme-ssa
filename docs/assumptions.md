# Assumption Register — GBM CTMC v1

This register catalogues every modeling assumption, its justification, and its
sensitivity analysis priority. It supplements the formal model specification.

**Priority levels:**
- `HIGH` — result is likely qualitatively sensitive to this assumption; must vary
- `MEDIUM` — moderate impact expected; vary in secondary analysis
- `LOW` — unlikely to affect qualitative conclusions

---

## A. Biological Architecture

| ID | Assumption | Justification | Priority |
|----|-----------|---------------|----------|
| A1 | 4-state model: S, P, D, Q only | Lan 2017 (3-state) + Blath 2023 (dormancy); Neftel excluded as incompatible | MEDIUM |
| A2 | S → P → D hierarchy is irreversible | Lan 2017 fate mapping; de-differentiation reported but not dominant | MEDIUM |
| A3 | Only P cells enter Q; not S | Blath 2023 models active cells only; S is already slow-cycling; separating dormancy layer from GSC layer | HIGH |
| A4 | D cells do not divide or switch state | Lan 2017: terminally differentiated; standard assumption | LOW |
| A5 | No spatial structure | Well-mixed approximation; valid for population-level therapy comparison | HIGH (for invasion) |
| A6 | No immune response | Excluded for v1; Baar 2016 framework available for v2 | HIGH (for immunotherapy) |
| A7 | No de novo genetic resistance | Lan 2017: TMZ selects pre-existing GSCs; phenotypic model sufficient for v1 | HIGH |

---

## B. Proliferation and Death Rates

| ID | Assumption | Default Value | Basis | Priority |
|----|-----------|---------------|-------|----------|
| B1 | S division rate λ_S | 0.02 day⁻¹ (doubling time ~35 d) | Lan 2017: GSC doubling > 24 h; upper bound 0.03 | HIGH |
| B2 | P division rate λ_P | 0.20 day⁻¹ (doubling time ~3.5 d) | ~10× GSC; consistent with literature on fast-cycling progenitors | HIGH |
| B3 | Natural death rates μ_x | 0.005 / 0.02 / 0.05 / 0.003 (S/P/D/Q) | Order-of-magnitude only | MEDIUM |
| B4 | Competition coefficient c_x | Equal across states | Simplification; in reality GSCs likely more resistant to crowding | MEDIUM |

---

## C. Phenotypic Switching

| ID | Assumption | Default Value | Basis | Priority |
|----|-----------|---------------|-------|----------|
| C1 | S → P commitment rate s_SP | 0.01 day⁻¹ | Uncalibrated; must reproduce slow GSC fraction | HIGH |
| C2 | P → D differentiation rate s_PD | 0.05 day⁻¹ | Uncalibrated; must reproduce D cell majority | HIGH |
| C3 | Spontaneous dormancy σ (P → Q) | 0.005 day⁻¹ | Blath 2023 rate structure; magnitude is free | HIGH |
| C4 | Spontaneous resuscitation ϱ (Q → P) | 0.02 day⁻¹ | Blath 2023 rate structure; magnitude is free | HIGH |

---

## D. Radiotherapy Kill

| ID | Assumption | Default Value | Basis | Priority |
|----|-----------|---------------|-------|----------|
| D1 | Per-fraction kill probability κ_S^RT | 0.03 | GSC radio-resistance; consistent with radio-biology literature | HIGH |
| D2 | Per-fraction kill probability κ_P^RT | 0.20 | Cycling cells most sensitive; 4 Rs of radiobiology | HIGH |
| D3 | Per-fraction kill probability κ_D^RT | 0.10 | Intermediate; post-mitotic | MEDIUM |
| D4 | Per-fraction kill probability κ_Q^RT | 0.01 | Deeply quiescent; cell-cycle arrested | HIGH |
| D5 | RT-induced dormancy rate σ_T^RT | 0.10 (per fraction) | Blath 2023 σ_T structure; magnitude is assumption | HIGH |
| D6 | Fractions modeled as daily events (incl. weekends) | — | Simplification; real Stupp is 5×/week over 6 weeks | LOW |

---

## E. Temozolomide Kill

| ID | Assumption | Default Value | Basis | Priority |
|----|-----------|---------------|-------|----------|
| E1 | TMZ kill rate δ_S^TMZ | 0.03 day⁻¹ | Lan 2017: pre-existing GSC resistance; low rate | HIGH |
| E2 | TMZ kill rate δ_P^TMZ | 0.20 day⁻¹ | Cycling cells sensitive to alkylation | HIGH |
| E3 | TMZ kill rate δ_D^TMZ | 0.05 day⁻¹ | Post-mitotic; lower sensitivity | MEDIUM |
| E4 | TMZ kill rate δ_Q^TMZ | 0.01 day⁻¹ | Non-replicating; alkylation not lethal without replication | HIGH |
| E5 | TMZ-induced dormancy rate σ_T^TMZ | 0.10 day⁻¹ (active days) | Blath 2023 structure; magnitude is assumption | HIGH |
| E6 | MGMT methylation kill multiplier | 2.0× | Order of magnitude only; sensitivity parameter | MEDIUM |

---

## F. Tumor Treating Fields

| ID | Assumption | Default Value | Basis | Priority |
|----|-----------|---------------|-------|----------|
| F1 | TTF kill rate δ_P^TTF | 0.08 day⁻¹ | Cycling cells in metaphase disrupted | HIGH |
| F2 | TTF kill rate δ_S^TTF / δ_Q^TTF | 0.005 / 0.002 day⁻¹ | Non-cycling; TTF negligible | MEDIUM |
| F3 | Compliance c_comp | 0.75 | EF-14 trial median | LOW |
| F4 | TTF effect modeled as continuous kill rate | — | Alternating fields are continuous; kill effect is time-averaged | LOW |

---

## G. Simulation Parameters

| ID | Assumption | Default Value | Priority |
|----|-----------|---------------|----------|
| G1 | Carrying capacity K | 1000 | Controls stochastic/deterministic crossover; must vary | HIGH |
| G2 | Initial conditions | (n_S=5, n_P=50, n_D=100, n_Q=2) | Representative small tumor; free parameter | MEDIUM |
| G3 | Gillespie vs. ODE agreement threshold | — | Both implemented; agreement validates implementation | N/A |
