# Extraction Examples

Before/after examples showing PRD → ADR transformation.

## Example 1: Architecture Decision

### PRD Input

From `relationship-reward-system/README.md`:

```
## Architecture

Loyalty Service → NSQ Queue → Runner Service

POST /transactions
       │
       ▼
Publish ONCE per transaction  ──────►    RelationshipBonus topic
  {                                              │
    distributionId,                              │
    transactionId,                               ▼
    transactionTotal                      relationship-bonus.js
  }                                              │
       │                                         ├── Fetch lineage
       ▼                                         ▼
Return to Bridge                          Call Loyalty API
(fast response)
```

### ADR Output

```markdown
---
status: accepted
date: 2025-12-18
---

# ADR-0001: Use Async Queue Processing for Relationship Bonuses

## Status

Accepted

## Context and Problem Statement

When a member makes a transaction, we need to distribute relationship bonuses to their parent members. The hierarchy can be 50+ levels deep. Inline processing would add 3-6 seconds to transaction response time, unacceptable for checkout flow.

## Decision Drivers

- Transaction response must be fast (<500ms)
- Hierarchy depth can exceed 50 levels
- Bonus processing failures should not affect main transaction
- Need audit trail for all bonus attempts

## Considered Options

1. Synchronous inline processing during transaction
2. Asynchronous queue processing via NSQ
3. Scheduled batch processing

## Decision Outcome

Chosen option: "Asynchronous queue processing via NSQ", because it decouples bonus processing from transaction flow, ensuring fast responses while handling deep hierarchies.

### Consequences

- Good, because transaction response reduced from 3-6s to ~50ms (publish time only)
- Good, because bonus failures don't rollback transactions
- Good, because Runner can process at own pace with retries
- Bad, because bonus distribution has eventual consistency
- Bad, because adds NSQ infrastructure dependency
- Neutral, because requires separate Runner service monitoring

## More Information

See architecture diagram in README.md
```

## Example 2: Reuse Decision (OFTEN MISSED)

### PRD Input

From `relationship-reward-system/README.md`:

```
## Architecture: Hybrid Approach

┌─────────────────────────────────────────────────────────────────┐
│  RelationshipBonusConfig (NEW - thin wrapper)                   │
│  ├─ relationshipGroupId: 1                                      │
│  ├─ triggerLevel: 2        (child level that triggers)          │
│  ├─ recipientLevel: 0      (parent level that receives)         │
│  └─ RewardId: FK ──────────────────────────────────────────────┐│
└─────────────────────────────────────────────────────────────────┘│
                                                                   │
┌─────────────────────────────────────────────────────────────────┐│
│  Reward (EXISTING - 1 new field)                                ◄┘
│  ├─ rewardable: 'wallet' | 'item' | 'achievement' | 'external' │
│  ├─ isRelationshipBonusOnly: true  ◄── NEW FIELD                │
│  └─ Criteria: [...]   (existing criteria system)                │
└─────────────────────────────────────────────────────────────────┘

### Why Hybrid?
| Benefit | Description |
|---------|-------------|
| Reuses existing Reward system | wallet, item, achievement, external all work |
| Reuses existing Criteria system | same trigger conditions |
| Minimal new code | 2 tables instead of 4 |
```

### ADR Output

```markdown
---
status: accepted
date: 2025-12-18
---

# ADR-0002: Reuse Existing Reward Model with Thin Wrapper

## Status

Accepted

## Context and Problem Statement

Relationship bonus distribution needs to support multiple reward types (wallet, item, achievement, external) with configurable eligibility criteria. We could build a complete parallel system or leverage existing Reward infrastructure.

## Decision Drivers

- Need to support all existing reward types
- Need criteria-based eligibility (same as regular rewards)
- Minimize new code and maintenance burden
- Maintain consistent admin experience

## Considered Options

1. Full parallel system: 4 new tables (Config, Criteria, Transaction, Audit)
2. Hybrid approach: Thin wrapper referencing existing Reward model
3. Extend existing Reward with relationship fields directly

## Decision Outcome

Chosen option: "Hybrid approach with thin wrapper", because it reuses battle-tested Reward and Criteria systems while adding only relationship-specific configuration.

### Consequences

- Good, because all existing reward types work automatically
- Good, because existing Criteria system handles eligibility
- Good, because 2 new tables instead of 4
- Good, because consistent admin UX for reward configuration
- Bad, because tighter coupling to Reward model changes
- Bad, because RelationshipBonusConfig cannot exist without parent Reward
- Neutral, because requires `isRelationshipBonusOnly` flag to filter from normal flow

## More Information

See "Why Hybrid?" table in README.md
```

