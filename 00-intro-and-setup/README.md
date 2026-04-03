# Module 00 — Intro & Setup

## What Claude Code is (and isn't)

Claude Code is a command-line AI assistant that runs in your terminal. It can:

- **Read and write real files** on your machine
- **Execute real code** (Python, R, shell commands)
- **Navigate your project** by reading directory structures and file contents
- **Iterate with you** in a conversational loop

It is **not**:
- A chatbot (it takes actions, not just gives answers)
- Copilot-style autocomplete (it works at the task level, not the line level)
- A replacement for your scientific judgment

## Installation

```bash
# Native installer (recommended)
curl -fsSL https://claude.ai/install.sh | sh
```

Claude Code also runs as a **VS Code or JetBrains extension**, a **desktop app** (macOS/Windows), and at **claude.ai/code** in the browser. The CLI is the primary interface for this workshop, but the same skills transfer.

Keep Claude Code up to date:
```bash
claude update
```

## Authentication

**Option A — API key (workshop default):**
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

**Option B — Claude Pro/Max subscription:**
Claude Code will prompt you to log in via browser on first run.

## Sanity check

```bash
# Start Claude Code in this directory
cd 00-intro-and-setup
claude

# Try asking:
# "What files are in this directory?"
# "Read the CLAUDE.md in project-structure-example and summarize it"
```

## Mental model: You're the PI, Claude is a postdoc

Claude is fast, capable, and tireless — but it doesn't know your scientific question, your lab's conventions, or when a result looks biologically wrong. You direct. You verify. You ensure rigor.

**Claude Code is only as good as the context you give it.** The rest of this workshop is about giving it great context.

## Project structure matters

Look at the `project-structure-example/` directory. This is a minimal but well-organized project layout. Claude reads your directory tree to orient itself — a clean structure helps it find the right files and understand your project. Claude can help you do this, but I highly recommend to organize your projects for most effective use of Claude. 

```
project-structure-example/
├── CLAUDE.md              ← Claude reads this first, every session
├── data/
│   ├── raw/               ← original, untouched data
│   └── processed/         ← cleaned/normalized data
├── results/
│   └── figures/           ← generated plots and visualizations
└── scripts/               ← analysis code
```

## Introducing CLAUDE.md

Every project can have a `CLAUDE.md` file at its root. Claude reads this file at the start of every session — it's your way of telling Claude about your project before you even type a prompt.

We'll cover this deeply in Module 03, but for now just know: it exists, it gets read automatically, and it's powerful.

## Key commands to know before you start

Claude Code has slash commands you can type at any point during a session. You'll learn more throughout the workshop, but two are worth knowing right now:

### `/help`

Shows available commands and usage info. When in doubt, start here.

### `/permissions`

Controls what Claude can do without asking you first. By default, Claude will ask before writing files, running code, or executing shell commands. You can grant broader permissions if you trust the workflow:

```
/permissions
```

This opens an interactive menu where you can allow or restrict specific tool categories. For this workshop, the defaults are fine — Claude will ask before doing anything potentially destructive.

### `/powerup`

Interactive lessons with animated demos — a quick way to explore Claude Code features hands-on. Good to run once you're set up:

```
/powerup
```

> **Tip:** See the `CHEATSHEET.md` in the repo root for a full list of slash commands.

## Exercise

1. Install Claude Code if you haven't already
2. Navigate to this directory and start a session (`claude`)
3. Try `/help` to see available commands
4. Ask Claude: "What is this workshop about?"
5. Ask Claude: "Look at the project-structure-example directory and tell me how it's organized"
6. Try: "Read the CLAUDE.md in project-structure-example and explain what conventions it sets"
