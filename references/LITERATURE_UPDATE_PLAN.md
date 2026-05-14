# Literature Update Plan: Glioblastoma Simulation Project

**Date compiled:** May 2026
**Scope:** Research directions from approximately 2020 onward, emphasis on 2023–2026.
**Purpose:** Identify what the current state of GBM research implies for the simulation project — not to incorporate all recent biology, but to ensure the model is grounded, honest, and positioned correctly relative to what is known.

---

## How to Read This Document

Each section covers one research area. For each:
- **Key idea** — what the current research says.
- **Model relevance** — why it matters for the CTMC framework.
- **V1 decision** — include / exclude / document-only.
- **Future extension** — what would need to change for a more advanced model.
- **Modeling consequence** — concrete implication for parameters, states, or architecture.
- **Search terms** — for follow-up reading.

At the end: a priority table summarizing all decisions.

---

## Priority Overview (Read This First)

| Area | V1 decision | Effort required |
|---|---|---|
| Clinical management / Stupp protocol | Document only — justifies therapy scenarios | None |
| Radiotherapy resistance (DNA repair, 4 Rs) | Include as parameter constraint | Low |
| TMZ resistance (MGMT, GSC selection) | Include as differential kill rates | Low |
| Cell-state plasticity (4 states: NPC/OPC/AC/MES) | Acknowledge; do not implement in v1 | None |
| GSC quiescence/dormancy | Include Q state — core of v1 | Already planned |
| Tumor heterogeneity and recurrence | Motivates model; document only | None |
| Tumor Treating Fields (TTF) | Include as optional 5th therapy scenario | Low |
| Immunotherapy / CAR-T | Future extension only | High |
| Mathematical oncology / RL-based optimization | Contextualizes project; future direction | None |
| Stochastic / ODE / PDE models | Confirms CTMC approach; informs implementation | Low |

**v1 model impact: minimal changes needed.** The 4-state CTMC (S/P/D/Q) with 4 therapy scenarios remains the right scope. TTF can be added as a 5th scenario at low cost. The Neftel 4-state transcriptional model is noted but intentionally not implemented.

---

## 1. Current Clinical Management of Adult Glioblastoma

### Key idea
The Stupp protocol (surgery → RT 60 Gy in 30 fractions + concomitant TMZ 75 mg/m² → 6 cycles adjuvant TMZ) remains the standard of care 20+ years after its introduction. Median overall survival is 14–16 months. In 2024–2025, the most established additive therapy is Tumor Treating Fields (TTF/Optune), which adds ~4.9 months median OS and brings the 5-year survival rate to ~13%. Phase I/II immunotherapy combinations (checkpoint inhibitors, CAR-T) show early promise but no new standard has been established.

MGMT promoter methylation remains the strongest predictive biomarker: methylated patients benefit more from TMZ. IDH wild-type classification is the current standard for GBM (WHO 2021).

### Model relevance
- The Stupp protocol defines the 4 canonical therapy scenarios that map to the 4 model experiment files: no therapy, RT, TMZ, RT+TMZ.
- The 6-cycle adjuvant TMZ structure with 5/28-day dosing is the reference schedule.
- Fractionated RT (30 fractions × 2 Gy) is the reference schedule.
- TTF is an approved standard option — justifies including it as a 5th scenario.

### V1 decision
**Document only.** The model does not need to be updated, but the README and model specification must state the Stupp protocol as the clinical reference. Any claim about survival outcomes requires careful framing (the model does not predict patient survival).

### Modeling consequence
```yaml
# config/experiment_combined.yaml — reference schedule
radiotherapy:
  total_dose_gy: 60
  fractions: 30
  fraction_dose_gy: 2.0
  schedule: daily_weekdays
temozolomide:
  concomitant_dose: 75  # mg/m2, simplified to rate multiplier
  adjuvant_cycles: 6
  cycle_days: 5
  cycle_length_days: 28
```
All dose values are clinical reference values, not model-calibrated parameters. Mark as `[CLINICAL REFERENCE — not model parameters]` in code.

### Search terms for follow-up
- "Stupp protocol 2024 update glioblastoma"
- "MGMT methylation GBM prognosis 2024"
- "GBM WHO 2021 classification IDH wildtype"

---

## 2. Radiotherapy Response and Resistance

