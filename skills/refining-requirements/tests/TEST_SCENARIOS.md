# Test Scenarios for refining-requirements Skill

## How to Run Tests

For each scenario:
1. Launch subagent with `refining-requirements` skill loaded
2. Provide the PRD as user input
3. Ask agent to refine the requirements
4. Score output against expected results
5. Document failures verbatim

---

## Category A: Application Scenarios (Core Functionality)

### A1: Standard Feature PRD

**Input PRD:**
```
We need to add password reset functionality to our Node.js/Express app.

Users should be able to reset their password via email. When they click "Forgot Password" on the login page, they enter their email. We send them a link that's valid for 1 hour. They click it, enter a new password twice, and we update their account.

The email should come from our existing SendGrid integration. Make it look nice with our brand colors.

Similar to how we did email verification - check that flow for patterns.
```

**Expected Output:**
- [ ] Scope section with in/out scope
- [ ] File mappings with EXISTS/CREATE markers
- [ ] Data model changes (reset token storage)
- [ ] API contracts (POST /forgot-password, POST /reset-password)
- [ ] Business logic (token expiry, validation)
- [ ] Test scenarios (happy path, expired token, wrong email)
- [ ] Security checklist (token hashing, rate limiting)
- [ ] UI copy table

---

### A2: Vague Requirements

**Input PRD:**
```
The app is slow. Make it faster.

Users are complaining about load times. We need to optimize performance.
```

**Expected Output:**
- [ ] CLARIFICATION NEEDED section with questions:
  - Which pages/endpoints are slow?
  - What are current load times vs target?
  - Frontend, backend, or database?
  - Any recent changes that caused this?
- [ ] Should NOT produce full refined spec without clarification

---

### A3: API Integration

**Input PRD:**
```
Integrate Stripe payments into our e-commerce platform (Node.js backend, React frontend).

Requirements:
- Accept credit card payments for orders
- Support both one-time purchases and subscriptions
- Handle failed payments gracefully
- Store payment method for returning customers
- PCI compliance - we never touch raw card numbers

The checkout flow is in app/pages/checkout/. Backend API is in app/controllers/v2/orders/.
```

**Expected Output:**
- [ ] API contracts for all payment endpoints
- [ ] Webhook handling (payment_intent.succeeded, etc.)
- [ ] Error handling matrix (card_declined, insufficient_funds, etc.)
- [ ] Security checklist (Stripe.js for PCI, no logging card data)
- [ ] Test scenarios including webhook testing
- [ ] File mappings with validated paths

---

### A4: Data Model Change

**Input PRD:**
```
Add user preferences feature to our Go backend.

Users should be able to set:
- Notification preferences (email, push, SMS)
- Language preference
- Timezone
- Theme (light/dark)

These preferences should be returned with the user profile and updatable via API.
Stored in PostgreSQL. We use sqlc for queries.
```

**Expected Output:**
- [ ] Data model with all fields, types, defaults
- [ ] Migration SQL (CREATE TABLE or ALTER TABLE)
- [ ] API contracts (GET/PATCH preferences)
- [ ] sqlc query definitions
- [ ] File mappings using Go patterns (not Node.js)

---

## Category B: Edge Case Scenarios

### B1: Greenfield Project (No Existing Code)

**Input PRD:**
```
Build a new authentication microservice from scratch.

Tech stack: Go with Gin framework, PostgreSQL, Redis for sessions.

Features:
- User registration with email verification
- Login with JWT tokens
- Password reset flow
- Session management with Redis
- Rate limiting on auth endpoints

This is a brand new service - no existing code.
```

**Expected Output:**
- [ ] Full project structure (cmd/, internal/, pkg/)
- [ ] All file mappings marked CREATE (none EXISTS)
- [ ] No references to "existing patterns" since greenfield
- [ ] Complete scaffolding offer at end
- [ ] Go-specific patterns (go.mod, Makefile, etc.)

---

### B2: Multi-Stack Monorepo

**Input PRD:**
```
Add real-time activity feed feature to our platform.

We have a monorepo with:
- Frontend: React (packages/web/)
- Backend API: Go (services/api/)
- ML Service: Python (services/ml/)
- Shared types: TypeScript (packages/shared/)

The activity feed needs:
- Frontend component showing recent activities
- Backend endpoint to fetch activities
- ML service to rank activities by relevance
- Shared types for activity schema
```

**Expected Output:**
- [ ] Separate file mapping sections per stack
- [ ] Correct file extensions per language
- [ ] Cross-service API contracts
- [ ] Shared type definitions
- [ ] Multiple tech-specific patterns applied

---

### B3: Unusual Tech Stack

**Input PRD:**
```
Add user session management to our Rust/Actix-web backend.

Requirements:
- Store sessions in Redis
- JWT token generation and validation
- Session timeout after 30 minutes of inactivity
- Refresh token rotation

We use:
- actix-web 4.x
- redis-rs
- jsonwebtoken crate
- sqlx for PostgreSQL
```

