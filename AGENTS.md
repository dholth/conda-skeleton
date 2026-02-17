# AGENTS.md

Guidance for coding agents working in this repository.

## Scope and precedence
- Applies to the entire repository.
- Follow: explicit user request > this file > local code patterns.
- Keep changes minimal and task-focused; avoid drive-by refactors.

## Repository quick facts
- Project name: `conda-skeleton`
- Python requirement: `>=3.10`
- Build backend: `hatchling` (`hatch-vcs` version source)
- Main config: `pyproject.toml`
- Main package: `conda_skeleton/`
- Tests root: `tests/`

## Cursor/Copilot rules status
- No `.cursorrules` file exists.
- No `.cursor/rules/` directory exists.
- No `.github/copilot-instructions.md` file exists.
- If any are added later, treat them as required and update this document.

## Setup
- Use a clean conda environment.
- Install editable package: `conda pypi install -e .`
- If tools are missing, install: `conda install pytest pytest-cov ruff python-build`

## Build commands
- Preferred: `python -m build`
- Alternative (if Hatch installed): `hatchling build`

## Lint/format commands
- Lint: `ruff check .`
- Auto-fix safe lint issues: `ruff check . --fix`
- Format (when needed): `ruff format .`
- Ruff target/version rules come from `pyproject.toml`.

## Test commands
- Full suite: `pytest`
- Single file: `pytest tests/test_api_skeleton.py`
- Single test function: `pytest tests/test_api_skeleton.py::test_sympy`
- Single parametrized case:
  - `pytest 'tests/test_api_skeleton.py::test_sympy[with version]'`
- Keyword selection: `pytest -k sympy`
- Marker selection:
  - `pytest -m sanity`
  - `pytest -m "not slow"`

## Pytest defaults in this repo
- Tests are discovered from `tests/` (`testpaths = ["tests"]`).
- `addopts` include:
  - `-vv`
  - `--tb=native`
  - `--strict-markers`
  - `--junitxml=junit.xml`
  - `--cov-append --cov-branch --cov-report=term --cov-report=xml`
  - `--durations=16`
- Known markers: `serial`, `slow`, `sanity`, `benchmark`, `memray`, `no_default_testing_config`.
- Multiple deprecation warnings are elevated to errors; warning noise may fail CI/tests.

## Import conventions
- Prefer `from __future__ import annotations` in typed modules.
- Keep import ordering consistent:
  1) standard library
  2) third-party
  3) local package imports
- Use explicit imports; avoid wildcard imports.
- For typing-only imports, use `if TYPE_CHECKING:` blocks.
- Avoid import-time side effects in modules used as CLI/plugin entrypoints.

## Typing conventions
- Use modern syntax (`str | None`, `list[str]`, `dict[str, Any]`).
- Add type hints for new public functions and non-trivial internal logic.
- Do not change runtime semantics just to satisfy typing.
- Keep typing pragmatic; avoid heavy abstractions unless already established.

## Naming conventions
- Follow PEP 8:
  - functions/variables/modules: `snake_case`
  - classes: `PascalCase`
  - constants: `UPPER_SNAKE_CASE`
- Prefer descriptive names over short abbreviations.
- Test names should be behavior-oriented: `test_<unit>_<behavior>`.

## Formatting/style conventions
- Respect Ruff lint selection: `E,F,FA,I,ISC,T10,TCH,UP,W`.
- Max line length: 120.
- Keep docstrings brief and behavior-focused.
- Avoid pure formatting churn in unrelated files.
- Match existing patterns in legacy modules when touching old code.

## Error handling
- Fail loudly with actionable errors when inputs/environment are invalid.
- Catch exceptions only when you can recover or add useful context.
- Never silently swallow exceptions.
- Preserve existing exception behavior unless there is a clear reason to change.
- Keep subprocess/network flows explicit, testable, and easy to debug.

## Testing expectations for changes
- Minimum: run targeted tests for modified code paths.
- Preferred before handoff: run full `pytest`.
- If lint-sensitive files changed, run `ruff check .`.
- If packaging/build logic changed, run `python -m build`.

## Dependency and change hygiene
- Keep patches small and scoped to the user request.
- Do not add new dependencies without clear justification.
- Do not edit generated artifacts unless task requires it.
- Add/update tests when behavior changes.
- If intent is unclear, infer from nearby code and existing tests first.

## Useful paths
- `pyproject.toml` (tooling/lint/pytest configuration)
- `conda_skeleton/plugin.py` (plugin entrypoint)
- `conda_skeleton/skeletons/` (skeleton implementations)
- `tests/test_api_skeleton.py` (API-level behavior tests)

## Quick command checklist
```bash
# setup
python -m pip install -e .

# lint/format
ruff check .
ruff format .

# tests
pytest tests/test_api_skeleton.py::test_sympy
pytest

# package build
python -m build
```
