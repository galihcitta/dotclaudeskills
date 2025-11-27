# Creating Skills

## The Basics

A skill is just a folder with a `SKILL.md` file. That's the minimum.

```
my-skill/
└── SKILL.md
```

## SKILL.md Format

```markdown
---
name: my-skill-name
description: What it does and when Claude should use it.
---

# My Skill

Your content here...
```

The `description` matters - it tells Claude when to activate this skill. Be specific about the trigger.

Good: "Helps debug N+1 queries in Prisma, Sequelize, and TypeORM"
Bad: "Helps with database stuff"

## Adding More Structure

For bigger skills, add references and scripts:

```
my-skill/
├── SKILL.md              # Main file - quick reference
├── references/           # Detailed docs
│   ├── framework-a.md
│   └── framework-b.md
└── scripts/              # Helper tools
    └── analyzer.py
```

Keep SKILL.md scannable. Put the deep stuff in `references/`.

## Scripts

If you add scripts:
- Python stdlib only (no pip dependencies)
- Include usage examples
- Make them CLI-friendly

```python
#!/usr/bin/env python3
"""
What this does.

Usage:
    python script.py input.txt
"""
```

## Testing

1. Copy to `~/.claude/skills/your-skill/`
2. Open Claude Code
3. Try requests that should trigger it
4. Iterate

## Tips

- Start with SKILL.md only, add structure as needed
- The description is your trigger - make it clear
- Tables work great for reference data
- Keep code examples copy-pasteable
