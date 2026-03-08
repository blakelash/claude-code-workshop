# Skill: DESeq2 Differential Expression Workflow

## Context

This skill runs a standard bulk RNA-seq differential expression analysis using pydeseq2. Use this when you have a raw count matrix and want to identify differentially expressed genes between two conditions.

## Inputs

- **Count matrix**: CSV file with genes as rows, samples as columns. First column is gene IDs (Ensembl format). Values are raw (unnormalized) integer counts.
- **Metadata**: CSV file with columns `sample_id` and `condition` at minimum. `sample_id` values must match count matrix column names.
- **Comparison**: Which two conditions to compare (e.g., "KO vs WT" — first term is numerator/treatment).
- **Output directory**: Where to save results (default: `results/`).

## Procedure

### Step 1 — Load and validate

1. Read the count matrix and metadata files
2. Verify all sample IDs in metadata match column names in count matrix
3. Verify the count matrix contains only non-negative integers (except allowed NAs)
4. Report: number of genes, number of samples per condition, any warnings

**Stop and ask the user if:** sample IDs don't match, fewer than 2 samples per condition, or >10% of values are NA.

### Step 2 — Pre-filtering

1. Remove genes where the total count across all samples is < 10
2. Report: how many genes removed, how many remaining

### Step 3 — Run DESeq2

1. Create a DeseqDataSet with design `~ condition`
2. Run `deseq2()` (fits model, estimates dispersions, runs Wald test)
3. Extract results for the specified comparison
4. Apply Benjamini-Hochberg correction

### Step 4 — Results table

1. Create results DataFrame with columns: `gene_id`, `baseMean`, `log2FoldChange`, `lfcSE`, `stat`, `pvalue`, `padj`
2. Sort by adjusted p-value
3. Save to `{output_dir}/de_results_{condition1}_vs_{condition2}.csv`
4. Report: total significant genes (padj < 0.05), number up-regulated, number down-regulated

### Step 5 — Diagnostic plots

Generate and save the following plots to `{output_dir}/figures/`:

1. **MA plot** (`ma_plot.png`): log2FC vs mean expression, significant genes highlighted
2. **Volcano plot** (`volcano_plot.png`): -log10(pvalue) vs log2FC, significant genes highlighted, top 10 genes labeled
3. **PCA plot** (`pca_plot.png`): first two PCs of variance-stabilized data, colored by condition
4. **Dispersion plot** (`dispersion_plot.png`): fitted vs gene-wise dispersion estimates

All plots: 300 DPI, 8×6 inches, colorblind-safe palette, descriptive titles and axis labels.

### Step 6 — Summary

Print a summary including:
- Number of input genes → number after filtering
- Number of significant DE genes (padj < 0.05)
- Top 5 up-regulated and top 5 down-regulated genes (by fold change among significant)
- Any warnings or notes

## Failure modes

| Issue | What to do |
|-------|-----------|
| Sample IDs don't match | Stop and report the mismatch |
| Fewer than 3 samples per condition | Warn user, proceed but flag results as underpowered |
| All genes filtered out | Stop — likely a data format issue |
| DESeq2 convergence warnings | Report the warnings, proceed, note affected genes |
| No significant DE genes | Report this clearly — it's a valid result, not an error |

## Dependencies

```python
import pandas as pd
import numpy as np
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
import matplotlib.pyplot as plt
import seaborn as sns
```