### Key idea
RT resistance in GBM is multifactorial. The **"4 Rs of radiotherapy"** remain the conceptual framework: Repair (of sublethal DNA damage), Repopulation (tumor regrowth between fractions), Redistribution (cell cycle phase shifts), Reoxygenation (hypoxic cells become more radiosensitive after each fraction). Of these, **repair** is most important in GBM.

At the molecular level, resistance is driven by:
- Efficient DNA double-strand break repair (NHEJ, HR pathways).
- Quiescent/slow-cycling GSCs that are in G0/G1 (most radioresistant cell cycle phase).
- BMP signaling mediates GSC quiescence and confers radiation resistance.
- HDACs contribute to RT resistance via modulation of DNA repair.

A 2022 Frontiers study built a multi-compartment ODE model of glioma response to fractionated RT parameterized from time-resolved microscopy — the most directly relevant mathematical RT model found.

**Key quantitative fact:** Dose escalation beyond 60 Gy shows no survival benefit (established by multiple trials). Hypofractionation (e.g., 40 Gy in 15 fractions for elderly patients) is used in certain populations.

### Model relevance
- The 4 Rs imply that a fractionated RT model should separate daily dose events (each fraction is an individual rate modification event in the CTMC timeline).
- The GSC radioresistance is already captured by the model: S-state cells have lower RT-induced death rate than P-state cells.
- Repopulation between fractions means proliferation continues between daily RT events — handled by the model's background dynamics between dose events.
- The BMP → GSC quiescence link suggests that RT can paradoxically drive more cells into the Q state, potentially worsening long-term outcomes despite short-term tumor reduction.

### V1 decision
**Include as parameter constraint.** The RT module in v1 should implement daily dose events (30 discrete time points over 6 weeks) rather than a single continuous rate. The differential sensitivity by cell state (S < D < P) should be explicit parameters with `[ORDER-OF-MAGNITUDE ASSUMPTION]` labels.

### Future extension
- Implement cell-cycle phase as a sub-state (G0/G1 vs. S/G2/M) to model radiation sensitivity variation across the cell cycle.
- Model reoxygenation effect (not feasible without spatial/hypoxia variable).
- The multi-compartment ODE model from the Frontiers 2022 paper is a candidate for parameterizing RT kill rates from microscopy data.

### Modeling consequence
```python
# radiotherapy.py
# RT kill rates: order-of-magnitude assumption, no calibrated source
RT_KILL_RATES = {
    CellState.S:  0.02,  # [ASSUMPTION] low — quiescent, G0/G1
    CellState.P:  0.15,  # [ASSUMPTION] high — actively cycling
    CellState.D:  0.05,  # [ASSUMPTION] moderate
    CellState.Q:  0.01,  # [ASSUMPTION] very low — quiescent
}
# Fractionation: 30 daily events (weekdays), each applying the above rates once
```

### Search terms
- "BMP signaling GSC quiescence radiation resistance glioblastoma"
- "multi-compartment glioma RT model fractionated radiation ODE"
- "4 Rs radiotherapy glioblastoma GSC"

---

## 3. Temozolomide Resistance

### Key idea
TMZ resistance is one of the most studied problems in GBM oncology. The primary mechanisms (2020–2025):

1. **MGMT overexpression** (O6-methylguanine-DNA methyltransferase): repairs the primary TMZ-induced DNA lesion. MGMT promoter methylation silences this gene → TMZ sensitive. MGMT unmethylated → highly resistant. ~50% of newly diagnosed GBM patients have MGMT-methylated tumors.

2. **Mismatch repair (MMR) deficiency**: secondary resistance mechanism. TMZ creates O6-methylguanine; if MGMT doesn't repair it, MMR recognizes but cannot repair the mismatch → futile cycling → cell death. Loss of MMR → cells tolerate the mismatch → resistance.

3. **GSC selection** (confirmed by Lan 2017, consistent with 2024 reviews): TMZ preferentially kills cycling cells, enriching for pre-existing drug-resistant GSCs. This is the most important mechanism for the CTMC model.

4. **TMZ-induced hypermutation**: extended TMZ exposure can trigger hypermutation in a subset of tumors (via MMR loss), creating a hypermutated recurrence phenotype. This is a genotypic escape mechanism.

5. **Autophagy**: cytoprotective autophagy protects GBM cells from TMZ-induced apoptosis.

6. **Blood-brain barrier**: limits TMZ delivery (relevant to dosing models, not cell-state models).

**Prevalence:** TMZ resistance occurs in approximately 50% of patients.

