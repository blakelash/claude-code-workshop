# Module 02 — Context Management

## The context window: what Claude "knows" right now

Everything Claude can work with in a session lives in its **context window** — a finite buffer that holds:

- Your prompts
- Claude's responses
- File contents it has read
- Code it has executed and its output
- Tool results

When this buffer fills up, older content gets compressed or dropped. Claude doesn't "forget" suddenly — it degrades gradually, like a conversation where someone starts confusing details from an hour ago.

## Why this matters for science

In a long analysis session, context degradation looks like:

- Claude hedges on variable names it was confident about earlier
- It re-reads files it already processed
- It quietly changes an analysis parameter without flagging the change
- It loses track of which samples were filtered in a previous step

See `examples/annotated_session_transcript.md` for a real example of this happening.

## The three decisions

When you notice Claude getting confused or a session getting long, you have three options:

### 1. `/clear` and reload

```
/clear
```

This wipes the session context but **everything on disk is preserved** — all files Claude wrote, all results it saved. You start fresh but lose no work. After clearing, you can re-orient Claude:

```
Read the files in results/ and data/processed/ to see what we've done so far.
Now continue with the differential expression analysis.
```

### 2. Start a fresh session

Just exit and restart `claude`. Same effect as `/clear` — disk state is preserved, context is reset.

### 3. Continue with a summary prompt

If you don't want to clear, give Claude a summary to anchor on:

```
To summarize where we are: we've loaded the count matrix from data/counts_raw.csv,
filtered out genes with < 10 counts across all samples, normalized using DESeq2's
median-of-ratios method, and saved the normalized matrix to data/processed/counts_normalized.csv.
The PCA shows clear separation between WT and KO on PC1.
Now let's run differential expression analysis.
```

This works but adds to the context window rather than freeing it.

## The discipline: one task per session

The single best habit for context management:

> **One analytical task per Claude session.**

Don't do QC, normalization, DE analysis, pathway analysis, and figure generation in one session. Do each as its own session. Claude's work persists on disk between sessions — there's no penalty for restarting.

### `/compact` — compress without clearing

Sometimes you don't want to wipe context entirely — you just want to free up space. The `/compact` command compresses the conversation history, keeping a summary of what's been done while reducing token usage:

```
/compact
```

You can also provide a focus hint to tell Claude what to prioritize in the summary:

```
/compact focus on the normalization steps and DE results
```

**`/clear` vs `/compact`:**
- `/clear` = total reset, re-reads `CLAUDE.md`, you re-orient from disk
- `/compact` = lossy compression, Claude retains a summary but some details will be lost

Use `/compact` when you want to keep going but the session is getting sluggish. Use `/clear` when Claude is actively confused or you're switching tasks.

## CLAUDE.md survives `/clear`

This is why `CLAUDE.md` is so powerful. When you `/clear` or start a new session, Claude re-reads `CLAUDE.md` automatically. Every convention, every preference, every instruction in that file carries over without you re-typing it.

This is the bridge to Module 03.

## Exercise

1. Start a Claude session in `01-core-loop/` and do several analysis steps (QC, a plot, some filtering)
2. After 5-6 exchanges, notice if Claude starts getting less precise
3. Try `/clear`, then ask Claude to pick up where you left off by reading the files on disk
4. Compare: is Claude sharper after the clear?

## Key lesson

**A confused Claude mid-session isn't a model problem — it's a context problem.** You can fix it by clearing and reloading. The cost is low (seconds), the benefit is high (fresh, focused context).
