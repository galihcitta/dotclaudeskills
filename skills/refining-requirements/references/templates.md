# Templates

Copy and fill these templates based on requirement type.

## Contents

**Output Templates (use based on Phase 7a threshold):**
- [Single-File Output Template](#single-file-output-template) - For simple features (< 150 lines)
- [Multi-File Output Templates](#multi-file-output-templates) - For complex features (≥ 150 lines)

**Feature-Type Templates (section content reference):**
- [API Feature Template](#api-feature-template)
- [Data Model Template](#data-model-template)
- [Integration Template](#integration-template)
- [Auth Flow Template](#auth-flow-template)

---

## Choosing Output Format

Use **Phase 7a threshold** from SKILL.md to decide:

| Feature Complexity | Typical Output | Format |
|--------------------|----------------|--------|
| Simple (1-2 files, no API, no DB) | 50-100 lines | Single file |
| Medium (3-5 files, some API or DB) | 100-200 lines | Check triggers |
| Complex (6+ files, API + DB + external) | 200-400+ lines | Multi-file |

**Threshold:** < 150 lines = single file, ≥ 150 lines = multi-file

**Always multi-file:** Greenfield, multi-stack, 3+ endpoints, external integrations, or ANY TWO of (DB + API + UI).

**When uncertain:** Multi-file is always acceptable.

---

## Feature-Type Templates

These templates show section content for different feature types. Use them as reference for WHAT to include, then output in the appropriate format (single-file or multi-file).

### API Feature Template

```markdown
# [Feature Name]

## Scope
### In Scope
- [Endpoint descriptions]
### Out of Scope
- [Deferred work]

## Complexity Assessment
| Metric | Value |
|--------|-------|
| Files to create | |
| Files to modify | |
| New endpoints | |
| Database migrations | |
| External dependencies | |
| Estimated effort | S / M / L |
| Risk areas | |

## File Mappings
### Validation Summary
| Path | Status | Action |
|------|--------|--------|

### Create
- `path/controller.js` — Purpose
### Modify
- `path/routes.js` — Register routes
### Reference
- `path/similar.js` — Pattern to follow

## API Contracts

### [METHOD] /path/to/endpoint
- **Auth**: Required/Optional
- **Request**:
```json
{ "field": "type — required/optional, constraints" }
```
- **Response 200**:
```json
{ "field": "type — description" }
```
- **Response 4xx**: `{ "error": "condition" }`

## Business Logic
### [Rule Name]
- **Trigger**: When applies
- **Process**: Steps
- **Error Handling**: On failure

## Test Scenarios
### Happy Path
| # | Scenario | Input | Expected |
|---|----------|-------|----------|
| 1 | | | |

### Input Validation
| # | Scenario | Input | Expected |
|---|----------|-------|----------|
| 1 | | | |

### Error Handling
| # | Scenario | Trigger | Expected |
|---|----------|---------|----------|
| 1 | | | |

## Security Checklist
### Authentication
- [ ] Rate limiting
- [ ] Token expiry

### Data Protection
- [ ] Mask PII in logs
- [ ] Encrypt at rest

### Integration Security
- [ ] Validate signatures
- [ ] Timeout handling

(Mark N/A for non-applicable sections)

## UI Copy (Bilingual)
### [Screen Name]
| Key | Indonesian | English |
|-----|------------|---------|
| title | | |
| button | | |

### Error Messages
| Code | Indonesian | English |
|------|------------|---------|
| ERROR_CODE | | |

## Execution Checklist
1. [ ] Create files
2. [ ] Implement logic
3. [ ] Register routes
4. [ ] Write tests
5. [ ] Test endpoints
```

---

## Data Model Template

```markdown
# [Feature Name]

## Scope
### In Scope
- Field additions to [Table]
- New table [Name]
### Out of Scope
- Data migration

## Data Model Changes

### [Model] (`path/to/model.js`)
| Field | Type | Nullable | Default | Index | Description |
|-------|------|----------|---------|-------|-------------|
| field | STRING | No | null | Yes | Purpose |

### Relationships
- [A] hasMany [B] via `foreignKey`

## File Mappings
### Create
- `migrations/YYYYMMDD-desc.js` — Schema migration
### Modify
- `app/models/name.js` — Add fields

## Migration Pattern
```js
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.addColumn('Table', 'field', {
      type: Sequelize.TYPE,
      defaultValue: value,
      allowNull: false
    });
  },
  down: async (queryInterface) => {
    await queryInterface.removeColumn('Table', 'field');
  }
};
```

## Execution Checklist
1. [ ] Create migration
2. [ ] Update model
3. [ ] Run migration locally
4. [ ] Test rollback
```

---

## Integration Template

```markdown
# [Integration Name]

## Scope
### In Scope
- Receive webhooks from [System]
- Call [API] for [purpose]
### Out of Scope
- External system config

## External System
- **Provider**: Name
- **Auth**: API Key / OAuth / HMAC
- **Env Vars**: `API_KEY`, `WEBHOOK_SECRET`

## Inbound Webhook
### POST /webhooks/system/event
- **Signature**: `X-Signature` header, HMAC-SHA256
- **Payload**: `{ "event": "type", "data": {...} }`
- **Response**: 200 OK immediately, process async

## Outbound API
### POST https://api.external.com/resource
- **Auth**: Bearer token
- **Timeout**: 30s
- **Request/Response**: Define schemas

## File Mappings
### Create
- `controllers/webhooks/system.js` — Handler
- `services/external_client.js` — API client
### Modify
- `routes/webhooks.js` — Register route

## Execution Checklist
1. [ ] Create webhook endpoint
2. [ ] Implement signature validation
3. [ ] Create API client
4. [ ] Test with sample payloads
```

---

## Auth Flow Template

```markdown
# [Flow Name]

## Complexity Assessment
| Metric | Value |
|--------|-------|
| Files to create | |
| Files to modify | |
| New endpoints | |
| Session storage | Redis / DB |
| External dependencies | |
| Estimated effort | S / M / L |
| Risk areas | |

## Flow Overview
```
User → Initiate → [Session Created]
     → Verify → [Validated] or [Failed]
     → Complete → [Access Granted]
```

## Token Design
- **Type**: JWT / Opaque / HMAC-signed
- **Contains**: [claims]
- **Expiry**: [duration]
- **Storage**: Redis `prefix:{id}`

## API Contracts

### POST /flow/initiate
- **Request**: `{ identifier }`
- **Response**: `{ sessionToken, expiresAt }`

### POST /flow/verify  
- **Request**: `{ sessionToken, proof }`
- **Response**: `{ success, accessToken }` or `{ error }`

## State Transitions
| State | Event | Next | Side Effect |
|-------|-------|------|-------------|
| initiated | verify_ok | verified | Send confirmation |
| initiated | verify_fail | failed | Increment attempts |
| initiated | timeout | expired | Cleanup |

## Security
- Rate limit: X req/min
- Max attempts: N before lockout
- Constant-time comparison

## Security Checklist
### Authentication
- [ ] Token entropy: minimum 256 bits
- [ ] Token expiry: defined max lifetime
- [ ] Invalidate after use (if single-use)
- [ ] Constant-time comparison
- [ ] Rate limiting: X req/min
- [ ] Account lockout after N failures

### Data Protection
- [ ] Mask PII in logs
- [ ] Encrypt sensitive fields at rest

### Integration (if external)
- [ ] Validate webhook signatures
- [ ] Timeout handling
- [ ] Circuit breaker

## UI Copy (Bilingual)
### [Flow Screen]
| Key | Indonesian | English |
|-----|------------|---------|
| title | | |
| description | | |
| button_primary | | |

### Success Messages
| Key | Indonesian | English |
|-----|------------|---------|
| verified | | |

### Error Messages
| Code | Indonesian | English |
|------|------------|---------|
| INVALID_TOKEN | | |
| SESSION_EXPIRED | | |
| ACCOUNT_LOCKED | | |

## Test Scenarios
### Happy Path
| # | Scenario | Steps | Expected |
|---|----------|-------|----------|
| 1 | Full flow | initiate → verify → complete | Access granted |

### State Transitions
| # | Start State | Action | Expected End State |
|---|-------------|--------|-------------------|
| 1 | initiated | verify(correct) | verified |
| 2 | initiated | verify(wrong) | initiated, attempt++ |
| 3 | initiated (attempt=max) | verify(wrong) | failed, locked |
| 4 | initiated | timeout | expired |

### Security Tests
| # | Scenario | Attack | Expected |
|---|----------|--------|----------|
| 1 | Token tampering | Modify token payload | 400 invalid signature |
| 2 | Replay attack | Reuse completed token | 400 already used |
| 3 | Brute force | Rapid attempts | 429 rate limited |

## Execution Checklist
1. [ ] Create session storage
2. [ ] Implement initiate
3. [ ] Implement verify
4. [ ] Add rate limiting
5. [ ] Write tests for all state transitions
6. [ ] Test expiry/lockout
```

---

## Single-File Output Template

Use for simple features with < 150 lines of output.

**Save as:** `agent-workflow/requirements/YYYYMMDD-feature-name.md`

```markdown
---
title: [Feature Name]
created: [ISO timestamp]
status: draft | review | approved
stack: [detected stack]
type: feature | bugfix
original_prd: [filename if provided]
---

# [Feature Name]

## Scope
### In Scope
- Deliverable 1
- Deliverable 2
### Out of Scope
- What NOT to build

## File Mappings
| Path | Status | Action |
|------|--------|--------|
| path/to/file.js | ✓ EXISTS | Modify |
| path/to/new.js | ✗ CREATE | New file |

## Business Logic
### [Rule Name]
- **Trigger**: When this applies
- **Action**: What happens

## Test Scenarios
| # | Scenario | Input | Expected |
|---|----------|-------|----------|
| 1 | Happy path | {...} | 200, success |
| 2 | Invalid input | {...} | 400, error |

## Security Checklist
- [ ] Input validation
- [ ] Authentication required (if applicable)

## Execution Checklist
1. [ ] First step
2. [ ] Second step
3. [ ] Write tests
4. [ ] Verify

---
*Generated by requirements-refiner skill*
```

---

## Multi-File Output Templates

Use for complex features with ≥ 150 lines of output, greenfield projects, or multi-stack features.

### README.md Template

```markdown
---
title: [Feature Name]
created: [ISO timestamp]
status: draft | review | approved
stack: [detected stack]
type: feature | greenfield
original_prd: [filename if provided]
---

# [Feature Name]

## Overview
[2-3 sentence summary of what this feature does and why]

## Project Context
- **Stack**: [Auto-detected or specified]
- **Conventions**: [From CLAUDE.md]
- **Related patterns**: [Files read for reference]

## Complexity Assessment
| Metric | Value |
|--------|-------|
| Files to create | |
| Files to modify | |
| New endpoints | |
| Database migrations | |
| External dependencies | |
| Estimated effort | S / M / L |
| Risk areas | |

## Navigation
- [Scope](scope.md) — What's in/out of this feature
- [File Mappings](file-mappings.md) — Files to create/modify
- [API Contracts](api-contracts.md) — Endpoint definitions *(remove if N/A)*
- [Data Model](data-model.md) — Database changes *(remove if N/A)*
- [Business Logic](business-logic.md) — Rules and processes
- [Test Scenarios](test-scenarios.md) — Test cases
- [Security](security.md) — Security checklist
- [UI Copy](ui-copy.md) — User-facing text *(remove if N/A)*
- [Execution Checklist](execution-checklist.md) — Implementation steps

## Quick Start
1. Read [scope.md](scope.md) to understand boundaries
2. Review [file-mappings.md](file-mappings.md) for affected files
3. Follow [execution-checklist.md](execution-checklist.md) step by step

---
*Generated by requirements-refiner skill*
```

### scope.md Template

```markdown
# Scope

## In Scope
- [Deliverable 1]
- [Deliverable 2]
- [Deliverable 3]

## Out of Scope
- [What NOT to build]
- [Deferred work]
- [Explicitly excluded features]

## Assumptions
- [Assumption 1]
- [Assumption 2]

## Dependencies
- [External system/service dependency]
- [Team/resource dependency]
```

### file-mappings.md Template

```markdown
# File Mappings

## Validation Summary
| Path | Status | Action |
|------|--------|--------|
| path/to/file.js | ✓ EXISTS | Modify |
| path/to/new.js | ✗ CREATE | New file |
| path/to/uncertain.js | ? VERIFY | Needs confirmation |

## Create
- `path/to/new/file.js` — [Purpose/description]

## Modify
- `path/to/existing/file.js` — [What changes]

## Reference (patterns read)
- `path/to/similar/file.js` — [Why this is relevant as a pattern]

## Multi-Stack (if applicable)

### Frontend (React/TypeScript)
| Path | Status | Action |
|------|--------|--------|

### Backend (Go/Node/Python)
| Path | Status | Action |
|------|--------|--------|

### Shared Types
| Path | Status | Action |
|------|--------|--------|
```

### api-contracts.md Template

```markdown
# API Contracts

## [METHOD] /path/to/endpoint

**Auth**: Required / Optional / None
**Rate Limit**: X req/min

### Request
```json
{
  "field": "type — required/optional, constraints"
}
```

### Response 200 (Success)
```json
{
  "field": "type — description"
}
```

### Response 4xx (Error)
| Code | Condition | Response |
|------|-----------|----------|
| 400 | Invalid input | `{"error": "validation_error", "details": {...}}` |
| 401 | Unauthorized | `{"error": "unauthorized"}` |
| 404 | Not found | `{"error": "not_found"}` |

---

## [Next Endpoint]
...
```

### data-model.md Template

```markdown
# Data Model Changes

## [ModelName] (`path/to/model.js`)

| Field | Type | Nullable | Default | Index | Description |
|-------|------|----------|---------|-------|-------------|
| field_name | STRING(255) | No | null | Yes | Purpose |

## Relationships
- [ModelA] hasMany [ModelB] via `foreign_key`
- [ModelB] belongsTo [ModelA]

## Migration

```js
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.addColumn('Table', 'field', {
      type: Sequelize.TYPE,
      defaultValue: value,
      allowNull: false
    });
  },
  down: async (queryInterface) => {
    await queryInterface.removeColumn('Table', 'field');
  }
};
```

## Indexes
- `idx_table_field` on `table.field` — [Why this index helps]
```

### business-logic.md Template

```markdown
# Business Logic

## [Rule Name]

**Trigger**: When this rule applies
**Condition**: If X then Y
**Action**: What happens
**Error Handling**: What to do on failure

## [Another Rule]
...

## State Transitions (if applicable)

| Current State | Event | Next State | Side Effect |
|---------------|-------|------------|-------------|
| pending | approve | approved | Send notification |
| pending | reject | rejected | Log reason |
```

### test-scenarios.md Template

```markdown
# Test Scenarios

## Happy Path

| # | Scenario | Input | Expected Output |
|---|----------|-------|-----------------|
| 1 | [Scenario name] | `{...}` | 200, `{...}` |

## Input Validation

| # | Scenario | Input | Expected Output |
|---|----------|-------|-----------------|
| 1 | Missing required field | `{...}` | 400, validation error |

## Edge Cases

| # | Scenario | Input | Expected Output |
|---|----------|-------|-----------------|
| 1 | [Edge case name] | `{...}` | [Expected] |

## Error Handling

| # | Scenario | Trigger | Expected Behavior |
|---|----------|---------|-------------------|
| 1 | External service down | API timeout | Retry 3x, then fail gracefully |

## Security Tests (if applicable)

| # | Scenario | Attack | Expected |
|---|----------|--------|----------|
| 1 | Token tampering | Modify payload | 400 invalid |
```

### security.md Template

```markdown
# Security Checklist

## Authentication
- [ ] Token validation
- [ ] Token expiry handling
- [ ] Rate limiting: X req/min

## Authorization
- [ ] Role-based access control
- [ ] Resource ownership verification

## Input Validation
- [ ] Sanitize user input
- [ ] Validate request body schema
- [ ] Limit payload size

## Data Protection
- [ ] Mask PII in logs
- [ ] Encrypt sensitive data at rest
- [ ] Use HTTPS only

## Integration Security (if external APIs)
- [ ] Validate webhook signatures
- [ ] Timeout handling
- [ ] Circuit breaker pattern

*(Mark N/A for non-applicable items)*
```

### ui-copy.md Template

```markdown
# UI Copy (Bilingual)

## [Screen/Component Name]

| Key | Indonesian | English |
|-----|------------|---------|
| title | | |
| description | | |
| button_primary | | |
| button_secondary | | |

## Success Messages

| Key | Indonesian | English |
|-----|------------|---------|
| success_saved | | |

## Error Messages

| Code | Indonesian | English |
|------|------------|---------|
| ERROR_INVALID_INPUT | | |
| ERROR_NOT_FOUND | | |

## Validation Messages

| Field | Indonesian | English |
|-------|------------|---------|
| email_required | | |
| email_invalid | | |
```

### execution-checklist.md Template

```markdown
# Execution Checklist

## Setup
1. [ ] Read [scope.md](scope.md) and [file-mappings.md](file-mappings.md)
2. [ ] Create new files listed in file-mappings.md

## Implementation
3. [ ] [First implementation step]
4. [ ] [Second step]
5. [ ] [Third step]

## Testing
6. [ ] Write tests for scenarios in [test-scenarios.md](test-scenarios.md)
7. [ ] Run tests locally
8. [ ] Verify edge cases pass

## Verification
9. [ ] Code review checklist complete
10. [ ] Security items in [security.md](security.md) addressed
11. [ ] Manual testing done
```
