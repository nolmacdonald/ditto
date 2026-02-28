# Contributing to ditto

Thank you for your interest in contributing! This guide walks through the
development workflow for ditto.

## Development Setup

ditto uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Clone the repository
git clone https://github.com/nolmacdonald/ditto.git
cd ditto

# Create the virtual environment and install dev dependencies
uv sync --extra dev

# Optionally install docs dependencies as well
uv sync --extra dev --extra docs
```

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

## Documentation

Build the documentation locally:

```bash
cd docs
uv run sphinx-build -b html . _build/html
```

Open `docs/_build/html/index.html` in a browser.

## Pull Request Process

1. Fork the repository and create a feature branch.
2. Write tests for your changes.
3. Ensure all checks pass (`ruff`, `ty`, `pytest`).
4. Open a pull request using the provided template.
5. A maintainer will review and merge your PR.

## Reporting Issues

Please use the issue templates in `.github/ISSUE_TEMPLATE/` when filing bugs,
feature requests, or documentation improvements.

## Code of Conduct

Be kind, inclusive, and constructive. Harassment of any kind is not tolerated.
