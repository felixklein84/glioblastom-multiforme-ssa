# Source Summary: Alfonso_2017.pdf

## 1. Bibliographic Information

- **Title:** The biology and mathematical modelling of glioma invasion: a review
- **Authors:** J. C. L. Alfonso, K. Talkenberger, M. Seifert, B. Klink, A. Hawkins-Daarud, K. R. Swanson, H. Hatzikirou & A. Deutsch
- **Year:** 2017
- **Journal:** Journal of the Royal Society Interface, 14: 20170490
- **DOI:** 10.1098/rsif.2017.0490

---

## 2. Why This Source Matters

This is the principal review paper on glioma invasion biology and its mathematical models. It covers the biological mechanisms underlying glioma heterogeneity, the go-or-grow dichotomy, cell phenotypic plasticity, and the landscape of mathematical modeling approaches from PDEs to agent-based and stochastic models. It provides both the biological vocabulary needed to frame the model and a survey of what modeling approaches already exist, allowing the new project to position itself appropriately. While the paper focuses on invasion (spatial), the biological sections on phenotypic plasticity, metabolic switching, and cell-state dynamics are directly relevant to a non-spatial CTMC model.

---

## 3. Biological Background

**Glioma classification:**
- WHO grade IV glioblastoma (IDH wild-type) is the most common (≈45% of all gliomas) and most aggressive primary brain tumor.
- 5-year survival for IDH wild-type GBM: approximately 5% from diagnosis.
- Low-grade gliomas (WHO grade II) eventually progress to high-grade.

**GBM hallmarks:**
- Fast, infiltrative spread.
- High proliferation.
- Phenotypic heterogeneity (multiple coexisting functional cell types).
- Widespread brain tissue infiltration makes complete surgical resection nearly impossible.

**Phenotypic plasticity and migration-proliferation dichotomy (key biological concept):**
- Migratory and proliferative behaviors of glioma cells are **mutually exclusive** and inversely correlated.
- Highly migratory cells: lower proliferation rate.
- Actively proliferating cells: move slowly.
- This either-or behavior is called the **go-or-grow mechanism** or **migration-proliferation dichotomy**.
- Supported by both in vitro and in vivo experiments.
- The go-or-grow switch is linked to metabolic stress: a glioma-expressed microRNA regulates the balance between migration and proliferation; carboxypeptidase E (CPE) has anti-migratory, pro-proliferative roles under oxygen/nutrient stress.

**Hypoxia and metabolic plasticity:**
- Glioma cells shift metabolism from oxidative phosphorylation to glycolysis (Warburg effect) — an aerobic glycolysis even in oxygen presence.
- Hypoxia triggers phenotypic switching between migrating and proliferating states.
- Highly hypoxic sites → acidosis → invasion potential increases; proliferation impaired at low pH.
- Pseudopalisade patterns (garland-like necrotic zones surrounded by migrating cells) are a GBM hallmark linked to hypoxia and the go-or-grow switch.

**Cell invasion mechanism:**
- Four steps: (1) detachment from tumor mass, (2) adhesion to ECM, (3) ECM degradation, (4) active migration.
- Glioma cells use integrin-mediated adhesion and MMP-mediated ECM degradation.
- Invasion is along white matter tracts and blood vessel walls.

**Genetic and phenotypic variability:**
- Gliomas are clinically, histologically, and genetically very heterogeneous.
- IDH wild-type GBM: usually no IDH mutations; characterized by EGFR amplification, PTEN deletion, etc.
- Genetic variability creates subpopulations with different invasion/proliferation/therapy-response profiles.

**Quiescence/dormancy (mentioned indirectly):**
- Slow-cycling, quiescent GSCs are implicated in recurrence (cited but not the focus of this review).
- Quiescence is linked to resistance to radiation and chemotherapy.

---

## 4. Therapy Relevance

**Standard of care mentioned:**
- Surgical resection + radiotherapy + TMZ chemotherapy (Stupp protocol) is mentioned as standard management.
- Inherent tendency of glioma cells to disseminate limits treatment responses.

**Therapy-induced phenotypic changes:**
- Treatments targeting the highly proliferative tumor mass do not eliminate invasive cells.
- Local invasion leads to recurrence despite treatment of the tumor core.

**Chemotherapy and the go-or-grow switch:**
- A model in [50] includes space- and chemotherapy-dose-dependent phenotypic switch rates between migrating and proliferating cells.
- This is one of the earliest references to modeling therapy as a modifier of the go-or-grow switch rate.

**Radiotherapy:** Mentioned as part of standard of care and as a subject of mathematical modeling (reaction-diffusion models), but not the focus of this review.

