# Baseline Test Results (WITHOUT Skill)

Date: 2025-12-27

## Summary

| Scenario | Expected | Agent Assessment | Gap |
|----------|----------|------------------|-----|
| 1: Obvious AI | Detect AI | Correctly detected | None |
| 2: AI-Assisted | Detect AI in docs | Correctly identified AI docs | None |
| 3: Clean Human | NOT AI | Correctly NOT flagged | None |
| 4: README/Metadata | Detect AI | **INCONCLUSIVE** | Major gap |

## Detailed Findings

### Scenario 1: Obvious AI Signals (TypeScript validation file)

**Agent Verdict:** "Almost Certainly AI-Generated" (95%+ confidence)

**Signals Caught:**
- Over-documented obvious operations
- Narrating comments ("First," "Here," "Now")
- Excessive JSDoc for simple functions
- Generic boilerplate file header
- Textbook-perfect structure
- High comment-to-code ratio (~50%)

**Signals Missed:** None - agent caught all major signals

**Notable Quote:**
> "A human developer would trust the reader to understand `const errors: string[] = []` without explanation."

---

### Scenario 2: AI-Assisted (Payments file with mixed signals)

**Agent Verdict:** "High probability of AI involvement, specifically in the JSDoc documentation block"

**Signals Caught:**
- JSDoc block is anomalous and misplaced
- Style inconsistency (casual code vs formal docs)
- Git history shows documentation added separately
- Parameter mismatch in docs vs code
- Correctly identified human sections (TODO, FIXME, "grabbed from SO")

**Signals Missed:** None - excellent detection of AI-assisted pattern

**Notable Quote:**
> "The contractor likely wrote the code themselves, then used AI to 'add documentation.'"

---

### Scenario 3: Clean Human Code (EventEmitter)

**Agent Verdict:** "Inconclusive - Cannot determine AI authorship with confidence"

**Correct Assessment:** Agent correctly avoided false positive

**Key Reasoning:**
- "Clean, idiomatic code for well-defined problems looks the same regardless of who writes it"
- Identified that no AI-typical markers present (no excessive comments, no over-documentation)
- Raised ethical concern about penalizing competence

**Notable Quote:**
> "If this submission is being scrutinized because it's 'too clean' or 'too similar to AI output,' that's a concerning standard."

---

### Scenario 4: README and Commit Patterns **[MAJOR GAP]**

**Agent Verdict:** "Insufficient evidence to determine AI involvement"

**THIS IS THE KEY FAILURE - Agent should have detected:**

1. **Uniform commit message pattern** - All commits follow "Add X" format:
   - "Add user authentication with JWT tokens"
   - "Add password recovery functionality"
   - "Add OAuth2 integration for Google and GitHub"
   - "Add rate limiting middleware"
   - etc.

   This mechanical uniformity is a strong AI signal.

2. **Template README structure** - Follows exact Claude/GPT README template:
   - Overview → Features → Installation → API Endpoints → Environment Variables
   - Perfect markdown tables
   - No personality or project-specific quirks

3. **Suspiciously complete documentation** - Full docs before any iteration

**What Agent Said:**
> "The uniformity and polish could suggest AI assistance, but equally could reflect an experienced developer"

**Gap:** Agent lacked systematic framework for metadata analysis. Treated uniform commit messages and template READMEs as equally likely to be human or AI.

---

## Gaps to Address in Skill

### 1. No Systematic Framework
Agents approached each scenario ad-hoc. Need tiered signal detection:
- Tier 1: Metadata (highest confidence)
- Tier 2: Comment patterns
- Tier 3: Code structure
- Tier 4: Anti-signals (what humans do, AI doesn't)

### 2. Metadata Analysis is Weak
Scenario 4 should have been HIGH CONFIDENCE AI detection based on:
- Commit message uniformity
- README template structure
- Documentation completeness

Agent treated these as ambiguous when they're actually strong signals.

### 3. Missing Specific Patterns
Need to explicitly list:
- Common AI commit message patterns ("Add X functionality", "Implement Y")
- README template structures (Claude/GPT specific)
- Co-Authored-By header detection
- Generated code footers

### 4. Confidence Scoring Needed
Agent confidence was inconsistent:
- Scenario 1: "95%+ confidence" ✓
- Scenario 4: "Insufficient evidence" ✗ (should have been high)

Need explicit scoring guidance.

---

## What Agents Did Well

1. **Caught obvious comment patterns** - "First, we...", "Here we...", "Now we..."
2. **Avoided false positives** - Correctly handled clean human code
3. **Identified AI-assisted patterns** - Mixed quality detection was excellent
4. **Good reasoning** - Understood why clean code ≠ AI code
5. **Ethical considerations** - Raised concern about penalizing competence
