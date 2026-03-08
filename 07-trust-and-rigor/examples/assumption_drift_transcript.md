# Assumption Drift — Annotated Transcript

This transcript shows Claude silently switching statistical tests mid-session. Annotations in **[brackets]** highlight the drift.

---

## Exchange 3

**You:** Compare expression of BRCA1 between WT and KO groups.

**Claude:** I'll compare BRCA1 expression between the groups using a Wilcoxon rank-sum test, which is appropriate for small sample sizes without assuming normality.

```python
from scipy.stats import mannwhitneyu
stat, pvalue = mannwhitneyu(wt_brca1, ko_brca1, alternative='two-sided')
```

> Wilcoxon rank-sum test: U=0.0, p=0.049. BRCA1 expression is significantly higher in KO.

**[✓ Good choice. Small sample size (n=3 per group), non-parametric test, appropriate.]**

---

## Exchange 7

**You:** Now compare TP53 expression between the groups.

**Claude:** I'll compare TP53 expression between WT and KO.

```python
from scipy.stats import ttest_ind
stat, pvalue = ttest_ind(wt_tp53, ko_tp53)
```

> t-test: t=-2.31, p=0.082. TP53 expression difference is not statistically significant.

**[⚠ Wait — Claude switched from Wilcoxon (non-parametric) to t-test (parametric) without mentioning the change. Same sample size, same experimental design. Why the switch? Claude doesn't say. You might not notice because the code runs fine and the output looks normal.]**

---

## Exchange 11

**You:** Test all 50 genes for differential expression between groups.

**Claude:** I'll run differential expression testing across all genes.

```python
from scipy.stats import ttest_ind

results = []
for gene in df.index:
    wt_vals = df.loc[gene, wt_samples]
    ko_vals = df.loc[gene, ko_samples]
    stat, pval = ttest_ind(wt_vals, ko_vals)
    results.append({'gene': gene, 'statistic': stat, 'pvalue': pval})
```

> Found 7 genes with p < 0.05 after Benjamini-Hochberg correction.

**[🚨 Now the t-test is locked in for all 50 genes. If you report this as "Wilcoxon rank-sum test" in your methods (because that's what Claude used initially), your methods section won't match your code. With n=3 per group and no normality check, the t-test assumptions are questionable.]**

---

## The fix

This drift happened because:
1. The session got long enough that Claude's initial reasoning (about why Wilcoxon was appropriate) faded from context
2. Claude defaults to common patterns, and `ttest_ind` is more commonly seen in training data than `mannwhitneyu`
3. There was no `CLAUDE.md` convention anchoring the statistical test choice

### Prevention

In `CLAUDE.md`:
```markdown
## Statistical conventions
- For small samples (n < 10 per group): use non-parametric tests (Wilcoxon rank-sum)
- For large samples with verified normality: parametric tests are acceptable
- ALWAYS state which test you're using and why when reporting results
- NEVER switch tests mid-analysis without explicitly flagging the change
```

### Detection

Ask periodically:
```
What statistical test are you using for these comparisons?
Is it the same test we used for BRCA1 earlier? If not, why did you change?
```
