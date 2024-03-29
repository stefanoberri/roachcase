.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help install lint lint/black
.DEFAULT_GOAL := help
PYTHON=python3



IS_RELEASE := 0
BETA_COUNTER := 1
USE_TEST_PYPI := 1

PYPI_USER := __token__
PYPI_TOKEN := atoken

BASEVERSION := $(shell cat VERSION)
ifeq ($(IS_RELEASE), 1)
	VERSION := $(BASEVERSION)
else
	VERSION := $(BASEVERSION)b$(BETA_COUNTER)
endif

ifeq ($(USE_TEST_PYPI), 1)
	REPOARGS = --repository testpypi
else
	REPOARGS =
endif

PACKAGE_NAME := roachcase
PACKAGE_FILE := dist/$(PACKAGE_NAME)-$(VERSION).tar.gz

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := $(PYTHON) -c "$$BROWSER_PYSCRIPT"

help:
	@$(PYTHON) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)
	@echo  "- VARIABLES -"
	@echo  "IS_RELEASE [0,1 - DEFAULT=$(IS_RELEASE)]: Specify if it is a release or beta version"
	@echo  "USE_TEST_PYPI [DEFAULT=$(USE_TEST_PYPI)]: Push to TestPyPI index instead of normal PyPI"
	@echo  "BETA_COUNTER [DEFAULT=$(BETA_COUNTER)]: Counter for the beta version"
	@echo  "PYPI_TOKEN: Token to push to PyPI"


clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr roachcase/_version.py Versionfile
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint/black: ## check style with black
	black --check roachcase tests

lint: lint/black ## check style

test: ## run tests quickly with the default Python
	$(PYTHON) -m pytest --verbose tests

typecheck: ## run type checker
	mypy roachcase \
		--config-file mypy.ini \
		--explicit-package-bases \
		--strict
	$(PYTHON) -m pytest --verbose --mypy-config-file=mypy.ini tests


test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source roachcase -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs_templates:
	rm -f docs/roachcase.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ roachcase
	sed -i.bak 's/^release = .*/release = "$(BASEVERSION)"/' docs/conf.py
	sed -i.bak 's/^roachcase/API/g' docs/modules.rst
	rm docs/conf.py.bak docs/modules.rst.bak

docs: docs_templates ## generate Sphinx HTML documentation, including API docs
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload --verbose $(REPOARGS) --username $(PYPI_USER) --password $(PYPI_TOKEN) dist/*

versionfile:
	@echo $(VERSION) > Versionfile
	@echo '__version__ = "$(VERSION)"' > roachcase/_version.py

dist: $(PACKAGE_FILE) ## builds source and wheel package

install: $(PACKAGE_FILE) ## install the package to the active Python's site-packages
	$(PYTHON) -m pip install $(PACKAGE_FILE)

$(PACKAGE_FILE): clean versionfile
	$(PYTHON) -m pip install --upgrade build
	$(PYTHON) -m build
	@echo "package build in $@"

