# Skill Scaffold — Build Your Own

Use this template to create a skill for a task you do repeatedly. Fill in each section, then save it as `SKILL.md` in a descriptive directory.

---

# Skill: [Name of your skill]

## Context

[What is this skill for? When should Claude use it? One paragraph.]

## Inputs

- **[Input 1]**: [Description, format, where to find it]
- **[Input 2]**: [Description, format, defaults]
- **[Output location]**: [Where results should be saved]

## Procedure

### Step 1 — [Name this step]

1. [First action]
2. [Second action]
3. [What to report to the user]

**Stop and ask if:** [conditions where Claude should not proceed without human input]

### Step 2 — [Name this step]

1. [Actions...]

### Step 3 — [Name this step]

1. [Actions...]

## Output expectations

- [What files are produced?]
- [What format?]
- [What should the user see as confirmation?]

## Failure modes

| Issue | What to do |
|-------|-----------|
| [Common problem 1] | [How to handle it] |
| [Common problem 2] | [How to handle it] |
| [Ambiguous situation] | Stop and ask the user |

## Dependencies

```python
# List the packages this skill requires
```

---

## Tips for writing good skills

1. **Be specific** — "normalize the data" is too vague; "apply DESeq2 median-of-ratios normalization" is right
2. **Include failure modes** — what can go wrong? When should Claude stop and ask?
3. **Define outputs precisely** — what columns, what format, what file names?
4. **Test it** — run the skill once and refine based on what Claude gets wrong
5. **Version control it** — skills should evolve as your methods do
