# Baseline Test Scenarios for prd-to-ralph

These scenarios test how Claude handles PRD-to-JSON conversion WITHOUT the skill.

## Expected Output Schema

```json
{
  "project": "[Project Name]",
  "branchName": "ralph/[feature-name-kebab-case]",
  "description": "[Feature description]",
  "userStories": [
    {
      "id": "US-001",
      "title": "[Story title]",
      "description": "As a [user], I want [feature] so that [benefit]",
      "acceptanceCriteria": ["..."],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

---

## Scenario A: Simple PRD

**Test focus:** Does it produce valid JSON? Does it add standard criteria?

### Input PRD

```markdown
# User Profile Feature

Add a user profile page where users can view and edit their information.

## Requirements

1. Display user's name, email, and avatar
2. Allow editing name and avatar (email is read-only)
3. Save changes with a confirmation message
```

### Expected Behavior
- Extract project name: "User Profile Feature"
- Generate branch: "ralph/user-profile-feature"
- Create 3 user stories
- Add standard criteria: typecheck, build, lint, tests pass

---

## Scenario B: Out-of-Order PRD

**Test focus:** Does it reorder based on dependencies?

### Input PRD

```markdown
# Notification System

Build a notification system for real-time alerts.

## User Stories

### Story 1: Notification Bell UI
Create a notification bell icon in the header that shows unread count badge.
- Clicking opens dropdown with notifications list
- Mark as read on click

### Story 2: Notification Preferences
Add a settings page where users can configure notification preferences.
- Email notifications toggle
- Push notifications toggle
- Notification frequency selector

### Story 3: Notification Database Schema
Create the notifications table with fields:
- id, user_id, type, title, message, read_at, created_at

### Story 4: Notification API
Create REST endpoints:
- GET /api/notifications - list user notifications
- PATCH /api/notifications/:id/read - mark as read
- POST /api/notifications - create notification (internal)
```

### Expected Behavior
- Reorder stories by dependency:
  1. Story 3 (Schema) - priority 1
  2. Story 4 (API) - priority 2
  3. Story 1 (UI - Bell) - priority 3
  4. Story 2 (UI - Preferences) - priority 4
- Detect that UI stories depend on API, API depends on schema

---

## Scenario C: Complex Prose-Heavy PRD

**Test focus:** Can it extract stories from prose and order correctly?

### Input PRD

```markdown
# E-Commerce Cart Redesign

We need to completely overhaul our shopping cart experience. The current implementation is slow and users are abandoning carts at a high rate.

## Background

Our analytics show that 67% of users abandon their carts. Exit surveys indicate the main issues are: slow loading, confusing UI, and lack of real-time updates.

## What We Want

First, we should probably update how we store cart data. Right now it's all in localStorage which causes sync issues. We want to move to a server-side cart with Redis caching for performance.

The new cart should show real-time updates - when you add something, the cart icon updates immediately without a page refresh. We're thinking websockets for this.

The checkout flow needs work too. Users should see their cart summary, be able to adjust quantities inline, apply promo codes, and see shipping estimates before going to payment.

Oh and we need a "save for later" feature. Users have been asking for this forever. They want to move items out of the cart but keep them saved somewhere.

The admin dashboard needs updates too - we want to see abandoned cart metrics and be able to send recovery emails.

## Technical Notes

- Our backend is Node.js with PostgreSQL
- Frontend is Next.js
- We use Stripe for payments
```

### Expected Behavior
- Extract ~5-6 user stories from prose
- Identify and order by dependency:
  1. Database/schema changes (cart storage migration)
  2. Backend/API (cart API, websocket setup)
  3. Frontend UI (cart components, real-time updates)
  4. Dashboard (admin metrics)
- Add standard criteria to each story
- Generate meaningful acceptance criteria from prose

---

## Success Criteria for Baseline

Document for each scenario:
1. Did it produce valid JSON matching the schema?
2. Did it add all 4 standard criteria (typecheck, build, lint, tests)?
3. Did it order stories by dependency correctly?
4. What rationalizations did it use when failing?

## Failure Patterns to Watch For

- Missing standard criteria
- Wrong priority order (UI before schema)
- Missing stories from prose
- Invalid JSON structure
- Missing required fields (passes, notes)
- Branch name not kebab-case