### Model relevance
- The most important mechanism for the CTMC is item 3: **TMZ kills cycling cells (P state) while enriching the GSC (S state) fraction**.
- MGMT methylation status could be modeled as two patient populations with different `mu_P^TMZ` values.
- TMZ-induced dormancy (P → Q transition) is the Blath 2023 mechanism and relevant here.
- Hypermutation is a genotypic event — not modeled in v1 CTMC (state space would need genotype axis).

### V1 decision
**Include as differential kill rates.** TMZ kill rate should be highest for P state, lower for S, minimal for Q and D. A two-population variant (MGMT-methylated vs. unmethylated) is a low-cost sensitivity analysis scenario.

### Future extension
- Add MGMT status as a binary modifier parameter (methylated: `μ_P^TMZ` ×1.0; unmethylated: `μ_P^TMZ` ×0.1).
- Model TMZ-induced hypermutation as a rare genotypic event (requires adding a resistance genotype state).

### Modeling consequence
```python
# temozolomide.py
TMZ_KILL_RATES = {
    CellState.S:  0.03,  # [ASSUMPTION] low — therapy resistant GSC
    CellState.P:  0.20,  # [ASSUMPTION] high — cycling cells, TMZ primary target
    CellState.D:  0.05,  # [ASSUMPTION] low — non-proliferative
    CellState.Q:  0.01,  # [ASSUMPTION] very low — dormant
}
TMZ_DORMANCY_INDUCTION = {
    CellState.P: 0.10,   # [ASSUMPTION] sigma_T: therapy-induced P -> Q rate
    CellState.S: 0.02,   # [ASSUMPTION] small therapy-induced S -> Q rate
}
# Sensitivity analysis: MGMT_MULTIPLIER in {0.1, 0.5, 1.0} applied to TMZ_KILL_RATES
```

### Search terms
- "MGMT methylation TMZ glioblastoma resistance mechanism 2024"
- "temozolomide resistance GSC selection enrichment"
- "TMZ hypermutation recurrence glioblastoma MMR"

---

## 4. Glioblastoma Cell-State Plasticity

### Key idea
The **Neftel et al. 2019 (Cell)** paper established that GBM malignant cells cycle among four transcriptional states:
- **NPC-like** (neural progenitor-like)
- **OPC-like** (oligodendrocyte progenitor-like)
- **AC-like** (astrocyte-like)
- **MES-like** (mesenchymal-like)

Individual cells are plastic: a single cell can generate progeny in all four states. Genetic alterations (EGFR, PDGFRA, CDK4, NF1) bias cells toward particular states but do not fix them. The MES-like state is associated with therapy resistance and poor prognosis.

**2024 updates:** Single-cell multi-omics studies (Science Advances, 2024) show region-specific plasticity — different tumor regions are enriched for different states. Cell 2024 shows a multi-layered spatial organization. Longitudinal studies (Nature Genetics 2025) show that the dominant malignant state changes at recurrence, co-evolving with the tumor microenvironment.

**Treatment-induced state shifts:** Drugs induce significant but reversible shifts in state distribution; MES-like state enrichment is observed after standard chemoradiation (the "mesenchymal reprogramming" seen at recurrence).

### Model relevance
The 4-state Neftel model is **orthogonal** to the 3-state Lan hierarchy. Lan describes the proliferative hierarchy (who can self-renew); Neftel describes transcriptional identity (what the cell looks like). They are not the same thing, though they are correlated: GSCs tend to cycle through NPC/OPC states; post-treatment recurrent tumors tend to be MES-enriched.

**v1 cannot incorporate both hierarchies.** Doing so would require at minimum a 4×4 = 16 state space, which becomes opaque and unparameterizable.

### V1 decision
**Acknowledge in documentation; do not implement.** The model specification should explicitly state: "The present model uses the Lan 2017 proliferative hierarchy (S/P/D/Q). The Neftel 2019 transcriptional state model is a distinct but complementary framework, not integrated in v1."

### Future extension
- A v2+ model could merge the two frameworks: each proliferative state (S, P, D) carries a secondary transcriptional state label (NPC, OPC, AC, MES), with transitions between them driven by therapy and microenvironment.
- Therapy-induced MES shift could be modeled as: post-RT/TMZ, increase in MES-like subpopulation within the S state → higher intrinsic resistance at recurrence.

