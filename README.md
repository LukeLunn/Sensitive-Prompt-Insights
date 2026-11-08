# Sensitive Prompt Insights

[![CI](https://github.com/LukeLunn/Sensitive-Prompt-Insights/actions/workflows/ci.yml/badge.svg)](https://github.com/LukeLunn/Sensitive-Prompt-Insights/actions/workflows/ci.yml)

Detect sensitive data in GenAI prompts, group prompts by how they are used, and
report insights with calibrated uncertainty. The intention for this repo is to practise AI-security-based tasks and develop and evidence skills for working in this field. The choices made are in part to be effective and solve the problems considered, but also to fill in gaps in my skillset. This means some models are not considered if I am already familiar with their use.

> **Data policy:** this project uses synthetic or public data only. It never uses
> real, employer or customer data.

## Status

Early stage. The project scaffolding is in place: packaging, a lockfile, linting,
strict type checking, tests and CI. The detection and analysis work comes next (see
[Roadmap](#roadmap)).

## Getting started

Requires [uv](https://docs.astral.sh/uv/). uv installs the pinned Python version
(3.13, from `.python-version`) if you don't have it.

```bash
git clone https://github.com/LukeLunn/Sensitive-Prompt-Insights.git
cd Sensitive-Prompt-Insights
uv sync                      # create .venv from the lockfile
uv run pre-commit install    # optional: run the checks on every commit
```

## Running the checks

These are the same checks CI runs:

```bash
uv run ruff check .          # lint
uv run ruff format --check . # formatting
uv run mypy src tests        # strict type checking
uv run pytest                # tests
```

## Project layout

```
src/sensitive_prompt_insights/   package code, one subpackage per pipeline stage:
  data/                          load Nemotron-PII, build the prompt dataset, split
  detection/                     regex and TF-IDF baselines, per-category metrics
  clustering/                    embeddings, UMAP + HDBSCAN, stability check
  uncertainty/                   bootstrap and Wilson intervals, calibration
  labelling/                     hand-labelled gold set, out-of-fold label audit
  reporting/                     usage-insight report
tests/                           pytest tests
.github/workflows/ci.yml         CI: lint, format, types, tests on Python 3.12 and 3.13
pyproject.toml / uv.lock         declared dependencies / exact locked versions
```

## Why it is set up this way

- **uv with a committed lockfile:** anyone can rebuild the exact same environment,
  and indirect dependencies can't drift between machines or CI runs.
- **src layout:** tests run against the installed package, not loose files in the
  working folder, so packaging mistakes show up early.
- **Python 3.13 (supports 3.12+):** recent, but with reliable pre-built wheels for
  ML libraries. CI tests both versions.
- **pre-commit plus CI:** the same Ruff checks run locally before each commit and
  on GitHub, so problems are caught before review.
- **mypy strict:** types act as checked documentation and catch errors early.
- **Dependencies added only when code needs them:** `pyproject.toml` shows what the
  project actually uses.

## Roadmap

- [ ] Prompt dataset (~2,000–3,000 prompts): Nemotron-PII passages wrapped in
      prompt templates, PII labels mapped to report categories, plus benign and
      hard-negative prompts. Document how it was built. Use a grouped split so
      near-duplicates never appear in both train and test.
- [ ] Baselines: a regex detector, and TF-IDF + logistic regression. Report
      precision, recall and F1 per category.
- [ ] Embeddings, UMAP and HDBSCAN clustering, with a stability check.
- [ ] Bootstrap confidence intervals and a calibration plot.
- [ ] Hand-labelled gold set with an out-of-fold label audit.
- [ ] Usage-insight report: share of risky prompts per cluster with Wilson
      intervals, flagging groups too small to report.

## Data and attribution

Source documents and PII labels come from
[Nemotron-PII](https://huggingface.co/datasets/nvidia/Nemotron-PII) by NVIDIA, a
synthetic dataset licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This project adapts it
by wrapping passages in prompt templates, grouping its PII labels into broader
categories, and adding benign prompts. The raw dataset is downloaded at runtime
and not stored in this repository.

## Use of AI assistance

I used an AI coding assistant (Claude Code) on this project. I write the project
code myself. The assistant helps with explanations, code review, and drafting
documentation. This log records what it helped with and what I changed.

| Date | Area | What the assistant did | What I did / corrected |
|------|------|------------------------|------------------------|
| 2026-11-04 | README | Drafted this README from my project notes. | Rewrote the introduction with some personal context and reasoning for this repo. |
| 2026-11-05 | Package structure | Helped put together the subpackage structure and module skeletons. | Chose the pipeline stages the structure follows. |
| 2026-11-08 | Docs | Aligned module docstrings and the README roadmap with the Nemotron-based dataset plan; added the data attribution section. | Chose the Nemotron approach and asked for the docs to be brought in line with it. |
