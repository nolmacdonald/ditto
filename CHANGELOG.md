# Changelog

All notable changes to ditto will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `scripts/rename_project.py`: one-shot, stdlib-only renamer that turns a
  generated repository into a real project (package directory, docs, workflows,
  issue templates, GitHub slugs).
- `TEMPLATE.md`: checklist of everything the rename script cannot automate.
- `.python-version` pinning the development interpreter to 3.14.
- CI: separate `lint` and `build` jobs; the `build` job installs the built wheel
  in an isolated environment to verify it imports.
- PEP 735 `[dependency-groups]` for `dev` and `docs`.
- `[project.urls]`, license metadata and trove classifiers in `pyproject.toml`.

### Changed

- Build backend switched from hatchling to `uv_build`.
- Minimum supported Python raised from 3.11 to 3.12, matching the floors already
  required by numpy and scipy. CI now tests 3.12, 3.13 and 3.14.
- Development dependencies moved from `[project.optional-dependencies]` to
  dependency groups, so `pip install ditto` no longer exposes `dev`/`docs`
  extras. Use `uv sync` and `uv sync --group docs` instead of `--extra`.
- CI pins `UV_FROZEN=1` so a stale `uv.lock` fails the build.
- GitHub Actions updated: `checkout@v5`, `setup-uv@v7`, `codecov-action@v5`;
  `setup-python` dropped in favour of uv-managed interpreters.

### Fixed

- `ty` configuration moved from `[tool.ty]` to `[tool.ty.environment]`, where
  `python-version` is actually read; the previous key was silently ignored.

## [0.1.0] – 2025-01-01

### Added

- Initial project structure with `src/` layout.
- `ExampleClass` and `example_function` demonstrating code conventions.
- Logging configuration utilities.
- Sphinx documentation with PyData theme.
- GitHub Actions CI workflows (test, docs build, docs deploy).
- Issue and pull request templates.
- Ruff formatting and linting configuration.
- `ty` type checking configuration.
- `uv` virtual environment support with `dev` and `docs` extras.

[Unreleased]: https://github.com/nolmacdonald/ditto/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/nolmacdonald/ditto/releases/tag/v0.1.0
