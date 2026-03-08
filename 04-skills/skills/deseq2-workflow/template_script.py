"""DESeq2 differential expression template.

Inputs:
  - count_matrix.csv: genes × samples, raw integer counts
  - metadata.csv: sample_id, condition columns

Outputs:
  - de_results_{cond1}_vs_{cond2}.csv
  - figures/: ma_plot.png, volcano_plot.png, pca_plot.png, dispersion_plot.png
"""

import pandas as pd
import numpy as np
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_palette("colorblind")

# --- Load ---
counts = pd.read_csv("count_matrix.csv", index_col=0)
metadata = pd.read_csv("metadata.csv", index_col="sample_id")

# Ensure sample order matches
metadata = metadata.loc[counts.columns]

# --- Pre-filter ---
keep = counts.sum(axis=1) >= 10
counts = counts.loc[keep]

# --- DESeq2 ---
dds = DeseqDataSet(
    counts=counts.T,
    metadata=metadata,
    design="~condition",
)
dds.deseq2()

stat_res = DeseqStats(dds, contrast=("condition", "KO", "WT"))
stat_res.summary()
results = stat_res.results_df

# --- Save ---
results.sort_values("padj").to_csv("de_results_KO_vs_WT.csv")

# --- Volcano plot ---
fig, ax = plt.subplots(figsize=(8, 6))
sig = results["padj"] < 0.05
ax.scatter(results.loc[~sig, "log2FoldChange"], -np.log10(results.loc[~sig, "pvalue"]),
           alpha=0.3, s=5, color="grey")
ax.scatter(results.loc[sig, "log2FoldChange"], -np.log10(results.loc[sig, "pvalue"]),
           alpha=0.5, s=5, color="tab:red")
ax.set_xlabel("log2 Fold Change")
ax.set_ylabel("-log10(p-value)")
ax.set_title("Volcano Plot — KO vs WT")
fig.savefig("volcano_plot.png", dpi=300, bbox_inches="tight")
plt.close()
