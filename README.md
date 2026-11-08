# Sensitive Prompt Insights

[![CI](https://github.com/LukeLunn/Sensitive-Prompt-Insights/actions/workflows/ci.yml/badge.svg)](https://github.com/LukeLunn/Sensitive-Prompt-Insights/actions/workflows/ci.yml)

Detect sensitive data in GenAI prompts, group prompts by how they are used, and
report insights with calibrated uncertainty. The intention for this repo is to practise AI-security-based tasks and develop and evidence skills for working in this field. The choices made are in part to be effective and solve the problems considered, but also to fill in gaps in my skillset. This means some models are not considered if I am already familiar with their use.

> **Data policy:** this project uses synthetic or public data only. It never uses
> real, employer or customer data.

## Status

In progress. Scaffolding is in place (packaging, lockfile, linting, strict typing,
tests, CI). Nemotron-PII loading and exploratory analysis are done; the detection
baselines are next (see [Roadmap](#roadmap)).

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
scripts/                         one-off analysis (e.g. explore_nemotron.py), not part of the package
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

- [x] Load Nemotron-PII into typed DataFrames; exploratory analysis of labels,
      spans and splits.
- [ ] Map the 55 PII labels to report categories.
- [ ] Baselines on the source documents: a regex detector, and TF-IDF + logistic
      regression. Report precision, recall and F1 per category, broken down by
      seen and unseen document types.
- [ ] Prompt dataset: wrap passages in prompt templates and add benign and
      hard-negative prompts (split by template), then re-run the baselines.
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

## Dataset notes

- 200,000 synthetic documents (100k train, 100k test) with 1.65M labelled PII
  spans across 55 labels. No missing or empty texts; 7 documents have no spans.
  Median 7 spans per document.
- **Split:** the source split holds out whole domains (30 train industries vs 29
  test). One domain, `Insurance`, appears in both and is removed from test. About
  24% of test rows share a document type with train, so results are reported
  separately for seen and unseen document types, to show whether the model learns
  the PII or the template wording.
- **Document types** (about 1,000, with many near-duplicates such as "Tax Return"
  vs "Tax Return Form") were rejected as a grouping key because near-duplicates
  would cross the split.
- **Offsets** were verified on all spans. 0.78% of span texts differ from the
  document only in letter case; positions are used as the source of truth.

## Use of AI assistance

I used an AI coding assistant (Claude Code) on this project. I write most of the
project code myself; where the assistant changed code, the log below says so. The
assistant helps with explanations, code review, and drafting
documentation. This log records what it helped with and what I changed.

| Date | Area | What the assistant did | What I did / corrected |
|------|------|------------------------|------------------------|
| 2026-11-04 | README | Drafted this README from my project notes. | Rewrote the introduction with some personal context and reasoning for this repo. |
| 2026-11-04 | Dataset research | Researched public PII datasets and licences (Nemotron-PII, Gretel, ai4privacy, PANOPTICON). | Chose Nemotron-PII. |
| 2026-11-04 | Environment | Diagnosed a Windows Smart App Control block on pandas 3.1.1 and excluded that version; explained the mypy override for untyped `datasets` and adding `pandas-stubs`. | Added the dependencies and mypy config. |
| 2026-11-05 | Package structure | Helped put together the subpackage structure and module skeletons. | Chose the pipeline stages the structure follows. |
| 2026-11-08 | Docs | Aligned module docstrings and the README roadmap with the Nemotron-based dataset plan; added the data attribution section. | Chose the Nemotron approach and asked for the docs to be brought in line with it. |
| 2026-11-08 | Exploration | Explained the span format and safe parsing (`ast.literal_eval`), suggested checks, cross-checked my numbers, and found the source split already holds out domains. | Wrote `explore_nemotron.py` and ran the analysis. |
| 2026-11-08 | Data loading | Reviewed my loader, added the typed `Span` and pandas conversion, and found span-text mismatches were case-only. | Wrote the first version, then revised the assistant's changes (renamed fields, simplified the structure). |
