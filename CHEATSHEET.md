# Claude Code Cheat Sheet

Quick reference for slash commands, keyboard shortcuts, and CLI flags.

## Slash commands (use inside a session)

| Command | What it does | Module |
|---------|-------------|--------|
| `/help` | Show available commands and usage info | 00 |
| `/permissions` | View and configure what Claude can do without asking | 00 |
| `/plan` | Enter planning mode — Claude outlines an approach before executing | 01 |
| `/clear` | Wipe session context (disk state preserved, CLAUDE.md reloaded) | 02 |
| `/compact` | Compress conversation history to free context space | 02 |
| `/compact [focus]` | Compress with a hint about what to prioritize | 02 |
| `/memory` | Add a convention or preference to CLAUDE.md from the session | 03 |
| `/model [name]` | Switch to a different model mid-session | 06 |
| `/cost` | Show token usage and estimated cost for the current session | 06 |

## CLI flags (use when starting Claude)

```bash
# Start Claude Code
claude

# Start with a specific model
claude --model claude-sonnet-4-6
claude --model claude-opus-4-6

# Start in plan mode
claude --plan

# Resume the most recent session
claude -c

# Go to sessions screen
claude --resume

#Run in skip permissions mode
claude --dangerously-skip-permissions

# Start with a specific prompt (non-interactive)
claude -p "summarize the data in results/"

# Print output as JSON (useful for scripting)
claude -p "list all CSV files" --output-format json
```

## Keyboard shortcuts (during a session)

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message |
| `Escape` | Cancel current generation |
| `Ctrl+C` | Cancel current generation / exit if idle |
| `Up/Down` | Scroll through prompt history |
| `Tab` | Accept autocomplete suggestion |

## Context management quick reference

| Situation | Action |
|-----------|--------|
| Session feels sluggish | `/compact` or `/clear` |
| Claude is confused or contradicting itself | `/clear` |
| Switching to a different task | Start a new session (`exit` + `claude`) |
| Want to preserve a correction for next time | `/memory [the convention]` |
| Long analysis, need fresh context | `/clear` then re-orient from files on disk |

## Model selection quick reference

| Task type | Model | Why |
|-----------|-------|-----|
| Data wrangling, parsing, file I/O | Sonnet | Fast, cheap, execution-focused |
| Making and iterating on plots | Sonnet | Iteration speed matters most |
| Writing analysis scripts | Sonnet | Handles 90% of code tasks |
| Statistical model selection | Opus | Needs deeper reasoning |
| Interpreting ambiguous results | Opus | Nuance and domain reasoning |
| Writing methods sections | Opus | Precision and completeness |
| Debugging subtle scientific errors | Opus | Needs to reason about correctness |

## The core workflow

```
1. Start session in your project directory
2. /plan for complex tasks (optional)
3. Ask → Inspect → Correct → Repeat
4. /compact when context gets heavy
5. /clear or new session when switching tasks
6. /memory to save corrections for next time
```

## File hierarchy Claude reads automatically

```
~/.claude/CLAUDE.md          ← your personal preferences (all projects)
./CLAUDE.md                  ← project conventions (this project)
./skills/*/SKILL.md          ← specialized procedures (referenced from CLAUDE.md)
```
