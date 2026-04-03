# Module 05 — Subagents and Agent Teams

## Subagents ≠ pipelines ≠ agent teams

Three different things that people conflate:

| Concept | What it is | When to use it |
|---------|-----------|----------------|
| **Pipeline** | Fixed steps, fixed logic, no judgment | Snakemake, Nextflow, bash scripts — not agents |
| **Subagents** | Workers spawned within one session, each with fresh context, reporting back to the parent | When a task requires reasoning per unit of work, or you want to keep verbose output out of your main context |
| **Agent teams** | Multiple independent Claude Code sessions coordinating via shared task list and messaging | When workers need to communicate with each other, challenge each other's findings, or coordinate across files |

The key question: **does the task require judgment, or just execution?**

- Processing 48 FASTQ files through trimming → alignment → counting? That's a pipeline. Use Snakemake (but Claude can help you write and QC the pipeline!).
- Reviewing 8 analysis notebooks for statistical errors? That requires reasoning per notebook. Use subagents.
- Having separate agents investigate competing hypotheses about why an experiment failed, then debate each other? They need to communicate. That's an agent team.

## Subagents in Claude Code

Subagents are specialized workers that run **within your current session**. Each gets its own context window, does its work, and reports results back. They cannot talk to each other — only back to the parent.

```
Your session (parent)
├── Subagent 1 → reads, reasons, reports back
├── Subagent 2 → reads, reasons, reports back
├── Subagent 3 → reads, reasons, reports back
└── Parent synthesizes across results
```

### Built-in subagents

Claude Code already has subagents it uses automatically:

| Subagent | Model | What it does |
|----------|-------|-------------|
| **Explore** | Haiku (fast) | Read-only codebase search and exploration |
| **Plan** | Inherits | Gathers context during plan mode |
| **General-purpose** | Inherits | Complex multi-step tasks requiring both reading and writing |

You've been using these without realizing it — when Claude searches your codebase, it often delegates to the Explore subagent to keep search results out of your main context.

### Custom subagents

You can define your own subagents as markdown files in `.claude/agents/` (project-level) or `~/.claude/agents/` (user-level). Each file has YAML frontmatter for configuration and markdown body for the system prompt:

```markdown
---
name: stats-reviewer
description: Reviews analysis scripts for statistical rigor. Use proactively after writing analysis code.
allowed-tools: Read, Grep, Glob
model: sonnet
auto-memory: true
skills:
  - deseq2-workflow
---

You are a statistical reviewer for scientific code. When invoked, check:

1. Are effect sizes reported alongside p-values?
2. Is multiple testing correction applied (Benjamini-Hochberg preferred)?
3. Are sample sizes checked (flag if n < 3 per group)?
4. Are random seeds set for all stochastic operations?
5. Are the chosen tests appropriate for the data distribution?

Report findings with specific line numbers and suggested fixes.
Organize by priority: critical (invalidates results) vs minor (best practice).
```

Claude will automatically delegate to this subagent when it encounters tasks matching the description. You can also invoke it explicitly: *"Use the stats-reviewer subagent on scripts/analysis.py"*

