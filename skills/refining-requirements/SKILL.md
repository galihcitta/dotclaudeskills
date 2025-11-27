---
name: refining-requirements
description: Refines PRDs, feature specs, and task descriptions for AI-assisted implementation. Handles both greenfield projects and feature additions. Auto-detects tech stack from project files, reads conventions from CLAUDE.md, validates file paths against codebase, and saves refined specs to agent-workflow/requirements/. Offers scaffolding of boilerplate files. Triggers on "refine this PRD", "new project", "build from scratch", "optimize requirements", or ambiguous specs.
---

# Requirements Refiner

Transform rough requirements into implementation-ready specifications optimized for Claude Code execution.

## When to Use

- Received a PRD/spec that's prose-heavy and ambiguous
- Requirements scatter file paths throughout text
- Specs say "similar to X" without explaining X
- Missing API contracts, data models, or clear scope
- Before starting implementation on complex features
- **Starting a new project from scratch (greenfield)**
- Need to identify missing information before coding

## Workflow

### Phase 0: Auto-Detect Project Context

**Step 1: Detect tech stack automatically**

```bash
# Run these checks to auto-detect stack
ls package.json 2>/dev/null && echo "DETECTED: Node.js"
ls go.mod 2>/dev/null && echo "DETECTED: Go"
ls requirements.txt pyproject.toml 2>/dev/null && echo "DETECTED: Python"
ls pom.xml build.gradle 2>/dev/null && echo "DETECTED: Java"
ls Gemfile 2>/dev/null && echo "DETECTED: Ruby"
ls composer.json 2>/dev/null && echo "DETECTED: PHP"
ls Cargo.toml 2>/dev/null && echo "DETECTED: Rust"
```

**Step 2: Read project conventions from CLAUDE.md**

```bash
# Check for project conventions
cat CLAUDE.md 2>/dev/null || cat .claude/CLAUDE.md 2>/dev/null || echo "No CLAUDE.md found"
```

Extract and apply:
- Code style preferences
- Naming conventions
- Architecture patterns
- Testing requirements
- Documentation standards

**Step 3: Detect project type**

| Type | Indicators | Template |
|------|------------|----------|
| Greenfield | "new project", "build from scratch", no existing files | Use `references/greenfield-patterns.md` |
| Feature | References existing code, adds to current system | Use standard templates |

### Phase 1: Check for Missing Information

Scan PRD for completeness. See `references/edge-cases.md` for checklist.

If critical info is missing, generate a **⚠️ Clarification Needed** section with:
- Critical (blocking) questions
- Important (affects design) questions  
- Assumptions being made

### Phase 2: Extract and Classify

Pull out: scope, file mappings, data models, API contracts, business logic, UI copy

### Phase 3: Validate File Paths Against Codebase

**Actually verify paths exist:**

```bash
# For each file path mentioned in PRD, check if it exists
find . -path "*/node_modules" -prune -o -name "filename.js" -type f -print
```

**Read similar files to understand patterns:**

```bash
# If PRD says "similar to existing controller", read it
cat app/controllers/v2/integrations/pos/pin/create.js 2>/dev/null | head -50
```

Mark paths as:
- `✓ EXISTS` — file found, will modify
- `✗ CREATE` — file doesn't exist, will create
- `? VERIFY` — path mentioned but needs confirmation

Include validation summary in output:
```markdown
## File Path Validation
| Path | Status | Action |
|------|--------|--------|
| app/models/egift.js | ✓ EXISTS | Modify — add field |
| app/controllers/v2/msite/verify.js | ✗ CREATE | New endpoint |
```

### Phase 4: Structure

Apply template from `references/templates.md`

Adapt to detected tech stack using `references/stack-patterns.md`:
- File extensions and paths
- Migration format
- Naming conventions
- Test patterns

### Phase 5: Generate Test Scenarios

Derive tests from business logic. See `references/test-patterns.md`

### Phase 6: Security & UI Copy

**Security**: Auto-generate checklist based on detected patterns. See `references/security-checklist.md`

**UI Copy**: Extract all user-facing text into bilingual table (ID/EN). See `references/ui-copy-patterns.md`

### Phase 7: Save Output

**Always save refined PRD to project:**

```bash
# Create output directory if needed
mkdir -p agent-workflow/requirements

# Save with timestamp and descriptive name
# Format: YYYYMMDD-feature-name.md
```

**Naming convention:**
- `agent-workflow/requirements/20241127-whatsapp-verification.md`
- `agent-workflow/requirements/20241127-pin-management-api.md`
- `agent-workflow/requirements/20241127-new-verification-service.md` (greenfield)

**Always include in saved file:**
```markdown
---
title: [Feature Name]
created: [ISO timestamp]
status: draft | review | approved
stack: [detected stack]
type: feature | greenfield
original_prd: [filename if provided]
---
```

