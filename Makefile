.PHONY: all install lint test clean

all: install lint test

install:
	pip install -e .[dev]

lint:
	flake8
	isort -rc -c -df **/*.py
	yapf -dr datatables/ tests/

test:
	pytest -vx

test-ci:
	pytest -qx --cov=datatables

clean:
	git clean -dfX