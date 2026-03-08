# Module 02 — Context Management

## What is context?

When you talk to Claude, it doesn't have memory between sessions. Everything it "knows" during a conversation comes from **context** — the text that's been fed into the model for this session. That includes your prompts, Claude's responses, file contents it read, code it ran, and the output of that code. All of it lives in one buffer called the **context window**.

### Tokens: the unit of context

Context is measured in **tokens**, not words or characters. A token is roughly ¾ of a word — so "differential expression analysis" is about 4 tokens. A 200-line Python script might be ~800 tokens. A CSV with 1,000 rows could be 10,000+ tokens.

Claude's context window is **200,000 tokens**. That sounds like a lot — and it is — but it fills up faster than you'd expect:

| Content | Approximate tokens |
|---------|-------------------|
| Your one-line prompt | 10–30 |
| Claude's response with code | 200–1,000 |
| A 500-line Python script Claude reads | ~2,000 |
| A CSV file with 1,000 rows | 5,000–15,000 |
| 10 back-and-forth exchanges with code | 10,000–30,000 |

After a long analysis session (20+ exchanges, several files read, lots of code output), you can easily hit 50-100k tokens. That's when things start to degrade.

### `/context` — check where you stand

You can check your current context usage at any time:

```
/context
```

This shows how much of the 200k window you've used. Get in the habit of checking this when a session feels sluggish — it tells you whether you need to `/compact` or `/clear`.

## The context window in practice

Everything Claude can work with in a session lives in this window — a finite buffer that holds:

- Your prompts
- Claude's responses
- File contents it has read
- Code it has executed and its output
- Tool results

When this buffer fills up, older content gets compressed or dropped. Claude doesn't "forget" suddenly — it degrades gradually, like a conversation where someone starts confusing details from an hour ago.

## Point to files — don't paste content

One of the fastest ways to burn through context is pasting data directly into the chat. If you copy-paste a 500-row CSV into your prompt, that's thousands of tokens sitting in context for the rest of the session. Every future exchange has to carry that payload.

Instead, **give Claude the file path and let it decide how to handle the data:**

```
# ❌ Don't do this
Here's my data:
gene_id,sample_WT_1,sample_WT_2,...
ENSG00000001,342,451,...
ENSG00000002,1203,1187,...
[500 more rows pasted in]

# ✅ Do this
Analyze the count matrix in data/counts_raw.csv
```

When you point Claude at a file, it reads what it needs intelligently — it might read the first few rows to understand the structure, then write code to process the full file without loading the entire thing into context. The data stays on disk where it belongs, and context stays clean for the actual conversation.

This applies to output too. If Claude generates a large table or result set, ask it to **save to a file** rather than printing everything to the chat:

```
Save the DE results to results/de_results.csv instead of printing them here.
```

**Rule of thumb:** if it's more than ~20 rows of data, it belongs in a file, not in the chat.

## Why this matters for science

In a long analysis session, context degradation shows up in predictable ways. Learn to recognize these:

**Precision fading:**
- Hedges on variable names it was confident about earlier ("I think the column was called...")
- Shifts from specific to vague language — "the p-value is 0.003" becomes "the p-value might be around 0.003"
- Mixes up sample or group names — calling "KO" samples "treatment," swapping condition labels

**Redundant work:**
- Re-reads files it already processed earlier in the session
- Rewrites a filtering or normalization step it already performed
- Asks you questions you already answered (or that are in `CLAUDE.md`)

**Silent drift:**
- Quietly changes a statistical test or parameter without flagging the change
- Loses track of which samples were filtered or excluded in a previous step
- Falls back to generic defaults (matplotlib, rainbow colors) instead of your project conventions from `CLAUDE.md`

**Confabulation:**
- Describes what a file contains from "memory" instead of re-reading it — and gets details wrong
- References file paths that don't exist or invents output file names

Any one of these is a signal to check `/context` and consider `/compact` or `/clear`.

See `examples/annotated_session_transcript.md` for a walkthrough showing several of these happening in sequence.

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

### 2. `/compact` — compress without clearing

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

### 3. Continue with a summary prompt

If you don't want to clear, and don't want compaction done by Claude give Claude a summary to anchor on:

```
To summarize where we are: we've loaded the count matrix from data/counts_raw.csv,
filtered out genes with < 10 counts across all samples, normalized using DESeq2's
median-of-ratios method, and saved the normalized matrix to data/processed/counts_normalized.csv.
The PCA shows clear separation between WT and KO on PC1.
Now let's run differential expression analysis.
```

This works but I would have Claude write this itself

## The discipline: one task per session

The single best habit for context management:

> **One analytical task per Claude session.**

Don't do QC, normalization, DE analysis, pathway analysis, and figure generation in one session. Do each as its own session. Claude's work persists on disk between sessions — there's no penalty for restarting.

## Autocompaction: what happens if you do nothing

If you never run `/compact` or `/clear`, Claude doesn't just crash when the context window fills up. It **autocompacts** — automatically compressing older parts of the conversation to make room for new exchanges. You'll see a message like "conversation was automatically compacted" when this happens.

This is a safety net, not a strategy. Autocompaction is lossy and you don't control what gets kept or dropped. Claude picks what to summarize, and it may compress away the exact details you needed (a specific filtering threshold, which samples were excluded, the exact test that was used). The earlier in the conversation something happened, the more aggressively it gets compressed.

**Bottom line:** Don't rely on autocompaction. It's better to proactively `/compact` (where you can provide a focus hint) or `/clear` when you notice context getting heavy. Check `/context` periodically so autocompaction doesn't surprise you.

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
