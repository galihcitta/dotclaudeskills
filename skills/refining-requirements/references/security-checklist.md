# Security Checklist

Auto-generate security considerations based on detected feature patterns.

## Contents
- [Detection Patterns](#detection-patterns)
- [Security Checklists by Pattern](#security-checklists-by-pattern)
- [Example Output](#example-output)
- [Non-Applicable Sections](#non-applicable-sections)

## Detection Patterns

Scan the PRD for these keywords to determine applicable security checks:

| Pattern | Keywords | Applicable Checks |
|---------|----------|-------------------|
| Authentication | PIN, password, login, token, session | Auth Security |
| Phone/PII | phone, email, address, name, KTP | Data Protection |
| External API | webhook, integration, external, third-party | Integration Security |
| File Upload | upload, file, image, document | File Security |
| Payment | payment, transaction, balance, points | Financial Security |

---

## Security Checklists by Pattern

### Auth Security
When PRD involves: PIN, password, login, token, session

```markdown
## Security Checklist

### Authentication
- [ ] Constant-time comparison for secrets (PIN, password)
- [ ] Rate limiting: max N attempts per user per timeframe
- [ ] Account lockout after failed attempts
- [ ] Token entropy: minimum 256 bits
- [ ] Token expiry: define max lifetime
- [ ] Invalidate token after use (if single-use)
- [ ] Secure token storage (httpOnly cookie / encrypted)
- [ ] Session invalidation on logout/password change
```

---

### Data Protection
When PRD involves: phone, email, personal data

```markdown
### Data Protection
- [ ] Mask PII in logs: `+62812****7890`, `j***@email.com`
- [ ] Encrypt sensitive fields at rest
- [ ] TLS required for transmission
- [ ] PII audit trail for compliance
- [ ] Data retention policy defined
- [ ] Right to deletion supported (if applicable)
```

---

### Integration Security
When PRD involves: webhook, external API, third-party

```markdown
### Integration Security
- [ ] Validate webhook signatures (HMAC-SHA256)
- [ ] Allowlist source IPs (if known)
- [ ] Timeout: max 30s for external calls
- [ ] Circuit breaker for repeated failures
- [ ] Retry with exponential backoff
- [ ] Don't leak internal errors to external parties
- [ ] Validate response schema from external API
- [ ] Log external call failures with correlation ID
```

---

### File Security
When PRD involves: file upload, image, document

```markdown
### File Security
- [ ] Validate file type (magic bytes, not just extension)
- [ ] Max file size limit
- [ ] Scan for malware (if applicable)
- [ ] Store outside webroot / use signed URLs
- [ ] Randomize stored filename
- [ ] Set Content-Disposition header on download
```

---

### Financial Security
When PRD involves: payment, points, balance, transaction

```markdown
### Financial Security
- [ ] Idempotency keys for transactions
- [ ] Double-entry bookkeeping / audit trail
- [ ] Prevent negative balance
- [ ] Rate limit high-value operations
- [ ] Require re-authentication for sensitive actions
- [ ] Log all financial operations with actor + timestamp
```

---

## Example Output

Given PRD with: WhatsApp phone verification, session token, external webhook

```markdown
## Security Checklist

### Authentication (detected: token, session)
- [ ] Token entropy: minimum 256 bits (use crypto.randomBytes)
- [ ] Token expiry: 10 minutes
- [ ] Invalidate token after successful verification
- [ ] Constant-time comparison for token validation

### Data Protection (detected: phone number)
- [ ] Mask phone in logs: +62812****7890
- [ ] Store eligiblePhoneNumber encrypted at rest
- [ ] Never log full phone in error messages

### Integration Security (detected: WA-Engine webhook)
- [ ] Validate webhook signature from WA-Engine
- [ ] Allowlist WA-Engine IP addresses
- [ ] Timeout: 30s for WA-Engine responses
- [ ] Circuit breaker: disable after 5 consecutive failures
- [ ] Return generic error to WA-Engine, log details internally
```

---

## Non-Applicable Sections

If a security category doesn't apply, explicitly state it:

```markdown
### File Security
Not applicable — no file uploads in this feature.

### Financial Security  
Not applicable — no monetary transactions.
```

This prevents reviewers from wondering if security was overlooked.
