---
name: generating-adrs
description: Use when PRD/TRD contains architectural decisions to document - extracts decisions from refined requirements (architecture choices, data model decisions, API patterns, technology selections, integration strategies, reuse patterns) and generates MADR-format ADRs. One ADR per decision point. Also use when asked to document decisions, create decision records, or retrospectively capture architectural choices.
---

# Generating ADRs

Extract architectural decisions from PRDs/TRDs and generate MADR (Markdown Any Decision Record) format ADR documents.

## When to Use

- PRD/TRD contains architectural choices to document
- User asks to "document decisions" or "create ADRs"
- Retrospectively capturing decisions from existing requirements
- Before implementation to formalize choices
- After implementation to document what was decided and why

## When NOT to Use

- Simple bug fixes with no architectural impact
- Requirements without design decisions
- Already-documented decisions (check existing ADRs first)

## Workflow

### Phase 0: Locate PRD and Existing ADRs

**Step 1: Find the source PRD/TRD**

Read the PRD directory or file provided by user.

**Step 2: Check for existing ADRs**

```bash
# Look for existing ADR directory at project level
ls -la <project>/adrs/ <project>/docs/adrs/ 2>/dev/null
```

If ADRs exist, determine next sequence number. If not, start at 0001.

**Step 3: Determine output location**

ADRs go in `<project>/adrs/` directory (project level, NOT inside PRD folder).

Example: PRD at `/Works/tada/bridge/agent-workflow/requirements/` → ADRs at `/Works/tada/bridge/adrs/`

### Phase 1: Identify Decision Points

Scan PRD for decision patterns. See `references/decision-patterns.md` for full taxonomy.

**Decision Types to Extract:**

| Type | Signals | Often Missed? |
|------|---------|---------------|
| Architecture | ASCII diagrams, "→", "async vs sync" | No |
| Data Model | "Key Design Decision", schema diagrams | No |
| API Design | "Internal API", auth patterns | Yes |
| Technology | "Uses Redis", TTL values | No |
| Integration | "Each X in own transaction", retry patterns | Yes |
| Business Logic | "Before/After", "Once per X not Y" | No |
| **Reuse Patterns** | "Hybrid approach", "Reuse existing" | **Yes** |

**Critical: Check for commonly missed decisions:**
- [ ] Reuse vs build-new decisions ("hybrid approach", "thin wrapper")
- [ ] Error isolation patterns ("each config in own transaction")
- [ ] Internal vs external API decisions
- [ ] Calculation context decisions (what value is used as base)

### Phase 2: Determine ADR Scope

For each decision, assess if it warrants own ADR:

**Create separate ADR when:**
- Affects multiple components
- Involves documented trade-offs
- May be questioned later
- Sets precedent for future work

**Combine into single ADR when:**
- Decisions tightly coupled
- Same rationale drives multiple choices
- From "Confirmed Decisions" table (can group)

**Skip ADR when:**
- Implementation detail only
- Standard practice with no alternatives
- Single-component impact

### Phase 3: Generate ADRs

Use MADR format from `references/madr-template.md`.

**Required sections (baseline test showed these are often missing):**

```markdown
---
status: accepted
date: YYYY-MM-DD
---

# ADR-NNNN: Title

## Status
{proposed | accepted | deprecated | superseded by ADR-XXXX}

## Context and Problem Statement
{WHY was this decision needed - 2-3 sentences}

## Decision Drivers
- {Driver 1}
- {Driver 2}

## Considered Options
1. {Option 1}
2. {Option 2}

## Decision Outcome
Chosen option: "{Option X}", because {justification}.

### Consequences
- Good, because {positive impact}
- Bad, because {negative impact}
- Neutral, because {neutral impact}
```

**Consequence format is critical - always use:**
- `Good, because {specific positive}`
- `Bad, because {specific negative}`
- `Neutral, because {neither positive nor negative}`

### Phase 4: Create Index

Generate `adrs/README.md`:

```markdown
# Architecture Decision Records

| ID | Title | Status | Date |
|----|-------|--------|------|
| [ADR-0001](ADR-0001-decision-title.md) | Decision Title | Accepted | YYYY-MM-DD |
| [ADR-0002](ADR-0002-another-decision.md) | Another Decision | Accepted | YYYY-MM-DD |
```

### Phase 5: Save Output

**Directory structure:**
```
<project>/adrs/
    README.md                              # Index
    ADR-0001-first-decision.md
    ADR-0002-second-decision.md
```

**Naming convention:**
- 4-digit sequence: `ADR-0001` not `ADR-001`
- Kebab-case: `ADR-0001-use-async-queue.md`
- Title in file: `# ADR-0001: Use Async Queue`

## Quick Reference

| Aspect | Correct | Incorrect |
|--------|---------|-----------|
| Location | `<project>/adrs/` | `<prd-folder>/adr/` |
| Numbering | `ADR-0001` (4 digits) | `ADR-001` (3 digits) |
| Consequences | `Good, because...` | Free-form text |
| Frontmatter | Include `status`, `date` | None |
| Options | At least 2 listed | Only chosen option |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing "Considered Options" | Always list 2+ options, even if one was obvious |
| Free-form consequences | Use "Good/Bad/Neutral, because" format |
| Missing reuse decisions | Check for "hybrid", "reuse", "thin wrapper" |
| ADRs in PRD folder | Put at project level `<project>/adrs/` |
| 3-digit numbering | Use 4 digits: `ADR-0001` |
| Missing context | Explain WHY decision was needed, not just what |

## Anti-Patterns

1. **Missing alternatives** - Always document what was NOT chosen
2. **Vague context** - Be specific about forces and constraints
3. **No negative consequences** - Every decision has trade-offs
4. **Wrong location** - ADRs at project level, not inside PRD
5. **Skipping reuse decisions** - "Hybrid approach" is architectural

## See Also

- `references/madr-template.md` - Full and minimal templates
- `references/decision-patterns.md` - How to identify decisions
- `references/extraction-examples.md` - PRD → ADR transformations
