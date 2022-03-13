.PHONY: help lint style clean venv changelog test

SRC_DIR=lazy_interval_tree

help:
	@echo "help             Show this help"
	@echo "lint             Run linter (pylint)"
	@echo "style            Run style check (flake8)"
	@echo "changelog        Print changelog"
	@echo "test             Run tests with verbose flags"
	@echo "format           Format using black"
	@echo "bench            Run benchmarks"
	@echo "mypy             Run mypy on Python files"

lint:
	pylint $(SRC_DIR) tests

style:
	flake8 $(SRC_DIR) tests

clean:
	rm -rf .pytest_cache/ .cache/ .tox/ || true
	find $(SRC_DIR) -name __pycache__ -exec rm -rf {} \; || true
	find $(SRC_DIR) -name *.pyc -exec rm -rf {} \; || true
	find tests -name __pycache__ -exec rm -rf {} \; || true
	find tests -name *.pyc -exec rm -rf {} \; || true

venv:
	@echo "deactivate"
	@echo "rm -rf _venv"
	@echo "virtualenv -p python3 _venv"
	@echo "source _venv/bin/activate"
	@echo "pip install -r requirements.txt"

changelog:
	gitchangelog

test:
	pytest -s -vvv

format:
	black -l 120 *.py lazy_interval_tree/*.py tests/*.py

bench:
	python benchmark.py

mypy:
	find . -name '*.py' | xargs mypy
