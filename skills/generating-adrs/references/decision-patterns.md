# Decision Patterns

How to identify architectural decisions in PRDs/TRDs.

## Decision Types

### 1. Architecture Decisions

**Signals in PRD:**
- "Architecture" section or ASCII diagram
- Service/component interaction patterns
- "async vs sync", "queue vs direct"
- Monolith vs microservice boundaries
- Data flow arrows (→, ▼)

**Examples:**
```
"Loyalty Service → NSQ Queue → Runner Service"
"Uses NSQ queue for async processing"
"Runner queries database directly (no Bridge API call)"
```

**ADR Focus:** Why this architecture? What latency/reliability tradeoffs?

### 2. Data Model Decisions

**Signals in PRD:**
- "Key Design Decision" subsections
- New tables/collections
- Field additions with rationale
- "Criteria come from X, NOT from Y"
- Schema diagrams

**Examples:**
```
"Criteria come from the parent Reward, NOT from config-level"
"Unique index on (ConfigId, transactionId)"
"isRelationshipBonusOnly flag on Reward model"
```

**ADR Focus:** Why this schema? What normalization tradeoffs?

### 3. API Design Decisions

**Signals in PRD:**
- Endpoint structure choices
- "Internal API" vs "External API"
- Auth patterns mentioned
- Request/response format choices
- Worker type choices

**Examples:**
```
"Internal API, no external auth required"
"Worker type: 'single' - bypasses Worker-Extractor"
"POST /loyalties/relationship-bonus/process"
```

**ADR Focus:** Why this interface? What security/simplicity tradeoffs?

### 4. Technology Selection

**Signals in PRD:**
- Framework/library names
- "Uses Redis" / "Uses NSQ"
- Cache TTL values
- Explicit "chose X because"

**Examples:**
```
"Uses Redis cache (5 min TTL)"
"NSQ for message queue"
"Shared library instead of HTTP API"
```

**ADR Focus:** Why this technology? What alternatives existed?

### 5. Integration Patterns

**Signals in PRD:**
- Caching strategies with TTL
- Error handling approaches
- Retry patterns
- "Each X processed in own transaction"
- Circuit breaker mentions

**Examples:**
```
"Lineage data is cached in Redis for 5 minutes"
"Each config is processed in its own transaction"
"If one config fails, others still succeed"
```

**ADR Focus:** Why this pattern? What failure modes handled?

### 6. Business Logic Decisions

**Signals in PRD:**
- "Before/After" comparisons
- Trigger patterns
- Calculation methods
- State transitions
- "Once per X, not per Y"

**Examples:**
```
"Trigger - Once Per Transaction (Not Per Wallet Reward)"
"Percentage is based on transactionTotal, not reward value"
"recipientLevel must be LESS than triggerLevel"
```

**ADR Focus:** Why this rule? What business impact?

### 7. Reuse vs New Decisions (OFTEN MISSED)

**Signals in PRD:**
- "Hybrid approach"
- "Reuse existing X model"
- "Instead of creating new Y"
- "Thin wrapper around existing"
- Architecture comparison tables

**Examples:**
```
"Hybrid approach: Reuse existing Reward model"
"Thin wrapper linking group → Reward"
"Instead of 4 new tables, reuse existing Reward system"
```

**ADR Focus:** Why reuse vs build new? What coupling tradeoffs?

## Extraction Checklist

For each PRD, scan these locations:

- [ ] "Key Design Decisions" section
- [ ] "Confirmed Decisions" table
- [ ] "Architecture" section/diagram
- [ ] Data Model "Why" notes
- [ ] Business Logic "Before/After" comparisons
- [ ] API Contracts "Internal vs External" notes
- [ ] "Complexity Assessment" approach choice
- [ ] ASCII architecture diagrams
- [ ] Tables with "Decision" / "Choice" / "Rationale" columns

## Decision Significance

Create ADR when:
- Decision has architectural significance (affects >1 component)
- Trade-offs worth documenting (what was given up)
- May be questioned later (why did we do this?)
- Sets pattern for future work (precedent)

Skip ADR when:
- Implementation detail (function naming, local vars)
- Standard practice (use Joi for validation)
- No alternatives considered
- Single-component impact only

## Common Missed Decisions

Baseline testing revealed these are often overlooked:

| Type | Example | Why Missed |
|------|---------|------------|
| **Reuse patterns** | "Hybrid approach using existing Reward" | Seems like implementation detail |
| **Error isolation** | "Each config in own transaction" | Buried in business logic |
| **Internal APIs** | "No external auth, internal only" | Security decisions overlooked |
| **Calculation context** | "Use transactionTotal not rewardValue" | Seems like minor detail |

**Always check for these specifically.**
