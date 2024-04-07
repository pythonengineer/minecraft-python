.PHONY: build dist redist install install-from-source clean uninstall

build:
	CYTHONIZE=1 ./setup.py build

dist:
	CYTHONIZE=1 ./setup.py sdist bdist_wheel

redist: clean dist

install:
	CYTHONIZE=1 pip install .

install-from-source: dist
	pip install dist/minecraft-python-0.31.20100104.tar.gz

clean:
	$(RM) -r build dist src/*.egg-info
	find . -name __pycache__ -exec rm -r {} +

uninstall:
	pip uninstall minecraft-python
