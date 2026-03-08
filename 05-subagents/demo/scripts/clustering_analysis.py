"""Cluster single-cell RNA-seq data and identify cell types."""

import scanpy as sc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load data
adata = sc.read_h5ad("/Users/agarcia/Desktop/scrnaseq_data/pbmc_3k.h5ad")

# Preprocessing
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
adata = adata[:, adata.var.highly_variable]

# Dimensionality reduction
sc.pp.scale(adata)
sc.tl.pca(adata, n_comps=50)
sc.pp.neighbors(adata, n_neighbors=15)
sc.tl.umap(adata)

# Clustering
sc.tl.leiden(adata, resolution=0.8)

# Find marker genes per cluster
sc.tl.rank_genes_groups(adata, groupby="leiden", method="t-test")

# Plot results
fig, axes = plt.subplots(1, 2)

sc.pl.umap(adata, color="leiden", ax=axes[0], show=False)
axes[0].set_title("Clusters")

sc.pl.umap(adata, color="n_genes", ax=axes[1], show=False)
axes[1].set_title("Gene count")

plt.savefig("clusters.png")
plt.close()

# Assign cell types based on markers
# Cluster 0 has high CD3D -> T cells
# Cluster 1 has high CD14 -> Monocytes
# Cluster 2 has high MS4A1 -> B cells
cell_type_map = {
    "0": "T cells",
    "1": "Monocytes",
    "2": "B cells",
    "3": "NK cells",
    "4": "Dendritic cells",
}

adata.obs["cell_type"] = adata.obs["leiden"].map(cell_type_map)

# Count cells per type
counts_per_type = adata.obs["cell_type"].value_counts()
print(counts_per_type)

# Quick statistical test: are there more T cells than expected?
from scipy.stats import binom_test
n_total = len(adata)
n_tcells = (adata.obs["cell_type"] == "T cells").sum()
p = binom_test(n_tcells, n_total, 0.2)
print(f"Binomial test p-value for T cell enrichment: {p}")

# Save
adata.write("clustered_pbmc.h5ad")
print(f"Saved {adata.n_obs} cells with {adata.obs['cell_type'].nunique()} cell types")
