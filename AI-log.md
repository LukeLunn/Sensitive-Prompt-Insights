# Use of AI assistance

I used an AI coding assistant (Claude Code) on this project. I write most of the
project code myself; where the assistant changed code, the log below says so. The
assistant helps with explanations, code review, and drafting
documentation. This log records what it helped with and what I changed.

| Date | Area | What the assistant did | What I did / corrected |
|------|------|------------------------|------------------------|
| 2026-11-04 | README | Drafted the README from my project notes. | Rewrote the introduction with some personal context and reasoning for this repo. |
| 2026-11-04 | Dataset research | Researched public PII datasets and their licences. | Chose Nemotron-PII. |
| 2026-11-04 | Environment | Diagnosed a Windows install block and explained the type-checking setup. | Added the dependencies and mypy config. |
| 2026-11-05 | Package structure | Helped put together the subpackage structure and module skeletons. | Chose the pipeline stages the structure follows. |
| 2026-11-08 | Docs | Aligned the docstrings and README with the dataset plan. | Chose the Nemotron approach and asked for the docs to match. |
| 2026-11-08 | Exploration | Explained the data format, suggested checks and cross-checked my results. | Wrote `explore_nemotron.py` and ran the analysis. |
| 2026-11-08 | Data loading | Reviewed my loader and added typing and the pandas conversion. | Wrote the first version, then revised the assistant's changes. |
| 2026-11-08 | Tests | Gave example tests and suggested extra cases. | Wrote the tests; caught a wrong offset in the assistant's example. |
| 2026-11-08 | Label mapping | Proposed the categories, typed out the mapping, reviewed my code and applied the final fix. | Approved the categories, scoped out quasi-identifier combinations, and wrote `categories_for` and the tests. |
