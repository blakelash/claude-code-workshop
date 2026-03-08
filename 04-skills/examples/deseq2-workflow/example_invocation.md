# Example: Running the DESeq2 Skill

## Prompt

```
Run the DESeq2 differential expression workflow:
- Count matrix: data/counts_raw.csv
- Metadata: data/sample_metadata.csv
- Comparison: KO vs WT
- Output: results/
```

## What happens

1. Claude reads `skills/deseq2-workflow/SKILL.md`
2. Follows the procedure step by step
3. Validates inputs, reports any issues
4. Runs the analysis
5. Generates all specified plots
6. Saves results and prints summary

## Expected output

```
Loaded count matrix: 18,562 genes × 6 samples (3 WT, 3 KO)
Pre-filtering: removed 4,231 genes (total count < 10), 14,331 remaining
Running DESeq2...
Results: 847 significant DE genes (padj < 0.05)
  - 412 up-regulated in KO
  - 435 down-regulated in KO

Top 5 up-regulated:
  BRCA1  (log2FC = 3.21, padj = 1.2e-15)
  TP53   (log2FC = 2.87, padj = 3.4e-12)
  ...

Saved: results/de_results_KO_vs_WT.csv
Saved: results/figures/ma_plot.png
Saved: results/figures/volcano_plot.png
Saved: results/figures/pca_plot.png
Saved: results/figures/dispersion_plot.png
```
