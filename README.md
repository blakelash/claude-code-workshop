# Claude Code for Scientists — Workshop

A hands-on workshop teaching scientists how to use [Claude Code](https://docs.anthropic.com/en/docs/claude-code) as an AI-powered research assistant. Designed for biologists, bioinformaticians, and computational researchers at Fred Hutch and beyond.

## Who this is for

Scientists who write code as part of their research — whether you're analyzing RNA-seq data, processing microscopy images, or wrangling clinical datasets. No prior AI coding assistant experience required.

## Workshop structure

| Module | Topic | Time |
|--------|-------|------|
| **00** | [Intro & Setup](00-intro-and-setup/) | 15 min |
| **01** | [The Core Loop](01-core-loop/) | 20 min |
| **02** | [Context Management](02-context-management/) | 15 min |
| **03** | [Memories & CLAUDE.md](03-memories-and-claude-md/) | 20 min |
| **04** | [Skills](04-skills/) | 20 min |
| **05** | [Subagents](05-subagents/) | 15 min |
| **06** | [Model Selection & Cost](06-model-and-token-cost/) | 5 min |
| **07** | [Trust & Rigor](07-trust-and-rigor/) | 15 min |

## Mental model

**You are the PI. Claude is a very fast postdoc.**

It's brilliant at executing tasks, tireless, and fast — but it doesn't know your scientific question, your lab's conventions, or when a result looks biologically implausible. Your job is to direct, verify, and ensure rigor. This workshop teaches you how.

## Prerequisites

- A terminal you're comfortable in (macOS Terminal, iTerm2, Windows Terminal, VS Code terminal)
- Node.js 18+ installed
- An Anthropic API key (provided for the workshop) or a Claude Pro/Max subscription
- A code editor (VS Code recommended but not required)

## Quick start

```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Clone this repo
git clone https://github.com/FredHutch/claude-code-workshop.git
cd claude-code-workshop

# Start Claude Code
claude
```

## After the workshop

- Browse the [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- Explore the [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)
- Build your lab's `CLAUDE.md` and `skills/` library
- This repo stays available as a reference
