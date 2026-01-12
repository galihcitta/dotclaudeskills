# Baseline Test Results

## Test Date: 2026-01-10

## Scenario B: Out-of-Order PRD

### Input
PRD with 4 stories in wrong order: UI Bell → UI Preferences → Schema → API

### Baseline Output (WITHOUT skill)

```json
{
  "userStories": [
    {"id": "US-001", "title": "Notification Bell UI", "priority": 1},
    {"id": "US-002", "title": "Notification Preferences", "priority": 2},
    {"id": "US-003", "title": "Notification Database Schema", "priority": 1},
    {"id": "US-004", "title": "Notification API", "priority": 1}
  ]
}
```

**Failures:**
- Stories in PRD order, not dependency order
- Multiple stories with priority 1 (incorrect)
- Missing all 4 standard criteria on every story

### GREEN Output (WITH skill)

```json
{
  "userStories": [
    {"id": "US-001", "title": "Notification Database Schema", "priority": 1},
    {"id": "US-002", "title": "Notification API", "priority": 2},
    {"id": "US-003", "title": "Notification Bell UI", "priority": 3},
    {"id": "US-004", "title": "Notification Preferences", "priority": 3}
  ]
}
```

**Fixes applied:**
- Stories reordered by dependency (Schema → API → UI)
- Correct priority assignment by layer
- All 4 standard criteria present on every story

## Comparison Table

| Metric | Baseline | With Skill | Pass |
|--------|----------|------------|------|
| Dependency order | No | Yes | PASS |
| Priority by layer | No | Yes | PASS |
| Standard criteria | 0/4 | 4/4 | PASS |
| Valid JSON | Yes | Yes | PASS |
| Required fields | Yes | Yes | PASS |

## Conclusion

Skill successfully addresses all baseline failures:
1. Enforces dependency-aware ordering
2. Assigns priorities based on layer classification
3. Auto-appends standard quality criteria
