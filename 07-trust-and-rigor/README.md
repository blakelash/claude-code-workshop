# Module 07 — Trust & Rigor

## The most important module in this workshop

Everything before this module made Claude faster and more capable. This module is about making sure you can **trust** its outputs.

Claude is a fast postdoc — but even fast postdocs make mistakes. The difference: a postdoc might catch their own errors on review. Claude often won't.

## Three failure modes

### 1. Silent errors

Code that runs, produces output, looks plausible — but is wrong.

See `examples/silent_error_demo.py`: a script that computes per-group means but has a subtle `groupby`/axis mistake. The code executes cleanly, produces a figure, and the figure looks reasonable. But the numbers are wrong.

Claude generates code like this regularly. Not because it's bad at coding — because these errors are hard to catch without domain knowledge.

### 2. Assumption drift

Over a long session, Claude quietly changes analytical decisions without flagging them.

See `examples/assumption_drift_transcript.md`: a session where Claude switches from a non-parametric test (Wilcoxon) to a parametric test (t-test) mid-analysis. It doesn't mention the change. If you're not watching closely, your methods section will say one thing and your code will do another.

### 3. Reproducibility gaps

Claude writes code that works right now but can't be re-run tomorrow:
- Hardcoded absolute paths that only exist on your machine
- Missing random seeds for stochastic methods
- Depending on the order of operations in a session (state that's not captured in code)
- Undeclared package dependencies

## The review checklist

Before trusting any Claude-generated analysis result, run through `examples/checklist.md`. Key questions:

1. **Did you verify the output independently?** (Not just "does it look right" — actually check a few numbers)
2. **Can you re-run the code from scratch?** (Exit Claude, run the script directly)
3. **Did the statistical method stay consistent?** (Check what was used, not what was described)
4. **Are there hardcoded paths or missing seeds?**
5. **Does the result make biological sense?** (This is YOUR job — Claude doesn't know your biology)

## Practical strategies

### Verify critical numbers

When Claude reports a result ("847 DE genes"), spot-check it:

```
Show me the code that produced the number 847. Let me see the actual
filtering step. How many genes had padj < 0.05 vs padj < 0.01?
```

### Ask Claude to explain its choices

```
Why did you use a t-test here instead of Wilcoxon?
What are the assumptions of this test and are they met?
```

If Claude can't justify the choice clearly, that's a red flag.

### Run code outside of Claude

Copy the final script out and run it independently. If it fails or produces different results, something in the session-dependent state was affecting the analysis.

### Use CLAUDE.md to enforce consistency

Put your statistical conventions in `CLAUDE.md`. Claude will follow them — and if it deviates, you'll notice because you know what it should be doing.

## Exercise

1. Read `examples/silent_error_demo.py` — find the bug before running it
2. Run it — does the output look wrong? (It won't be obvious)
3. Read `examples/assumption_drift_transcript.md` — identify where the switch happens
4. Review `examples/checklist.md` and think about your own work

## Key lesson

**Scientific rigor applies to AI outputs too.** Claude is a tool, not an authority. Your job as PI — to verify, to question, to ensure reproducibility — doesn't go away. It gets more important, because Claude is fast enough to produce a lot of plausible-looking results very quickly.
