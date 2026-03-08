"""Differential expression analysis between treatment groups."""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Load data
counts = pd.read_csv("/home/jsmith/project/data/counts_normalized.csv", index_col=0)
metadata = pd.read_csv("/home/jsmith/project/data/sample_metadata.csv")

# Split into groups
treated = counts[metadata[metadata["condition"] == "treated"].sample_id]
control = counts[metadata[metadata["condition"] == "control"].sample_id]

# Run t-test for each gene
results = []
for gene in counts.index:
    t_stat, pval = stats.ttest_ind(treated.loc[gene], control.loc[gene])
    results.append({"gene": gene, "pvalue": pval, "t_statistic": t_stat})

results_df = pd.DataFrame(results)

# Filter significant genes
significant = results_df[results_df["pvalue"] < 0.05]
print(f"Found {len(significant)} significant genes out of {len(results_df)}")

# Volcano plot
plt.figure()
plt.scatter(results_df["t_statistic"], -np.log10(results_df["pvalue"]),
            c="red", alpha=0.5)
plt.xlabel("t-statistic")
plt.ylabel("-log10(p)")
plt.title("Volcano Plot")
plt.savefig("volcano.png")
plt.close()

# Heatmap of top genes
top_genes = significant.nsmallest(50, "pvalue")["gene"]
top_counts = counts.loc[top_genes]

plt.figure()
plt.imshow(top_counts.values, aspect="auto", cmap="jet")
plt.colorbar()
plt.savefig("heatmap.jpg")
plt.close()

# Save results
significant.to_csv("de_results.csv", index=False)
print("Done!")
