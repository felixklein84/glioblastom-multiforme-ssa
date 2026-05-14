# Source Summary: 1-s2.0-S0096300321003945-main.pdf

## 1. Bibliographic Information

- **Title:** Mathematical modeling of glioma invasion: acid- and vasculature mediated go-or-grow dichotomy and the influence of tissue anisotropy
- **Authors:** Martina Conte, Christina Surulescu
- **Year:** 2021
- **Journal:** Applied Mathematics and Computation, 407, 126305
- **DOI:** 10.1016/j.amc.2021.126305

---

## 2. Why This Source Matters

This paper represents the current state of the art in multiscale PDE-based glioma invasion modeling. It deduces a macroscopic reaction-advection-diffusion system from subcellular kinetic transport equations, incorporating the go-or-grow dichotomy, hypoxia, tissue acidity, and vascularization dynamics. It is the most mathematically sophisticated paper in the reference set. Its relevance to the CTMC project is indirect: it defines the spatial modeling horizon toward which the non-spatial CTMC model could eventually be extended, and its treatment of the go-or-grow phenotypic switch at the subcellular level provides context for how switch rates might be derived from first principles.

---

## 3. Biological Background

**Go-or-grow dichotomy:**
- Two mutually exclusive tumor subpopulations: **migrating** and **proliferating** glioma cells.
- States are transient and reversible; the tumor can change composition in response to environmental signals.
- Phenotypic switch regulated by: acidity (pH), hypoxia (oxygen supply), available space, vasculature.

**Hypoxia:**
- Inconsistent intratumor oxygenation causes highly hypoxic sites, acidosis, and tissue necrosis.
- Hypoxia is responsible for inducing acidosis through shift in cellular metabolism (Warburg effect).
- Cancer cells exhibit enhanced glycolysis → high acid load → acidic extracellular pH → boosts invasion, impairs proliferation.
- Pseudopalisade patterns: garland-like necrotic zones with stacks of actively migrating cells — a GBM hallmark.

**Vascularization / angiogenesis:**
- Pro-angiogenic factors attract endothelial cells → blood vessel formation.
- Tumor cells in unfavorable environments deter proliferation for migration toward more favorable areas.

**Brain tissue anisotropy:**
- Glioma cells preferentially invade along white matter tracts.
- The model incorporates tissue fiber orientation as a directional bias (haptotaxis along fibers, repellent pH-taxis).

---

## 4. Therapy Relevance

**Minimal therapy content.** The paper focuses on untreated invasion dynamics.
- One reference is made to an earlier model where chemotherapy dose modulates phenotypic switch rates (migrating ↔ proliferating) — this is not implemented here.
- No specific therapy protocol is modeled.

**Indirect therapy relevance:**
- A spatial invasion model is the prerequisite for modeling how therapy affects not just the tumor core but also the invasive front.
- The phenotypic switch (migrating ↔ proliferating) is the mechanism by which therapy can paradoxically increase invasion (killing proliferating cells may shift the balance toward migrating cells).

---

## 5. Mathematical / Modeling Relevance

**Modeling levels (multiscale):**

**Subcellular (microscopic):**
- ODE system for receptor occupancy dynamics:
  - `y₁(t)`: receptors bound to tissue fibers
  - `y₂(t)`: transmembrane entities occupied by protons
  - Binding/occupying follows mass action kinetics with attachment rate k⁺ and detachment rate k⁻.
  - Steady state: `y* = f̄(Q, S)` (function of tissue density Q and proton concentration S).

**Mesoscopic (kinetic transport):**
- Densities `p(t, x, v, y)` and `r(t, x, y)` of migrating and proliferating glioma cells.
- Kinetic transport equations describe cell movement with velocity v, modulated by the activity variable y (receptor occupancy).

**Macroscopic (PDE):**
After parabolic limit (upscaling from KTEs):
- System of reaction-advection-diffusion PDEs for: total tumor burden, endothelial cells, proton concentration.
- Nonlinear myopic diffusion, haptotaxis along fiber gradients, repellent pH-taxis.
- Phenotypic switch rates between migrating and proliferating populations depend on y (= f̄(Q,S)) — environment-dependent.

**Go-or-grow switch rates:**
- Transition rates between migrating (M) and proliferating (P) states are functions of the receptor occupancy y*, which encodes local tissue density and acidity:
  - High acidity / low tissue → higher M, lower P.
  - Low acidity / high tissue → higher P, lower M.
- This provides a mechanistic derivation of environment-dependent switch rates.

**CTMC / Gillespie relevance:**
- Not used in this paper.
- However, the subcellular ODE for y* is the microscale justification for the state-dependent switch rates in the CTMC. In a non-spatial CTMC, the switch rates would be parameters (not derived from this subcellular model), but the derivation here shows where those parameters come from in principle.

---

## 6. Parameters and Quantitative Information

From the Appendix (nondimensionalization and parameter assessment):

| Parameter | Role | Range / typical values |
|---|---|---|
| k⁺₁, k⁻₁ | Attachment/detachment to tissue | Assumed fast (quasi-steady state) |
| k⁺₂, k⁻₂ | Binding to proton receptors | Assumed fast (quasi-steady state) |
| Diffusion coefficient (migrating) | Cell motility | Order 10⁻² – 10⁻¹ mm²/day (estimated) |
| Proliferation rate | P cells | Order 0.1–0.5 per day (estimated) |
| Switch rate M → P | Phenotypic transition | Function of tissue density and acidity |
| Switch rate P → M | Phenotypic transition | Function of tissue density and acidity |

**Note:** All parameter values in this paper are estimated for dimensionless simulations, not fit to specific patient data. Spatial parameters (diffusion, advection) are not applicable to a non-spatial CTMC.

---

## 7. Assumptions and Limitations

- The model is purely spatial (PDE) and has no meaning in a non-spatial context.
- The subcellular ODE (receptor binding) equilibrates rapidly — this quasi-steady state assumption may not hold under fast environmental changes.
- The model does not include cell proliferation hierarchy (GSC/progenitor/differentiated) — tumor is treated as a homogeneous migrating/proliferating binary.
- No therapy, immune cells, or genetic heterogeneity.
- Tissue anisotropy data (white matter fiber orientation) from diffusion tensor MRI would be required for patient-specific simulations — not available in this project.
- The paper solves the PDE system numerically but does not compare to clinical outcome data.

---

## 8. Possible Use in This Project

- **Use in version 1:** None. The paper is not applicable to a non-spatial CTMC.
- **Use for documentation:** The subcellular derivation of go-or-grow switch rates provides mathematical justification for why these rates depend on the microenvironment. Cite in the model specification when describing what the go-or-grow extension would require.
- **Use for future extension:** The PDE system here is the starting point for a spatial extension of the project. The phenotypic switch mechanism (receptor-occupancy dependent, derived from subcellular dynamics) is the mechanistic basis for future spatially explicit switch rates.
- **Background only:** The multiscale derivation, kinetic transport equations, tissue anisotropy model.

---

## 9. Modeling Interpretation

> **[INTERPRETATION — not a source fact]**
> This paper shows that the go-or-grow switch rates between proliferating (P) and migrating (M) states can be derived from first principles at the subcellular level — they are not arbitrary parameters but emerge from receptor binding dynamics coupled to local tissue density and acidity. In the CTMC v1, these rates are treated as free parameters to be varied in sensitivity analysis. In a future spatial extension, they would be replaced by spatially varying functions f̄(Q(x), S(x)) derived from tissue imaging data. This paper is therefore the long-term mathematical roadmap, not an immediate modeling input.
