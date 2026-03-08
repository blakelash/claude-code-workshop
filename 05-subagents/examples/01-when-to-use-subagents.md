# When to Use Subagents

## The decision tree

```
Does the task require judgment/reasoning for each unit of work?
│
├─ NO → Is it repetitive execution of fixed steps?
│       │
│       ├─ YES → Use a pipeline tool (Snakemake, Nextflow, bash loop)
│       └─ NO  → Probably just do it in one session
│
└─ YES → Do the workers need to communicate with each other?
         │
         ├─ YES → Agent team (experimental — see docs)
         │
         └─ NO  → Are the units of work independent?
                  │
                  ├─ NO → Do it sequentially in one session
                  │       (each step informs the next)
                  │
                  └─ YES → How many units?
                           │
                           ├─ 2-3  → One session is fine
                           ├─ 4-10 → Subagents
                           └─ 10+  → Subagents, probably batched
```

## Examples by category

### Use a pipeline, not subagents

These tasks are mechanical — no reasoning required per unit:

- **Trimming adapters from 96 FASTQ files** → fixed parameters, same tool, every time
- **Converting 200 BAM files to CRAM** → a format conversion, no judgment needed
- **Running FastQC on all samples** → deterministic tool, same flags
- **Renaming files to match a sample sheet** → string manipulation

### Use a single session, not subagents

These require reasoning but aren't worth the overhead:

- **Reviewing 2 short scripts** → they'll fit in one context window easily
- **Analyzing one dataset exploratively** → you need to see intermediate results
- **Debugging a specific pipeline failure** → requires back-and-forth, iterative reasoning
- **Sequential analysis where step N depends on step N-1** → can't parallelize

### Use subagents

These require independent reasoning AND benefit from fresh context per unit:

- **Reviewing 8 analysis notebooks** for methodology issues → each notebook needs independent judgment
- **Investigating 6 failed experiments** by reading QC reports → reasoning per failure
- **Summarizing papers from 4 different subfields** → each summary requires reading comprehension
- **Auditing 10 scripts for lab convention compliance** → each script needs independent code review

### Use agent teams

These require workers to **communicate with each other**:

- **Competing hypotheses about a bug** → agents investigate different theories and debate
- **Multi-perspective code review** → security reviewer, performance reviewer, and test reviewer share findings
- **Cross-layer feature work** → frontend, backend, and test agents coordinate on interfaces
- **Adversarial paper review** → agents challenge each other's interpretations of your manuscript

## The litmus test

Two questions:

1. *"Could I write a bash one-liner or Snakemake rule that does this?"*
   - **Yes** → It's a pipeline. Don't use agents.
   - **No, because each item needs to be read and understood** → Subagents or agent team.

2. *"Do the workers need to talk to each other?"*
   - **No** → Subagents (fan-out, work, fan-in).
   - **Yes** → Agent team (shared task list, messaging, collaboration).