### Phase 8: Offer Scaffolding (Optional)

After saving refined PRD, ask:

> "Would you like me to scaffold the boilerplate files for this feature?"

If yes, create:
- Empty controller/handler files with correct structure
- Model files with field definitions
- Migration files with schema
- Test file skeletons
- Route registrations

**Scaffolding rules:**
- Read existing files to match code style
- Use project's linting/formatting conventions from CLAUDE.md
- Add TODO comments for implementation
- Don't overwrite existing files (create `.new` suffix if conflict)

## Output Structure

```markdown
---
title: [Feature Name]
created: 2024-11-27T10:00:00Z
status: draft
stack: nodejs | go | python | java
type: feature | greenfield
original_prd: int-1429.md
---

# [Feature Name]

## Scope
### In Scope
- Deliverable 1
- Deliverable 2
### Out of Scope
- What NOT to build

## Project Context
- **Stack**: Auto-detected or specified
- **Conventions**: From CLAUDE.md
- **Related patterns**: Files read for reference

## Complexity Assessment
| Metric | Value |
|--------|-------|
| Files to create | N |
| Files to modify | N |
| New endpoints | N |
| Database migrations | N |
| External dependencies | List |
| Estimated effort | S/M/L (days) |
| Risk areas | List |

## File Mappings
### Validation Summary
| Path | Status | Action |
|------|--------|--------|
| path/to/file.js | ✓ EXISTS | Modify |
| path/to/new.js | ✗ CREATE | New file |

### Create
- `path/to/new.js` — Purpose
### Modify  
- `path/to/existing.js` — What changes
### Reference (patterns read)
- `path/to/pattern.js` — Why relevant

## Data Model Changes
### [ModelName] (`path/to/model.js`)
| Field | Type | Nullable | Default | Description |
|-------|------|----------|---------|-------------|

## API Contracts
### POST /v2/endpoint
- **Request**: `{ field: "type — description" }`
- **Response 200**: `{ ... }`
- **Response 4xx**: Error conditions

## Business Logic
### [Rule Name]
- **Trigger**: When this applies
- **Condition**: If X then Y
- **Action**: What happens

## Test Scenarios
### Happy Path
| # | Scenario | Input | Expected Output |
|---|----------|-------|-----------------|
| 1 | Valid request | {...} | 200, {...} |

### Edge Cases
| # | Scenario | Input | Expected Output |
|---|----------|-------|-----------------|
| 1 | Invalid input | {...} | 400, error |

### Error Handling
| # | Scenario | Trigger | Expected Behavior |
|---|----------|---------|-------------------|
| 1 | Service down | API timeout | Retry 3x, then fail gracefully |

## Security Checklist
[Auto-generated based on feature type]

## UI Copy (Bilingual)
### [Screen/Component Name]
| Key | Indonesian | English |
|-----|------------|---------|
| title | ... | ... |
| button | ... | ... |

### Error Messages
| Code | Indonesian | English |
|------|------------|---------|
| ERROR_CODE | ... | ... |

## Execution Checklist
1. [ ] First implementation step
2. [ ] Second step
3. [ ] Write tests for scenarios above
4. [ ] Verification step

---
*Generated by requirements-refiner skill*
*Saved to: agent-workflow/requirements/[filename].md*
```

## Claude Code Commands

Quick reference for commands used by this skill:

```bash
# Auto-detect stack
ls package.json go.mod requirements.txt pyproject.toml pom.xml 2>/dev/null

# Read project conventions
cat CLAUDE.md 2>/dev/null

# Validate file exists
test -f "path/to/file.js" && echo "EXISTS" || echo "CREATE"

# Read existing pattern
cat path/to/similar/file.js | head -100

# Create output directory
mkdir -p agent-workflow/requirements

# Save refined PRD
cat > agent-workflow/requirements/YYYYMMDD-feature-name.md << 'EOF'
[content]
EOF

# Scaffold files (with conflict check)
test -f "path/to/file.js" && cp "path/to/file.js" "path/to/file.js.new" || touch "path/to/file.js"
```

## Examples

See `references/transformation-patterns.md` for detailed before/after examples including:
- API integration features
- Data model changes
- Complex verification flows

## Anti-Patterns

1. **Narrative flow** — Use structured sections, not stories
2. **Embedded paths** — Consolidate all paths in File Mappings
3. **Implicit comparisons** — "Like existing flow" needs explanation
4. **Mixed concerns** — Separate UI copy from business logic
5. **Missing edge cases** — Explicitly list: what if X fails?
6. **Not reading existing code** — Always `cat` similar files first
7. **Not saving output** — Always save to `agent-workflow/requirements/`
