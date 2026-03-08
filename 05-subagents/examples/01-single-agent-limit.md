# The Single-Agent Limit

## Scenario

You have 48 RNA-seq samples to process through a standard pipeline:
1. Read QC (fastqc-style checks)
2. Adapter trimming
3. Alignment to reference genome
4. Count quantification
5. Sample-level QC report

## What happens in one session

```
Exchange 1-5:   Samples 1-3 processed perfectly. Clean code, exact parameters.
Exchange 6-10:  Samples 4-6 processed. Still good, but Claude re-reads the
                reference genome path each time (it's losing track of state).
Exchange 11-20: Samples 7-12. Claude starts abbreviating QC checks — skipping
                the adapter content plot it generated for early samples.
Exchange 25-35: Samples 15-20. Context is heavy. Claude processes a sample but
                uses trimming parameters from 3 samples ago. You don't notice
                because the code runs without errors.
Exchange 40+:   You're lucky to get here. Claude may start hallucinating file
                paths or confusing sample metadata.
```

## The problem isn't Claude — it's context

Each sample adds ~2,000 tokens of code and output to the context window. By sample 15, that's 30,000+ tokens of accumulated processing history that Claude must navigate. Important details from the beginning get compressed or lost.

## The solution: one worker per sample (or small batch)

```
Orchestrator:
  "Process all 48 samples. Here's the pipeline spec. Dispatch workers."

Worker (×48, each with fresh context):
  "Process sample_WT_01.fastq through the pipeline.
   Parameters: [exact params from skill file]
   Save results to results/sample_WT_01/"

Orchestrator:
  "All workers done. Read results from results/*/. Build summary table."
```

Each worker has:
- Fresh, clean context
- Only its own sample to think about
- The same exact instructions (from the skill file)
- No accumulated baggage from other samples