### Modeling consequence
No code change needed. Add to `docs/assumptions.md`:
```
The Neftel 2019 four-state transcriptional model (NPC/OPC/AC/MES) is not 
incorporated in v1. This is a deliberate simplification. The model's S/P/D/Q 
states capture proliferative hierarchy, not transcriptional identity.
```

### Search terms
- "Neftel 2019 glioblastoma four states NPC OPC AC MES plasticity"
- "GBM mesenchymal reprogramming recurrence 2024"
- "single cell RNA seq glioblastoma state transition 2024 2025"

---

## 5. Glioma Stem-Like Cells and Dormancy/Quiescence

### Key idea
This is the area most directly relevant to the v1 model. Confirmed findings from 2020–2025:

- **Quiescent GSCs (qGSCs)** drive tumor initiation, expansion, and recurrence following chemotherapy (PMC8820651, 2022).
- qGSCs are defined by: slow cycling, BMP pathway activation (vs. TGF-β in proliferative GSCs), high expression of quiescence markers (p27, QSOX1, BEX2, GPD1).
- **BMP signaling** maintains qGSC state and confers treatment resistance (radiation + TMZ).
- qGSCs are NOT permanently quiescent — they can exit quiescence and re-enter the cell cycle, contributing to recurrence.
- Cancer cell dormancy review (Springer 2023): dormancy, stemness, and therapy resistance are interconnected. The stemness → dormancy connection is well-established.

**Key 2022 paper (Quiescent human GBM CSCs — PMC8820651):** Quiescent GBM cancer stem cells (defined by label retention) drive tumor recurrence following TMZ chemotherapy. This paper directly confirms the Q state's role in GBM recurrence.

**New markers:** p27 (cell cycle arrest), BEX2 (brain-expressed X-linked 2), QSOX1 (quiescent markers). These are not modeled but are relevant for future experimental calibration.

**Activation:** IFNα treatment has been shown to activate dormant stem-like cells in hematopoietic cancers, then eliminate them with 5-FU — a "prime and kill" approach. The GBM analogy is unexplored but theoretically relevant.

### Model relevance
This confirms the Q state is biologically well-grounded for GBM specifically (not just cancer in general). The following transitions are supported by literature:
- S → Q (spontaneous: BMP-driven quiescence entry)
- P → Q (therapy-induced: TMZ and RT drive cycling cells into quiescence)
- Q → S (dormancy exit → stem-like re-entry)
- Q → P (dormancy exit → progenitor re-entry)
- Q → † (slow death rate for dormant cells)

BMP signaling could be modeled as an environmental variable that modifies σ (S → Q rate), but this adds complexity not needed in v1.

### V1 decision
**Include Q state — already planned.** The literature search confirms this is the right choice. The quiescence-dormancy-recurrence axis is the central biological justification for the v1 model's departure from the old thesis.

### Future extension
- Add BMP/TGF-β as a binary microenvironment switch that modifies S → Q vs. S → P branching ratio.
- "Prime and kill" protocol: drug A forces Q → P (activates dormant cells), then drug B kills P cells. Directly testable in the Blath 2023 framework.
- Calibration target: quiescent GSC fraction is estimated at ~5–15% of GSC population in some models (needs literature verification).

### Modeling consequence
The Q state transitions should be labeled in `parameters.py` with specific evidence levels:
```python
# S -> Q: [ASSUMPTION — biologically motivated by BMP-driven qGSC literature]
# P -> Q: [LITERATURE — Blath 2023; consistent with TMZ-induced dormancy in GBM]
# Q -> S: [ASSUMPTION — dormancy exit rate; no GBM-specific calibration]
# Q -> P: [ASSUMPTION — dormancy exit to progenitor; order-of-magnitude only]
```

### Search terms
- "quiescent glioblastoma stem cells recurrence 2022 2023"
- "BMP signaling GSC quiescence resistance"
- "dormancy cancer stem cells therapy resistance review 2023"
- "prime and kill dormant cancer cells activation"

---

## 6. Tumor Heterogeneity and Recurrence

### Key idea
GBM recurrence is driven by three interconnected mechanisms (2024 consensus):
1. **GSC reservoir:** quiescent GSCs survive therapy and regenerate the tumor hierarchy.
2. **Clonal selection:** therapy selects for resistant subclones (pre-existing in the heterogeneous tumor). This is Darwinian evolution at the tumor level.
3. **Mesenchymal reprogramming:** chemoradiation shifts the tumor toward a MES-like state at recurrence, which is more aggressive and invasive.

