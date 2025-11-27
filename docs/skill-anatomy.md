# Skill Anatomy

A look at how I structure my skills.

## Basic Structure

```
skill-name/
├── SKILL.md              # The main file (required)
├── references/           # Deep docs (optional)
├── scripts/              # Tools (optional)
└── evals/                # Tests (optional)
```

## SKILL.md

This is what Claude reads first. I keep it scannable:

```markdown
---
name: debugging-orm-queries
description: Converts ORM calls to raw SQL...
---

# Debugging ORM Queries

## References
| Topic | Link |
|-------|------|
| Node.js ORMs | [references/nodejs.md] |

## Scripts
python scripts/query_analyzer.py logs.txt

## Quick Patterns
**Enable logging**: Check reference for ORM-specific config
**Find N+1**: Run query_analyzer on your logs
```

Quick patterns at the bottom for common stuff.

## references/

This is where the detailed docs go. I organize by:

**Language/framework:**
```
references/
├── nodejs.md
├── python.md
└── golang.md
```

**Or by topic:**
```
references/
├── sql-patterns.md
├── anti-patterns.md
└── security-checklist.md
```

Whatever makes sense for the skill.

## scripts/

Helper tools. Rules I follow:
- Python stdlib only
- CLI-friendly (argparse, stdout)
- Usage in docstring

Example from my query analyzer:
```python
#!/usr/bin/env python3
"""
Detect N+1 queries from logs.

Usage:
    python query_analyzer.py queries.log [--json]
"""
```

## Size Guidelines

Rough targets:
- SKILL.md: 50-150 lines
- Each reference: 200-500 lines
- Scripts: 50-300 lines
- Total skill: under 200KB

Keep SKILL.md tight. If it's getting long, move stuff to references.
