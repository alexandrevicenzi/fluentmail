PYTHON        = python3
PANDOC        = pandoc
PIP           = pip3

.PHONY: setup pandoc build upload db test docs clean

setup:
	$(PIP) install --upgrade setuptools wheel twine

pandoc:
	$(PANDOC) README.md -o README.rst

build: clean pandoc
	$(PYTHON) setup.py sdist bdist_wheel

upload:
	twine upload dist/*

test:
	$(PYTHON) -m tests.test -v

clean:
	rm -rf README.rst
	rm -rf build
	rm -rf dist
	rm -rf fluentmail.egg-info
	rm -rf fluentmail/__pycache__
