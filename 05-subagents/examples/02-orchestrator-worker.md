# The Orchestrator/Worker Pattern

## Concept

```
┌─────────────────────────────────────────────┐
│                ORCHESTRATOR                   │
│                                               │
│  1. Identify all units of work                │
│  2. Define the worker instructions            │
│  3. Dispatch workers (parallel or batched)    │
│  4. Monitor progress                          │
│  5. Validate worker outputs                   │
│  6. Aggregate results                         │
└──────────┬──────────┬──────────┬─────────────┘
           │          │          │
     ┌─────▼───┐ ┌────▼────┐ ┌──▼──────┐
     │ Worker 1 │ │ Worker 2│ │ Worker 3│  ...
     │          │ │         │ │         │
     │ Fresh    │ │ Fresh   │ │ Fresh   │
     │ context  │ │ context │ │ context │
     │          │ │         │ │         │
     │ One unit │ │ One unit│ │ One unit│
     │ of work  │ │ of work │ │ of work │
     └─────┬────┘ └────┬────┘ └────┬────┘
           │           │           │
           ▼           ▼           ▼
        result_1    result_2    result_3
           │           │           │
           └───────────┼───────────┘
                       ▼
              Aggregated results
```

## Analogy: Snakemake/Nextflow

If you've used workflow managers, this is the same idea:

| Workflow Manager | Claude Subagents |
|-----------------|------------------|
| Snakefile rule | Worker prompt / skill |
| Input wildcards | List of samples/files |
| Independent jobs | Worker agents |
| Target rule | Orchestrator aggregation |
| `--cores 8` | Parallel worker dispatch |

The key insight: **each job/worker is independent and stateless**. It reads its inputs, does its work, writes its outputs. No shared state between workers.

## Pseudocode

```python
# The orchestrator's logic (conceptual, not literal code)

# Step 1: Identify work units
samples = list_files("data/raw/*.fastq")

# Step 2: Define worker instructions
worker_instructions = """
Process the following sample through the RNA-seq pipeline:
- Input: {sample_path}
- Reference: data/references/GRCh38.fa
- Parameters: see skills/rnaseq-pipeline/SKILL.md
- Save results to: results/{sample_name}/
- Save QC metrics to: results/{sample_name}/qc_metrics.json
"""

# Step 3: Dispatch workers
for sample in samples:
    spawn_worker(worker_instructions.format(
        sample_path=sample,
        sample_name=sample.stem
    ))

# Step 4: Wait for completion, validate outputs
for sample in samples:
    result = read(f"results/{sample.stem}/qc_metrics.json")
    validate(result)  # check expected fields exist, values are reasonable

# Step 5: Aggregate
all_metrics = collect_results("results/*/qc_metrics.json")
create_summary_table(all_metrics, "results/qc_summary.csv")
create_summary_plots(all_metrics, "results/figures/")
```

## When to use this pattern

✅ **Good fit:**
- 10+ samples through the same pipeline
- Tasks that are truly independent (no sample depends on another)
- Processing that fills context if done sequentially
- When consistency across samples is critical

❌ **Not a good fit:**
- Fewer than 5 samples (just do them sequentially)
- Tasks where each step depends on previous results
- Exploratory analysis (you need to see results before deciding next steps)
- When the task fits comfortably in one session
