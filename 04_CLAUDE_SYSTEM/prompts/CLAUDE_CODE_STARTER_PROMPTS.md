# CLAUDE_CODE_STARTER_PROMPTS.md

## First Audit Prompt

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

## README Upgrade Prompt

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

## Privacy Review Prompt

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

## Final Release Review Prompt

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