**Immunotherapy:** Briefly noted in the broader context of adjuvant therapies.

---

## 5. Mathematical / Modeling Relevance

**Landscape of mathematical models for glioma invasion:**
The review classifies existing models into:

1. **Macroscopic continuous (PDE) models:**
   - Reaction-diffusion models (Murray type): most common; describe glioma cell density evolution.
   - Recent extensions: reaction-advection-diffusion with multiple taxis (haptotaxis, pH-taxis, chemotaxis).
   - Extensions to include tumor heterogeneity: subpopulations (hypoxic/normoxic/necrotic, migrating/proliferating).

2. **Multiscale models:**
   - Start from subcellular or kinetic transport equations (mesoscale).
   - Upscale to macroscopic PDEs.
   - Example: Surulescu group (see Conte & Surulescu 2021 for the latest version).

3. **Agent-based / discrete models:**
   - Describe individual cell behavior on a lattice.
   - Capture heterogeneity and spatial structure explicitly.

4. **Stochastic models:**
   - Mentioned as a relevant category for small populations and fluctuation-driven phenomena.
   - Stochastic multiscale settings referenced (e.g., [42, 43, 45]).

**Go-or-grow in mathematical models:**
- The migration-proliferation dichotomy has been modeled as mutually exclusive subpopulations.
- Phenotypic switch rates between migrating (M) and proliferating (P) states can be modeled as functions of local acidity, oxygen, nutrient levels, or therapy dose.
- The simplest formulation: two ODE compartments (M and P) with switch rates that depend on the microenvironment.

**CTMC / Gillespie relevance:**
- The review does not specifically discuss CTMC or Gillespie algorithm for this problem — these are not the primary tools for invasion modeling.
- However, the cell-state transition framework described (M ↔ P with environmentally-dependent rates) is structurally identical to a CTMC with state-dependent rates.

---

## 6. Parameters and Quantitative Information

- No explicit CTMC-level parameter values given.
- Background clinical statistics:
  - IDH wild-type GBM 5-year survival: ~5%
  - Most common adult primary brain tumor: ≈45% of all gliomas

**For PDE models referenced:**
- Invasion speeds on the order of mm/year (not relevant for a non-spatial model).
- Diffusion coefficients and proliferation rates for glioma PDE models are referenced but not extracted here (not needed for CTMC).

---

## 7. Assumptions and Limitations

- The review focuses on invasion (spatial) biology. A non-spatial model is, by definition, a simplification that ignores the features this review highlights as most important.
- The go-or-grow dichotomy is described as a biological phenomenon, but its molecular mechanisms are still incompletely understood — any model that switches cells between Go and Grow states imposes a discretization on what may be a continuous spectrum.
- The review covers models up to 2017. More recent work (e.g., tumor cell networks in Venkataramani 2022) is not included.
- The review focuses on invasion; recurrence mechanisms, therapy resistance, and stem cell hierarchy are covered only briefly.

---

## 8. Possible Use in This Project

- **Use in version 1:** The biological sections (phenotypic plasticity, go-or-grow, metabolic switching) provide the vocabulary and literature grounding for the assumptions document. The review justifies including a phenotypic state transition mechanism in the model. The classification of mathematical approaches provides context for explaining why a CTMC approach is chosen over PDEs.
- **Use for documentation:** The paper provides the definitive reference for stating "go-or-grow is a well-established biological phenomenon in glioma" in the assumptions document.
- **Use for future extension:** The PDE and multiscale model landscape described here is the roadmap for a spatial extension (v2+). The go-or-grow switch can be added to the CTMC as a Migrating state M with P ↔ M transitions.
- **Background only:** The molecular invasion mechanisms (integrin adhesion, MMP secretion, EMT) are not modeled at the CTMC level.

---

## 9. Modeling Interpretation

> **[INTERPRETATION — not a source fact]**
> This review supports including a go-or-grow phenotypic switch in the model as a biologically motivated future extension, but makes it clear this would require a spatial framework to be mechanistically meaningful. In a non-spatial v1 CTMC, modeling the go-or-grow switch would only capture the cell-state dynamics (cells switch between Proliferating and Migrating states) without the spatial consequence (actual invasion). This is acceptable if clearly documented as a simplification. A Migrating state M could be added in v2 as a state in which: (a) cells do not proliferate, (b) transition rate P → M depends on a proxy for microenvironmental stress, and (c) the transition M → P is the return to proliferation. The review also provides the justification for treating GBM as a phenotypically heterogeneous population rather than a homogeneous cell mass — the key conceptual argument for using a multi-state model.
