PYTHON_FILES = rhasspyhermes/*.py tests/*.py setup.py

.PHONY: check dist venv test

check:
	flake8 $(PYTHON_FILES)
	pylint $(PYTHON_FILES)
	mypy $(PYTHON_FILES)
	black .
	yamllint -c .yamllint.yml .
	pip list --outdated

dist:
	python3 setup.py sdist

test:
	coverage run -m unittest
	coverage report -m
	coverage xml

venv:
	rm -rf .venv/
	python3 -m venv .venv
	.venv/bin/pip3 install --upgrade pip
	.venv/bin/pip3 install wheel setuptools
	.venv/bin/pip3 install -r requirements.txt
	.venv/bin/pip3 install -r requirements_dev.txt
