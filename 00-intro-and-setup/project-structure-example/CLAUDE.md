# Example Project CLAUDE.md

This is an example of a project-level CLAUDE.md for a typical biology research project.

## Project overview

Single-cell RNA-seq analysis of mouse cortical organoids comparing wildtype vs. GENE-X knockout at day 30 of differentiation.

## Key conventions

- Genome build: GRCm39 (mouse), Ensembl release 110
- Preferred packages: scanpy, pandas, seaborn, matplotlib
- Figure style: publication-ready, 300 DPI, colorblind-safe palette
- File naming: `{date}_{descriptor}_{version}.ext` (e.g., `2025-03-01_umap_clusters_v2.png`)
- Random seed: 42

## Directory structure

- `data/raw/` — original count matrices, do not modify
- `data/processed/` — filtered, normalized, batch-corrected data
- `results/figures/` — all generated plots
- `scripts/` — analysis scripts, numbered in execution order

## Statistical notes

- Use Wilcoxon rank-sum for differential expression (scanpy.tl.rank_genes_groups)
- Benjamini-Hochberg correction for multiple testing
- Minimum 3 cells per group for any comparison
