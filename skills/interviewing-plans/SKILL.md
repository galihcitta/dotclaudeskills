---
name: interviewing-plans
description: Use when a plan, PRD, or spec has vague requirements, undefined terms, or missing details - conducts structured interview using AskUserQuestion to surface hidden assumptions, challenge ambiguities, and produce implementation-ready specs. Also use proactively when encountering plans that say things like "make it faster" or "improve UX" without concrete definitions.
---

# Interviewing Plans

## Overview

Plans fail because of hidden assumptions, not missing features. This skill systematically interviews stakeholders to surface ambiguities before they become bugs.

**Core principle:** Every vague term is a bug waiting to happen. "Make it faster" means nothing until someone says "reduce P95 latency from 800ms to 200ms."

## When to Use

**Trigger conditions:**
- User invokes `/interview-plan <file>`
- Plan contains undefined qualitative terms ("better", "faster", "modern", "relevant")
- Requirements reference external artifacts without links ("design has mockups")
- Technical approach lacks specifics ("add caching", "use React")
- Timeline exists without milestone breakdown
- User complaints mentioned without specific pain points

**Do NOT use for:**
- Already-detailed specs with concrete acceptance criteria
- Simple bug fixes with clear reproduction steps
- Tasks where user explicitly wants implementation, not planning

## Required Categories

Interview is NOT complete until ALL categories are covered:

| Category | Must Surface |
|----------|--------------|
| **Technical** | Architecture decisions, data flow, state management, API contracts |
| **UX/Design** | User flows, states (loading/empty/error), mobile strategy, accessibility |
| **Tradeoffs** | What are we NOT doing? What's MVP vs future? What's negotiable? |
| **Edge Cases** | High-volume users, empty states, failure modes, concurrent access |
| **Security** | Auth/authz, data exposure, input validation, audit requirements |
| **Testing** | How do we know it works? Unit/integration/E2E split, test data |
| **Rollback** | What if it fails in prod? Feature flags? Parallel running? |
| **Dependencies** | Who owns what? What's blocking? Who approves? |

## Interview Protocol

### 1. Read and Analyze

Read the plan file. For each section, identify:
- **Undefined terms**: Words that mean different things to different people
- **Missing specifics**: Numbers, formats, thresholds not specified
- **Assumed context**: References to things not in the document
- **Hidden dependencies**: Things that must be true for the plan to work

### 2. Ask in Batches by Topic

Use `AskUserQuestion` with 2-4 related questions per batch. Group by category.

**Before each batch, state your reasoning:**
```
I notice the plan says "[quote]" but doesn't specify [gap].
This matters because [consequence if undefined].
```

### 3. Challenge Vague Answers

When user gives a deflecting or vague answer:

| User Says | You Respond |
|-----------|-------------|
| "We'll figure it out later" | "What specifically needs to be true before we can figure it out? Who decides?" |
| "It should be fast enough" | "What's the current latency? What would make you say 'this is too slow'?" |
| "Standard approach" | "Which standard? Can you point to an example in this codebase?" |
| "Design will handle that" | "Has design delivered this? If not, when? What's our fallback?" |
| "Users will understand" | "Which users? Have we tested this assumption? What's the support cost if wrong?" |
| "I trust you to figure it out" | "My job is to surface gaps, not make assumptions. What would happen if I guess wrong on [specific item]?" |
| "We're running out of time" | "I can compress into 2 more batches. But skipping categories means shipping bugs. Which risks do you want documented as 'owner: you'?" |
| "Just start building" | "Building with gaps means rework. 5 more minutes now saves days later. What's the real constraint - time or energy?" |

**Never accept:**
- Qualitative terms without quantitative definitions
- Future tense without owners and dates
- References to artifacts without links or locations
- "Someone" instead of a specific name/team

### 4. Probe for Non-Obvious Gaps

**Obvious questions** (avoid these as primary questions):
- "What are the requirements?"
- "What's the timeline?"
- "Who's the user?"

**Non-obvious questions** (these surface real gaps):
- "What happens to in-flight requests during deployment?"
- "If this succeeds beyond expectations, what breaks first?"
- "What's the most expensive assumption we're making?"
- "Which part of this plan are you least confident about?"
- "What would make you cancel this project tomorrow?"
- "Who will be upset when this ships, and why?"
- "What's the first thing users will try that we haven't designed for?"

### 5. Track Coverage

Maintain mental checklist. After each batch, assess:
- [ ] Technical architecture clear?
- [ ] UX states defined?
- [ ] Tradeoffs explicit?
- [ ] Edge cases identified?
- [ ] Security considered?
- [ ] Testing strategy exists?
- [ ] Rollback plan defined?
- [ ] Dependencies confirmed?

## Handling Time Pressure

When stakeholder is impatient:

**Compress, don't skip.** Combine remaining categories into 1-2 dense batches. Never skip a category entirely.

**Make risk explicit.** If they insist on skipping: "I'll document [Security: TBD, Owner: @you] in the spec. You're accepting this risk."

**Name the tradeoff.** "5 more minutes now, or 2 days of rework when we discover [gap] in production. Your call."

**Never rationalize:**
- "They know their business" - They don't know what they haven't thought about
- "I can figure it out" - Your assumptions are bugs waiting to happen
- "They seem confident" - Confidence is not evidence of completeness
- "I'm being annoying" - Surfacing gaps IS the job

## Completion Criteria

Interview is complete when:

1. **All vague terms operationalized** - Every qualitative word has a number or concrete definition
2. **All categories covered** - Checklist above is complete
3. **No deflections remaining** - All "we'll figure it out" answers have been challenged and resolved
4. **Dependencies confirmed** - External people/teams/artifacts are named and accessible
5. **You cannot find more gaps** - Genuinely exhausted questioning, not just tired of asking

## Output Format

When interview is complete, write structured spec:

```markdown
# [Project Name] - Implementation Spec

## Overview
[1-2 sentences: what this is and why it matters]

## Success Criteria
- [ ] [Measurable criterion with number]
- [ ] [Measurable criterion with number]

## Technical Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| [Area] | [What we're doing] | [Why, including rejected alternatives] |

## User Experience
### Happy Path
[Step by step flow]

### Edge Cases
| Scenario | Behavior |
|----------|----------|
| [Case] | [What happens] |

### Error States
| Error | User Sees | Recovery |
|-------|-----------|----------|
| [Type] | [Message/UI] | [How to fix] |

## Security Considerations
- [Item with mitigation]

## Testing Strategy
- **Unit**: [What's covered]
- **Integration**: [What's covered]
- **E2E**: [Critical paths]

## Rollback Plan
[How we undo this if it fails]

## Open Questions
- [ ] [Anything still unresolved, with owner]

## Dependencies
| Dependency | Owner | Status |
|------------|-------|--------|
| [Thing] | [Person/team] | [Confirmed/Pending/Blocked] |
```

## Red Flags - Dig Deeper

When you hear these, the interview is NOT done:

- "That's a good question, we should think about that"
- "I'm not sure, but probably..."
- "The other team handles that"
- "We've always done it this way"
- "That won't happen" (about edge cases)
- "We'll add that later"
- "It's just like [other project]" (without specifics)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Accepting first answer | Always ask "why?" at least once |
| Asking obvious questions | Lead with non-obvious probes |
| Moving on when stuck | Challenge deflections explicitly |
| Single questions | Batch 2-4 by topic |
| Not showing reasoning | Explain why each question matters |
| Stopping when tired | Check completion criteria, not energy level |