Two useful subagent frontmatter options shown above:
- **`auto-memory: true`** — the subagent maintains its own auto memory (stored separately from the main session's memory), so it accumulates knowledge about the scripts it reviews over time
- **`skills:`** — preload specific skills into the subagent's context so it has relevant procedures available without needing to search for them

For parallel or long-running work, you can also set `background: true` and `isolation: "worktree"` in agent calls — the subagent runs in an isolated git worktree so its file changes don't interfere with your main session.

> **Tip**: Use `/agents` in Claude Code to create and manage subagents interactively.

### When subagents make sense

Subagents are good when:

1. **Each unit of work requires judgment** — not just running a fixed procedure
2. **Workers are independent** — no worker needs another worker's output
3. **You want to preserve main context** — keeping verbose search/analysis output out of your conversation
4. **Consistency matters** — each worker gets the same instructions from the subagent definition

### Example: reviewing analysis scripts in parallel

```
I have 6 analysis scripts in scripts/. Each was written by a different
rotation student. Use the stats-reviewer subagent on each script.
After all reviews are done, synthesize the common issues across all scripts.
```

Each subagent worker reads a script, *understands* what it does, checks it against the review criteria, and reports back. The parent then synthesizes across all six reviews.

### Example: researching across subfields

```
I need to understand how three fields approach single-cell clustering.
Research each area using separate subagents:

1. Read the immunology papers in papers/immunology/ — summarize batch effect approaches
2. Read the neuroscience papers in papers/neuro/ — summarize cluster validation methods
3. Read the cancer biology papers in papers/onco/ — summarize heterogeneity handling

After all workers finish, synthesize where these fields agree and diverge.
```

Each worker reads and interprets papers — that's reasoning, not pipeline execution.

### Where subagents go wrong

1. **Using them for pipeline work**: Processing files through fixed steps doesn't need reasoning → use Snakemake/Nextflow/bash
2. **Vague worker instructions**: Worker A interprets "check for errors" differently than Worker B → write specific subagent definitions with exact criteria
3. **Too many workers**: Each worker's results return to your main context. 20 detailed reports will flood it → batch workers or have them write results to disk
4. **Overkill**: Using subagents for 2-3 items that would take 5 minutes in one session → just do it sequentially

### Running parallel sessions with `--worktree`

For heavy parallel workloads, you can launch separate Claude Code sessions in isolated git worktrees with the `-w` flag:

```bash
claude -w   # starts in a new worktree
```

Each worktree gets its own branch. The sessions operate independently and can't accidentally overwrite each other's work. This is the lower-level alternative to agent teams — useful when you want fully independent sessions that you manually coordinate.

## Agent teams: when workers need to talk to each other

> **Note**: Agent teams are experimental and disabled by default. Enable with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` in settings.

Subagents report back to the parent but can't communicate with each other. Agent teams are different: they're **multiple independent Claude Code sessions** with a lead that coordinates, a shared task list, and direct messaging between teammates.

```
Lead session
├── Teammate 1 ──────────┐
├── Teammate 2 ◄─────────┤ teammates can message each other
├── Teammate 3 ──────────┘
└── Shared task list (teammates claim and complete tasks)
```

### Subagents vs agent teams

|  | Subagents | Agent teams |
|--|-----------|-------------|
| **Context** | Own context, results return to parent | Fully independent sessions |
| **Communication** | Report to parent only | Teammates message each other directly |
| **Coordination** | Parent manages everything | Shared task list, self-coordination |
| **Best for** | Focused tasks where only the result matters | Work requiring discussion and collaboration |
| **Token cost** | Lower | Higher (each teammate is a full session) |

### When agent teams make sense for scientists

- **Building apps with interacting components**: A dashboard with frontend, backend, and tests — teammates negotiate the API contract, then build to it
- **Competing hypotheses**: Teammates investigate different theories about why an experiment failed, then debate to converge on the root cause
- **Cross-layer code changes**: One teammate handles data processing, another handles visualization, another handles tests — they coordinate to keep interfaces consistent
- **Research and synthesis**: Teammates explore different aspects of a problem, share findings, and challenge each other's conclusions

### Example: building a lab data dashboard

```
Build a lab data dashboard with three teammates:
- "backend": FastAPI server that serves experiment QC data
- "frontend": HTML/JS interface that displays the data
- "tests": pytest tests for the API endpoints

The backend and frontend should agree on the API contract before building.
The tests should match the actual endpoints.
```

Why this needs an agent team: if you dispatched three independent subagents, the frontend would call `/api/experiments`, the backend would serve `/experiments/list`, and the tests would check `/get_experiments`. Three pieces that don't connect. Agent team teammates message each other to agree on interfaces first.

### Example: competing hypotheses about a failure

```
The clustering script produces different results every run.
Create an agent team to investigate:
- One teammate checks if random seeds are set everywhere
- One teammate checks if input data order is deterministic
- One teammate checks if package versions changed between runs
Have them share findings and challenge each other's theories.
```

The debate structure matters — a single agent tends to find one explanation and stop. Multiple agents actively trying to disprove each other are more likely to find the actual root cause.

## Decision guide

```
Does the task require reasoning per unit of work?
│
├─ NO → Use a pipeline tool (Snakemake, Nextflow, bash)
│
└─ YES → Do the workers need to communicate with each other?
         │
         ├─ NO → How many independent units?
         │       ├─ 2-3:  One session is fine
         │       └─ 4+:   Subagents
         │
         └─ YES → Agent team
```

## Examples and demo

| Resource | What it demonstrates |
|----------|---------------------|
| `examples/01-when-to-use-subagents.md` | Decision guide: pipeline vs subagent vs agent team |
| `examples/02-orchestrator-worker.md` | The subagent pattern with a worked code review example |
| `examples/03-code-review-dispatch/` | Orchestrator and worker prompts for script review |
| `demo/` | **Live demo materials** — see `demo/DEMO_GUIDE.md` |
| `demo/agents/` | Three custom subagent definitions (stats, figures, reproducibility) |
| `demo/scripts/` | Three intentionally flawed analysis scripts to review |
| `demo/DEMO_GUIDE.md` | Full walkthrough: subagent review demo + agent team build demo |

## Key lesson

**Subagents are for parallel reasoning, not parallel execution.** If each unit of work requires reading, understanding, and making judgments, subagents give each task fresh context. If workers need to talk to each other and challenge each other's findings, that's an agent team. And if the task is just running the same fixed steps on many inputs, use a pipeline tool — that's what they're for.
