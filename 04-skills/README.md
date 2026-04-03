# Module 04 — Skills

## What is a skill?

A skill is a `SKILL.md` file that gives Claude deep, specific instructions for a specialized task. Think of it as an SOP (Standard Operating Procedure) — but one Claude can actually execute.

You reference skills in your `CLAUDE.md` so Claude knows they exist:

```markdown
## Available skills

- DESeq2 workflow: see skills/deseq2-workflow/SKILL.md
- Image segmentation: see skills/image-segmentation/SKILL.md
- Parse lab Excel files: see skills/parse-lab-excel/SKILL.md
```

Then when you ask Claude to do that task, it reads the skill file and follows the procedure exactly.

## The SOP analogy

Scientists already write SOPs. Every lab has them — for library prep, for staining protocols, for analysis pipelines. A skill is the same thing, but executable:

| Traditional SOP | Claude Skill |
|----------------|--------------|
| Written for humans | Written for Claude (and humans) |
| Interpreted loosely | Followed precisely |
| Gets stale in a binder | Lives in version control |
| Training takes hours | Claude reads it in seconds |
| One person's knowledge | Shared across the lab |

## Anatomy of a skill

Look at `skills/deseq2-workflow/SKILL.md` for a complete example.

### What gets loaded into context and when

This is the key design insight — a skill has two parts that are loaded at **different times**:

**1. YAML frontmatter** (`name` + `description`) — loaded **every session**, always in context. Claude reads these to know what skills exist and when to use them. Keep this short.

```yaml
---
name: deseq2-workflow
description: Run a bulk RNA-seq DE analysis using pydeseq2. Use when you have a raw count matrix and want to identify DE genes between two conditions.
---
```

**2. The markdown body** (everything below the frontmatter) — loaded **only when the skill is invoked**. This is where the detailed instructions live. This can be as long and specific as you need, because it only enters context when Claude actually needs it.

The frontmatter supports several useful options beyond just `name` and `description`:

| Option | What it does |
|--------|-------------|
| `paths:` | Only activate this skill when working with matching files (glob patterns) |
| `allowed-tools:` | Restrict which tools Claude can use within this skill |
| `model:` | Override the model for this skill (e.g., always run on Opus) |
| `effort:` | Override effort level (`low`/`medium`/`high`/`max`) |
| `context: fork` | Run this skill in a subagent so it doesn't pollute main context |
| `disable-model-invocation: true` | Claude will never auto-invoke this skill — only you can trigger it |

Example with several options set:

```yaml
---
name: deseq2-workflow
description: Run bulk RNA-seq DE analysis using pydeseq2.
model: claude-opus-4-6
effort: high
context: fork
paths:
  - "data/counts/**"
  - "results/de/**"
---
```

### Passing arguments to skills

Skills can accept arguments via `$ARGUMENTS` substitutions:

```
/deseq2-workflow data/counts_raw.csv KO vs WT
```

Inside the skill body:
- `$ARGUMENTS` — all arguments as a string
- `$1`, `$2`, `$3` — individual positional arguments

```markdown
Run DE analysis on $1 comparing $2 vs $3.
```

### Dynamic context injection

Skills can run shell commands at load time and inject the output into the skill body using `` !`command` `` syntax:

```markdown
## Current project state
Recent results: !`ls -la results/de/`
Active git branch: !`git branch --show-current`
```

This is useful for skills that need live data — for example, a QC skill that automatically reads the current sample manifest before running.

**3. Other files in the skill directory** — **never automatically loaded**. Your `SKILL.md` can reference companion files (example inputs, template scripts, reference configs), but Claude only reads them if it decides it needs to. This gives you a third tier of context: zero cost until Claude actively pulls it in.

```
skills/deseq2-workflow/
├── SKILL.md                  # loaded on invocation
├── example_invocation.md     # loaded only if Claude reads it
├── template_script.py        # loaded only if Claude reads it
└── expected_output.csv       # loaded only if Claude reads it
```

