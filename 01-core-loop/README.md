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

### Step 0 — Plan before you execute (`/plan`)

For complex tasks, ask Claude to **plan** before it starts writing code. The `/plan` command puts Claude into planning mode — it will outline an approach and ask for your approval before executing anything.

```
/plan
```

Then describe your task:

```
I want to do QC on this RNA-seq count matrix, filter low-count genes,
normalize, and make a PCA plot. What's your approach?
```

Claude will outline the steps, you approve or adjust, then it executes. This is the PI/postdoc dynamic in action — you wouldn't let a postdoc run an experiment without discussing the plan first.

**When to use `/plan`:** multi-step analyses, unfamiliar data, anything where the wrong approach wastes significant time. For quick one-off tasks (make a plot, fix this bug), just ask directly.

### Step 1 — Inspect first, ask later

Start every analysis by letting Claude look at your data before you ask it to do anything:

```
Look at the data in data/counts_raw.csv and tell me what you see.
```

This establishes shared context. Claude will report dimensions, column names, data types, obvious issues — and you'll catch misunderstandings before they compound.

### Step 2 — Ask for QC

```
Run basic QC on this count matrix:
- Check for missing values
- Show the library size distribution across samples
- Flag any outlier samples (>3 SD from mean library size)
```

Watch what Claude does. It will write and execute Python code. Check that the code makes sense, that the outputs look right.

### Step 3 — Ask for a visualization

```
Make a PCA plot of these samples, colored by condition.
```

You'll probably get something functional but ugly. That's expected.

### Step 4 — Iterate on the plot

This is where the core loop shines. Instead of re-prompting from scratch:

```
Good start. Now:
- Use a colorblind-safe palette
- Add sample labels
- Increase the figure size to 8x6
- Add the variance explained to axis labels
```

Then maybe:

```
Move the legend outside the plot area. Make the title more descriptive.
```

Each correction takes seconds. You're steering, not re-driving.

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
