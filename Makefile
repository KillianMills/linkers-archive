VENV := .venv
PY := $(VENV)/Scripts/python
PIP := $(VENV)/Scripts/pip

.PHONY: venv install test clean

venv:
	python -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .

test:
	$(PY) -m pytest -q

clean:
	rmdir /s /q $(VENV) || true
	rmdir /s /q build dist || true
	del /s /q *.egg-info || true
