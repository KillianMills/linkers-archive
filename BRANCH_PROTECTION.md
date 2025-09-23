# Branch Protection Guide

Recommended settings to enable on GitHub (Settings → Branches):

- Protect the `main` branch.
- Require pull request reviews before merging.
  - Require review from CODEOWNERS.
- Require status checks to pass before merging:
  - `CI` (the GitHub Action for running `pytest`)
  - `mypy` (type checks)
  - `black` (format check)
- Require branches to be up to date before merging (optional).
- Restrict who can push to the protected branch (optional).

These rules help maintain code quality and ensure automated checks run on every PR.
