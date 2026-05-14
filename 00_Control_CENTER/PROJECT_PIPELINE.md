# PROJECT_PIPELINE.md

## Purpose

This file defines the standard workflow for upgrading any repository into a professional GitHub portfolio project.

The goal is to make each project cleaner, safer, more reproducible, better documented, and more useful for my public technical profile.

This pipeline should be used together with:

- MASTER_PLAN.md
- PERSONAL_POSITIONING.md
- GLOBAL_CLAUDE.md
- repo_CLAUDE_template.md

---

## Core Rule

Do not work on many repositories at once.

Use this sequence:

```text
One repository → one branch → one audit → one roadmap → small improvements → review → publish decision
```

The goal is not to create activity.

The goal is to create strong public-facing projects.

---

## Repository Upgrade Pipeline

Every repository should go through the following stages.

---

## Stage 0: Select the Repository

Before starting, decide why this repository matters.

Ask:

1. Does this project support my technical profile?
2. Is it strong enough to become public?
3. Does it show a relevant skill?
4. Can it be explained clearly?
5. Can it be made visually understandable?
6. Is there private or sensitive material inside?
7. Is the time investment worth it?

If the answer is unclear, do an audit first, but do not polish the project yet.

---

## Stage 1: Prepare Local Workspace

Recommended local structure:

```text
Felix-Personal-Engineering-System/
├── 01_REPO_INBOX/
├── 02_ACTIVE_REPOS/
├── 03_FINISHED_SHOWCASE_PROJECTS/
└── 05_PORTFOLIO_ASSETS/
```

Use:

```bash
cd ~/Documents/Claude/Projects/Felix-Personal-Engineering-System/02_ACTIVE_REPOS
```

Clone or move the repository into this folder.

Example:

```bash
git clone git@github.com:felixklein84/REPOSITORY_NAME.git
cd REPOSITORY_NAME
```

Check status:

```bash
git status
```

---

## Stage 2: Add Repository-Specific CLAUDE.md

Copy the template into the repository root:

```bash
cp ../04_CLAUDE_SYSTEM/repo_CLAUDE_template.md ./CLAUDE.md
```

Then edit the placeholders.

Minimum fields to fill:

```text
Project name
Short description
Current project type
Public positioning
Current goal
Known test command
Known run command
Publication status
Known constraints
Known limitations
Known future work
```

Do not skip this step.

The repository-specific CLAUDE.md is what prevents Claude Code from guessing.

---

## Stage 3: Create Upgrade Branch

Work on a branch.

Default:

```bash
git checkout -b portfolio-upgrade
```

If the repo already has that branch:

```bash
git checkout portfolio-upgrade
```

Alternative branch names:

```text
repo-cleanup
readme-upgrade
portfolio-polish
public-release-prep
docs-and-examples
```

Avoid working directly on main unless the change is tiny and intentional.

---

## Stage 4: Start Claude Code

From inside the repository:

```bash
claude
```

First prompt:

```text
Read CLAUDE.md first.

Please audit this repository for professional GitHub portfolio readiness.

Do not edit files yet.

Inspect the structure, README, dependencies, tests, privacy risks, and visual potential.

Then produce:
1. Current state
2. Strengths
3. Weaknesses
4. Risks
5. Quick wins
6. Larger improvements
7. Recommended public positioning
8. First implementation phase
```

Expected output:

- honest assessment
- no edits yet
- clear priorities
- public positioning
- risk list
- recommended first phase

---

## Stage 5: Audit Checklist

Claude should inspect:

```text
Repository structure
README
Dependency files
Tests
Example scripts
Notebooks
Data files
Assets
Git status
Large files
Private files
Credentials
Local paths
Public presentation
Visual potential
```

For Python projects, check:

```text
pyproject.toml
requirements.txt
setup.py
src/
tests/
notebooks/
examples/
```

For web projects, check:

```text
package.json
src/
public/
components/
pages/
app/
README.md
build scripts
deployment setup
```

