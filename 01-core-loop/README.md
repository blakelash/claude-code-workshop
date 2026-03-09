# Module 01 — The Core Loop

## The skill isn't prompting — it's iterating

The most common mistake new users make: spending 10 minutes crafting the "perfect" prompt. Don't. The real workflow is:

```
Ask → Inspect → Correct → Repeat
```

Claude will rarely get everything right on the first try. That's fine. The power is in how fast you can iterate.
Claude can/will ask you questions as part of the build, this is where a lot of the iteration happens. 

## Setup

```bash
cd 01-core-loop
claude
```

## Walkthrough

### Step 0 — Inspect first, ask later

Start every analysis by letting Claude look at your data and repo before you ask it to do anything:

```
Look at the data in data/counts_raw.csv and tell me what you see.
```

This establishes shared context. Claude will report dimensions, column names, data types, obvious issues — and you'll catch misunderstandings before they compound. Think of it like handing a new rotation student the dataset and asking "what do you notice?" before giving them instructions.

### Step 1 — Plan before you execute (`/plan`)

Now that Claude has seen the data, ask it to **plan** before writing code. The `/plan` command puts Claude into planning mode — it will outline an approach and ask for your approval before executing anything.

```
/plan
```

Then describe your task:

```
I want to do QC on this RNA-seq count matrix, filter low-count genes,
normalize, and make a PCA plot. What's your approach?
```

During planning, Claude may ask you clarifying questions — e.g., "What normalization method do you prefer?" or "Should I filter by minimum counts per gene or per sample?" This back-and-forth is the **interview**, and you can proactively ask Claude questions too.

Once the plan is finalized, Claude presents the **execute options**:

```
Claude has written up a plan and is ready to execute. Would you like to proceed?

 ❯ 1. Yes, clear context (11% used) and auto-accept edits (shift+tab)
   2. Yes, auto-accept edits
   3. Yes, manually approve edits
   4. Type here to tell Claude what to change
```

- **Option 1 (clear context)** is often the best choice. The plan is saved to a file, so Claude can follow it even after clearing the conversation. This frees up maximum context for the actual execution — especially valuable for multi-step analyses. (More on context in [Module 02](../02-context-management/).)
- **Option 2** auto-accepts edits but keeps the current context.
- **Option 3** lets you approve each file edit individually — useful when you want to review closely.
- **Option 4** lets you push back and refine the plan before any code is written.

**When to use `/plan`:** multi-step analyses, unfamiliar data, anything where the wrong approach wastes significant time. For quick one-off tasks (make a plot, fix this bug), just ask directly.

### Step 2 — Iterate on a plot

This is where the core loop shines. Ask Claude for a PCA plot:

```
Make a PCA plot of these samples, colored by condition.
```

You'll probably get something functional but ugly. That's expected — now iterate:

```
Good start. Now:
- Use a colorblind-safe palette
- Add sample labels
- Increase the figure size to 8x6
- Add the variance explained to axis labels
```

Then keep going:

```
Move the legend outside the plot area. Make the title more descriptive.
```

Each correction takes seconds. You're steering, not re-driving. Notice how each round builds on the previous state — Claude remembers what it did and modifies in place.

## Key lesson

**Resist the urge to write a perfect prompt.** Start rough, inspect the output, correct what's wrong, repeat. Three fast iterations beats one slow attempt at perfection every time.

## Exercise

1. Start a Claude session in this directory
2. Point Claude at `data/counts_raw.csv` and ask it to explore the data
3. Ask for a QC summary
4. Ask for a plot — accept the first version even if it's imperfect
5. Iterate at least 3 times to improve the plot
6. **Bonus:** Try the same workflow with `exercises/plate_reader.csv`

## What to notice

- How quickly you can go from raw data to a polished figure
- How each correction builds on the previous state (Claude remembers what it did)
- When Claude misunderstands something, a one-line correction is faster than a detailed re-prompt
