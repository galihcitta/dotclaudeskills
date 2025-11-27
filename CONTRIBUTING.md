# Contributing

Want to add a skill or improve one? Cool, here's how.

## Adding a New Skill

1. Fork this repo
2. Create `skills/your-skill-name/` with at least a `SKILL.md`
3. Test it with Claude Code
4. Open a PR

### Skill Structure

```
skills/your-skill-name/
├── SKILL.md        # Required
├── references/     # Optional - for detailed docs
└── scripts/        # Optional - helper tools
```

### SKILL.md Format

```markdown
---
name: your-skill-name
description: What it does and when to use it.
---

# Your Skill

Content here...
```

The `description` is important - it tells Claude when to activate the skill.

### Quick Checklist

- [ ] Has a `SKILL.md` with name and description
- [ ] Description clearly says when to use it
- [ ] Scripts (if any) use Python stdlib only - no pip installs
- [ ] Actually tested it works

## Improving Existing Skills

Found a bug or want to add something? Just:

1. Fork
2. Make changes
3. Test
4. PR

## Scripts

If you add scripts:
- Python stdlib only (no dependencies)
- Include usage in a docstring
- Make them work from command line

## Questions?

Open an issue.
