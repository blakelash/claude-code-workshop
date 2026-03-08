# Module 05 — Subagents

## When one agent isn't enough

Most of the time, a single Claude session handles your task fine. But some tasks are bigger than one context window or naturally parallel:

- Processing 50 samples through the same pipeline
- Analyzing images from a 384-well plate
- Running the same QC checks across 20 datasets
- Comparing results across multiple experimental batches

This is where subagents come in.

## The orchestrator/worker pattern

Think of it like a Snakemake or Nextflow pipeline:

```
Orchestrator (one agent)
├── Worker 1 → Sample A → Result A
├── Worker 2 → Sample B → Result B
├── Worker 3 → Sample C → Result C
└── Worker 4 → Sample D → Result D
         ↓
Orchestrator aggregates results
```

- **Orchestrator**: decomposes the task, dispatches workers, aggregates results
- **Workers**: each handles one independent unit of work with its own fresh context

Each worker gets a clean context window — no cross-contamination between samples, no degradation from accumulated history.

## Why not just loop in one session?

If you process 50 samples sequentially in one session:

1. Context fills up with code and output from each sample
2. By sample 20, Claude is slower and less precise
3. By sample 35, it might confuse parameters from sample 12 with sample 35
4. One error can cascade through remaining samples

With subagents:
- Each sample gets fresh context
- Samples can run in parallel (faster)
- One worker failing doesn't affect others
- Results are consistent because each worker starts from the same instructions

## How it works in Claude Code

Claude Code can spawn subagents using the Agent tool. In practice, you describe the pattern to Claude and it handles the orchestration:

```
I need to process all 48 .fastq files in data/raw/ through our QC pipeline.
Each file should be processed independently.
Use the QC skill in skills/fastq-qc/SKILL.md for each file.
Save results to results/qc/{sample_name}_qc.json.
After all files are processed, aggregate the QC metrics into a single summary table.
```

Claude will:
1. List the input files
2. Spawn a worker agent for each file (or batch of files)
3. Each worker runs the QC pipeline independently
4. The orchestrator collects results and builds the summary

## Examples

| Example | What it demonstrates |
|---------|---------------------|
| `01-single-agent-limit.md` | Why a single session hits a wall |
| `02-orchestrator-worker.md` | The pattern explained with pseudocode |
| `03-parallel-sample-processing/` | Full worked example with prompts |

## Where things go wrong

Subagents aren't magic. Common pitfalls:

1. **Inconsistent decisions**: Worker A normalizes differently than Worker B because their prompts aren't specific enough → **Fix: detailed skill files with exact parameters**

2. **Orchestrator loses track**: With many workers, the orchestrator's context fills with status updates → **Fix: workers write results to disk, orchestrator reads files**

3. **Cascading errors**: Orchestrator doesn't check worker results before proceeding → **Fix: validate each worker's output before aggregation**

4. **Overkill**: Using subagents for a 5-sample task that would take 2 minutes in one session → **Fix: only reach for subagents when the task genuinely exceeds one context window**

## Key lesson

**Subagents are for when the task is bigger than one context window or naturally parallel.** Don't reach for them early — a single well-managed session handles 90% of tasks. But when you need them, the orchestrator/worker pattern is powerful and maps directly to how scientists already think about batch processing.
