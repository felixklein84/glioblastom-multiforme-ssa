# Source Summary: Baar_SI.pdf

## 1. Bibliographic Information

- **Title:** Supplementary Information — A stochastic model for immunotherapy of cancer
- **Authors:** Martina Baar, Loren Coquille, Hannah Mayer, Michael Hölzel, Meri Rogava, Thomas Tüting & Anton Bovier
- **Year:** 2016
- **Journal:** Scientific Reports (supplement to main paper srep24169)
- **DOI:** See main paper: 10.1038/srep24169

---

## 2. Why This Source Matters

This supplementary document provides the complete formal mathematical specification of the Baar et al. stochastic model, including the full infinitesimal generator of the Markov process, explicit clock rates for all events, and the measure-valued process formalism. It is the primary reference for correctly implementing the Baar et al. CTMC framework. If the new project's code is to be mathematically rigorous, the generator formulation here — not the informal description in the main paper — is the authoritative source. The SI also gives parameter values used in the quantitative comparison to experimental data.

---

## 3. Biological Background

Identical to main paper (Baar_2016.md). No additional biological content in the SI.

---

## 4. Therapy Relevance

The SI provides parameter values calibrated to the Landsberg et al. melanoma immunotherapy experiment. See Baar_2016.md for therapy context. No additional therapy content beyond the main paper.

---

## 5. Mathematical / Modeling Relevance

**Full measure-valued Markov process:**

The state space is the set of finite rescaled point measures on X:
```
M_K(X) = {(1/K) Σ δ_{x_i} : n ∈ ℕ, x_1,...,x_n ∈ X}
```

**Infinitesimal generator L^K:**

For bounded measurable φ: M_K → ℝ, the generator acts on η ∈ M_K by:

For each cancer cell of type (g, p):
- **Clonal birth** at rate `(1-μ_g)[b(p) - Σ c_b(p,p̃)η(p̃)]_+`:
  cell count increases by 1 at (g,p).
- **Mutant birth** at rate `μ_g[b(p) - Σ c_b(p,p̃)η(p̃)]_+`:
  a new cell of type (g̃,p̃) appears according to mutation kernel m.
- **Natural mortality** at rate `d(p) + Σ c(p̃,p)η(p̃) + [b(p) - Σ c_b(p,p̃)η(p̃)]_-`:
  cell disappears (note: birth-reducing competition acts as additional death when net birth would be negative).
- **Therapy mortality** at rate `Σ_z t(z,p)η(z)`:
  cell disappears; `ℓ^kill_w(z,p)` cytokines of type w are produced.
- **Phenotypic switch** at rate `Σ_{p̃} (s^g(p,p̃) + Σ_w s^g_w(p,p̃)η(w))`:
  cell transitions from phenotype p to p̃.

For each T-cell of type z:
- Natural birth rate: `b(z)`
- Natural death rate: `d(z)`
- Reproduction rate: `Σ_p b(z,p)η(p)` (produces T-cell + ℓ^prod_w cytokines)

For each cytokine of type w:
- Death rate: `d(w)`

**Key structural points for implementation:**
1. All rates are linear or bilinear in η (current population measure) — standard CTMC structure.
2. Birth-reducing competition: the term `[b(p) - Σ c_b(p,p̃)η(p̃)]_-` acts as additional natural death — be careful to implement this correctly (positive part of net birth, negative part as additional death).
3. Therapy kills cells and simultaneously produces cytokines — this coupling must be modeled jointly, not sequentially.
4. The mutation kernel m is normalized: `Σ_{g̃,p̃} m((g,p),(g̃,p̃)) = 1`.

**ODE limit:**
For completeness, the SI derives the deterministic limit more carefully than the main paper, showing convergence in the sense of Ethier-Kurtz.

---

## 6. Parameters and Quantitative Information

The SI gives parameters for the quantitative comparison to Landsberg et al. experimental data. These are melanoma-specific and must not be transferred to GBM without justification.

| Parameter | Description | Note |
|---|---|---|
| K | Carrying capacity | = 10⁵ in quantitative simulation |
| b(x), b(y) | Birth rates of differentiated and dedifferentiated melanoma | Fit to mouse experiment |
| d(x), d(y) | Death rates | Fit to mouse experiment |
| c(p,p̃) | Competition kernels | Fit to mouse experiment |
| t(z,p) | Therapy kill rates | Fit to mouse experiment |
| s(p,p̃) | Natural switch rates | Fit to mouse experiment |
| s_w(p,p̃) | Cytokine-induced switch rates | Fit to mouse experiment |

All values are melanoma/mouse-specific. **Do not reuse numerically.**

---

## 7. Assumptions and Limitations

Same as main paper. Additionally:
- The measure-valued process formalism assumes a well-mixed population (no spatial structure).
- The `b·c⁻¹` competition term requires that all competing cells interact equally — a mean-field assumption.
- The positive-part operator `[·]_+` on birth rates prevents negative birth rates but creates a non-smooth rate function that requires careful numerical handling near zero population.

---

## 8. Possible Use in This Project

- **Use in version 1:** The generator formulation is the reference for implementing `transitions.py` (Q-matrix construction). The clock rate formulas directly give the CTMC transition rates. The positive-part handling of birth-reducing competition is an implementation detail to note.
- **Use for documentation:** The formal measure-valued process description provides the mathematical notation for the model specification document.
- **Background only:** The specific parameter values (all melanoma-specific).

---

## 9. Modeling Interpretation

> **[INTERPRETATION — not a source fact]**
> The SI clarifies one subtle but important implementation detail: the birth-reducing competition `c_b(p,p̃)` is subtracted from the birth rate, not added to the death rate. When the net birth rate becomes negative, the negative part acts as an additional death rate. In a simple CTMC implementation without this feature, competition would only enter via an increased death rate — which is mathematically different. Whether to include birth-reducing competition in the GBM model is a design choice. For a first version, omitting it and using only competition-increased death (standard logistic) is simpler and justifiable as a simplification.