This is why skills exist as a separate concept from `CLAUDE.md`. If you put your entire DESeq2 SOP in `CLAUDE.md`, those 80+ lines are in context *every session* — even when you're doing something completely unrelated. With a skill, the frontmatter costs you ~30 tokens always, the full instructions only appear when invoked, and reference files only appear when needed.

### Body structure

The markdown body should include:

**Inputs** — What does Claude need to start? (file paths, parameters, metadata)

**Steps** — The exact procedure, in order. Be specific — "normalize the data" is too vague, "apply DESeq2 median-of-ratios normalization using pydeseq2" is right.

**Output expectations** — What should the outputs look like? File formats, required columns, figure specifications.

**Failure modes** — What can go wrong? What should Claude check for? When should it stop and ask for help?

## Example skills

This module includes three example skills of varying complexity:

| Skill | Complexity | Domain |
|-------|-----------|--------|
| `parse-lab-excel/` | Simple | General |
| `deseq2-workflow/` | Medium | Genomics |
| `image-segmentation/` | Complex | Imaging |

## Let Claude write your skills for you

You don't have to write skills from scratch. If you already have scripts, notebooks, or analysis code that represents your workflow, point Claude at it:

```
Look at my DE analysis pipeline in scripts/run_deseq2.py and
notebooks/de_analysis.ipynb. Write a SKILL.md that captures this
workflow so you can reproduce it on new datasets.
```

Claude will read your code, extract the logic, and draft a skill that mirrors what you actually do — not a generic textbook version. This is often better than writing from memory because:

- Your code captures the edge cases you've already handled
- Claude picks up on patterns you might not think to document (e.g., the specific filtering thresholds you use, the order you generate plots)
- You can iterate: "add the part where I check for batch effects" or "the QC step should also flag samples with < 1M reads"

This works especially well for turning one-off analyses into reusable skills. If you did it once in a notebook and it worked, that notebook is the blueprint.

## Live build exercise

In this exercise, Claude will build a skill for you from an existing notebook.

### Setup

Copy a Jupyter notebook from your own work into the `live-build/` directory. Pick one that represents a workflow you repeat — QC, DE analysis, plotting, data cleanup, etc.

If you don't have one handy, use the example notebook provided:
- `live-build/example_notebook.ipynb`

### Steps

1. Start a Claude Code session in this directory
2. Ask Claude to turn the notebook into a skill:
   ```
   Read the notebook in live-build/ and create a SKILL.md that
   captures this workflow as a reusable skill. Put it in
   live-build/my-skill/SKILL.md
   ```
3. Review what Claude generates — does it capture the key steps? The edge cases?
4. Iterate: ask Claude to add anything it missed, or remove anything too specific to the original dataset
5. Test it: ask Claude to execute the skill on different inputs

## The long-term vision

Imagine a lab with a `skills/` directory that grows over time:

```
skills/
├── deseq2-workflow/SKILL.md
├── cellpose-segmentation/SKILL.md
├── plate-reader-qc/SKILL.md
├── flow-cytometry-gating/SKILL.md
├── western-blot-quantification/SKILL.md
└── methods-section-writer/SKILL.md
```

A new lab member joins. On day one, they have access to the entire lab's accumulated analytical knowledge — executable, version-controlled, and always up to date.

## Built-in skills worth knowing

Claude Code ships with a few built-in skills that are immediately useful:

**`/simplify`** — reviews all files you've changed in a session for code quality and efficiency. It spawns three parallel review agents and fixes issues it finds. Good to run after a coding-heavy session before committing.

**`/batch <instruction>`** — for large-scale parallel changes across a codebase. Give it a high-level instruction ("add docstrings to all analysis scripts"), and it decomposes the work, spawns agents in isolated git worktrees, and opens PRs automatically. More relevant for software projects than typical analysis scripts, but worth knowing.

## Community skills for scientists

You don't have to start from zero. The [claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) repository is an open collection of ready-made skills for scientific workflows — bioinformatics, data analysis, figure generation, and more. Browse what's there, fork what's useful, and adapt to your lab's conventions.

## Key lesson

**Skills are how you get compounding returns from Claude Code.** Every SOP you encode is work you'll never re-explain. The lab that builds this well has a permanent advantage.