**Expected Output:**
- [ ] Rust-specific file patterns (src/handlers/, src/models/)
- [ ] Cargo.toml dependency additions
- [ ] Rust idioms (Result types, impl blocks)
- [ ] Reference to Actix extractors/middleware patterns

---

### B4: Multi-Service Feature

**Input PRD:**
```
Add real-time notifications to our platform.

Components:
1. Frontend (React): Display notification bell with count, dropdown with recent notifications
2. Backend (Node.js): REST API for fetching notifications, marking as read
3. WebSocket server (Node.js): Push new notifications in real-time
4. Database: PostgreSQL for storing notifications

Flow:
- Event happens (order placed, message received, etc.)
- Backend creates notification record
- WebSocket server pushes to connected clients
- Frontend updates UI in real-time
```

**Expected Output:**
- [ ] Separate sections for each service
- [ ] Cross-service data flow diagram or description
- [ ] WebSocket protocol/message format
- [ ] Event-driven architecture patterns
- [ ] Integration test scenarios

---

### B5: PRD with Visual References

**Input PRD:**
```
Implement the new login page based on the attached wireframe.

[See attached: login-wireframe.png]

The wireframe shows:
- Email input field
- Password input with show/hide toggle
- "Remember me" checkbox
- "Forgot password?" link
- "Sign in" button
- Social login options (Google, GitHub)
- "Don't have an account? Sign up" link

Match our existing design system colors and spacing.
```

**Expected Output:**
- [ ] Acknowledge that wireframe was referenced
- [ ] Extract all UI elements from description
- [ ] UI copy table with all labels
- [ ] Note any ambiguities from visual-only spec
- [ ] Request clarification if wireframe details unclear

---

## Category C: Trigger Scenarios

### C1: Simple Bug Fix (Should NOT Trigger Full Refinement)

**Input:**
```
Fix typo in the error message on login page.

Currently says "Invalide email or password" - should be "Invalid email or password"

File: app/pages/login/LoginForm.tsx line 45
```

**Expected Behavior:**
- [ ] Should NOT produce full refined PRD
- [ ] May suggest this doesn't need refinement
- [ ] If produces anything, minimal scope only

---

### C2: Build From Scratch (Should Trigger)

**Input:**
```
Build new microservice for handling push notifications.

Requirements:
- Firebase Cloud Messaging integration
- APNs for iOS
- Store device tokens per user
- Send targeted notifications
- Track delivery and open rates

New service, deploy to Kubernetes.
```

**Expected Behavior:**
- [ ] SHOULD trigger full refinement
- [ ] Greenfield patterns applied
- [ ] Complete output with all sections

---

### C3: Ambiguous File Paths (Should Trigger)

**Input:**
```
Update the API controller for handling user profile updates.

Add endpoint for uploading profile picture. Store in S3, update user record with URL.
```

**Expected Behavior:**
- [ ] SHOULD trigger refinement
- [ ] Ask clarifying questions OR validate paths
- [ ] File mappings should have ? VERIFY markers

---

### C4: Well-Structured Jira Ticket (May Not Need Full Refinement)

**Input:**
```
JIRA-1234: Add 'last_login_at' timestamp to users table

Acceptance Criteria:
- Add column: last_login_at TIMESTAMP NULL
- Update on successful login in AuthController.login()
- Include in GET /api/users/:id response
- Migration file: 20241201_add_last_login_at.sql

Files to modify:
- app/models/User.js (add field)
- app/controllers/AuthController.js (update on login)
- app/serializers/UserSerializer.js (include in response)
- migrations/20241201_add_last_login_at.sql (new file)
```

**Expected Behavior:**
- [ ] Recognize this is already well-structured
- [ ] May suggest minimal refinement or validation only
- [ ] Should not bloat with unnecessary sections

---

### C5: Refactoring Request (Should Trigger)

**Input:**
```
Refactor authentication from session-based to JWT tokens.

Current state:
- Express-session with Redis store
- Cookie-based auth
- Session stored server-side

Target state:
- JWT access tokens (15 min expiry)
- Refresh tokens (7 day expiry)
- Stateless authentication
- Keep Redis for refresh token blacklist only

Need to maintain backward compatibility during migration.
```

**Expected Behavior:**
- [ ] SHOULD trigger full refinement
- [ ] Migration strategy section
- [ ] Backward compatibility considerations
- [ ] Security implications documented

---

## Scoring Rubric

For each test:

| Criterion | Points | Description |
|-----------|--------|-------------|
| Completeness | 0-3 | All expected sections present |
| Accuracy | 0-3 | File paths validated, contracts correct |
| Judgment | 0-2 | Correct trigger decision |
| Quality | 0-2 | Actionable, clear, no ambiguity |

**Pass threshold:** 8/10 points per scenario
