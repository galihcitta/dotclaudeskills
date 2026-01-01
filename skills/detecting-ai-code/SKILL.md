---
name: detecting-ai-code
description: Use when auditing code for AI authorship, reviewing acquisitions/contractors, verifying academic integrity, or during code review - provides systematic tiered framework for detecting fully AI-generated AND AI-assisted code patterns with confidence scoring
---

# Detecting AI-Generated Code

## Overview

Systematic framework for detecting AI-generated and AI-assisted code. Uses tiered signal detection with confidence scoring.

**Core principle:** Check metadata FIRST (highest confidence), then comments, then code patterns. Multiple signals compound confidence.

## Detection Framework (Check in Order)

### Tier 1: Metadata Signals (Highest Confidence)

**ALWAYS CHECK THESE FIRST - they're definitive.**

| Signal | What to Look For | Confidence |
|--------|------------------|------------|
| Git headers | `Co-Authored-By: Claude`, `Co-Authored-By: GitHub Copilot` | Definitive |
| Commit patterns | Uniform "Add X functionality" pattern across all commits | High |
| Generated footers | "Generated with [Claude Code]", "Created by Copilot" | Definitive |
| Config files | `.cursorrules`, `CLAUDE.md` in repo | High |
| README template | Exact Claude/GPT README structure (see below) | High |

**AI README Template Pattern:**
```
# Project Name
## Overview
[Formal description]
## Features
- Feature 1
- Feature 2
## Installation
[Perfect instructions]
## API Endpoints (table)
## Environment Variables (table)
## Contributing
## License
```

If README follows this EXACT structure with perfect tables and no personality → High AI probability.

**AI Commit Message Patterns:**
```
Add user authentication with JWT tokens
Add password recovery functionality
Add comprehensive documentation      ← "comprehensive" is strong AI tell
Implement feature X
Update component Y
Fix bug in Z
```

Mechanical uniformity + "Add/Implement/Update/Fix" pattern → AI signal.

**Human commit patterns (for contrast):**
```
wip: payments
fix typo in readme
initial payment setup
refactor auth - cleanup
oops forgot the tests
```

### Tier 2: Comment Patterns (High Confidence)

| Signal | Example | Confidence |
|--------|---------|------------|
| Narrating comments | "First, we...", "Here we...", "Now we..." | High |
| Restating code | `// Initialize array` above `const arr = []` | High |
| Tutorial style | "This function will...", "Let me explain..." | High |
| Perfect grammar | No typos, formal English in all comments | Medium |
| Over-documentation | 20-line JSDoc for 5-line function | High |

**Verbatim AI Phrases:**
- "This file contains..."
- "This function handles..."
- "Here we define..."
- "Now we check..."
- "Finally, we return..."

### Tier 3: Code Structure (Medium Confidence)

| Signal | Example | Confidence |
|--------|---------|------------|
| Over-engineering | Comprehensive error handling for impossible cases | Medium |
| Template repetition | Same pattern copied across files exactly | Medium |
| Perfect consistency | Identical formatting across entire codebase | Low-Medium |
| Defensive coding | Null checks on values that can't be null | Medium |

**Important:** Clean code alone is NOT evidence of AI. Experienced developers also write clean code.

### Tier 4: Anti-Signals (What Humans Do, AI Doesn't)

These DECREASE AI probability:

| Human Signal | Why |
|--------------|-----|
| TODO/FIXME comments | AI rarely leaves work incomplete |
| Debug code left in | `console.log`, commented code |
| Shortcuts/abbreviations | `amt`, `curr`, `intl` instead of full words |
| Domain jargon | Industry-specific terms, internal naming |
| Stack Overflow attribution | "grabbed from SO", "copied from [link]" |
| Inconsistent formatting | Mixed styles within file |
| Pragmatic compromises | "prod will have proper checks" |

## Confidence Scoring

| Signals Found | Confidence Level | Recommendation |
|---------------|------------------|----------------|
| 1 Tier-1 signal | High | Flag for review |
| 2+ Tier-2 signals | High | Likely AI-generated |
| Tier-2 + Tier-3 combined | Medium-High | Probably AI-assisted |
| Only Tier-3 signals | Low-Medium | Investigate more |
| Anti-signals present | Reduces confidence | Human likely involved |

**Compound scoring:** Multiple signals from different tiers = higher confidence than multiple signals from same tier.

## AI-Assisted Detection (Partial AI Use)

Look for:
- **Style jumps** - Casual code with formal JSDoc blocks
- **Git history jumps** - "Add comprehensive documentation" as separate commit
- **Quality inconsistency** - Some files over-documented, others bare
- **Misplaced docs** - JSDoc on library calls, not wrapper functions
- **Parameter mismatches** - Docs describe different params than code has

This pattern: Human wrote code → Asked AI to add documentation.

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| "Clean code = AI" | Experienced developers write clean code too |
| Only checking code | Metadata is highest-confidence signal |
| Missing git history | "Add comprehensive documentation" commits reveal AI use |
| Binary thinking | AI-assisted is different from fully AI-generated |
| Single signal certainty | Compound multiple signals before concluding |

## Quick Reference Workflow

1. **Check git log** - Look for Co-Authored-By, uniform commit patterns
2. **Check README** - Template structure? Perfect tables? No personality?
3. **Check file headers** - Generated footers? "This file contains..." comments?
4. **Check code comments** - Narrating style? Over-documentation?
5. **Check for anti-signals** - TODOs? Shortcuts? Debug code?
6. **Score confidence** - Compound signals from multiple tiers
7. **Report with evidence** - List specific signals found

## When NOT to Flag

- Clean, well-written code (without other signals)
- Standard patterns for solved problems (EventEmitter, validators)
- Good documentation (if style matches rest of codebase)
- Experienced developer output

**Clean code without Tier-1 or Tier-2 signals = insufficient evidence.**
