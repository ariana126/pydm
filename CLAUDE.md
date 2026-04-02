# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**pydm** (published to PyPI as `pydmpro`) is a lightweight Python dependency injection / IoC container library. It automatically resolves and wires service dependencies using constructor type hints, supports interface-to-implementation binding, factory bindings, and runtime parameter injection (from memory or environment variables).

## Commands

```bash
# Install for development
pip install ".[dev]"

# Run all tests
pytest

# Run a single test
pytest tests/test_service_container.py::TestName

# Build distribution
python -m build

# Publish to PyPI
twine upload dist/*
```

**Requirements:** Python ≥ 3.10

## Architecture

The library has three core components in `pydm/`:

- **`service_container.py`** — The central singleton IoC container. Resolves services recursively using `inspect.signature` to introspect constructor type hints, caches all resolved instances, and dispatches to bindings/factories/parameters as needed.
- **`parameters_bag.py`** — Abstracts parameter sources. `InMemoryParametersBag` wraps a dict; `EnvParametersBag` reads from `os.getenv()`. Both implement `ParametersBagInterface`.
- **`__init__.py`** — Re-exports the public API surface.

### Dependency Resolution Flow

When `ServiceContainer.get_service(SomeClass)` is called:
1. Return cached instance if already resolved
2. If an interface binding exists, recurse with the bound implementation
3. If a factory binding exists, delegate to the factory method
4. Otherwise, use `inspect.signature` to walk constructor parameters: each arg is either fetched from the `ParametersBag` (if mapped via `bind_parameters`) or resolved recursively as another service

### Key Design Details

- `ServiceContainer` is a **singleton** via a custom `__new__` + `get_instance()` pattern
- All resolved services are **singleton-scoped** (cached in `__services`)
- The container extends `Encapsulated` from the `underpy` package (via `underpyx`), which enforces OOP-style private attribute access control
- `InMemoryParametersBag` is both `Encapsulated` and `Immutable` (from `underpy`), preventing mutation after construction

### Runtime Dependency

The only non-dev runtime dependency is `underpyx >= 0.1.1`, which provides `Encapsulated` and `Immutable` base classes from the `underpy` package.

## CI/CD

GitHub Actions (`.github/workflows/publish-to-pypi.yml`) automatically builds and publishes to PyPI on GitHub releases using a `PYPI_API_TOKEN` secret.
