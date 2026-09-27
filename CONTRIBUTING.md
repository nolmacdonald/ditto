# Contributing to ditto

Thank you for your interest in contributing! This guide walks through the
development workflow for ditto.

## Development Setup

ditto uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Clone the repository
git clone https://github.com/nolmacdonald/ditto.git
cd ditto

# Create the virtual environment and install the project + dev group
uv sync

# Optionally install the docs group as well
uv sync --group docs
```

`uv sync` provisions the interpreter pinned in `.python-version` (currently
3.14), so you do not need a matching `python` on your `PATH`. Dependencies are
installed from `uv.lock`; CI runs with `UV_FROZEN=1`, so commit the lockfile
whenever you change `pyproject.toml`.

ditto supports Python 3.12, 3.13 and 3.14, and CI tests all three.

## Code Style

All code must pass [Ruff](https://docs.astral.sh/ruff/) formatting and linting:

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type check
uv run ty check src/
```

## Testing

Run the test suite with coverage:

```bash
uv run pytest
```

## Building

ditto builds with the [uv build backend](https://docs.astral.sh/uv/concepts/build-backend/):

```bash
uv build
```

This produces an sdist and a wheel in `dist/`. CI additionally installs the
built wheel in an isolated environment to confirm it imports.

## Documentation

Build the documentation locally:

```bash
uv sync --group docs
uv run sphinx-build -b html docs/source docs/_build/html -W --keep-going
```

Open `docs/_build/html/index.html` in a browser. CI builds with `-W`, so
warnings are errors.

## Pull Request Process

1. Fork the repository and create a feature branch.
2. Write tests for your changes.
3. Ensure all checks pass (`ruff`, `ty`, `pytest`) and that `uv build` succeeds.
4. Open a pull request using the provided template, with a bracketed title
   prefix (see Titles below).
5. A maintainer will review and merge your PR.

## Reporting Issues

Please use the issue templates in `.github/ISSUE_TEMPLATE/` when filing bugs,
feature requests, or documentation improvements.

## Titles

Issue and pull request titles start with an all-caps type in brackets:

| Prefix          | Use for                                          | Label               |
|-----------------|--------------------------------------------------|---------------------|
| `[BUG]`         | Something broken or behaving unexpectedly        | `type::bug`         |
| `[DOCS]`        | Documentation additions or corrections           | `type::docs`        |
| `[FEATURE]`     | A brand-new feature or capability                | `type::feature`     |
| `[ENHANCEMENT]` | Polish or quality-of-life on an existing feature | `type::enhancement` |
| `[REFACTOR]`    | Restructuring code without changing behaviour    | `type::refactor`    |
| `[RELEASE]`     | Version bumps, changelog, release coordination   | `type::release`     |

For example: `[BUG] Logger drops messages below WARNING`. The issue templates
pre-fill the prefix for you.

## Labels

Labels are defined in `.github/labels.yml` and synced to GitHub by
`.github/workflows/labels.yml` on every push to `main` that changes that file.
Edit the YAML, not the GitHub UI — labels missing from the file are removed on
the next sync. Each issue or PR should carry one `type::` label, plus any of:

- `priority::` — `critical`, `high`, `medium`, `low`
- `status::` — `triage`, `in-progress`, `blocked`, `needs-info`,
  `ready-for-review`, `needs-changes`, `wont-fix`
- `scope::` — `frontend`, `backend`, `core`, `deps`, `testing`

## Code of Conduct

Be kind, inclusive, and constructive. Harassment of any kind is not tolerated.
