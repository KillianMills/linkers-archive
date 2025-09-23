# linkers-archive

Minimal Python package scaffold for linkers-archive.

Usage

- Install in editable mode: `pip install -e .`
- Run tests: `pytest -q`

Badges

- CI: ![CI](https://github.com/KillianMills/linkers-archive/actions/workflows/ci.yml/badge.svg)
- Release: ![Release](https://github.com/KillianMills/linkers-archive/actions/workflows/release.yml/badge.svg)

Development

- Create and activate a virtualenv:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

- Install dev dependencies and the package:

```powershell
.venv\Scripts\pip install -r requirements-dev.txt
.venv\Scripts\pip install -e .
```

- Run tests and checks:

```powershell
python -m pytest -q
python -m mypy src
python -m black --check .
```

Branch protection (recommended)

- Require reviews from CODEOWNERS and enable status checks (`pytest`, `mypy`, `black`).
- Configure branch protection in the repository Settings → Branches on GitHub.
