# Interview Patterns Reference

Non-obvious question templates for deep-dive requirements interviews using `AskUserQuestion`.

## Core Principle

**Surface questions** ask WHAT is being built.
**Deep questions** ask WHAT HAPPENS WHEN things go wrong, scale, or hit edge cases.

Never ask:
- "What database will you use?" (obvious, they'll tell you)
- "What's the endpoint name?" (implementation detail)
- "What fields do you need?" (they'll specify)

Always ask:
- "What happens when X fails/times out/conflicts?"
- "How does this behave under Y constraint?"
- "Who else is affected by Z?"

---

## Question Categories

### 1. Technical Edge Cases

**Failure & Recovery:**
```
- "If [external service] is down for 30+ seconds, what should the user see?"
- "If the user closes the browser mid-transaction, what state do they see when they return?"
- "What's the rollback strategy if deployment fails mid-migration?"
- "If this API call fails 3 times, do we retry, fail silently, or escalate?"
- "What happens to in-flight requests during a deployment?"
```

**Concurrency & Race Conditions:**
```
- "If two users update the same record simultaneously, which wins?"
- "Can this action be triggered multiple times by rapid clicking? What happens?"
- "If the backend processes faster than the UI updates, any issues?"
- "What happens if webhook retries arrive out of order?"
- "Can this operation be safely retried if it times out mid-way?"
```

**Scaling & Performance:**
```
- "If this gets 100x expected traffic tomorrow, what breaks first?"
- "What's the expected data volume in 6 months? 2 years?"
- "Are there any operations that get slower as data grows?"
- "What's the cache invalidation strategy?"
- "Any hot spots that could cause lock contention under load?"
```

**Data Integrity:**
```
- "If power cuts during this write, what's the worst case?"
- "Can this operation leave data in an inconsistent state?"
- "What's the recovery procedure if data gets corrupted?"
- "Are there any operations that should be atomic but aren't?"
```

### 2. User Experience Flows

**Loading & Waiting States:**
```
- "What should the user see during the 3-5 second wait?"
- "Is there a skeleton screen, spinner, or progress indicator?"
- "At what latency does this feel 'broken'? What do we show then?"
- "What's the experience on 3G mobile with 500ms latency?"
```

**Error Presentation:**
```
- "If validation fails on field 3 of 5, do we stop or show all errors?"
- "Should error messages be technical or user-friendly?"
- "What's the recovery path after an error? Retry button? Back to start?"
- "Are there errors that should be hidden from users but logged?"
```

**Multi-Platform:**
```
- "What's the mobile experience? Same, simplified, or different?"
- "Does this need to work offline? What's the degraded experience?"
- "Any tablet-specific considerations?"
- "What about accessibility - screen readers, keyboard navigation?"
```

**User Segments:**
```
- "How does an advanced user's flow differ from a new user?"
- "Are there admin-only views or actions?"
- "What about users with different permission levels?"
- "Any features that should be hidden until user reaches certain state?"
```

**Edge Interactions:**
```
- "What if user navigates away mid-flow? Warn, save draft, or lose progress?"
- "What happens if the user's session expires during this action?"
- "Can this be done in multiple browser tabs simultaneously?"
- "What if user hits back button in the middle of a multi-step flow?"
```

### 3. Data & Security

**PII & Sensitive Data:**
```
- "Who can see/access this data? Any PII concerns?"
- "Does this data need to be encrypted at rest?"
- "Should this appear in logs? What should be masked?"
- "What's the data retention policy? When does it get deleted?"
```

**Compliance & Legal:**
```
- "Are there compliance/legal implications for storing this?"
- "Does this need GDPR right-to-erasure support?"
- "If legal asks for a complete audit trail, can we provide it?"
- "Any industry-specific regulations (HIPAA, PCI, SOC2)?"
```

**Access Control:**
```
- "What happens if someone accesses this without permission?"
- "Should failed access attempts be logged/alerted?"
- "Can permissions be delegated? By whom?"
- "What about API key/token management for integrations?"
```

**Audit & Accountability:**
```
- "Do we need to track who changed what and when?"
- "Should changes be reversible? By whom?"
- "What's the process for investigating suspicious activity?"
- "Are there actions that require approval before execution?"
```

### 4. Business Logic

**Rule Conflicts:**
```
- "If two business rules conflict, which takes priority?"
- "Are there exceptions to these rules? Who can grant them?"
- "What if the user is in multiple categories with different rules?"
- "How do promotions/discounts stack? Cap? Exclusive?"
```

**State Transitions:**
```
- "What states can this entity be in? What transitions are valid?"
- "Can a state transition be reversed? Under what conditions?"
- "What triggers automatic state changes?"
- "Are there time-based state changes (expires after X)?"
```

**Edge Cases in Rules:**
```
- "What happens at exactly the boundary condition?"
- "What if the calculation results in negative/zero/infinity?"
- "Time zones - whose time zone matters for deadlines?"
- "What about leap years, daylight saving, date edge cases?"
```

**Dependencies & Ordering:**
```
- "Does this depend on another feature/service being completed first?"
- "What's the order of operations if multiple things trigger at once?"
- "Are there circular dependencies we need to handle?"
- "What happens if a dependency is removed after this is created?"
```

### 5. Operational Concerns

**Deployment & Rollout:**
```
- "Feature flag? Percentage rollout? Big bang?"
- "What's the rollback procedure if this goes wrong?"
- "Do we need a kill switch for emergencies?"
- "What about database migrations - reversible or not?"
```

**Monitoring & Alerting:**
```
- "What metrics indicate this feature is healthy?"
- "What error rate triggers an alert?"
- "What dashboards do we need?"
- "How do we know if this is performing as expected?"
```

**Support & Debugging:**
```
- "What info does support need to debug issues?"
- "Are there admin tools needed for manual intervention?"
- "What's the escalation path for edge cases?"
- "How do we handle data correction requests?"
```

### 6. Tradeoffs & Prioritization

**Scope:**
```
- "If we had to cut scope, which part is essential vs nice-to-have?"
- "What's the MVP vs the ideal implementation?"
- "Are there features we should explicitly NOT build?"
- "What's the iteration plan - what comes in v2?"
```

**Quality Attributes:**
```
- "Speed vs consistency - which matters more here?"
- "Simplicity vs flexibility - optimize for which?"
- "Security vs convenience - where's the line?"
- "Cost vs performance - any budget constraints?"
```

**Build vs Buy:**
```
- "Build custom vs use existing library/service?"
- "Managed service vs self-hosted?"
- "Perfect now vs good enough with iteration?"
- "Standard approach vs optimized for our specific case?"
```

---

## AskUserQuestion Construction

### Option Design

**Good options are:**
- Mutually exclusive (one clear choice)
- Specific (not vague like "depends")
- Actionable (leads to concrete decision)

**Example - Good:**
```
options: [
  { label: "Show all errors at once", description: "User sees complete list, can fix all at once" },
  { label: "Stop at first error", description: "Fix one at a time, simpler but slower" },
  { label: "Highlight inline as typed", description: "Real-time validation, immediate feedback" }
]
```

**Example - Bad:**
```
options: [
  { label: "Yes", description: "Do it" },
  { label: "No", description: "Don't do it" },
  { label: "Maybe", description: "It depends" }  // Useless
]
```

### Multi-Select Usage

Use `multiSelect: true` when:
- Selecting multiple features/options
- Choosing which edge cases to handle
- Picking platforms to support

Don't use when:
- Choices are mutually exclusive
- Need a single definitive answer

### Question Phrasing

**Specific > General:**
```
BAD:  "How should errors be handled?"
GOOD: "If the payment API returns a timeout after 30s, should we: retry, fail with message, or queue for later?"
```

**Scenario-based > Abstract:**
```
BAD:  "What about concurrency?"
GOOD: "If user A and user B both click 'submit' on the same order within 1 second, what happens?"
```

---

## Interview Anti-Patterns

### Questions to NEVER Ask

| Anti-Pattern | Why It's Bad | Better Alternative |
|--------------|--------------|-------------------|
| "What framework should we use?" | They'll specify, or you should know | Don't ask - detect from codebase |
| "What should the API return?" | Too low-level for interview | "What info does the caller need to proceed?" |
| "Is security important?" | Obviously yes | "What's the blast radius if auth is bypassed?" |
| "Should it be fast?" | Obviously yes | "What's acceptable latency? What's unacceptable?" |
| "Any other requirements?" | Too open-ended | Ask specific probing questions |

### Avoiding Leading Questions

```
BAD:  "Should we use JWT since it's the industry standard?"
GOOD: "What's your token strategy - stateless JWT, server-side sessions, or hybrid?"

BAD:  "We should cache this, right?"
GOOD: "What's the acceptable staleness for this data? Real-time, seconds, minutes?"
```

### Avoiding Premature Solutioning

```
BAD:  "Should we use Redis or Memcached for caching?"
GOOD: "What data needs to be fast to access? What's the access pattern?"

BAD:  "Should this be a microservice or part of the monolith?"
GOOD: "Does this need to scale independently from the rest of the system?"
```

---

## Interview Flow Patterns

### Opening Assessment

After reading PRD, ask yourself:
1. What's NOT specified that could go multiple ways?
2. What edge cases are not mentioned?
3. What integrations have undefined failure modes?
4. What user journeys have gaps?

### Progressive Depth

**Round 1:** High-impact architectural questions
**Round 2:** Edge cases and failure modes
**Round 3:** UX details and user segments
**Round 4:** Operational concerns and monitoring
**Round N:** Diminishing returns - offer to proceed

### Recognizing Completion

Stop interviewing when:
- Answers become "same as before" or "standard approach"
- User says "that's enough" or shows impatience
- Questions become increasingly hypothetical
- Core decisions are locked, only details remain

### Skip Offer

If PRD is already detailed, offer:
```
"Your requirements look comprehensive. Would you like to:
1. Proceed directly to spec generation
2. Quick sanity-check interview (5-10 questions)
3. Deep-dive interview (thorough exploration)"
```

---

## Domain-Specific Question Banks

### Payment/Financial Features
- "What happens if charge succeeds but our DB write fails?"
- "How do we handle partial refunds?"
- "What's the reconciliation process?"
- "Currency conversion - who bears the FX risk?"

### Authentication/Authorization
- "What happens to active sessions when password changes?"
- "How long before inactive sessions expire?"
- "Can users see their active sessions and revoke them?"
- "What's the account recovery flow if all auth methods are lost?"

### Notifications/Messaging
- "What if the user's notification preferences change mid-campaign?"
- "Rate limiting - how many notifications before it's spam?"
- "What's the retry policy for failed deliveries?"
- "How do we handle bounced emails/blocked numbers?"

### Data Import/Export
- "What's the max file size? What happens if exceeded?"
- "How do we handle malformed rows - skip, fail, or partial?"
- "Can imports be cancelled mid-way?"
- "What about duplicate detection?"

### Search/Filtering
- "What happens when search returns 10,000 results?"
- "How fresh does search index need to be?"
- "What about typos and fuzzy matching?"
- "Are there any fields that should NOT be searchable?"

### Integrations/Webhooks
- "What's our retry policy for failed webhook deliveries?"
- "How do we verify webhook authenticity?"
- "What if the external API changes their contract?"
- "How do we handle rate limits from the third party?"
