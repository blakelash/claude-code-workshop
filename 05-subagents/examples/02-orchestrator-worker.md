# The Orchestrator/Worker Pattern

## Concept

```
┌─────────────────────────────────────────────┐
│                ORCHESTRATOR                   │
│                                               │
│  1. Identify all units of work                │
│  2. Define the worker instructions            │
│  3. Dispatch workers (parallel or batched)    │
│  4. Collect worker outputs                    │
│  5. Synthesize across results                 │
└──────────┬──────────┬──────────┬─────────────┘
           │          │          │
     ┌─────▼───┐ ┌────▼────┐ ┌──▼──────┐
     │ Worker 1 │ │ Worker 2│ │ Worker 3│  ...
     │          │ │         │ │         │
     │ Fresh    │ │ Fresh   │ │ Fresh   │
     │ context  │ │ context │ │ context │
     │          │ │         │ │         │
     │ READS    │ │ READS   │ │ READS   │
     │ REASONS  │ │ REASONS │ │ REASONS │
     │ DECIDES  │ │ DECIDES │ │ DECIDES │
     └─────┬────┘ └────┬────┘ └────┬────┘
           │           │           │
           ▼           ▼           ▼
        output_1    output_2    output_3
           │           │           │
           └───────────┼───────────┘
                       ▼
               Synthesis / Summary
```

## Key difference from a pipeline

In a pipeline, each worker runs **the same fixed logic** on different inputs. In the subagent pattern, each worker **reasons independently** — it reads material, makes judgments, and produces an analysis that couldn't be reduced to a deterministic script.

## Worked example: auditing analysis scripts

**Your prompt to Claude:**

```
I have 6 analysis scripts in scripts/. Each was written by a different person.
I need each script reviewed for:

1. Reproducibility: Are random seeds set? Are package versions pinned?
2. Statistical rigor: Are effect sizes reported? Is multiple testing corrected?
3. Figure quality: 300 DPI? Colorblind-safe palettes? Axis labels present?
4. Code quality: Hardcoded paths? Magic numbers? Missing docstrings?

For each script, write a review to reviews/{script_name}_review.md with:
- A pass/fail for each of the 4 categories
- Specific line numbers where issues occur
- Suggested fixes

After all reviews are done, write reviews/summary.md ranking the scripts
from most to least issues, and listing the top 3 most common problems.
```

**What the orchestrator does:**

1. Lists scripts in `scripts/`
2. For each script, spawns a worker with:
   - The script to review
   - The review criteria (all 4 categories)
   - The output format specification
3. Each worker reads its assigned script, understands the analysis logic, checks each criterion, and writes a structured review
4. Orchestrator reads all `reviews/*_review.md` files
5. Synthesizes a cross-script summary

**Why this needs subagents, not a pipeline:**

You can't write a bash script that determines whether a statistical test is appropriate for the data, or whether a figure's axis labels are meaningful. Each review requires *understanding the code* — that's reasoning.

## Structured output is still important

Even though workers reason independently, the orchestrator needs to aggregate their outputs. Give workers a clear output format:

```markdown
## Review: {script_name}

### Reproducibility: PASS/FAIL
- [specific findings]

### Statistical Rigor: PASS/FAIL
- [specific findings]

### Figure Quality: PASS/FAIL
- [specific findings]

### Code Quality: PASS/FAIL
- [specific findings]

### Summary
- Total issues: N
- Critical issues: N
```

This gives the orchestrator a reliable structure to parse when building the cross-script summary.
