# End-of-Session Review Checklist

Run through these questions before trusting any Claude-generated analysis result.

## Data integrity

- [ ] Did Claude read the correct input file(s)?
- [ ] Were any samples or data points unexpectedly dropped?
- [ ] Are the sample sizes in the output what you expect?
- [ ] Did Claude modify the raw data in any way it shouldn't have?

## Statistical methods

- [ ] What statistical test was actually used? (Check the code, not Claude's description)
- [ ] Is it the same test throughout the analysis, or did it change?
- [ ] Are the assumptions of the test met? (normality, independence, sample size)
- [ ] Was the correct multiple testing correction applied?
- [ ] Are p-values AND effect sizes reported?

## Results verification

- [ ] Do the numbers make biological sense?
- [ ] Spot-check: pick 2-3 results and verify them manually or with a different method
- [ ] Are there any suspiciously clean results? (perfect p-values, impossibly large effects)
- [ ] Does the total number of results match what you'd expect?

## Reproducibility

- [ ] Can you run the script from scratch (outside of Claude) and get the same results?
- [ ] Are random seeds set for all stochastic methods?
- [ ] Are file paths relative (not absolute)?
- [ ] Are all package dependencies documented?
- [ ] Is the code self-contained (doesn't depend on session state)?

## Figures

- [ ] Do axis labels match the actual data?
- [ ] Is the color scheme accessible (colorblind-safe)?
- [ ] Does the figure title accurately describe what's shown?
- [ ] Are legends complete and correct?
- [ ] Is the figure resolution sufficient (≥300 DPI)?

## Documentation

- [ ] Would someone else understand what this code does?
- [ ] Is the analytical logic clear from the code, or does it depend on context from the Claude session?
- [ ] Are key decisions (filtering thresholds, test choices, parameter values) documented in comments or the code itself?

---

## Quick version (5 questions)

If you're short on time, at minimum ask:

1. **Can I re-run this script independently and get the same result?**
2. **Did the statistical method stay consistent throughout?**
3. **Do the numbers make biological sense?**
4. **Are there hardcoded values that should be parameters?**
5. **Did I actually verify a result, or did I just accept Claude's summary?**
