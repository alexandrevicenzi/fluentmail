all: clean build install test

build:
	python setup.py build

dist:
	python setup.py bdist
	python setup.py sdist
	python setup.py bdist_egg

install:
	python setup.py install -f

test:
	python -m unittest -v test

pypi: clean build dist

clean:
	rm -rf build dist fluentmail.egg-info