For thesis or academic projects, check:

```text
model assumptions
data availability
reproducibility
plots
notebooks
references
privacy constraints
```

---

## Stage 6: Decide Upgrade Level

After the audit, classify the project.

### Level 1: Archive Only

Use when the project is not worth polishing.

Actions:

- clean private data
- add minimal README
- keep private or archive
- do not pin publicly

### Level 2: Basic Public Repo

Use when the project is useful but not a main showcase.

Actions:

- clean README
- add install/run notes
- add limitations
- remove private data
- maybe keep public but not pinned

### Level 3: Showcase Project

Use when the project should represent me strongly.

Actions:

- professional README
- visual assets
- architecture diagram
- reproducible examples
- tests or validation
- polished repo description
- GitHub topics
- portfolio website case study

### Level 4: Flagship Project

Use only for the strongest projects.

Actions:

- all Level 3 actions
- GIF/video/demo
- strong project page
- refined screenshots
- technical writeup
- polished diagrams
- potential blog post
- pinned on GitHub

---

## Stage 7: Implementation Phases

Do not implement everything at once.

Use phases.

### Phase 1: Safety and Cleanup

Tasks:

- check git status
- check private files
- update .gitignore
- remove obvious generated junk
- identify large files
- identify sensitive files
- document what should stay private

Do not delete important files without confirmation.

### Phase 2: Repository Structure

Tasks:

- clarify folder names
- separate source code from notebooks
- separate examples from tests
- move assets into assets/ or docs/assets/
- remove duplicate or dead files if safe
- document structure in README

### Phase 3: Reproducibility

Tasks:

- clarify Python/Node version
- clean dependency files
- document installation
- document run commands
- add example command
- add minimal smoke test if useful
- document manual validation if no tests exist

### Phase 4: README Upgrade

Tasks:

- rewrite project title and short description
- add overview
- add motivation
- add technical approach
- add installation
- add usage
- add example output
- add limitations
- add future work
- add tech stack

### Phase 5: Visual Assets

Tasks:

- identify existing plots/screenshots
- create or request missing visuals
- add architecture diagram
- add example output image
- add simulation GIF if useful
- create project thumbnail for portfolio
- compress large visual files

### Phase 6: Code Quality

Tasks:

- remove obvious duplication
- improve names where safe
- add comments only where useful
- simplify confusing functions
- preserve behavior
- add tests for changed behavior
- avoid large rewrites

### Phase 7: Public Release Polish

Tasks:

- final privacy check
- final README check
- final test run
- update repo description
- add GitHub topics
- choose pinned status
- prepare portfolio summary
- prepare LinkedIn/GitHub short description if needed

---

## Stage 8: Review After Each Phase

After every implementation phase, run:

```bash
git status
git diff
```

Run tests where possible:

```bash
pytest
python -m pytest
poetry run pytest
npm test
npm run build
```

Use the correct command for the project.

If tests fail:

1. Identify whether the failure existed before.
2. Identify whether the current changes caused it.
3. Fix if in scope.
4. Document if out of scope.

Do not pretend tests passed.

---

## Stage 9: Commit Discipline

Use small commits.

Good commit examples:

```text
Add repository-specific Claude instructions
Improve README structure and project positioning
Document installation and usage workflow
Add example output assets
Clean repository structure for public presentation
Add smoke test for simulation run
```

Bad commit examples:

```text
fix
update
final
stuff
claude edits
changes
```

Before commit:

```bash
git status
git diff
```

Then:

```bash
git add .
git commit -m "Improve README structure and project positioning"
```

Push branch:

```bash
git push origin portfolio-upgrade
```

---

## Stage 10: Public Release Checklist

Before making a repo public or pinning it:

```text
README is clear
Project description is strong
Installation instructions work
Usage example exists
Limitations are honest
No private data
No credentials
No raw company data
No private emails or phone numbers
No local file paths
No oversized unnecessary files
No broken links
Tests or validation steps are documented
Visual output exists where useful
Repo topics are set
Repo name is clean
```

