# MADR Template

Based on [MADR 4.0.0](https://github.com/adr/madr) - Markdown Any Decision Records.

## Standard Template

```markdown
---
status: "{proposed | accepted | deprecated | superseded by ADR-XXXX}"
date: {YYYY-MM-DD}
---

# ADR-NNNN: {Short title summarizing problem and solution}

## Status

{proposed | accepted | deprecated | superseded by ADR-XXXX}

## Context and Problem Statement

{Describe the context and problem statement, e.g., in free form using two to three sentences. What forces are at play? What constraints exist?}

## Decision Drivers

- {Driver 1, e.g., "Deep hierarchies (50+ levels) add latency"}
- {Driver 2, e.g., "Transaction response must be fast"}
- ...

## Considered Options

1. {Option 1}
2. {Option 2}
3. {Option 3}

## Decision Outcome

Chosen option: "{Option X}", because {justification linking to decision drivers}.

### Consequences

- Good, because {positive consequence}
- Good, because {another positive consequence}
- Bad, because {negative consequence}
- Neutral, because {neutral consequence}

## More Information

{Links to PRD sections, related ADRs, implementation files}
```

## Minimal Template

For simpler decisions:

```markdown
# ADR-NNNN: {Short title}

## Status

{proposed | accepted | deprecated | superseded by ADR-XXXX}

## Context and Problem Statement

{Two to three sentences describing why this decision was needed.}

## Considered Options

1. {Option 1}
2. {Option 2}

## Decision Outcome

Chosen option: "{Option X}", because {justification}.

### Consequences

- Good, because {positive consequence}
- Bad, because {negative consequence}
```

## Section Requirements

| Section | Required | Notes |
|---------|----------|-------|
| Status | Yes | Must be one of: proposed, accepted, deprecated, superseded |
| Context and Problem Statement | Yes | WHY was decision needed |
| Decision Drivers | Recommended | Forces that influenced the choice |
| Considered Options | Yes | At least 2 options, including chosen |
| Decision Outcome | Yes | WHAT was decided and WHY |
| Consequences | Yes | Use "Good/Bad/Neutral, because" format |
| More Information | Optional | Links to related docs |

## Consequence Format

Always use structured format:
- `Good, because {specific positive impact}`
- `Bad, because {specific negative impact}`
- `Neutral, because {impact that is neither positive nor negative}`

Example:
```markdown
### Consequences

- Good, because transaction response time reduced from 3-6s to ~50ms
- Good, because bonus processing failures don't affect main transaction
- Bad, because adds operational complexity (queue monitoring)
- Neutral, because requires separate Runner service deployment
```

## Naming Convention

- File: `ADR-NNNN-kebab-case-title.md` (4-digit number)
- Title in file: `# ADR-NNNN: Title Case With Spaces`

Examples:
- `ADR-0001-use-async-queue-for-bonus-processing.md`
- `ADR-0002-trigger-once-per-transaction.md`
- `ADR-0003-percentage-based-on-transaction-total.md`
