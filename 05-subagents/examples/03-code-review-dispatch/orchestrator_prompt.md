# Orchestrator Prompt — Code Review Dispatch

## The prompt you'd give Claude

```
I have 6 analysis scripts in scripts/ that need review before we submit our paper.
Each script was written by a different rotation student over the past year.

The scripts are:
1. scripts/01_preprocessing.py — raw data cleaning and normalization
2. scripts/02_clustering.py — dimensionality reduction and clustering
3. scripts/03_differential_expression.py — DE analysis between conditions
4. scripts/04_pathway_analysis.py — gene set enrichment
5. scripts/05_survival_analysis.py — clinical outcome correlations
6. scripts/06_figure_generation.py — all paper figures

For each script, I need a thorough review checking:
- Reproducibility: random seeds set? Package versions noted?
- Statistical rigor: effect sizes alongside p-values? Multiple testing correction?
- Figure conventions: 300 DPI? Colorblind-safe palettes? Labeled axes?
- Code quality: no hardcoded paths? No magic numbers? Has docstring?

Write each review to reviews/{script_number}_review.md.
After all reviews, write reviews/summary.md with the overall assessment.
```

## What the orchestrator does

1. Lists the 6 scripts from your prompt
2. For each script, spawns a worker agent with:
   - The specific script to review
   - The review criteria (all 4 categories)
   - The output path
3. Workers run independently — each reads and *understands* its script
4. Orchestrator waits for all workers to complete
5. Reads all review files from `reviews/`
6. Writes the cross-script summary

## Why this works as subagents

Each worker needs to:
- Read and understand code written by a different person
- Judge whether statistical choices are appropriate
- Identify subtle issues (e.g., a seed set for clustering but not for train/test split)
- Write specific, actionable feedback with line numbers

This is reasoning, not execution. You can't write a linter that checks whether a statistical test is appropriate for the data structure.
