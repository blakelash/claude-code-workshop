# Module 03 — Memories & CLAUDE.md

## Two levels of persistent context

Claude Code has two mechanisms for remembering things across sessions:

### 1. User-level memory (`~/.claude/CLAUDE.md`)

Your personal preferences that apply to **every** project:

- "Always use dark-background figures"
- "I prefer concise explanations"
- "Default to Python, not R"

### 2. Project-level memory (`CLAUDE.md` in your project root)

Project-specific conventions that apply to **this** project:

- Genome build and annotation version
- Preferred packages and their versions
- Statistical defaults
- File naming conventions
- Output format requirements

### `/memory` — quick-add memories from a session

You can add to your project or user memory without editing files manually. The `/memory` command lets you save a convention or preference on the fly:

```
/memory always use log2 fold change, not log10, for DE volcano plots
```

This appends to your `CLAUDE.md` so it persists across sessions. Useful when you catch yourself correcting Claude — instead of correcting and moving on, correct and `/memory` so it never happens again.

## Why this matters

Every convention you put in `CLAUDE.md` is a mistake Claude will never make again.

Without `CLAUDE.md`:
```
You: Make a plot of the gene expression
Claude: *uses base matplotlib, 72 DPI, rainbow colormap*
You: No, use seaborn with colorblind palette, 300 DPI
Claude: *fixes it*
You: *next session, same conversation again*
```

With `CLAUDE.md`:
```
You: Make a plot of the gene expression
Claude: *reads CLAUDE.md, uses seaborn, colorblind palette, 300 DPI, publication-ready*
```

Every. Single. Time.

## Anatomy of a good CLAUDE.md

Look at `templates/CLAUDE.md.biology-lab` for a full example. Key sections:

### Project overview
What is this project? One paragraph. Claude needs to know what it's working on.

### Preferred tools and packages
Be specific. Not just "use Python" — say "use pandas 2.x, seaborn 0.13+, scanpy 1.10+".

### Data conventions
- Where does raw data live? Processed data?
- What genome build? What annotation source?
- File naming patterns

### Analysis conventions
- Default statistical tests
- Multiple testing correction method
- Minimum sample sizes
- When to flag for human review

### Output conventions
- Figure size, DPI, color palette
- File formats (PNG for quick looks, PDF for publications)
- Naming patterns for output files

## Templates

This module includes three templates of increasing specificity:

| Template | Use case |
|----------|----------|
| `CLAUDE.md.minimal` | Starting point — fill in your own conventions |
| `CLAUDE.md.biology-lab` | Full example for a molecular biology / genomics lab |
| `CLAUDE.md.imaging-lab` | Full example for a microscopy / image analysis lab |

## Exercise

1. Look at `templates/CLAUDE.md.biology-lab` to understand the format
2. Copy `templates/CLAUDE.md.minimal` to a new file
3. Fill it in with your own lab's conventions (spend 10 minutes on this)
4. Start a Claude session and test it: ask Claude to do something that your conventions should influence
5. Verify Claude follows your conventions without being told

## Key lesson

**`CLAUDE.md` is free context, loaded every session.** Every convention you encode here is work you'll never re-explain. Build it incrementally — add a new rule every time you catch yourself correcting Claude on the same thing twice.
