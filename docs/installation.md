# Installation

## Quick Setup

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/dotclaudeskills.git
cd dotclaudeskills

# Symlink the skills you want
ln -s "$(pwd)/skills/debugging-orm-queries" ~/.claude/skills/
ln -s "$(pwd)/skills/optimizing-queries" ~/.claude/skills/
ln -s "$(pwd)/skills/refining-requirements" ~/.claude/skills/
ln -s "$(pwd)/skills/creating-handoffs" ~/.claude/skills/
ln -s "$(pwd)/skills/writing-skills" ~/.claude/skills/
ln -s "$(pwd)/skills/testing-skills-with-subagents" ~/.claude/skills/
```

Done. Skills activate automatically when you ask something relevant.

## Why Symlinks?

When you `git pull` updates, your skills update too. No need to copy again.

## Alternative: Direct Copy

If you prefer copying:

```bash
cp -r skills/debugging-orm-queries ~/.claude/skills/
cp -r skills/optimizing-queries ~/.claude/skills/
```

Just remember to copy again when there are updates.

## Check It Worked

```bash
ls ~/.claude/skills/
# Should show your linked skills
```

## Uninstall

Just remove the symlink or folder:

```bash
rm ~/.claude/skills/debugging-orm-queries
```