**Treatment-induced heterogeneity increase:** The tumor at recurrence is MORE heterogeneous than at diagnosis because therapy applied selective pressure to a heterogeneous starting population.

**Spatial heterogeneity:** A 2024 Cell paper ("Integrative spatial analysis reveals a multi-layered organization") shows GBM is spatially organized with local enrichment of specific states, creating therapeutic access challenges.

**Clonal dynamics (from 3D whole-tumor study, Cell 2024):** Trunk mutations (shared by all cells) set the backbone; branching evolution creates subclones. No two recurrent tumors are genetically identical to their primary, even from the same patient.

### Model relevance
The CTMC framework captures the GSC reservoir mechanism naturally — it is built on the hierarchy. Clonal selection is only partially modeled (the model selects for S cells via differential kill rates, but does not track genotypic subclones). Mesenchymal reprogramming is not modeled.

The "treatment-induced heterogeneity increase" is an important conceptual point: a model that starts with a narrow initial distribution of cell states and ends with a broader distribution after therapy is capturing something real, even without explicit genotypic tracking.

### V1 decision
**Motivates the model; document only.** The model specification should explicitly connect "therapy selects for resistant GSCs" to the asymmetric kill rate design.

### Future extension
- Track subclonal genotypes (requires a 2D state space: phenotypic × genotypic).
- Model spatial architecture at recurrence (requires PDE extension).

### Modeling consequence
No code change. Add to README:
```
GBM recurrence is driven by quiescent GSCs that survive therapy and 
re-establish the tumor hierarchy. The model captures this mechanism 
through the Q state and asymmetric therapy kill rates, not through 
explicit tracking of genetic subclones.
```

### Search terms
- "glioblastoma recurrence mechanisms 2024 GSC clonal evolution"
- "GBM mesenchymal reprogramming chemoradiation recurrence"
- "3D whole-tumor glioblastoma heterogeneity Cell 2024"

---

## 7. Tumor Treating Fields (TTF / Optune)

### Key idea
Tumor Treating Fields (TTF, trade name Optune/Optune Gio) is an FDA-approved locoregional therapy delivering alternating electric fields (200 kHz, ~1–3 V/cm) via scalp transducer arrays. It is now standard of care alongside TMZ for newly diagnosed GBM (added ~4.9 months median OS; 5-year survival ~13%).

**Mechanism of action (multimodal):**
1. Disrupts mitotic spindle assembly → impairs cell division in M phase.
2. Inhibits DNA replication and damage response.
3. Interferes with cell motility (inhibits invasion).
4. Activates the type I interferon pathway → immune activation in situ.

**Clinical efficacy (2024 meta-analysis):**
- Newly diagnosed GBM: pooled median OS 21.7 months, PFS 7.2 months.
- Recurrent GBM: pooled median OS 10.3 months, PFS 5.7 months.
- Compliance ≥75% is associated with significantly improved OS.
- Main side effect: skin irritation from transducer arrays (~38.4% prevalence).

**New combinations:** TTF + pembrolizumab phase 2 study (2025) shows improved PFS/OS in patients with biopsy-only resection. TTF + radiation (new pivotal studies announced).

### Model relevance
TTF has a unique multimodal mechanism:
- Anti-mitotic effect → primarily targets cells in M phase (a subset of the P state).
- Anti-motility effect → reduces P → Migrating transition (future extension).
- Immune activation → not modeled in v1.

For a CTMC model, the simplest representation: TTF increases death rate of P cells (via mitotic disruption) and potentially the P → Q rate (cells that survive TTF may enter quiescence rather than complete division).

The key model distinction from RT: TTF acts continuously (device worn ~18 hours/day) rather than in discrete fractions. This makes it a continuous rate modification rather than a pulsed event.

### V1 decision
**Include as optional 5th therapy scenario.** Low implementation cost: it is a continuous modification to `mu_P^TTF` (P-state death rate) and `mu_S^TTF` (S-state death rate, lower). Framing: "TTF is approximated as a continuous enhancement of mitosis-disruption kill rate for cycling cells."

This gives the model 5 canonical scenarios: no therapy, RT only, TMZ only, RT+TMZ (Stupp), TTF+TMZ.

### Future extension
- Frequency-tuned kill rates (different TTF frequencies have different effects on different cell types).
- Combine TTF + immunotherapy immune activation effect.
- Compliance modeling: TTF kill rate is proportional to hours/day of use → stochastic on/off model.

