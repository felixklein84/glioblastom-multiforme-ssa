# Source Summary: Kraut_2021.pdf

## 1. Bibliographic Information

- **Title:** Mathematische Modelle in der Immuntherapie von Tumoren (Mathematical Models in Tumor Immunotherapy)
- **Author:** Anna Kraut
- **Year:** 2021
- **Journal/Source:** Mitteilungen der Deutschen Mathematiker-Vereinigung (DMV), vol. 29, issue 1, pp. 10–13
- **DOI:** mentioned as "DOI ./dmvm--" (incomplete in document)
- **Language:** German

---

## 2. Why This Source Matters

This is a short accessible article by Anna Kraut (one of the authors of the Blath 2023 dormancy paper) presenting the Bovier group's research program on stochastic individual-based models for tumor immunotherapy. It explains the mathematical framework (individual-based Markov process, Gillespie algorithm, deterministic ODE limit) in a compact, precise way that is directly relevant to the new project's implementation approach. It also explicitly describes the stochastic-deterministic hybrid algorithm used in their simulations. While the biological application is melanoma immunotherapy (same as Baar 2016), the mathematical explanation is the clearest short description of the simulation methodology in the entire reference set.

---

## 3. Biological Background

**Melanoma immunotherapy (ACT therapy):**
- Tumor cells appear in two forms: normal (Tum₁, antigen-positive) and "hidden" (Tum₂, antigen-negative).
- ACT therapy: antigen-specific immune cells (Imm) are injected to recognize and kill Tum₁ cells.
- At the same time, active immune cells release cytokines (Bot = Botenstoffe = messenger molecules) that cause Tum₁ cells to change form into Tum₂ (antigen-negative) → therapy fails.
- Goal of research: understand tumor dynamics, test therapy combinations (e.g., with chemotherapy), investigate tumor survival strategies.

**Cell types in the model:**
- Tum₁: normal (differentiated) tumor cells
- Tum₂: "hidden" (dedifferentiated) tumor cells
- Imm: immune cells
- Bot: cytokines / messenger molecules

---

## 4. Therapy Relevance

**Immunotherapy (ACT):**
- Modeled as T-cell injection → immune cell population Imm added to system.
- T-cells kill Tum₁ cells at rate proportional to immune cell population.

**Combination with chemotherapy:** Mentioned as a research goal but not detailed in this article.

**Stochastic therapy failure:**
- Key result: the stochastic model can predict therapy failure even when the deterministic ODE predicts remission. This happens when immune cells or tumor cells stochastically die out before the deterministic equilibrium is reached.
- In particular: whether the tumor is cured or relapses depends on which cell type (tumor or immune) goes extinct first — a purely stochastic event that cannot be captured by ODEs.

---

## 5. Mathematical / Modeling Relevance

**Individual-based Markov process:**
- State of the process: population vector n(t) ∈ ℕ^X, where n_x(t) = number of individuals of type x ∈ X at time t.
- Events occur at random exponential times; each event changes the population vector.
- Example: birth of type x at rate b_x → state changes from n(t) to n(t) + δ_x.
- Generator:
  ```
  Lφ(n) = Σ_{e∈E} (φ(n + v_e) - φ(n)) r_e(n)
  ```
  where v_e is the state change and r_e(n) is the total rate of event e.

**Gillespie algorithm (explicitly described):**
- In each step: simulate the random waiting time until the next event, then decide which event occurs.
- Key property used: the minimum of independent exponential random variables is itself exponential with rate = sum of all individual rates.
- This means: only ONE random time needs to be generated per step (not one per possible event).
- The probability that event e is the one that fires is proportional to its rate r_e(n).
- Advantage: exact simulation, no time-discretization error.
- Disadvantage: for large populations, many events occur per unit time → very many simulation steps → slow.

**ODE (deterministic) limit:**
- From Ethier-Kurtz (1986): the rescaled stochastic process converges to the solution of an ODE system as population size → ∞:
  ```
  d/dt n_x(t) = Σ_{e∈E} (v_e)_x r_e(n(t))
  ```
- This is the law of large numbers for individual-based Markov processes.
- The ODE can be used to approximate the stochastic system in large-population regimes, using standard Runge-Kutta solvers.

**Hybrid stochastic-deterministic algorithm:**
- Neither the pure stochastic (Gillespie) nor the pure deterministic (ODE) approach is always appropriate.
- Hybrid: use Gillespie for small populations (where stochastic effects matter), switch to ODE for large populations (where stochastic effects average out).
- Collaboration with the Mayer group at Bonn (implied by "in einer Art Zusammenarbeit").
- The hybrid approach is also discussed in the context of the Baar 2016 paper simulations.

**Why stochastic vs. deterministic matters (key insight, explicitly stated):**
- "Even when the cell division rate exceeds the death rate [so the deterministic system shows positive net growth], it can happen that cells randomly die before they can divide, and the tumor goes extinct." — This stochastic extinction effect is invisible in the ODE.
- Near the final stages of therapy (few tumor and immune cells remaining): which cell type goes extinct first is purely stochastic and determines cure vs. relapse.

---

## 6. Parameters and Quantitative Information

- Individual rates in the interaction diagram are shown symbolically (b_{Tum₁}, b_{Tum₂}, s_{Tum₁,Tum₂}, b_{Imm}·n_{Tum₁}, etc.).
- No numerical values given — article is purely conceptual.

---

## 7. Assumptions and Limitations

- Well-mixed population (no spatial structure).
- Finite-type individual-based model — the trait space is discrete.
- Exponential waiting times for all events — this is the core CTMC assumption.
- The hybrid algorithm requires a user-defined threshold for switching between stochastic and deterministic modes — this threshold is a modeling decision without an obvious automatic rule.
- Mutation is mentioned but not quantified; the article focuses on phenotypic switching.

---

## 8. Possible Use in This Project

- **Use in version 1:** The Gillespie algorithm description (section "Stochastisch vs. deterministisch") is the clearest algorithmic specification in the reference set and should be used as the direct reference for implementing `gillespie.py`. The ODE limit formula is the reference for `ode.py`. The generator formula is the reference for `transitions.py`.
- **Use for documentation:** The article provides the best single-paragraph justification for why a stochastic model is necessary (in German — can be translated/paraphrased in the project README or model specification).
- **Use for future extension:** The hybrid stochastic-deterministic algorithm is the target for a performance optimization in later stages.
- **Background only:** The specific melanoma immunotherapy application.

---

## 9. Modeling Interpretation

> **[INTERPRETATION — not a source fact]**
> This article provides the clearest algorithmic description of the Gillespie simulation approach in the entire reference set. The key implementation insight: generate one exponential random time with rate = sum of all event rates, then select which event fires with probability proportional to its individual rate. This is the standard SSA (Stochastic Simulation Algorithm) and maps directly to a clean Python implementation. The article also provides the justification for maintaining both a stochastic and a deterministic module in the project: large populations are well-approximated by ODEs (faster, smoother), but small populations (near therapy-induced remission) require stochastic simulation to capture extinction probabilities correctly.
