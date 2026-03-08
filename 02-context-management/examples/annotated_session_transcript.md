# Annotated Session Transcript — Context Degradation Example

This is an edited transcript showing how Claude's outputs degrade over a long session. Annotations in **[brackets]** highlight what's going wrong.

---

## Exchange 1 (fresh context)

**You:** Load the count matrix from data/counts_raw.csv and show me a summary.

**Claude:** I'll read the count matrix and provide a summary.

*[Reads file, writes precise code, correctly identifies 6 samples, 50 genes, reports exact dimensions, notes the NA value in sample_KO_2]*

> The matrix contains 50 genes × 6 samples (3 WT, 3 KO). There is one missing value in sample_KO_2 for gene ENSG00000023. Library sizes range from 45,230 to 67,891 counts.

**[✓ Sharp and precise. Exact numbers, correct sample names, catches the NA.]**

---

## Exchange 5 (moderate context load)

**You:** Now filter out low-count genes and normalize.

**Claude:** I'll filter genes with low counts and apply normalization.

*[Code is correct but Claude says "the 6 samples" without specifying WT/KO breakdown. Still functional.]*

> Filtered from 50 to 43 genes. Applied median-of-ratios normalization. Saved to data/processed/counts_normalized.csv.

**[~ Still correct, but notice it's less specific about details it was precise about earlier.]**

---

## Exchange 9 (heavy context load)

**You:** Run differential expression between the conditions.

**Claude:** I'll run differential expression analysis comparing the two groups.

*[Claude writes the code but refers to columns as "control" and "treatment" instead of "WT" and "KO" — the actual column names. The code still works because it re-reads the file, but the language is drifting.]*

> Found 7 differentially expressed genes (adjusted p < 0.05) between control and treatment groups.

**[⚠ "Control and treatment" — those aren't the group names. Claude is paraphrasing from fading context instead of citing exactly. The analysis is still correct because the code reads from disk, but the verbal descriptions are getting imprecise.]**

---

## Exchange 13 (context degradation)

**You:** Make a volcano plot of the DE results.

**Claude:** I'll create a volcano plot showing the differential expression results.

*[Claude writes plotting code but uses `plt.figure(figsize=(10,8))` despite CLAUDE.md specifying 8x6 as default. It also uses the default matplotlib color cycle instead of the colorblind-safe palette specified in conventions.]*

> Here's the volcano plot showing significantly differentially expressed genes highlighted in red.

**[⚠ Multiple convention violations: wrong figure size, wrong palette, "red" highlighting instead of colorblind-safe colors. Claude has lost track of the project conventions from CLAUDE.md — they've been pushed out of active context by 13 exchanges of code and output.]**

---

## Exchange 16 (significant degradation)

**You:** Now let's do pathway enrichment on the DE genes.

**Claude:** I'll perform pathway enrichment analysis. Let me first check what DE genes we identified...

*[Claude re-reads the DE results file — good. But then it applies enrichment using ALL genes in the results, not just the significant ones (p < 0.05). It also switches from Benjamini-Hochberg to Bonferroni correction without mentioning the change.]*

> Pathway enrichment analysis complete. Found 3 significantly enriched pathways (corrected p < 0.05).

**[🚨 Two silent errors: (1) Used all genes instead of just significant DE genes. (2) Switched multiple testing correction method without flagging it. Both are scientifically meaningful errors that would affect your conclusions. Claude didn't flag either change.]**

---

## What should you do here?

At exchange 9-10, this session was ready for a `/clear or /compact`. The signs:

1. **Imprecise language** — paraphrasing instead of using exact terms
2. **Convention drift** — forgetting project-level settings from CLAUDE.md
3. **Silent parameter changes** — switching methods without flagging

After `/clear`:
```
Read CLAUDE.md, then read the DE results in results/de_results.csv.
Run pathway enrichment on the significant DE genes (adjusted p < 0.05)
using Benjamini-Hochberg correction as specified in our conventions.
```

Fresh context, explicit instructions, correct results.
