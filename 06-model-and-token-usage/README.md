# Module 06 — Model Selection & Usage

## Two models, different strengths

Claude Code gives you access to different models. The two you'll use most:

### Sonnet (default- currently Sonnet 4.6)

- **Fast** — responds in seconds
- **Cheap** — a typical analysis session costs cents
- **Great for:** iteration, exploration, writing code, fixing bugs, generating plots, data wrangling
- **Use this 90% of the time**

### Opus (currently Opus 4.6)

- **Slower** — noticeably longer response times
- **More expensive** — roughly 5-10x the token usage of Sonnet
- **Better reasoning** — handles genuinely complex logic, multi-step inference, ambiguous situations
- **Great for:** statistical model selection, interpreting ambiguous results, writing a methods section, debugging subtle scientific errors, complex refactoring
- **Use this deliberately, not by default**

## Usage intuition


| Task                              | Model  | Approximate usage |
| --------------------------------- | ------ | ---------------- |
| Load data, run QC, make a plot    | Sonnet | $0.01–0.05       |
| Full DE analysis with plots       | Sonnet | $0.05–0.20       |
| Iterate on a figure 10 times      | Sonnet | $0.05–0.15       |
| Complex statistical reasoning     | Opus   | $0.50–2.00       |
| Writing a plan for a big pipeline | Opus   | $1.00-2.00       |


These are rough estimates — actual usage depends on how much data Claude reads and how many iterations you do.

## How to switch models

```bash
# Start with a specific model
claude --model claude-sonnet-4-6
claude --model claude-opus-4-6

# Or switch mid-session
/model claude-opus-4-6
/model claude-sonnet-4-6
```

## Checking your usage: `/usage`

Want to know how much a session has used so far? Use `/usage`:

```
/usage
```

This shows token usage and estimated usage for the current session. Helpful for building intuition about what uses few vs. many tokens — especially early on when you're calibrating.

## The rule of thumb

> **Default to Sonnet. Upgrade to Opus deliberately.**

Ask yourself: "Does this task require deep reasoning, or is it execution?" If it's execution (write this code, make this plot, parse this file), Sonnet is perfect. If it's reasoning (which statistical test is appropriate here? what does this unexpected result mean?), consider Opus.

Don't burn Opus on file parsing. Don't use Sonnet for subtle statistical reasoning. Match the model to the task.

## Key lesson

**Sonnet handles 90% of scientific computing tasks. Opus is for when you need a second opinion on something genuinely complex.** The usage difference is real — be intentional about when you upgrade.