# Test Patterns

Generate test scenarios from business logic and API contracts.

## Contents
- [Deriving Tests from Business Rules](#deriving-tests-from-business-rules)
- [Test Scenario Checklist](#test-scenario-checklist)

## Deriving Tests from Business Rules

### Pattern: Validation Rule → Test Cases

**Business Rule:**
```
PIN must be exactly 6 numeric digits
Cannot be sequential (123456) or repeated (111111)
```

**Derived Tests:**
| # | Scenario | Input | Expected |
|---|----------|-------|----------|
| 1 | Valid PIN | "482916" | ✓ Pass |
| 2 | Too short | "12345" | ✗ 400 "PIN must be 6 digits" |
| 3 | Too long | "1234567" | ✗ 400 "PIN must be 6 digits" |
| 4 | Non-numeric | "12345a" | ✗ 400 "PIN must be numeric" |
| 5 | Sequential ascending | "123456" | ✗ 400 "PIN cannot be sequential" |
| 6 | Sequential descending | "654321" | ✗ 400 "PIN cannot be sequential" |
| 7 | All same digit | "111111" | ✗ 400 "PIN cannot be repeated" |

---

### Pattern: Conditional Flow → Branch Tests

**Business Rule:**
```
IF program.isUsingWhatsappVerification == false: skip verification
IF deliveryChannel IN ['email', 'push']: skip verification  
IF deliveryChannel IN ['sms', 'whatsapp']: require verification
```

**Derived Tests:**
| # | Scenario | Conditions | Expected |
|---|----------|------------|----------|
| 1 | WA verification disabled | isUsingWA=false, channel=sms | Skip verification |
| 2 | Email delivery | isUsingWA=true, channel=email | Skip verification |
| 3 | Push notification | isUsingWA=true, channel=push | Skip verification |
| 4 | SMS delivery + WA enabled | isUsingWA=true, channel=sms | Require verification |
| 5 | WhatsApp delivery | isUsingWA=true, channel=whatsapp | Require verification |

---

### Pattern: State Transition → Sequence Tests

**Business Rule:**
```
States: initiated → verified → completed
       initiated → failed (after max attempts)
       initiated → expired (after timeout)
```

**Derived Tests:**
| # | Scenario | Start State | Action | End State |
|---|----------|-------------|--------|-----------|
| 1 | Happy path | initiated | verify(correct) | verified |
| 2 | Complete flow | verified | complete() | completed |
| 3 | Wrong verification | initiated | verify(wrong) | initiated (attempt++) |
| 4 | Max attempts exceeded | initiated (attempt=5) | verify(wrong) | failed |
| 5 | Session timeout | initiated | wait(11min) | expired |
| 6 | Verify after expired | expired | verify(correct) | error "session expired" |

---

### Pattern: API Endpoint → Request/Response Tests

**API Contract:**
```
POST /v2/pin/login
Request: { memberId, pin }
Response 200: { success, token, expiresAt }
Response 401: { error: "Invalid PIN" }
Response 423: { error: "Account locked" }
```

**Derived Tests:**

#### Happy Path
| # | Scenario | Request | Expected Response |
|---|----------|---------|-------------------|
| 1 | Valid login | { memberId: "123", pin: "482916" } | 200 { success: true, token: "jwt...", expiresAt: "..." } |

#### Input Validation
| # | Scenario | Request | Expected Response |
|---|----------|---------|-------------------|
| 2 | Missing memberId | { pin: "482916" } | 400 { error: "memberId required" } |
| 3 | Missing pin | { memberId: "123" } | 400 { error: "pin required" } |
| 4 | Empty body | {} | 400 { error: "memberId required" } |

#### Authentication Errors
| # | Scenario | Request | Expected Response |
|---|----------|---------|-------------------|
| 5 | Wrong PIN | { memberId: "123", pin: "000000" } | 401 { error: "Invalid PIN" } |
| 6 | Member has no PIN | { memberId: "456", pin: "123456" } | 404 { error: "No PIN configured" } |
| 7 | Member not found | { memberId: "999", pin: "123456" } | 404 { error: "Member not found" } |
| 8 | Account locked | { memberId: "123", pin: "482916" } | 423 { error: "Account locked..." } |

---

### Pattern: Integration/Webhook → End-to-End Tests

**Flow:**
```
1. User clicks verify → POST /initiate → { sessionToken }
2. User sends WA message → WA-Engine webhook
3. WA-Engine calls POST /verify → { status, linkUrl }
4. User clicks link → GET /complete → voucher page
```

**Derived Tests:**
| # | Scenario | Steps | Expected |
|---|----------|-------|----------|
| 1 | Full happy path | initiate → WA message → verify → complete | Voucher displayed |
| 2 | Phone mismatch | initiate → WA from different phone → verify | status: "invalid" |
| 3 | Expired session | initiate → wait 11min → verify | error "session expired" |
| 4 | Invalid token | initiate → tamper token → verify | error "invalid session" |
| 5 | Replay attack | initiate → verify → verify again | error "already used" |

---

## Test Scenario Checklist

When generating tests, ensure coverage of:

- [ ] **Happy path** — Normal successful flow
- [ ] **Input validation** — Missing, empty, wrong type, boundary values
- [ ] **Authentication/Authorization** — Wrong creds, expired tokens, no permission
- [ ] **State errors** — Wrong state for action, already processed
- [ ] **External failures** — Timeout, service down, invalid response
- [ ] **Race conditions** — Concurrent requests, duplicate submissions
- [ ] **Security** — Injection, tampering, replay attacks
