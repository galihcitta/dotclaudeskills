# Edge Cases & Missing Information

Handle incomplete PRDs, external dependencies, and special requirements.

## Contents
- [Detecting Incomplete PRDs](#detecting-incomplete-prds)
- [Missing Info Template](#missing-info-template)
- [External Dependencies](#external-dependencies)
- [Performance & SLA Requirements](#performance--sla-requirements)
- [Feature Flags & Rollout](#feature-flags--rollout)
- [Compliance & Regulatory](#compliance--regulatory)
- [A/B Testing Requirements](#ab-testing-requirements)
- [API Versioning](#api-versioning)
- [Edge Case Checklist](#edge-case-checklist)

## Detecting Incomplete PRDs

Scan for missing critical information:

| Missing | Indicator | Action |
|---------|-----------|--------|
| **Scope unclear** | No clear deliverables | Ask: "What specifically should be delivered?" |
| **No acceptance criteria** | No success definition | Ask: "How do we know when this is done?" |
| **Tech stack unknown** | No file paths or patterns | Ask: "What tech stack is this for?" |
| **Data model vague** | Fields mentioned without types | Ask: "What are the field types and constraints?" |
| **API undefined** | Behavior described, no contract | Propose contract, ask for confirmation |
| **Auth unclear** | "Users can access..." | Ask: "What authentication/authorization is required?" |
| **Error handling missing** | Only happy path described | Add: "What happens when X fails?" |

## Missing Info Template

When PRD is incomplete, generate a questions section:

```markdown
## ⚠️ Clarification Needed

Before implementation, please clarify:

### Critical (Blocking)
1. [ ] What database table stores X? (No model specified)
2. [ ] What authentication is required for these endpoints?
3. [ ] What's the expected response format for errors?

### Important (Affects Design)
4. [ ] Should this support pagination? What limits?
5. [ ] Are there rate limiting requirements?
6. [ ] What's the expected latency SLA?

### Nice to Know (Can Assume)
7. [ ] Preferred error code format? (Will assume: UPPER_SNAKE_CASE)
8. [ ] Logging level for this feature? (Will assume: INFO for success, ERROR for failures)

---
**Proceeding with assumptions marked above. Please confirm or correct.**
```

---

## External Dependencies

Track dependencies on other teams/services:

```markdown
## External Dependencies

### Blocking Dependencies
| Dependency | Owner | Status | ETA | Impact if Delayed |
|------------|-------|--------|-----|-------------------|
| WA-Engine webhook endpoint | Platform Team | 🟡 In Progress | Nov 30 | Cannot test integration |
| Auth service token validation | Auth Team | 🟢 Ready | - | None |

### Non-Blocking Dependencies
| Dependency | Owner | Workaround |
|------------|-------|------------|
| Analytics events | Data Team | Log locally, backfill later |
| Email templates | Marketing | Use placeholder text |

### Third-Party APIs
| Service | Documentation | Sandbox Available | Rate Limits |
|---------|---------------|-------------------|-------------|
| Meta WhatsApp API | [link] | Yes | 1000 msg/day |
| Twilio SMS | [link] | Yes | Free tier |
```

---

## Performance & SLA Requirements

Add when performance matters:

```markdown
## Performance Requirements

### Latency Targets
| Endpoint | p50 | p95 | p99 |
|----------|-----|-----|-----|
| POST /verify | 100ms | 300ms | 500ms |
| GET /voucher | 50ms | 100ms | 200ms |

### Throughput
- Expected: 100 requests/second
- Peak: 500 requests/second (during campaigns)

### Availability
- Target: 99.9% uptime
- Maintenance window: Sundays 2-4 AM

### Caching Strategy
| Data | TTL | Storage | Invalidation |
|------|-----|---------|--------------|
| Voucher details | 5 min | Redis | On update |
| User sessions | 10 min | Redis | On logout |

### Database Considerations
- Expected table size: 1M rows/month
- Indexes needed: [list]
- Partitioning: By created_at (monthly)
```

---

## Feature Flags & Rollout

For gradual rollouts:

```markdown
## Feature Flags

### Flag Definition
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| ENABLE_WA_VERIFICATION | boolean | false | Enable WhatsApp verification flow |
| WA_VERIFICATION_PERCENTAGE | number | 0 | Percentage of users to enable (0-100) |

### Rollout Plan
| Phase | Flag Value | Audience | Duration | Success Criteria |
|-------|------------|----------|----------|------------------|
| 1 | 10% | Internal users | 1 day | No errors |
| 2 | 25% | Beta users | 3 days | Error rate < 1% |
| 3 | 50% | All users | 1 week | Conversion maintained |
| 4 | 100% | All users | - | Full rollout |

### Rollback Trigger
- Error rate > 5%
- Latency p99 > 2s
- Customer complaints > 10

### Kill Switch
```bash
# Immediate disable
curl -X POST /admin/feature-flags -d '{"ENABLE_WA_VERIFICATION": false}'
```
```

---

## Compliance & Regulatory

When data protection matters:

```markdown
## Compliance Requirements

### Data Classification
| Field | Classification | Retention | Encryption |
|-------|----------------|-----------|------------|
| phone_number | PII | 2 years | At rest + transit |
| session_token | Sensitive | 24 hours | Transit only |
| voucher_code | Internal | 5 years | None |

### GDPR Considerations
- [ ] Right to access: API to export user data
- [ ] Right to deletion: Cascade delete on user removal
- [ ] Data portability: Export in standard format
- [ ] Consent: Record consent timestamp

### Audit Trail
| Event | Fields to Log | Retention |
|-------|---------------|-----------|
| Verification attempted | user_id, timestamp, result | 1 year |
| Voucher redeemed | user_id, voucher_id, timestamp | 5 years |

### Local Regulations (Indonesia)
- OJK compliance for financial data
- Store data in local data center
```

---

## A/B Testing Requirements

When experimenting:

```markdown
## A/B Testing

### Experiment Definition
| Variant | Description | Allocation |
|---------|-------------|------------|
| Control | Existing PIN flow | 50% |
| Treatment | New WA verification | 50% |

### Metrics to Track
| Metric | Type | Expected Impact |
|--------|------|-----------------|
| Verification success rate | Primary | +10% |
| Time to complete | Secondary | -20% |
| Drop-off rate | Guardrail | No increase |

### Experiment Duration
- Minimum: 2 weeks
- Sample size: 10,000 users per variant

### Implementation
```python
if experiment.get_variant(user_id, "wa_verification") == "treatment":
    return wa_verification_flow()
else:
    return pin_verification_flow()
```
```

---

## API Versioning

When backward compatibility matters:

```markdown
## API Versioning Strategy

### Current Versions
| Version | Status | Sunset Date |
|---------|--------|-------------|
| v1 | Deprecated | 2025-03-01 |
| v2 | Current | - |
| v3 | Beta | - |

### Breaking Changes in v2
| Change | Migration Path |
|--------|----------------|
| `phone` → `phoneNumber` | Rename field |
| Response wrapper added | Update parser |

### Backward Compatibility
- Support v1 for 6 months after v2 release
- Log v1 usage for migration tracking
- Return deprecation header: `Sunset: Sat, 01 Mar 2025 00:00:00 GMT`
```

---

## Edge Case Checklist

When refining, check for these edge cases:

### Data Edge Cases
- [ ] What if field is null/empty?
- [ ] What if record doesn't exist?
- [ ] What if duplicate submission?
- [ ] What if data exceeds limits?

### Timing Edge Cases
- [ ] What if session expires mid-flow?
- [ ] What if concurrent requests?
- [ ] What if request times out?
- [ ] What if retry after failure?

### User Edge Cases
- [ ] What if user has no permission?
- [ ] What if user is deleted mid-flow?
- [ ] What if user changes device?
- [ ] What if user is in different timezone?

### Integration Edge Cases
- [ ] What if external service is down?
- [ ] What if webhook is delayed?
- [ ] What if response format changes?
- [ ] What if rate limit exceeded?

### Business Edge Cases
- [ ] What if voucher already redeemed?
- [ ] What if voucher expired?
- [ ] What if user already verified?
- [ ] What if phone number changes?
