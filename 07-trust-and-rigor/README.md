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

### Ask Claude to check its own work

This is one of the simplest and most effective strategies. After Claude produces an analysis, explicitly ask it to review what it just did:

```
Now review the code you just wrote. Check for:
- Off-by-one errors
- Incorrect groupby/axis operations
- Whether the statistical test matches what we discussed
- Whether the filtering thresholds are applied correctly
```

Or more broadly:

```
Before I trust these results, play devil's advocate. What could be
wrong with this analysis? What assumptions might be violated?
```

Claude is surprisingly good at finding its own mistakes when prompted to look — it just won't do it spontaneously. Make self-review a habit at the end of any analysis block.

### Build reviewing subagents

For recurring review tasks, encode them as subagents that run automatically. Claude Code's subagent system (Module 05) lets you dispatch dedicated reviewers against your code:

```
Review the script analyze_rnaseq.py. Spin up three subagents in parallel:

1. A stats reviewer: check that statistical methods are appropriate,
   assumptions are met, effect sizes are reported, and multiple testing
   correction is applied.

2. A reproducibility reviewer: check for hardcoded paths, missing random
   seeds, undeclared dependencies, and session-dependent state.

3. A figure reviewer: check that all plots have correct labels, colorblind-safe
   palettes, sufficient DPI, and accurate legends.

Compile the findings into a single review summary.
```

This is powerful because each subagent focuses on one dimension of quality, and they run in parallel. You can also save these review patterns as skills (Module 04) so they're always one command away:

```
/review-analysis analyze_rnaseq.py
```

The key insight: **don't just use Claude to write code — use Claude to review Claude's code.** A fresh subagent reviewing code has no sunk-cost bias toward defending it.

### Use extended thinking for genuinely hard problems

For complex statistical decisions — which model to use, how to interpret a surprising result, whether a method's assumptions hold — you can ask Claude to think more deeply by including "ultrathink" in your prompt:

```
ultrathink: is a negative binomial model appropriate here, given this sample distribution?
```

This triggers extended reasoning mode where Claude works through the problem more carefully before responding. It's slower and costs more, so save it for situations where you genuinely need deep analysis — not for routine coding tasks.

### Run code outside of Claude

Copy the final script out and run it independently. If it fails or produces different results, something in the session-dependent state was affecting the analysis.

### Use CLAUDE.md to enforce consistency

Put your statistical conventions in `CLAUDE.md`. Claude will follow them — and if it deviates, you'll notice because you know what it should be doing.

## Exercise

1. Read `examples/silent_error_demo.py` — find the bug before running it
2. Run it — does the output look wrong? (It won't be obvious)
3. Ask Claude to review `silent_error_demo.py` — does it catch the bug on its own?
4. Read `examples/assumption_drift_transcript.md` — identify where the switch happens
5. Try the subagent review pattern: ask Claude to spin up parallel reviewers (stats, reproducibility, figures) against `silent_error_demo.py` and see what they find
6. Review `examples/checklist.md` and think about your own work

## Key lesson

**Scientific rigor applies to AI outputs too.** Claude is a tool, not an authority. Your job as PI — to verify, to question, to ensure reproducibility — doesn't go away. It gets more important, because Claude is fast enough to produce a lot of plausible-looking results very quickly.
