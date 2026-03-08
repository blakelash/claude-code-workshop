"""
Silent Error Demo
==================
This script computes per-group mean expression from an RNA-seq count matrix.
It runs without errors, produces a plausible-looking bar plot — but contains
a subtle bug that makes the results incorrect.

Can you spot the error before running it?
(Hint: pay attention to the axis argument in the mean calculation)
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

# Generate synthetic data
np.random.seed(42)
genes = [f"Gene_{i}" for i in range(1, 21)]
wt_samples = ["WT_1", "WT_2", "WT_3"]
ko_samples = ["KO_1", "KO_2", "KO_3"]

# WT genes: baseline expression around 500
# KO genes: some genes upregulated (higher expression)
wt_data = np.random.negative_binomial(5, 0.01, size=(20, 3))
ko_data = np.random.negative_binomial(5, 0.01, size=(20, 3))

# Make genes 0-4 clearly upregulated in KO
ko_data[:5, :] = ko_data[:5, :] * 3

# Build DataFrame
df = pd.DataFrame(
    np.hstack([wt_data, ko_data]),
    index=genes,
    columns=wt_samples + ko_samples
)

# ============================================================
# THE BUG IS HERE
# ============================================================
# We want the mean expression of each gene within each group.
# axis=1 computes the mean across columns (correct for per-gene means).
# But watch what happens with the group selection...

wt_mean = df[wt_samples].mean(axis=0)  # BUG: axis=0 gives per-SAMPLE mean, not per-gene
ko_mean = df[ko_samples].mean(axis=0)  # Same bug

# This produces 3 values (one per sample) instead of 20 values (one per gene).
# The plot below "works" but shows sample means, not gene means.
# ============================================================

# Plot — this looks like a reasonable bar plot, but it's answering
# the wrong question entirely
fig, ax = plt.subplots(figsize=(8, 6))

x = np.arange(len(wt_mean))
width = 0.35

ax.bar(x - width/2, wt_mean.values, width, label='WT', color='#4878CF')
ax.bar(x + width/2, ko_mean.values, width, label='KO', color='#D65F5F')

ax.set_xlabel('Sample')
ax.set_ylabel('Mean Expression')
ax.set_title('Mean Expression by Group')
ax.set_xticks(x)
ax.set_xticklabels(wt_mean.index, rotation=45)
ax.legend()

plt.tight_layout()
plt.savefig('mean_expression_plot.png', dpi=300)
print(f"Plot saved. WT means: {wt_mean.values}")
print(f"KO means: {ko_mean.values}")
print("Looks reasonable, right? But these are per-SAMPLE means, not per-GENE means.")
print()
print("The correct code would use axis=1:")
print("  wt_mean = df[wt_samples].mean(axis=1)  # 20 values, one per gene")
print("  ko_mean = df[ko_samples].mean(axis=1)  # 20 values, one per gene")
