# dotclaudeskills

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

Claude Code skills I use in my daily workflow. They help me debug ORM queries, optimize database performance, turn vague requirements into actionable specs, and create handoffs for seamless session transfers.

Feel free to use them, tweak them, or use them as a starting point for your own.

## What's a Skill?

Skills give Claude specialized knowledge for specific tasks. When you ask something that matches a skill's description, Claude automatically uses that knowledge to help you better.

Think of them as "expert modes" you can plug into Claude.

## Skills I've Built

| Skill | What it does |
|-------|--------------|
| [debugging-orm-queries](skills/debugging-orm-queries/) | Helps me trace ORM calls to raw SQL, catch N+1 queries, and debug slow database code. Works with Sequelize, Prisma, TypeORM, GORM, SQLAlchemy, Django ORM, and more. |
| [optimizing-queries](skills/optimizing-queries/) | Analyzes queries and suggests indexes, rewrites, and fixes. Covers PostgreSQL, MySQL, MongoDB, Redis, DynamoDB, Elasticsearch. |
| [refining-requirements](skills/refining-requirements/) | Takes messy PRDs or feature ideas and turns them into clean, implementable specs. Auto-detects tech stack. |
| [creating-handoffs](skills/creating-handoffs/) | Creates handoff documents for seamless AI agent session transfers. Solves context exhaustion in long-running sessions. |

## Getting Started

```bash
# Clone
git clone https://github.com/galihcitta/dotclaudeskills.git
cd dotclaudeskills

# Link to Claude (symlinks keep them updated when you pull)
ln -s "$(pwd)/skills/debugging-orm-queries" ~/.claude/skills/
ln -s "$(pwd)/skills/optimizing-queries" ~/.claude/skills/
ln -s "$(pwd)/skills/refining-requirements" ~/.claude/skills/
ln -s "$(pwd)/skills/creating-handoffs" ~/.claude/skills/
```

That's it. Skills activate automatically when relevant.

## How I Use These

**When my Prisma queries are slow:**
```
> Why is this query slow? [paste query]
> Is this an N+1 problem?
> Show me the raw SQL
```

**When I need to optimize a query:**
```
> This takes 5 seconds, help me speed it up
> What indexes should I add?
> Check this for anti-patterns
```

**When I get vague requirements:**
```
> Refine this PRD: "we need user dashboard"
> Turn this into a proper spec
> New project from scratch: task management API
```

**When context is getting full or I need to pause:**
```
> Create a handoff
> Save state before I close this session
> Resume from handoff
> Continue where we left off
```

## Want to Build Your Own?

Check out [docs/creating-skills.md](docs/creating-skills.md) - it's pretty straightforward.

Basic structure:
```
your-skill/
├── SKILL.md        # Required - the main skill file
├── references/     # Optional - detailed docs
└── scripts/        # Optional - helper scripts
```

## Contributing

Got a skill you want to share? PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) - do whatever you want with these.
