.PHONY: check dist venv test

check:
	flake8 rhasspyhermes/*.py test/*.py
	pylint rhasspyhermes/*.py test/*.py

dist:
	python3 setup.py sdist

test:
	python3 -m unittest test

venv:
	rm -rf .venv/
	python3 -m venv .venv
	.venv/bin/pip3 install wheel setuptools
	.venv/bin/pip3 install -r requirements_all.txt
