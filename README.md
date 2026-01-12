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
| [writing-skills](skills/writing-skills/) | Guides creating new skills using TDD - test with subagents first, write skill to address failures, iterate until bulletproof. |
| [testing-skills-with-subagents](skills/testing-skills-with-subagents/) | Tests skills before deployment using RED-GREEN-REFACTOR cycle. Runs baseline without skill, writes to fix failures, closes loopholes. |
| [troubleshooting-kubernetes](skills/troubleshooting-kubernetes/) | Diagnoses K8s issues (CrashLoopBackOff, OOMKilled, ImagePullBackOff, pending pods) with interactive remediation. Always presents fix options before applying. |
| [code-reviewer](skills/code-reviewer/) | Comprehensive code review with automated analysis, security scanning, and checklist generation. Supports TypeScript, JavaScript, Python, Swift, Kotlin, Go. |
| [detecting-ai-code](skills/detecting-ai-code/) | Systematic framework for detecting AI-generated code with tiered signal detection and confidence scoring. Use for auditing acquisitions, contractors, or code review. |
| [prd-to-ralph](skills/prd-to-ralph/) | Converts PRDs into structured JSON for Ralph Wiggum autonomous coding loops. Orders stories by dependency, auto-adds quality gates. |
| [generating-adrs](skills/generating-adrs/) | Extracts architectural decisions from PRDs/TRDs and generates MADR-format ADR documents. One ADR per decision point. |
| [interviewing-plans](skills/interviewing-plans/) | Interviews vague plans to surface hidden assumptions. Uses 8 required categories (Technical, UX, Tradeoffs, Edge Cases, Security, Testing, Rollback, Dependencies). |

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
ln -s "$(pwd)/skills/writing-skills" ~/.claude/skills/
ln -s "$(pwd)/skills/testing-skills-with-subagents" ~/.claude/skills/
ln -s "$(pwd)/skills/troubleshooting-kubernetes" ~/.claude/skills/
ln -s "$(pwd)/skills/code-reviewer" ~/.claude/skills/
ln -s "$(pwd)/skills/detecting-ai-code" ~/.claude/skills/
ln -s "$(pwd)/skills/prd-to-ralph" ~/.claude/skills/
ln -s "$(pwd)/skills/generating-adrs" ~/.claude/skills/
ln -s "$(pwd)/skills/interviewing-plans" ~/.claude/skills/
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

**When I'm building a new skill:**
```
> Create a skill for [task]
> Test this skill with subagents
> Run baseline without the skill first
```

**When my pods are crashing or services unreachable:**
```
> Pod keeps crashing with OOMKilled
> Service returning 502, help me debug
> Deployment stuck in pending
```

**When reviewing code or PRs:**
```
> Review this PR for issues
> Check this code for security problems
> Generate a code review checklist
```

**When auditing code for AI authorship:**
```
> Check if this code was AI-generated
> Audit this codebase for AI patterns
```

**When converting PRDs to Ralph format:**
```
> Convert this PRD to Ralph JSON
> Prepare these requirements for autonomous iteration
```

**When documenting architectural decisions:**
```
> Generate ADRs from this PRD
> Document the decisions in this spec
```

**When plans are vague or ambiguous:**
```
> Interview this plan for hidden assumptions
> This PRD says "make it faster" - help me clarify
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
