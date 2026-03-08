# CLAUDE.md — Lab Starter Template

This is the project-level CLAUDE.md for the claude-code-workshop repository.
Claude reads this file at the start of every session.

## About this project

This is a workshop teaching scientists to use Claude Code effectively.
The repo contains teaching materials, example data, and exercises organized by module.

## Conventions

- All Python code should use Python 3.10+ syntax
- Prefer pandas, seaborn, matplotlib, scanpy, and statsmodels for data analysis
- Use snake_case for variables and functions
- Figures: 300 DPI, colorblind-safe palettes (use seaborn's "colorblind" palette by default)
- File naming: `{descriptor}_{version}.{ext}` (e.g., `counts_normalized_v2.csv`)
- Always set random seeds for reproducibility (`random_state=42` unless otherwise specified)
- When writing scripts, include a brief docstring at the top explaining purpose and inputs/outputs

## Statistical defaults

- For differential expression: DESeq2 (via pydeseq2) or Wilcoxon rank-sum as appropriate
- Always report effect sizes alongside p-values
- Use Benjamini-Hochberg for multiple testing correction
- Flag any result with n < 3 per group for human review

## Project structure

```
00-intro-and-setup/     — installation and orientation
01-core-loop/           — the ask → inspect → correct → repeat workflow
02-context-management/  — understanding and managing the context window
03-memories-and-claude-md/ — persisting conventions across sessions
04-skills/              — encoding lab SOPs as executable skills
05-subagents/           — orchestrator/worker patterns for large tasks
06-model-and-token-cost/ — choosing the right model
07-trust-and-rigor/     — verification, reproducibility, scientific rigor
```