If any critical item is missing, do not pin the repository yet.

---

## Stage 11: Portfolio Website Extraction

For each finished showcase project, create a portfolio summary.

Template:

```markdown
# Project Case Study: [PROJECT_NAME]

## One-Sentence Summary

[Clear short summary]

## Problem

[What problem this project addresses]

## Approach

[What was built and how it works]

## Technical Highlights

- [Highlight 1]
- [Highlight 2]
- [Highlight 3]

## Tools

[Languages, frameworks, libraries]

## Output

[Screenshot, plot, GIF, or result]

## Limitations

[Honest limitations]

## Future Work

[What could be improved]

## Why This Project Matters

[How this project supports my technical profile]
```

This summary can later be used for:

- portfolio website
- GitHub profile README
- CV project bullets
- interview talking points
- LinkedIn project post

---

## Stage 12: GitHub Profile Integration

Once a repository is polished, decide whether it should be:

```text
Pinned
Public but not pinned
Private
Archived
Merged into another showcase
Converted into portfolio-only case study
```

Pinned repositories should be limited to the strongest projects.

Recommended pinned set:

```text
1. Multi-Agent Tractor Simulation
2. Glioblastoma Markov Modeling
3. Supply Chain Automation / Data Quality
4. Winery Digital Commerce System
5. Portfolio Website
6. Optional strong data/visualization project
```

---

## Stage 13: Finish and Move On

After a repository is complete:

1. Merge or keep branch open.
2. Update finished project tracker.
3. Move assets to portfolio assets folder if needed.
4. Add project to portfolio website backlog.
5. Decide whether to pin the repo.
6. Start the next repository only after finishing the current one.

Do not leave ten half-upgraded repositories.

---

## Standard Claude Code Prompts

### Audit Prompt

```text
Read CLAUDE.md first.

Audit this repository for professional GitHub portfolio readiness.

Do not edit files yet.

Inspect structure, README, dependencies, tests, privacy risks, and visual potential.

Return:
1. Current state
2. Strengths
3. Weaknesses
4. Risks
5. Quick wins
6. Larger improvements
7. Recommended public positioning
8. First implementation phase
```

### Phase Planning Prompt

```text
Based on the audit, create a phased implementation roadmap.

Do not edit files yet.

Prioritize small, reviewable changes.

Separate:
1. Safety and privacy
2. Documentation
3. Reproducibility
4. Visual assets
5. Code quality
6. Public release polish
```

### README Upgrade Prompt

```text
Upgrade the README for professional public portfolio presentation.

Preserve technical accuracy.

Do not invent results.

Include:
- overview
- motivation
- technical approach
- installation
- usage
- example output placeholders if needed
- limitations
- future work
- tech stack

Keep the tone precise, technical, and non-generic.
```

### Privacy Review Prompt

```text
Review this repository for privacy and publication risks.

Look for:
- credentials
- tokens
- private emails
- phone numbers
- local paths
- raw company data
- confidential research data
- unpublished documents
- large unnecessary files
- metadata risks

Do not delete anything yet.

Return a risk list and recommended actions.
```

### Final Release Prompt

```text
Review this repository as if it were about to be made public and pinned on GitHub.

Check:
- README
- reproducibility
- visual assets
- privacy risks
- tests or validation
- repo description
- GitHub topics
- portfolio value

Return:
1. Ready / not ready
2. Blocking issues
3. Nice-to-have improvements
4. Suggested GitHub description
5. Suggested GitHub topics
6. Suggested pinned-project summary
```

---

## Definition of Done

A repository is done when it is no longer just technically present, but publicly understandable.

Done means:

```text
A recruiter, engineer, professor, or collaborator can open the repo and understand:
- what it is
- why it matters
- what I built
- how to run it
- what the output looks like
- what the limitations are
- why it represents my abilities
```

The final standard is:

```text
professional portfolio quality, not student submission quality
```
