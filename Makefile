.PHONY: all install lint test clean

all: install lint test

install:
	pip install -e .[dev]

install-examples:
	pip install -e .[examples]

lint:
	flake8
	isort -rc -c -df **/*.py
	yapf -dr datatables/ tests/ examples/

test:
	pytest -vx

test-ci:
	pytest -qx --cov=datatables

clean:
	git clean -dfX