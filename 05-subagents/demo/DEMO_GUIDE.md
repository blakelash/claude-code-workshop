# Module 05 Demo Guide

## Setup

The `scripts/` directory contains three intentionally flawed analysis scripts written by fictional rotation students. Each script has issues across statistics, figures, and reproducibility — but the issues are different per script, which is the point.

The `agents/` directory contains three custom subagent definitions. To use them in the demo, copy them to the project's `.claude/agents/` directory:

```bash
mkdir -p .claude/agents
cp 05-subagents/demo/agents/*.md .claude/agents/
```

Then restart Claude Code (or use `/agents` to verify they loaded).

---

## Demo 1: Subagents — parallel independent review

### What to show

Three custom subagents each review the same scripts from a different angle, independently. Each subagent has its own context window. They report results back to you — they don't talk to each other.

### The prompt

```
I have three analysis scripts in 05-subagents/demo/scripts/ written by
different rotation students. I need each script reviewed before we submit.

For each of the three scripts, run all three reviewers:
- Use the stats-reviewer subagent to check statistical methods
- Use the figure-reviewer subagent to check figure quality
- Use the reproducibility-reviewer subagent to check reproducibility

Save each review to 05-subagents/demo/reviews/{script}_{reviewer}.md.

After all reviews are done, write a summary to 05-subagents/demo/reviews/summary.md
that identifies the top 5 most common issues across all scripts.
```

### What the audience should notice

- Claude dispatches 9 subagent tasks (3 scripts × 3 reviewers)
- Each subagent has a **focused system prompt** — the stats reviewer doesn't comment on figures, the figure reviewer doesn't comment on p-values
- Each subagent works with **fresh context** — no cross-contamination between scripts
- The **parent session** stays clean — it only sees the summaries, not the full reasoning
- At the end, the parent synthesizes across all 9 reviews

### Intentional issues planted in the scripts

**differential_expression.py**:
- No multiple testing correction (tests ~20k genes with raw p < 0.05)
- No effect sizes (no fold change calculation)
- No random seed
- Hardcoded absolute paths (`/home/jsmith/...`)
- Jet colormap on heatmap
- Saves heatmap as JPEG
- No DPI setting
- No docstring for inputs/outputs
- Magic number: 50 (top genes) and 0.05 (threshold) unexplained

**clustering_analysis.py**:
- No random seeds for PCA, UMAP, or Leiden clustering
- Hardcoded absolute path (`/Users/agarcia/...`)
- Deprecated `binom_test` (should use `binomtest`)
- No effect size for the binomial test
- No DPI on figure save
- Cell type assignment is manual/hardcoded without validation
- No package version info
- Magic numbers: resolution=0.8, n_neighbors=15, n_top_genes=2000

**survival_analysis.py**:
- Tests 10 genes without multiple testing correction
- No effect sizes (hazard ratios not extracted from log-rank)
- No random seed for train_test_split
- Hardcoded absolute paths (`/data/tcga/...`)
- No DPI on KM plot saves
- Default matplotlib colors
- Magic numbers: test_size=0.3, median split cutoff
- No docstring for inputs/outputs
- Scaling before train/test split (data leakage)

---

## Demo 2: Agent team — build a lab data dashboard

### What to show

An agent team where teammates **coordinate across boundaries** to build a working app. This is the canonical agent team use case: frontend, backend, and tests are separate concerns, but they share interfaces (API contracts, data shapes) and need to stay in sync.

### Why this can't be subagents

If you dispatched three independent subagents to build frontend, backend, and tests:
- The frontend subagent would invent an API contract
- The backend subagent would invent a *different* API contract
- The test subagent would test against a *third* API contract
- Nothing would work together

Agent teams solve this because teammates **message each other** to agree on shared interfaces before building.

### Prerequisites

Agent teams are experimental. Enable first:
```bash
# In settings.json or as environment variable
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

### The prompt

```
Build a simple lab data dashboard for viewing experiment QC results.
Create it in 05-subagents/demo/dashboard/.

The app should:
- Display a table of experiments with their QC status (pass/fail)
- Let users click an experiment to see detailed QC metrics
- Have a simple API that serves experiment data from a JSON file
- Include sample data for 10 experiments with realistic QC metrics
  (RIN scores, library complexity, mapping rates, etc.)

Create an agent team with three teammates:

1. "backend": Build a FastAPI server that serves experiment data.
   Create the sample data JSON. Define the API endpoints.

2. "frontend": Build a simple HTML/JS frontend (no framework needed,
   just vanilla JS) that fetches from the API and displays the table
   and detail view.

3. "tests": Write tests for the API endpoints using pytest.
   Make sure the tests match the actual API contract.

The backend and frontend teammates should coordinate on the API
contract before building. The tests teammate should wait for the
backend to define the endpoints before writing tests.

Keep it simple — this is a demo, not production code.
```

### What the audience should notice

- The **lead** creates a task list with dependencies: API contract first, then parallel build, then integration
- The **backend teammate** defines endpoints and shares the contract with the others
- The **frontend teammate** waits for (or messages) the backend to confirm the API shape before building
- The **tests teammate** writes tests against the *actual* endpoints, not guessed ones
- Teammates **message each other** when interfaces change: "I added a `/experiments/{id}/qc` endpoint, update your fetch calls"
- The result is a working app where all three pieces fit together — something that would be very hard with independent subagents

### Key teaching moment

After the demo, ask the audience:

> "What would have happened if we used subagents instead of an agent team?"

Answer: Each subagent would have built its piece in isolation. The frontend would call `/api/experiments`, the backend would serve `/experiments/list`, and the tests would check `/get_experiments`. Three pieces that don't connect. Agent teams let them negotiate the contract first, then build to it.

> "When does this matter for science?"

Answer: Any time you're building something with multiple interacting components — a pipeline with a config system and a reporting layer, a Shiny/Streamlit app with data processing and visualization, an analysis framework where modules need to agree on data formats. If the pieces need to talk to each other at design time, use an agent team.

---

## Side-by-side comparison for the audience

| | Demo 1: Subagents | Demo 2: Agent team |
|--|---|---|
| **Task** | Review scripts against known criteria | Build an app with interacting components |
| **Workers** | Each reviews independently, reports back | Each builds a component, coordinating on interfaces |
| **Communication** | Workers → parent only | Workers ↔ workers + lead |
| **Output** | 9 independent reviews + synthesis | 1 working app where all pieces fit together |
| **Why this pattern** | Criteria are fixed; independence prevents anchoring | Components share interfaces; coordination prevents mismatch |