### Modeling consequence
```python
# therapy/ttfields.py
TTF_KILL_RATES = {
    CellState.S:  0.005,  # [ASSUMPTION] minimal — not in mitosis
    CellState.P:  0.08,   # [ASSUMPTION] moderate — mitotic disruption
    CellState.D:  0.002,  # [ASSUMPTION] minimal — non-cycling
    CellState.Q:  0.002,  # [ASSUMPTION] minimal — quiescent
}
TTF_SCHEDULE = "continuous"  # ~18 hours/day approximated as continuous
TTF_COMPLIANCE = 0.75  # fraction of time device is used — scales kill rates
```

### Search terms
- "Tumor Treating Fields mechanism glioblastoma 2024"
- "TTFields compliance survival glioblastoma"
- "Optune glioblastoma clinical outcomes meta-analysis 2024"

---

## 8. Immunotherapy and CAR-T Approaches

### Key idea
Immunotherapy for GBM has been an active clinical area with major recent progress, though no new standard of care has been established yet.

**Checkpoint inhibitors:**
- Anti-PD-1 (nivolumab) failed to improve OS in two large phase III trials (CheckMate 143, CheckMate 498).
- NRG-BN002 phase I (anti-CTLA-4 + anti-PD-1) showed median OS of 20.7 months — promising but phase I, not definitive.
- TTF + pembrolizumab (2025 phase II): improved PFS/OS in biopsy-only subgroup.

**CAR-T therapy (major 2024–2025 developments):**
- INCIPIENT trial (MGH, NEJM 2024): CAR-T cells targeting EGFRvIII with a TEAM construct → "dramatic and rapid" tumor regression in 3 patients with recurrent GBM. First truly encouraging CAR-T results in GBM.
- Penn/ASCO 2025: Bivalent CAR-T targeting both IL13Rα2 and EGFR-806, administered intrathecally. 18 patients, median follow-up 8.1 months. First bivalent intracranial CAR-T reported.
- Key challenge: antigen escape (tumor heterogeneity means no single target covers all tumor cells). Bivalent/multi-target approaches attempt to address this.

**Why previous immunotherapy failed in GBM:**
- Highly immunosuppressive tumor microenvironment (tumor-associated macrophages, myeloid-derived suppressor cells).
- Blood-brain barrier limits systemic immune cell access.
- GBM downregulates antigen expression under immune pressure (phenotypic escape — analogous to Baar 2016 melanoma model).

### Model relevance
Immunotherapy is **not in v1 scope** and should not be added. However:
- The phenotypic escape mechanism (antigen downregulation under immune pressure → treatment failure) is biologically analogous to the Baar 2016 phenotypic switching model. If immunotherapy is added later, the Baar framework applies directly.
- The CAR-T "antigen escape" problem is the GBM-specific version of the melanoma therapy escape modeled in Baar 2016.
- Current CAR-T outcomes are so early-phase that parameter estimation is not feasible.

### V1 decision
**Future extension only.** Do not implement. State in README: "Immunotherapy modeling is beyond the scope of this project. The stochastic framework used (Baar et al.) was originally designed for immunotherapy modeling and is structurally capable of extension in this direction."

### Future extension
- Add an Immune state (immune cell population, analogous to Baar 2016 T-cell population).
- Model antigen escape as a phenotypic switch S/P → hidden state, analogous to differentiated → dedifferentiated in Baar 2016.
- The "prime and kill" dormancy activation strategy (Section 5) could combine with immunotherapy: activate dormant cells, then eliminate with immune cells or drugs.

### Modeling consequence
No code. Add to `docs/future_work.md`:
```
Immunotherapy extension: The Baar 2016 framework — already used as the 
mathematical template for this project — was designed for immunotherapy modeling. 
A direct extension would add immune cell populations (T-cells or CAR-T) and 
model antigen expression as a phenotypic state, consistent with current CAR-T 
antigen escape biology.
```

### Search terms
- "glioblastoma CAR-T 2024 2025 clinical results"
- "anti-PD1 nivolumab glioblastoma trial failure"
- "antigen escape immunotherapy glioblastoma"

---

## 9. Mathematical Oncology and Model-Informed Therapy

### Key idea
Mathematical oncology for GBM has advanced significantly in 2022–2025. Key developments:

