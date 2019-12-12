.PHONY: check dist venv

check:
	flake8 rhasspyhermes/*.py
	pylint rhasspyhermes/*.py

dist:
	python3 setup.py sdist

venv:
	rm -rf .venv/
	python3 -m venv .venv
	.venv/bin/pip3 install wheel setuptools
	.venv/bin/pip3 install -r requirements_all.txt
