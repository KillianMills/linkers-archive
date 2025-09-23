# Contributing

Thanks for considering contributing.

- Set up a venv: `python -m venv .venv` then activate it.
- Install dev deps: `.venv\Scripts\pip install -r requirements-dev.txt`
- Run tests: `python -m pytest -q`
- Run lint: `python -m black --check .` and `python -m mypy src`
- Run format: `python -m black .`

Open a PR against `main` and include tests for new behavior.

Branch protection (recommended)

- Require at least one review from a CODEOWNER before merging.
- Require passing status checks: `pytest`, `mypy`, and `black`.
- Configure these rules in the repository Settings → Branches on GitHub.
