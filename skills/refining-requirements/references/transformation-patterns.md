# Transformation Patterns

> **Stack-agnostic**: Examples use Node.js syntax but patterns apply to any stack. See `references/stack-patterns.md` for adaptation.

## Contents
- [Pattern 1: "Similar to X" → Explicit Behavior](#pattern-1-similar-to-x--explicit-behavior)
- [Pattern 2: Scattered Paths → Consolidated Mappings](#pattern-2-scattered-paths--consolidated-mappings)
- [Pattern 3: Prose Data Models → Tables](#pattern-3-prose-data-models--tables)
- [Pattern 4: Narrative Flow → Decision Logic](#pattern-4-narrative-flow--decision-logic)
- [Pattern 5: "You Decide" → Constrained Defaults](#pattern-5-you-decide--constrained-defaults)
- [Pattern 6: Missing API Contract → Full Spec](#pattern-6-missing-api-contract--full-spec)
- [Checklist](#checklist)

## Pattern 1: "Similar to X" → Explicit Behavior

### Before
```
The business logic, pattern and behaviour should be same with 
PIN management system in POS Integration `app/controllers/v2/integrations/pos/pin`
```

### After
```markdown
## Business Logic

### PIN Validation (copy from `pos/pin/create.js`)
- Exactly 6 numeric digits
- Reject sequential: 123456, 654321
- Reject repeated: 111111, 000000

### Lockout (copy from `pos/pin/login.js`)
- Track failed attempts per member
- Lock after 5 consecutive failures
- Lockout duration: 30 minutes
- Reset counter on success
```

---

## Pattern 2: Scattered Paths → Consolidated Mappings

### Before
```
check CardProgram(app/models/card_program.js). add new field...
The Egift is generated from egift_manager(lib/egift_manager.js)...
you can take a look generate_as_vendor(app/controllers/v1/egifts/generate_as_vendor.js)...
```

### After
```markdown
## File Mappings

### Modify
- `app/models/card_program.js` — Add isUsingWhatsappVerification field
- `app/models/egift.js` — Add eligiblePhoneNumber field
- `lib/egift_manager.js` — Pass phone to generated egift

### Reference
- `app/controllers/v1/egifts/generate_as_vendor.js` — Generation pattern
```

---

## Pattern 3: Prose Data Models → Tables

### Before
```
add new field called isUsingWhatsappVerification boolean type. the default 
value is false. add new field eligiblePhoneNumber allowNull true in Egift model.
```

### After
```markdown
## Data Model Changes

### CardProgram (`app/models/card_program.js`)
| Field | Type | Nullable | Default | Description |
|-------|------|----------|---------|-------------|
| isUsingWhatsappVerification | BOOLEAN | No | false | Enable WA verification |

### Egift (`app/models/egift.js`)
| Field | Type | Nullable | Default | Description |
|-------|------|----------|---------|-------------|
| eligiblePhoneNumber | STRING(20) | Yes | null | E.164 format phone |
```

---

## Pattern 4: Narrative Flow → Decision Logic

### Before
```
Check whether the Verify phone number via whatsapp is YES / NO. 
If No, the journey will be like existing (only with PIN or without PIN).
If yes, continue step 3. Check the delivery of the voucher link...
```

### After
```markdown
## Business Logic

### Verification Requirement Check
```
INPUT: program, deliveryChannel
OUTPUT: requiresVerification (boolean)

IF program.isUsingWhatsappVerification == false: RETURN false
IF deliveryChannel IN ['email', 'push']: RETURN false
IF deliveryChannel IN ['sms', 'whatsapp']: RETURN true
RETURN false
```
```

---

## Pattern 5: "You Decide" → Constrained Defaults

### Before
```
Adjust SSO Wallet api that will pass the new header data from the 
response from PIN Login (it can be token or others) you decide it
```

### After
```markdown
### SSO Wallet Integration
Modify `sso/wallet.js`:
1. Accept header: `X-PIN-Token`
2. Validate token not expired (JWT exp claim or Redis lookup)
3. Include in response: `X-PIN-Token` (forward for client persistence)
4. Token format: JWT with claims `{ memberId, iat, exp }`
5. Expiry: 1 hour from login
```

---

## Pattern 6: Missing API Contract → Full Spec

### Before
```
the request payload will be look like this:
{ phoneNumber, maskedEgiftEgroupId, sessionToken }
and the response would be like this 
{ status: valid/invalid, linkUrl: link to voucher page }
```

### After
```markdown
### POST /v2/chatbot/verify-egift-egroup
Webhook from WA-Engine after receiving Meta callback.

- **Auth**: Internal service token
- **Request**:
```json
{
  "phoneNumber": "string — E.164 format from Meta webhook",
  "maskedEgiftEgroupId": "string — masked ID from user message",
  "sessionToken": "string — HMAC-signed token from initiate"
}
```
- **Response 200 (match)**:
```json
{
  "status": "valid",
  "linkUrl": "https://domain.com/voucher?token=xxx",
  "expiresAt": "ISO8601 — link valid for 10 minutes"
}
```
- **Response 200 (mismatch)**:
```json
{
  "status": "invalid",
  "reason": "phone_mismatch"
}
```
- **Response 400**: `{ "error": "invalid_session" }` — expired/tampered token
```

---

## Checklist

When refining, verify:

- [ ] Scope has In/Out sections
- [ ] All file paths in File Mappings
- [ ] Data models in table format
- [ ] APIs have method, path, request, response, errors
- [ ] Business logic as pseudocode/tables
- [ ] No "like X" without explaining X
- [ ] No "you decide" without constraints
- [ ] Execution checklist at end
