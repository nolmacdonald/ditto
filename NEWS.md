# News

## Unreleased

**uv end to end.** ditto now builds with the
[uv build backend](https://docs.astral.sh/uv/concepts/build-backend/) instead of
hatchling, so uv handles the interpreter, the lockfile, the environment and the
wheel. Development dependencies moved to PEP 735 dependency groups
(`uv sync`, `uv sync --group docs`).

**Python 3.12–3.14.** The minimum supported version is now 3.12 — the floor
numpy and scipy already require — and CI tests 3.12, 3.13 and 3.14. The
development interpreter is pinned to 3.14 in `.python-version`.

**Actually a template.** `scripts/rename_project.py` renames the package,
the docs, the workflows and the GitHub slugs in one pass; `TEMPLATE.md` lists
what is left to do by hand.

## ditto 0.1.0

Released: 2025-01-01

Initial release of **ditto** — Development Infrastructure Template Tool for Optimization.

ditto provides a fully configured Python package template with:

- `src/` layout with hatchling build backend
- Ruff for formatting and linting
- `ty` for type checking
- `uv` for virtual environment and dependency management
- pytest for unit testing with coverage
- Sphinx documentation with PyData theme
- GitHub Actions for CI/CD