## Example 3: Business Logic Decision

### PRD Input

From `relationship-reward-system/business-logic.md`:

```
## BR-002: Trigger - Once Per Transaction

**Key Change**: Bonus is triggered once per transaction, not per wallet reward.

This allows:
- Multiple RelationshipBonusConfigs (from different Rewards) to be evaluated
- Each config's Reward.Criteria determines if bonus is distributed
- Parent can receive multiple rewards from a single transaction

Transaction: type='purchase', total=150000
    ↓
Publish ONCE with transactionTotal=150000
    ↓
Manager finds all matching configs:
  ├── Config A (Reward A criteria: type='purchase') ✓ → distribute
  └── Config B (Reward B criteria: total>100000) ✓ → distribute
    ↓
Parent receives BOTH rewards
```

### ADR Output

```markdown
---
status: accepted
date: 2025-12-18
---

# ADR-0003: Trigger Bonus Once Per Transaction

## Status

Accepted

## Context and Problem Statement

When a transaction occurs, we need to decide when to trigger bonus evaluation. Initially considered triggering for each wallet reward earned, which could create multiple queue messages per transaction.

## Decision Drivers

- Transaction may match multiple bonus configurations
- Each config has different Criteria from its Reward
- Parent should receive all applicable bonuses
- Minimize redundant queue messages

## Considered Options

1. Trigger per wallet reward earned
2. Trigger once per transaction with full transaction data

## Decision Outcome

Chosen option: "Trigger once per transaction", because it enables evaluation of all applicable bonus configurations while minimizing queue messages.

### Consequences

- Good, because single queue message per transaction
- Good, because all matching configs evaluated with same context
- Good, because parent receives all applicable bonuses
- Bad, because runner must handle multiple config evaluations
- Neutral, because percentage calculations use transactionTotal consistently

## More Information

See BR-002 in business-logic.md
```

## Example 4: From Confirmed Decisions Table

### PRD Input

From `fraud-transaction-checker/README.md`:

```
## Confirmed Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| First Run Behavior | Alert if current > 0 | Treat zero baseline as anomaly |
| Timezone | Jakarta (UTC+7) | Matches business hours |
| Worker Type | `type: 'single'` | Runner queries DB directly |
```

### ADR Output

```markdown
---
status: accepted
date: 2025-12-29
---

# ADR-0001: Fraud Checker Configuration Decisions

## Status

Accepted

## Context and Problem Statement

The fraud transaction checker needed several configuration decisions before implementation, including how to handle first-run scenarios, timezone selection, and worker architecture.

## Decision Drivers

- Must handle merchants with no historical data
- Should align with business operating hours
- Runner needs direct database access for queries

## Considered Options

### First Run Behavior
1. Skip alerting when no baseline exists
2. Alert if current > 0 with zero baseline

### Timezone
1. UTC
2. Jakarta (UTC+7)

### Worker Type
1. Standard Worker-Extractor pipeline
2. Direct `type: 'single'` with database queries

## Decision Outcome

- First Run: "Alert if current > 0" - treats zero baseline as potential anomaly
- Timezone: "Jakarta (UTC+7)" - matches business operating hours
- Worker: "`type: 'single'`" - Runner queries database directly, no extraction needed

### Consequences

- Good, because no missed anomalies on day one
- Good, because alerts align with business hours
- Good, because simpler architecture (no Worker-Extractor)
- Bad, because may generate false positives on first day
- Neutral, because adds scheduled job infrastructure

## More Information

See Confirmed Decisions table in README.md
```

## Extraction Pattern Summary

| PRD Pattern | ADR Extraction |
|-------------|----------------|
| ASCII architecture diagram | Architecture decision with component rationale |
| "Why X?" benefit table | Reuse/design decision with tradeoffs |
| "Before/After" comparison | Business logic decision |
| "Confirmed Decisions" table | Multiple decisions, can group or separate |
| "Key Design Decision" section | Data model or integration decision |
