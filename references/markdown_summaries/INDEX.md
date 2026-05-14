# Reference Library Index

Markdown summaries of the 10 source PDFs in `05_PORTFOLIO_ASSETS/pdf/`.

Each summary follows a standardized structure: bibliographic info, biological background, therapy relevance, mathematical relevance, parameters, assumptions, use classification, and modeling interpretation. Interpretations are clearly marked `[INTERPRETATION — not a source fact]`.

---

## Priority Classification

### Version 1 — Core References (use directly in model design)

| File | Paper | Key Contribution |
|---|---|---|
| [Lan_2017_nature23666.md](Lan_2017_nature23666.md) | Lan et al. 2017, *Nature* | Experimental justification for the 3-state GSC hierarchy (S → P → D). TMZ selects pre-existing resistant GSCs. |
| [Baar_2016.md](Baar_2016.md) | Baar et al. 2016, *Sci. Reports* | Mathematical framework: stochastic individual-based CTMC with phenotypic switching, therapy, and ODE limit. Template for the model. |
| [Blath_2023.md](Blath_2023.md) | Blath et al. 2023, *bioRxiv* | Full CTMC model with dormancy (active/dormant states), multi-drug therapy, ODE limit, extinction probability. Direct template for the Q state. |
| [Baar_2016_SI.md](Baar_2016_SI.md) | Baar et al. 2016 SI | Full infinitesimal generator, clock rate formulas, formal Markov process. Reference for `transitions.py` implementation. |
| [Kraut_2021.md](Kraut_2021.md) | Kraut 2021, *DMV* | Clearest description of Gillespie algorithm and ODE limit. Reference for `gillespie.py` and `ode.py`. |

### Version 1 — Supporting References (use for documentation and assumptions)

| File | Paper | Key Contribution |
|---|---|---|
| [Alfonso_2017.md](Alfonso_2017.md) | Alfonso et al. 2017, *J.R. Soc. Interface* | Review of glioma invasion biology and mathematical model landscape. Justifies go-or-grow as a real biological phenomenon. Positions CTMC relative to PDE/ABM approaches. |
| [Oliveira_2017_go_or_grow.md](Oliveira_2017_go_or_grow.md) | Oliveira et al. 2017, *Cell Commun. Signal.* | Experimental evidence that go-or-grow switch is microenvironment-regulated in GBM. Justifies environment-dependent switch rates. |

### Future Extensions Only (do not implement in version 1)

| File | Paper | Key Contribution |
|---|---|---|
| [Venkataramani_2022.md](Venkataramani_2022.md) | Venkataramani et al. 2022, *Cell* | Neuronal-like invasive cells vs. connected network cells as two functional states. Tumor microtubes, therapy resistance mechanisms. Future connected/invasive state extension. |
| [Conte_Surulescu_2021.md](Conte_Surulescu_2021.md) | Conte & Surulescu 2021, *Appl. Math. Comput.* | Multiscale PDE model for spatial invasion with go-or-grow and tissue anisotropy. Roadmap for future spatial extension. |
| [Dwivedi_2023_game_theory.md](Dwivedi_2023_game_theory.md) | Dwivedi et al. 2023, *Sci. Reports* | Game-theoretic analysis of go-or-grow. Qualitative constraint on switch rate ratios. Future game-theory comparison. |

---

## Key Findings by Topic

### Cell State Hierarchy
- **3 states (literature-grounded):** Stem-like GSC (S), Progenitor (P), Differentiated/Non-proliferative (D) → Lan et al. 2017
- **4th state:** Quiescent/Dormant (Q) → Blath et al. 2023
- **Direction:** S → P → D (with P self-renewal); Q entered from S or P under therapy/stress

### Therapy Resistance
- TMZ selects pre-existing resistant GSCs — not de novo resistance: Lan et al. 2017
- Dormancy-induced therapy failure even for classically sensitive cells: Blath et al. 2023
- Phenotypic switching as immune escape (melanoma analogy): Baar et al. 2016

### Mathematical Framework
- CTMC / individual-based stochastic model: Baar 2016, Blath 2023, Kraut 2021
- ODE mean-field limit (K → ∞): Baar 2016, Blath 2023, Kraut 2021
- Gillespie SSA: Kraut 2021 (algorithmic description), Baar 2016 (applied)
- Extinction probability = μ/λ (unchanged by dormancy): Blath 2023

### Go-or-Grow
- Biology: Alfonso 2017, Oliveira 2017
- PDE model: Conte & Surulescu 2021
- Game theory: Dwivedi 2023
- Neuronal mechanisms: Venkataramani 2022

---

## Parameter Availability Summary

| Source | Parameters given | Quality |
|---|---|---|
| Lan 2017 | Qualitative only (GSC doubling time > 24h) | Low for CTMC |
| Baar 2016 | Melanoma-fit (K = 10⁵) | Not transferable to GBM |
| Blath 2023 | Abstract/dimensionless only | Not calibrated |
| Kraut 2021 | None (conceptual) | None |
| Alfonso 2017 | None for CTMC | PDE-only |
| Others | None relevant | — |

**Conclusion:** No paper in the reference set provides CTMC transition rates calibrated to human GBM. All rates in the v1 model are free parameters to be justified by order-of-magnitude estimates and clearly labeled as assumptions.

---

## Notation Summary

| Symbol | Used in | Meaning |
|---|---|---|
| K | Baar 2016, Blath 2023 | Carrying capacity (population scaling parameter) |
| λ | Blath 2023 | Active cell division rate |
| μ | Blath 2023 | Active cell natural death rate |
| σ | Blath 2023 | Spontaneous dormancy entry rate |
| σ_T | Blath 2023 | Therapy-induced dormancy entry rate |
| ϱ | Blath 2023 | Spontaneous resuscitation rate |
| ϱ_T | Blath 2023 | Drug-induced resuscitation rate (can be negative) |
| b(p) | Baar 2016 | Birth rate of phenotype p |
| d(p) | Baar 2016 | Death rate of phenotype p |
| s^g(p,p̃) | Baar 2016 | Natural phenotypic switch rate from p to p̃ |
| t(z,p) | Baar 2016 | Therapy kill rate (T-cell z, cancer phenotype p) |
| n_x(t) | Kraut 2021 | Number of individuals of type x at time t |
| L | Kraut 2021 | Generator of the Markov process |
