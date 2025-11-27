# Templates

Copy and fill these templates based on requirement type.

## Contents
- [API Feature Template](#api-feature-template)
- [Data Model Template](#data-model-template)
- [Integration Template](#integration-template)
- [Auth Flow Template](#auth-flow-template)

## API Feature Template

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
