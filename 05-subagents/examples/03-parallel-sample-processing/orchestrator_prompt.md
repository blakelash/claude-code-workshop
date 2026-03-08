# Orchestrator Prompt — Parallel Sample Processing

## The prompt you'd give Claude

```
I need to run differential expression analysis on 6 experimental comparisons.
Each comparison is independent.

The comparisons are:
1. DrugA_high vs DMSO — using data/counts/drugA_high_vs_dmso.csv
2. DrugA_low vs DMSO — using data/counts/drugA_low_vs_dmso.csv
3. DrugB_high vs DMSO — using data/counts/drugB_high_vs_dmso.csv
4. DrugB_low vs DMSO — using data/counts/drugB_low_vs_dmso.csv
5. DrugA_high vs DrugB_high — using data/counts/drugA_vs_drugB_high.csv
6. DrugA_low vs DrugB_low — using data/counts/drugA_vs_drugB_low.csv

For each comparison:
- Follow the DESeq2 workflow skill in skills/deseq2-workflow/SKILL.md
- Save results to results/{comparison_name}/
- Generate all standard plots (MA, volcano, PCA)
- Save a summary JSON with: n_significant, n_up, n_down, top_5_genes

After all comparisons are complete:
- Build a summary table comparing results across all 6 comparisons
- Generate an upset plot showing overlap of DE genes across comparisons
- Save the combined summary to results/cross_comparison_summary.csv
```

## What the orchestrator does

1. Parses the 6 comparisons from your prompt
2. For each comparison, spawns a worker agent with:
   - The specific input file
   - The skill file reference
   - The output directory
3. Workers run independently (potentially in parallel)
4. Orchestrator waits for all workers to complete
5. Reads results from each `results/{comparison}/` directory
6. Builds cross-comparison summaries and plots
