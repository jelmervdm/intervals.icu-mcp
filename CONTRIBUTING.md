# Contributing to Intervals.icu MCP Server

Thank you for considering contributing to `intervals.icu-mcp`!

## Getting Started

1. Fork and clone the repository.
2. Set up a virtual environment and install development dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[dev,router]"
```

## Running Tests

Run the test suite with `pytest`:

```bash
pytest tests/ -v
```

## Code Style

- Code must adhere to PEP 8. Format code using `black` and check with `flake8` and `mypy`:

```bash
black src tests
flake8 src tests
mypy src
```

## Submitting Pull Requests

- Keep PRs focused and single-purpose.
- Ensure all tests and lint checks pass before requesting review.
