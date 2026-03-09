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
- **Infrastructure knowledge** — teach Claude how your compute environment works (e.g., SLURM partitions, which queue to use for GPU jobs vs. CPU jobs, module load commands, scratch vs. home directory paths)

> **Connection to context management:** In Module 02 we saw that every token in context costs attention and money. `CLAUDE.md` is loaded **in full** into context at the start of every session, automatically — it counts against your 200k token limit just like everything else. That's why you want to keep it focused and accurate: it's always there, Claude treats it as ground truth, and bloated instructions eat into your working space. If you have more detailed instructions for Claude on how to do specific things, this does not go here, we will talk about this in the next module. 

### `/memory` — view and edit memory files

The `/memory` command shows you all the CLAUDE.md and rules files loaded in your current session. From there you can:

- See which files Claude is actually reading (useful for debugging "why isn't Claude following my rule?")
- Select any file to open it in your editor
- Toggle auto memory on or off

```
/memory
```

If you want Claude to remember something, just tell it in conversation:

```
Remember: always use log2 fold change, not log10, for DE volcano plots
```

Claude saves this to its auto memory (see below). If you want the instruction in `CLAUDE.md` instead, say so explicitly ("add this to CLAUDE.md") or open the file through `/memory` and edit it yourself.

### 3. Auto memory — Claude takes its own notes

Auto memory lets Claude accumulate knowledge across sessions without you writing anything. As you work, Claude decides what's worth saving — build commands, debugging insights, code style preferences, workflow patterns — and writes notes for itself that persist to future sessions.

**Where it lives:** each project gets a memory directory at `~/.claude/projects/<project>/memory/`, containing:

```
memory/
├── MEMORY.md          # Concise index, loaded every session (first 200 lines)
├── debugging.md       # Detailed notes on debugging patterns
├── patterns.md        # Code patterns and conventions
└── ...                # Any other topic files Claude creates
```

**How it works:**
- The first 200 lines of `MEMORY.md` are loaded at the start of every conversation
- Claude keeps `MEMORY.md` concise by moving detailed notes into separate topic files
- Topic files are read on demand, not loaded at startup
- Auto memory is machine-local and scoped per git repository

**What gets saved:** Claude doesn't save something every session. It saves things like:
- Corrections you make ("use this test runner, not that one")
- Build/run commands it discovers
- Debugging insights that would help in future sessions
- Architecture or workflow patterns specific to the project

**Editing auto memory:** everything is plain markdown. You can read, edit, or delete any file at any time. Run `/memory` to browse what Claude has saved.

**Disabling auto memory:** it's on by default. Toggle it via `/memory` or set `"autoMemoryEnabled": false` in your project settings.

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
Be specific. Not just "use Python" — say "use pandas 2.x, seaborn 0.13+, scanpy 1.10+" (or using a package manager like uv with pinned deps in pyproject.toml is even better)

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

**`CLAUDE.md` is loaded every session — it costs tokens but saves time.** Every convention you encode here is work you'll never re-explain. Build it incrementally — add a new rule every time you catch yourself correcting Claude on the same thing twice.