**Physics-informed / PDE-based personalized models:**
- GliODIL (Nature Communications 2025): infers full spatial tumor distribution from multi-modal MRI, uses Fisher-Kolmogorov PDE to inform individualized RT planning.
- Physics-informed neural networks (PINNs) for GBM infiltration prediction (Medical Image Analysis 2024).
- These are clinical decision-support tools, not mechanistic stochastic models.

**Multiscale agent-based + ODE models:**
- PMC10628546 (2023): multiscale model integrating agent-based cellular phenotypes, ODE signaling pathways, stochastic gene mutations, spatial microenvironmental factors. Validated against scRNA-seq data. Most comprehensive single model found.
- This model is much more complex than the proposed CTMC but confirms that stochastic + deterministic hybrid approaches are current best practice.

**Reinforcement learning for therapy optimization:**
- Science Advances 2025 (M4RL): multiscale ABM-informed RL to optimize drug combination scheduling for GBM. Combines MSABM (glioma-macrophage interactions) → stochastic DE/ODE hybrid → Fokker-Planck equations → RL policy optimization.
- Earlier work (ScienceDirect 2021): RL for optimal TMZ scheduling in GBM.
- This is the frontier of mathematical oncology for GBM. The CTMC project is a simpler building block toward this direction.

**Stochastic hierarchical glioma models:**
- PMC10163130 (2023): stochastic hierarchical model for low-grade glioma evolution using piecewise deterministic Markov processes (PDMPs). Related to but distinct from CTMC.

**Patient-specific modeling:**
- Bayesian inference and PDE-constrained optimization for patient-specific tumor growth models.
- Machine learning surrogate models for fast PDE simulation.

### Model relevance
The project's CTMC approach is a modest but rigorous contribution to mathematical oncology — more rigorous than most clinical PDE models (which use phenomenological parameters), but less complex than the multiscale ABM models. The correct positioning is: "a minimal stochastic mechanistic model for population dynamics and therapy comparison, grounded in known biological hierarchy, implementable without patient imaging data."

The RL therapy optimization direction is the natural long-term trajectory: use the CTMC model as the forward simulator in a simple RL or control optimization framework. This is feasible in a future version.

### V1 decision
**Contextualizes the project; no code change.** Use this knowledge to position the project correctly in the README relative to the existing landscape.

### Future extension
- Use the CTMC model as a forward simulator in an RL framework to find optimal therapy schedules (frequency, dose, sequence of RT/TMZ/TTF).
- Connection to Science Advances 2025 paper — this is the frontier being approached.

### Modeling consequence
Add to README positioning section:
```
This project sits at the intersection of the Baar/Blath stochastic 
population dynamics tradition and the model-informed therapy optimization 
direction exemplified by recent work in mathematical oncology (e.g., 
multiscale RL approaches). The CTMC framework provides a tractable 
forward model for therapy simulation; future work could use it as the 
simulator in reinforcement-learning-based treatment optimization.
```

### Search terms
- "mathematical oncology glioblastoma model-informed therapy 2024 2025"
- "reinforcement learning TMZ scheduling glioblastoma"
- "multiscale glioblastoma model stochastic ODE hybrid 2023"

---

## 10. Stochastic, ODE, PDE, and Agent-Based Glioblastoma Models

### Key idea
The 2022–2025 landscape of glioblastoma modeling:

**Stochastic CTMC / branching process models:**
- PMC10163130 (2023): stochastic hierarchical model for low-grade glioma using PDMPs. Confirms the research direction of the new project.
- ScienceDirect (2021): stochastic ODE models for chemotherapy predicting cure rates — directly analogous.
- **Gap found:** No paper found (from this search) uses a CTMC with the Lan 2017 GSC hierarchy for GBM specifically with therapy comparison. This is the niche the new project occupies.

**Agent-based models:**
- PMC10628546 (2023): multiscale ABM + ODE signaling + stochastic mutations for GBM. Most comprehensive but requires scRNA-seq input data.
- ABM is appropriate for spatial questions; CTMC is appropriate for population dynamics and extinction probability questions.

**PDE models (dominant approach for spatial invasion):**
- GliODIL (Nature Communications 2025), PINNs (2024): patient-specific spatial infiltration.
- PMC10031411 (2023): data-driven spatio-temporal GBM modeling.
- These are focused on tumor boundary and radiation target volume — different question from the CTMC project.

**Key modeling comparison (PLOS One study — older but relevant):** Comparison of stochastic DEs vs. ABM for early-stage cancer: both approaches give similar results for population-level predictions but differ at small population sizes where stochastic effects dominate. This confirms the theoretical motivation for the CTMC approach.

