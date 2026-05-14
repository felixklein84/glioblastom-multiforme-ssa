# repo_CLAUDE_template.md

This file is a reusable template.

Copy this file into the root of an individual repository and rename it to:

```text
CLAUDE.md
```

Then replace the placeholders with project-specific information.

---

# CLAUDE.md

## Project Identity

Project name:

`[INSERT_PROJECT_NAME]`

Short description:

`[INSERT_ONE_SENTENCE_DESCRIPTION]`

This repository is intended to become a professional public portfolio project.

The goal is to make the project understandable, reproducible, visually presentable, and suitable for GitHub, portfolio website, job applications, interviews, and technical discussions.

---

## Current Project Type

Select the relevant type:

- [ ] Robotics / simulation
- [ ] Mathematical modeling
- [ ] Data science / analytics
- [ ] Supply chain / operations
- [ ] Web / e-commerce
- [ ] Academic / thesis-related
- [ ] Portfolio website
- [ ] Other: `[INSERT]`

---

## Public Positioning

This project should be framed as:

`[INSERT_PUBLIC_POSITIONING]`

Examples:

- simulation and scheduling framework for autonomous agricultural field operations
- continuous-time Markov chain model for glioblastoma cell population dynamics
- data quality and purchase order monitoring workflow for supply chain operations
- digital commerce and product data system for a family winery

The public explanation should be precise, technical, honest, and not exaggerated.

Avoid student-project wording.

Avoid generic AI or startup language.

---

## Current Goal

The current goal of this repository upgrade is:

`[INSERT_CURRENT_GOAL]`

Examples:

- audit the current repository and create a cleanup plan
- improve README and public documentation
- make the project reproducible
- add tests or smoke tests
- create visual assets for GitHub
- prepare the repo for publication
- refactor selected code without changing behavior

---

## Working Rules

Before editing files:

1. Inspect the repository structure.
2. Read README.md if present.
3. Identify the programming language and dependency files.
4. Identify how to run the project.
5. Identify tests or missing tests.
6. Check Git status.
7. Check for private or sensitive files.
8. Produce a short audit and plan.

Do not begin with implementation.

---

## Editing Rules

When editing:

- make small, reviewable changes
- preserve existing behavior unless explicitly asked otherwise
- do not delete files without asking
- do not rewrite core logic without a plan
- avoid unnecessary dependencies
- keep documentation consistent with code
- prefer clarity over cleverness
- add or update tests when behavior changes
- update README when public usage changes

---

## Git Rules

Before work:

```bash
git status
```

Recommended branch:

```bash
git checkout -b portfolio-upgrade
```

After changes:

```bash
git diff
```

Do not commit automatically unless explicitly asked.

Suggest professional commit messages.

---

## Testing / Validation

Known test command:

```bash
[INSERT_TEST_COMMAND_OR_UNKNOWN]
```

Known run command:

```bash
[INSERT_RUN_COMMAND_OR_UNKNOWN]
```

If no tests exist:

- identify minimal smoke tests
- document manual validation steps
- do not invent test results

---

## Privacy and Security

Before making this repository public, check for:

- credentials
- API keys
- tokens
- .env files
- private emails
- phone numbers
- local file paths
- company-private data
- university-private documents
- raw exports
- confidential research data
- unpublished thesis material
- private images or PDFs

Sensitive files or folders:

```text
[INSERT_IF_KNOWN]
```

Publication status:

- [ ] already public
- [ ] private, intended to become public
- [ ] private, parts may become public
- [ ] must remain private

---

## README Requirements

The README should eventually include:

- clear project title
- one-sentence description
- overview
- motivation
- technical approach
- repository structure
- installation
- usage
- example output
- limitations
- future work
- tech stack

The README should not sound like:

- a university assignment
- a generic AI-written project
- an inflated startup pitch
- an unexplained code dump

---

## Visual Requirements

This project should eventually include, where useful:

- screenshots
- plots
- simulation GIF
- architecture diagram
- workflow diagram
- project thumbnail
- example output

Recommended folder:

```text
assets/
```

or:

```text
docs/assets/
```

---

## Documentation Style

Use writing that is:

- precise
- technical
- clear
- calm
- professional
- honest about limitations

Avoid:

- buzzwords
- overclaiming
- vague motivation
- excessive emojis
- generic “passionate about” wording
- claims not supported by the code

---

## Known Constraints

Known technical constraints:

```text
[INSERT_CONSTRAINTS]
```

Known project limitations:

```text
[INSERT_LIMITATIONS]
```

Known future work:

```text
[INSERT_FUTURE_WORK]
```

---

## Done Definition

This repository is ready for public portfolio use when:

- README is clear and professional
- installation and usage are documented
- sensitive data is removed
- repository structure is understandable
- project has visual proof of output where possible
- limitations are honest
- tests or manual validation are documented
- project description supports my overall technical profile
- GitHub repo description and topics are updated

---

## First Task for Claude

When starting work on this repository, begin with this prompt:

```text
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

---

## Example Filled Version: Multi-Agent Tractor Simulation

Project name:

`Multi-Agent Tractor Simulation`

Short description:

`Simulation and scheduling framework for autonomous agricultural field operations.`

Current Project Type:

- [x] Robotics / simulation
- [ ] Mathematical modeling
- [ ] Data science / analytics
- [ ] Supply chain / operations
- [ ] Web / e-commerce
- [ ] Academic / thesis-related
- [ ] Portfolio website
- [ ] Other

Public Positioning:

`simulation and scheduling framework for autonomous agricultural field operations`

Current Goal:

`Prepare this repository as a professional robotics/simulation portfolio project.`

Known test command:

```bash
poetry run pytest
```

Known run command:

```bash
[INSERT_PROJECT_SPECIFIC_RUN_COMMAND]
```

Known technical constraints:

```text
The project uses Python 3.11 and geospatial/simulation libraries such as Shapely, NetworkX, Matplotlib, and Pytest.
```

Known project limitations:

```text
The current version is a simulation and scheduling framework, not a deployed autonomous driving system.
```

Known future work:

```text
Dynamic replanning, richer field events, improved scheduler logic, better visualization, and optional MILP-based optimization.
```
