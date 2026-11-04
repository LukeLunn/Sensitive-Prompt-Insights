# Sensitive Prompt Insights

Portfolio project: detect sensitive data in GenAI prompts, group usage, and report
insights with calibrated uncertainty. Uses synthetic or public data only. Never use
real, employer or customer data.

## Stack and layout
- Python 3.13 (pinned in `.python-version`; supports >=3.12), managed with uv.
- Dependencies are declared in `pyproject.toml`; exact versions are in `uv.lock`.
  Commit both. Never commit `.venv/`.
- src layout: code in `src/sensitive_prompt_insights/`, tests in `tests/`.
- Dev tools (pytest, ruff, mypy, pre-commit) are in the `dev` dependency group.

## Commands (run from the repo root)
- Sync environment: `uv sync`
- Tests: `uv run pytest`
- Lint: `uv run ruff check .`
- Format check: `uv run ruff format --check .`
- Types (strict): `uv run mypy src tests`
- Add a dependency: `uv add <pkg>`; dev tool: `uv add --dev <pkg>`. Do not use `pip install`.

## Conventions
- Typed code (mypy strict). Add tests with new code.
- Style is enforced by Ruff through pre-commit and CI. Run the tools; don't restate rules here.
- Small, single-purpose commits with short imperative subjects. Name files in `git add`
  (not `git add .`) and check `git status` and `git diff --staged` first.
- CI (`.github/workflows/ci.yml`) runs ruff, mypy and pytest on Python 3.12 and 3.13
  using `uv sync --locked`. Keep it green.
- Never commit secrets. `.env` is gitignored.

## Environment
- Windows machine. VS Code terminal is a bash-style shell (MSYS2/Git Bash), so use bash
  syntax. Venv scripts live in `.venv/Scripts/`.
- Line endings are LF in the repo (`.gitattributes`).
- GitHub: LukeLunn/Sensitive-Prompt-Insights.

## Decisions and why
- Python 3.13, not 3.15: the newest release may lack pre-built wheels for ML libraries.
- src layout: tests run against the installed package, not the working folder.
- uv with a lockfile: reproducible environments; stops indirect dependencies drifting.
- pre-commit plus CI: the same checks run locally and on GitHub.
- Dependencies are added only when code needs them, so `pyproject.toml` stays honest.

## How I like to work
- I want to understand every step and the reason for it. Explain the why briefly with
  each change, and go step by step.
