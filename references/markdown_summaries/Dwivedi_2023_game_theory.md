# Source Summary: s41598-023-43199-3.pdf

## 1. Bibliographic Information

- **Title:** Game-theoretical description of the go-or-grow dichotomy in tumor development for various settings and parameter constellations
- **Authors:** Shalu Dwivedi, Christina Glock, Sebastian Germerodt, Heiko Stark, Stefan Schuster
- **Year:** 2023
- **Journal:** Scientific Reports, 13: 16758
- **DOI:** 10.1038/s41598-023-43199-3

---

## 2. Why This Source Matters

This paper applies evolutionary game theory to the go-or-grow dichotomy in tumors, analyzing when cells "decide" to proliferate (stay) versus invade (go) as a function of nutrient availability and motility costs. It is a theoretical modeling paper that complements the PDE and stochastic approaches. Its relevance to the CTMC project is limited but non-zero: it provides an alternative mathematical perspective on the go-or-grow switch that could justify parameter choices for go-or-grow switch rates, and it frames the go-or-grow decision as a population-level equilibrium outcome rather than a stochastic individual event.

---

## 3. Biological Background

**Go-or-grow dichotomy:**
- Tumors can either grow at the primary site (sessile/proliferative phenotype) or migrate to distant sites (motile phenotype).
- In GBM specifically: highly migratory cells have lower proliferation rate; actively proliferating cells move slowly.
- The go-or-grow decision is modeled here as a strategic choice between competing tumor cells.

**Relevant cancer type mentioned:**
- Hepatocellular carcinoma is used as a representative example.
- GBM is in the background context but not the focus.

**Nash equilibria and population behavior:**
- Depending on game type (determined by nutrient availability `b` and motility cost `c`):
  - **Deadlock game** (c > b): all cells stay (proliferative Nash equilibrium).
  - **Prisoner's Dilemma** (c < b, specific conditions): both go — a collectively suboptimal but individually rational outcome.
  - **Hawk-dove** (intermediate): coexistence of go and grow phenotypes.

**Modified game variants:**
- Five modified versions of the Basanta-Hatzikirou-Deutsch (BHD) model are analyzed.
- Additional parameters: `a` = nutrient accessibility at distant site.
- Result: if nutrient supply at distant site is high, all cells predicted to go.

**Clinical implications discussed:**
- Caloric restriction and methionine limitation as strategies to suppress metastasis by reducing `b` (nutrient benefit).

---

## 4. Therapy Relevance

**Indirect therapy relevance:**
- Caloric restriction and vitamin/methionine limitation are discussed as potential interventions to reduce the benefit parameter `b`, shifting equilibrium toward the "grow" (stay) phenotype.
- Chemotherapy and radiotherapy are not modeled.

**GBM-specific therapy:** Not discussed.

---

## 5. Mathematical / Modeling Relevance

**Game-theoretic framework:**
- Symmetric 2-player, 2-strategy game.
- Payoff matrix for (Proliferative, Motile):
  ```
  Proliferative / Proliferative: (b/2, b/2)   — share nutrients
  Proliferative / Motile:        (b, b-c)      — motile leaves, sessile gains full b
  Motile / Proliferative:        (b-c, b)      — symmetric
  Motile / Motile:               (b-2c, b-2c)  — both leave, split cost
  ```
- Game types (12 possible) depend on parameter ordering: b, c, b/2, b-c, b-2c.
- Nash equilibrium identifies the population-level stable strategy.

**BHD model (Basanta-Hatzikirou-Deutsch):**
- The paper reanalyzes this existing model and extends it.
- Three game types arise from the BHD model: Deadlock (c > b), Hawk-dove (b/2 < c < b), Prisoner's Dilemma (c < b/2).

**Relationship to CTMC:**
- The game-theoretic equilibrium is a deterministic prediction about the long-run fraction of go vs. grow cells.
- In a CTMC, the equivalent is the stationary distribution of the (Migrating, Proliferating) states at equilibrium — determined by the ratio of switch rates P → M and M → P.
- The game theory result says the equilibrium ratio should depend on b (nutrient benefit of migration) and c (cost of migration). This could inform the parameter ratio σ_{P→M} / σ_{M→P} in the CTMC.

---

## 6. Parameters and Quantitative Information

| Parameter | Meaning | Range studied |
|---|---|---|
| b | Nutrient benefit of being alone (without competition) | > 0 |
| c | Cost of motility | > 0 |
| a | Nutrient accessibility at distant site | > 0 (Modification I) |

- Deadlock game: c > b
- Hawk-dove game: b/2 < c < b
- Prisoner's Dilemma: c < b/2

No experimentally measured values are given. The paper is purely theoretical.

---

## 7. Assumptions and Limitations

- The game is symmetric: all tumor cells have the same strategy set. Real GBM has a GSC/progenitor/differentiated hierarchy that breaks this symmetry.
- The model has only two strategies (go/grow) — no quiescence, no stem cell hierarchy.
- Nutrient supply is a scalar parameter — no spatial gradient.
- The stochastic fluctuations mentioned are qualitative — no Gillespie simulation.
- The model does not include therapy.
- The paper focuses on metastasis generally — the GBM context is peripheral.

---

## 8. Possible Use in This Project

- **Use in version 1:** None directly.
- **Use for documentation:** The game-theoretic analysis provides a complementary theoretical justification for including a go-or-grow state transition in the model. The result that equilibrium strategy depends on nutrient availability can be cited as justification for making go-or-grow switch rates environment-dependent (rather than constant).
- **Use for future extension:** If a resource/nutrient variable is added to the CTMC, the game-theory result provides a qualitative guide for how the switch rate ratio should depend on nutrient availability.
- **Background only:** The game type classification details, the five modified BHD variants.

---

## 9. Modeling Interpretation

> **[INTERPRETATION — not a source fact]**
> The game-theoretic analysis suggests that the ratio of go to grow cells at equilibrium is determined by the balance of nutrient benefit and motility cost — not by an arbitrary parameter choice. In the CTMC model, this translates to: the ratio of switch rates P → M (go) to M → P (grow) should be set such that the resulting stationary distribution is biologically meaningful. Concretely, if nutrient conditions are favorable (low stress), most cells should be in the P (proliferating/grow) state; under stress, more cells shift to M (migrating/go). This is a qualitative constraint on parameter choice, not a quantitative one, since no numerical values of b and c are given for GBM.