**Hybrid approaches (current best practice):**
- Stochastic at small scales, ODE at large scales — exactly the architecture planned for the new project.
- The M4RL paper (Science Advances 2025) uses a similar hybrid: MSABM → SDE/ODE hybrid → Fokker-Planck.

### Model relevance
The search confirms:
1. **The CTMC approach is methodologically sound** — consistent with best practice in the field.
2. **The specific combination** (Lan 2017 hierarchy + dormancy + multi-therapy CTMC) has not been published. This is an original contribution.
3. **The hybrid stochastic/ODE architecture** is correct — the ODE module is not just a convenience; it is the standard complement to stochastic simulation.
4. **PDE/spatial models** are a complementary, not competing, approach — they answer different questions (where is the tumor?) vs. the CTMC (what fraction of cells survive therapy?).

### V1 decision
**Confirms existing design; low-cost implementation adjustments.** Specifically: implement both Gillespie SSA and ODE mean-field, as planned. The PLOS One comparison study supports reporting both and explicitly showing where they diverge (near extinction boundary).

### Future extension
- Piecewise deterministic Markov process (PDMP) formulation for more efficient simulation with continuous dynamics between jump events.
- Fokker-Planck equation as an approximation between Gillespie (discrete) and ODE (deterministic continuous).
- Connection to spatial PDE models via a hybrid model where each spatial voxel contains a CTMC population.

### Modeling consequence
Add to README:
```
The project implements both exact stochastic simulation (Gillespie SSA) 
and deterministic ODE mean-field approximation. Comparison of the two 
reveals where population size matters: near the extinction boundary 
(therapy-induced remission), stochastic fluctuations dominate and 
the ODE is unreliable. This duality is a core scientific result of 
the project, not just a computational convenience.
```

### Search terms
- "continuous time Markov chain tumor therapy stochastic 2022 2023"
- "stochastic hierarchical glioma model 2023"
- "piecewise deterministic Markov process cancer model"
- "data-driven glioblastoma model stochastic 2023 2024"

---

## Summary: V1 Model Impact

The following table summarizes the concrete changes implied by the literature search for the v1 model implementation:

| Component | Change required | Evidence level |
|---|---|---|
| Q state (quiescence) | Already planned; confirmed by 2022 GBM quiescent GSC paper | Literature |
| RT as daily fractionated events | Change RT from continuous to 30 discrete events | Clinical reference |
| RT kill rate differential by state (S < D < P) | Already planned; confirmed by BMP/quiescence literature | Literature + assumption |
| TMZ kill rate differential by state | Already planned; confirmed by GSC selection literature | Literature + assumption |
| TMZ dormancy induction (P → Q) | Already planned; confirmed by Blath 2023 + GBM dormancy literature | Literature + assumption |
| TTF as 5th therapy scenario | New; add as continuous rate modification for P state | Clinical reference |
| MGMT as sensitivity analysis parameter | New; multiply TMZ kill rates by MGMT factor in experiment config | Clinical reference |
| ODE + SSA comparison plots | Already planned; confirmed as best practice | Literature |
| 4-state Neftel model | Explicitly excluded; document the exclusion | Deliberate simplification |
| Immunotherapy states | Explicitly excluded; document as future work | Out of scope |

**Lines of code implied:** The only new implementation item not already planned is the TTF module (~30 lines) and an MGMT sensitivity analysis parameter (~5 lines in config).

Everything else is documentation and parameter labeling.

---

## Recommended Next Papers to Acquire

These papers were found in the search but are not in the current reference library. Priority order:

| Priority | Paper | Why |
|---|---|---|
| 1 | PMC8820651 (2022) — Quiescent human GBM CSCs drive recurrence | Direct GBM-specific justification for Q state |
| 2 | Neftel et al. 2019 (Cell) — 4-state integrative model | Standard reference for GBM cell states; must be cited if states are discussed |
| 3 | Frontiers 2022 — Multi-compartment RT model parameterized from microscopy | RT kill rate parameterization reference |
| 4 | Science Advances 2025 — M4RL reinforcement learning for GBM | Future work positioning |
| 5 | PMC12139195 (2025) — TMZ resistance review | Updated TMZ resistance overview |

These papers should be downloaded and processed into Markdown summaries (Stage 1 format) before writing the model specification.
