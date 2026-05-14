# GLOBAL_CLAUDE.md

## Purpose

This file defines the global working rules for Claude and Claude Code when helping me upgrade repositories, technical projects, GitHub presentation, portfolio content, CV material, documentation, and code quality.

## General Working Principle

Never optimize blindly.

Default workflow:

```text
Inspect -> Understand -> Plan -> Implement small changes -> Test -> Review diff -> Document -> Commit suggestion
```

## Default Behavior

Claude should usually:

- inspect the repository before suggesting changes
- create a plan before editing many files
- prefer small, reviewable steps
- preserve existing behavior unless asked otherwise
- avoid large rewrites
- explain tradeoffs clearly
- update README when public behavior changes
- check for private data before publication
- prioritize professional presentation
- avoid generic AI-style writing

Claude should not:

- delete files without asking
- rewrite core logic without a plan
- invent results, metrics, benchmarks, or project outcomes
- claim production readiness unless true
- expose private company, university, or personal information
- over-engineer simple projects
- add unnecessary dependencies
- make huge changes in one pass

## Git Rules

Before changes:

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

## Project Positioning Rules

### Multi-Agent Tractor Simulation

Frame as:

> simulation and scheduling framework for autonomous agricultural field operations

### Glioblastoma Modeling

Frame as:

> continuous-time Markov chain model for glioblastoma cell population dynamics

### Supply Chain Automation

Frame as:

> data quality and purchase order monitoring workflow for supply chain operations

### Winery Digital Commerce System

Frame as:

> digital commerce and product data system for a family winery

## Privacy and Security Rules

Before making a repository public, check for:

- API keys
- credentials
- private URLs
- customer or supplier names
- internal company names if sensitive
- private emails
- phone numbers
- local file paths
- unpublished research data
- confidential university or company documents
- private images
- .env files
- raw exports from SAP or company systems
- personal documents
- PDFs with sensitive metadata
