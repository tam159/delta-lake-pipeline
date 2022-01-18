.PHONY: install update test lint clean-pyc clean-build clean-test clean upload-job upload-libs

help:
	@echo "install - install the packages by poetry"
	@echo "update - update the packages by poetry"
	@echo "test - run tests with pytest"
	@echo "lint - check code quality and fix"
	@echo "clean - remove all build, test, cache and Python artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-test - remove test and coverage artifacts"

install:
	poetry install

update:
	poetry update

test:
	poetry run pytest tests

lint:
	poetry run black .
	poetry run isort .
	-poetry run mypy .
	-poetry run flake8
	-poetry run pydocstyle

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-build:
	find . -name '*.zip' -exec rm -f {} +

clean-test:
	rm -rf .tox/
	rm -rf htmlcov/
	rm -f .coverage

clean: clean-build clean-pyc clean-test

upload-jobs:
	dbfs cp -r --overwrite spark_jobs/ dbfs:/spark_jobs/

upload-libs: clean-build
	$(eval TIMESTAMP=$(shell date -u +%Y-%m-%dT%H:%M:%SZ))
	cd spark_libs && zip -r ../$(TIMESTAMP).zip * && cd ..
	dbfs rm --recursive dbfs:/spark_libs
	dbfs cp --overwrite $(TIMESTAMP).zip dbfs:/spark_libs/$(TIMESTAMP).zip
	rm -f $(TIMESTAMP).zip
