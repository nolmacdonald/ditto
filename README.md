<p align="center">
  <img src="docs/source/_static/logo/ditto_readme.svg" width="300">
</p>

<p align="center">
<span style="color: #D8D8D8;"><strong>Developer Integrated Toolkit for Technical Optimization (DITTO)</strong></span>
  
</p>

<p align="center">
  <a href="https://github.com/nolmacdonald/ditto/actions/workflows/ci.yml">
    <img src="https://github.com/nolmacdonald/ditto/actions/workflows/ci.yml/badge.svg" alt="CI" />
  </a>
  <a href="https://github.com/nolmacdonald/ditto/actions/workflows/docs.yml">
    <img src="https://github.com/nolmacdonald/ditto/actions/workflows/docs.yml/badge.svg" alt="Docs" />
  </a>
  <a href="https://github.com/nolmacdonald/ditto">
    <img 
      src="https://img.shields.io/badge/python-3.10%2B-777BB4?logo=python&logoColor=white" 
      alt="Python >=3.10"
    />
  </a>
  <img 
  src="https://img.shields.io/badge/linting-ruff-46a2f1?logo=ruff&logoColor=white" 
  alt="Ruff"
  />
  <img 
  src="https://img.shields.io/badge/docs-sphinx-0A507A?logo=sphinx&logoColor=white" 
  alt="Sphinx Docs"
  />
  <img 
    src="https://img.shields.io/badge/build-hatchling-4051b5" 
    alt="Hatchling"
  />
</p>


<p align="center">
  <a href="https://nolmacdonald.github.io/ditto"> Documentation</a> |
  <a href="https://github.com/nolmacdonald/ditto/issues"> Report Bug</a> |
  <a href="https://github.com/nolmacdonald/ditto/issues"> Request Feature</a>
</p>

---

**ditto** is a batteries-included Python package template for scientific computing projects.
Stop copying boilerplate between repos — clone ditto and get straight to the science.

## Features

<p align="center">

| Feature              | Tooling                                                                                             |
|----------------------|-----------------------------------------------------------------------------------------------------|
| Build backend        | [hatchling](https://hatch.pypa.io/)                                                                 |
| Formatting & linting | [ruff](https://docs.astral.sh/ruff/)                                                                |
| Type checking        | [ty](https://github.com/astral-sh/ty)                                                               |
| Virtual environment  | [uv](https://docs.astral.sh/uv/)                                                                    |
| Testing & coverage   | [pytest](https://docs.pytest.org/) + pytest-cov                                                     |
| Units                | [pint](https://pint.readthedocs.io/)                                                                |
| Documentation        | [Sphinx](https://www.sphinx-doc.org/) + [PyData theme](https://pydata-sphinx-theme.readthedocs.io/) |
| CI/CD                | [GitHub Actions](https://github.com/features/actions)                                               |

</p>

## Quick Start

```bash
git clone https://github.com/nolmacdonald/ditto.git
cd ditto
uv sync
uv run pytest
```

## Installation

```bash
uv pip install ditto
```

## Development

```bash
# Install dev dependencies
uv sync --extra dev --extra docs

# Format and lint
uv run ruff format .
uv run ruff check .

# Type check
uv run ty check src/

# Run tests
uv run pytest
```

## Documentation

```bash
uv sync --extra docs
cd docs && uv run sphinx-build -b html . _build/html
```

Full documentation is available at **[nolmacdonald.github.io/ditto](https://nolmacdonald.github.io/ditto)**.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
