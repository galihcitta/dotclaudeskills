# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

Collection of Claude Code skills for database debugging and query optimization. Skills are specialized knowledge modules that activate automatically when Claude encounters relevant tasks.

## Skill Structure

Each skill lives in `skills/<skill-name>/` with this structure:

```
skill-name/
├── SKILL.md              # Required - main skill file
├── references/           # Optional - detailed documentation
├── scripts/              # Optional - helper tools
└── evals/                # Optional - test cases
```

### SKILL.md Format

Required frontmatter with `name` and `description`:

```markdown
---
name: skill-name
description: What it does and when Claude should use it.
---

# Skill Title

Content...
```

The `description` field is critical - it determines when Claude activates the skill. Be specific about trigger conditions.

### Size Guidelines
- SKILL.md: 50-150 lines (scannable, quick reference)
- Each reference file: 200-500 lines
- Scripts: 50-300 lines
- Total skill: under 200KB

Move detailed content to `references/` to keep SKILL.md tight.

## Script Conventions

- Python standard library only (no pip dependencies)
- CLI-friendly with argparse
- Include usage example in docstring
- Output to stdout for piping

## Installation

Skills install via symlink to `~/.claude/skills/`:

```bash
ln -s "$(pwd)/skills/debugging-orm-queries" ~/.claude/skills/
```

## Testing Skills

1. Copy/symlink to `~/.claude/skills/your-skill/`
2. Open Claude Code
3. Try requests that should trigger the skill
4. Iterate on SKILL.md description if activation is wrong
