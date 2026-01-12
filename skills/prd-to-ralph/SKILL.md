---
name: prd-to-ralph
description: Use when converting PRD/requirements into JSON format for Ralph Wiggum autonomous loops. Extracts user stories, orders by dependency (schema first, then backend, then UI, then dashboard), auto-adds standard criteria (typecheck, build, lint, tests), outputs structured JSON ready for autonomous iteration.
---

# PRD to Ralph JSON Converter

Convert PRD/requirements into structured JSON optimized for Ralph Wiggum autonomous coding loops.

## Overview

Ralph Wiggum workflows iterate autonomously toward success criteria. This skill converts human-readable PRDs into machine-parseable JSON with:
- Dependency-ordered user stories (schema before API before UI)
- Testable acceptance criteria
- Standard quality gates on every story

## When to Use

- Converting PRD/requirements for Ralph autonomous workflow
- Preparing features for autonomous iteration
- Need structured JSON from prose requirements

## When NOT to Use

- Already have JSON in correct format
- Single-task changes (no stories needed)
- Non-coding requirements

## Output Schema

```json
{
  "project": "Project Name",
  "branchName": "ralph/feature-name-kebab-case",
  "description": "Feature description from PRD",
  "userStories": [
    {
      "id": "US-001",
      "title": "Story title",
      "description": "As a [user], I want [feature] so that [benefit]",
      "acceptanceCriteria": [
        "Criterion from PRD",
        "Another criterion",
        "Typecheck passes",
        "Build succeeds",
        "No lint errors",
        "Tests pass"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

## Workflow

### Phase 1: Extract Project Metadata

1. **Project name**: Use PRD title or main heading
2. **Branch name**: Convert to kebab-case with `ralph/` prefix
3. **Description**: First paragraph or intro section

### Phase 2: Identify User Stories

Extract stories from:
- Explicit "User Story" sections
- Numbered requirements
- Feature bullet points
- Prose paragraphs describing functionality

For each story, create:
- Unique ID (US-001, US-002, etc.)
- Title (short, descriptive)
- Description (user story format: As a... I want... so that...)
- Acceptance criteria from PRD content

### Phase 3: Classify Story Layer

**CRITICAL: Classify each story into exactly one layer:**

| Layer | Priority | Keywords/Patterns |
|-------|----------|-------------------|
| Schema/Database | 1 | table, migration, schema, column, field, index, foreign key, database, model definition |
| Backend/API | 2 | endpoint, API, route, controller, service, handler, REST, GraphQL, server action |
| Frontend/UI | 3 | component, page, button, form, modal, UI, display, render, click, user interface |
| Dashboard/Admin | 4 | dashboard, admin, metrics, analytics, reports, monitoring, management |

**Detection rules:**
- Schema: Creates/modifies database structure
- Backend: Implements server logic or API endpoints
- Frontend: User-facing interface components
- Dashboard: Admin/analytics views (depends on everything else)

### Phase 4: Order by Dependency

**MANDATORY: Reorder stories so dependencies come first.**

```
Priority 1: Schema/Database stories
Priority 2: Backend/API stories
Priority 3: Frontend/UI stories
Priority 4: Dashboard/Admin stories
```

**Within same layer:** Maintain original PRD order.

**NEVER output stories in PRD order if that violates dependency order.**

### Phase 5: Add Standard Criteria

**MANDATORY: Append these 4 criteria to EVERY story:**

```json
"acceptanceCriteria": [
  "...criteria from PRD...",
  "Typecheck passes",
  "Build succeeds",
  "No lint errors",
  "Tests pass"
]
```

**No exceptions. Every story gets all 4 standard criteria.**

### Phase 6: Generate JSON

Output valid JSON with:
- All required fields populated
- `passes: false` for all stories
- `notes: ""` empty string
- Stories sorted by priority (1 → 2 → 3 → 4)

### Phase 7: Validate

Before outputting, verify:
- [ ] Stories ordered by dependency (schema → API → UI → dashboard)
- [ ] All 4 standard criteria present on every story
- [ ] Valid JSON syntax
- [ ] Branch name is kebab-case
- [ ] All required fields present

## Dependency Detection Patterns

### Schema/Database (Priority 1)
```
- "create table", "add column", "migration"
- "database schema", "data model"
- "foreign key", "index", "constraint"
- "notifications table", "users table"
- Any mention of table structure or fields
```

### Backend/API (Priority 2)
```
- "API endpoint", "REST", "GraphQL"
- "GET/POST/PATCH/DELETE /api/"
- "controller", "handler", "service"
- "server action", "backend logic"
- "authentication", "authorization" (server-side)
```

### Frontend/UI (Priority 3)
```
- "component", "page", "view"
- "button", "form", "modal", "dropdown"
- "click", "hover", "display"
- "header", "footer", "sidebar"
- "user interface", "UI"
```

### Dashboard/Admin (Priority 4)
```
- "dashboard", "admin panel"
- "metrics", "analytics", "reports"
- "monitoring", "management view"
- "aggregate", "statistics"
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Keep PRD order | Always reorder by dependency |
| Skip standard criteria | Add all 4 to every story |
| Same priority for all | Use layer-based priority (1-4) |
| Missing passes/notes fields | Always include with false/"" |
| Space in branch name | Use kebab-case only |

## Red Flags - STOP and Fix

- UI story has priority 1 (should be 3+)
- Schema story has priority 3+ (should be 1)
- Missing "Typecheck passes" criterion
- Stories not sorted by priority number
- Multiple stories with same priority across different layers

## Example Transformation

**Input PRD:**
```markdown
# Notification System

## Stories
1. Notification Bell UI - show bell with unread count
2. Notification API - GET/POST endpoints
3. Notification Schema - create notifications table
```

**Output JSON:**
```json
{
  "project": "Notification System",
  "branchName": "ralph/notification-system",
  "description": "Notification system for real-time alerts",
  "userStories": [
    {
      "id": "US-001",
      "title": "Notification Schema",
      "description": "As a developer, I want a notifications table so that notification data can be persisted",
      "acceptanceCriteria": [
        "Notifications table created with required fields",
        "Typecheck passes",
        "Build succeeds",
        "No lint errors",
        "Tests pass"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-002",
      "title": "Notification API",
      "description": "As a developer, I want API endpoints so that the frontend can access notifications",
      "acceptanceCriteria": [
        "GET endpoint returns user notifications",
        "POST endpoint creates notifications",
        "Typecheck passes",
        "Build succeeds",
        "No lint errors",
        "Tests pass"
      ],
      "priority": 2,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-003",
      "title": "Notification Bell UI",
      "description": "As a user, I want a notification bell so that I can see my unread notifications",
      "acceptanceCriteria": [
        "Bell icon displayed in header",
        "Unread count badge shown",
        "Typecheck passes",
        "Build succeeds",
        "No lint errors",
        "Tests pass"
      ],
      "priority": 3,
      "passes": false,
      "notes": ""
    }
  ]
}
```

**Note:** Stories reordered from PRD (UI→API→Schema) to dependency order (Schema→API→UI).
