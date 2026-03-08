"""Survival analysis correlating gene expression with patient outcomes."""

import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load clinical + expression data
clinical = pd.read_csv("/data/tcga/clinical_data.csv")
expression = pd.read_csv("/data/tcga/gene_expression.csv", index_col=0)

# Merge on patient ID
data = clinical.merge(expression.T, left_on="patient_id", right_index=True)

# Filter to genes of interest
genes_of_interest = ["BRCA1", "TP53", "EGFR", "MYC", "PTEN",
                     "RB1", "APC", "KRAS", "PIK3CA", "BRAF"]

# For each gene, split patients into high/low expression and test survival
for gene in genes_of_interest:
    median_expr = data[gene].median()
    data[f"{gene}_group"] = np.where(data[gene] > median_expr, "high", "low")

    high = data[data[f"{gene}_group"] == "high"]
    low = data[data[f"{gene}_group"] == "low"]

    result = logrank_test(
        high["survival_months"], low["survival_months"],
        high["event"], low["event"]
    )

    if result.p_value < 0.05:
        print(f"{gene}: significant (p={result.p_value:.4f})")

        # Plot KM curves
        kmf = KaplanMeierFitter()

        plt.figure(figsize=(8, 6))
        kmf.fit(high["survival_months"], high["event"], label="High")
        kmf.plot()
        kmf.fit(low["survival_months"], low["event"], label="Low")
        kmf.plot()
        plt.title(f"{gene} Expression and Survival")
        plt.xlabel("Months")
        plt.ylabel("Survival Probability")
        plt.savefig(f"km_{gene}.png")
        plt.close()

# Multivariate Cox model with top genes
top_genes = ["BRCA1", "TP53", "EGFR"]
cox_data = data[["survival_months", "event"] + top_genes + ["age", "stage"]].dropna()

# Encode stage
cox_data["stage_numeric"] = cox_data["stage"].map({"I": 1, "II": 2, "III": 3, "IV": 4})
cox_data = cox_data.drop("stage", axis=1)

# Scale features
scaler = StandardScaler()
feature_cols = top_genes + ["age", "stage_numeric"]
cox_data[feature_cols] = scaler.fit_transform(cox_data[feature_cols])

# Fit Cox model
cph = CoxPHFitter()
cph.fit(cox_data, duration_col="survival_months", event_col="event")
cph.print_summary()

# Train/test split for validation
train, test = train_test_split(cox_data, test_size=0.3)
cph_val = CoxPHFitter()
cph_val.fit(train, duration_col="survival_months", event_col="event")
c_index = cph_val.score(test)
print(f"Validation C-index: {c_index:.3f}")

# Save significant genes
sig_genes = cph.summary[cph.summary["p"] < 0.05].index.tolist()
pd.DataFrame({"gene": sig_genes}).to_csv("significant_survival_genes.csv", index=False)
