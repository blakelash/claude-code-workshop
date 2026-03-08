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

Look at `examples/deseq2-workflow/SKILL.md` for a complete example. Key components:

### 1. Context
What is this skill for? When should Claude use it?

### 2. Inputs
What does Claude need to start? (file paths, parameters, metadata)

### 3. Steps
The exact procedure, in order. Be specific — "normalize the data" is too vague, "apply DESeq2 median-of-ratios normalization using pydeseq2" is right.

### 4. Output expectations
What should the outputs look like? File formats, required columns, figure specifications.

### 5. Failure modes
What can go wrong? What should Claude check for? When should it stop and ask for help?

## Example skills

This module includes three example skills of varying complexity:

| Skill | Complexity | Domain |
|-------|-----------|--------|
| `parse-lab-excel/` | Simple | General |
| `deseq2-workflow/` | Medium | Genomics |
| `image-segmentation/` | Complex | Imaging |

## Live build exercise

1. Open `live-build/scaffold.md` — this is a blank skill template
2. Pick a task from your own work that you do repeatedly
3. Fill in the scaffold with your specific procedure
4. Test it: start a Claude session, point it at your skill, and ask it to execute

Ideas for your first skill:
- Parsing a specific instrument's output format
- Your lab's standard QC pipeline
- A figure generation protocol for your paper
- Data cleanup for a recurring experiment type

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

## Key lesson

**Skills are how you get compounding returns from Claude Code.** Every SOP you encode is work you'll never re-explain. The lab that builds this well has a permanent advantage.
