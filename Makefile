.PHONY: check dist venv test

check:
	flake8 rhasspyhermes/*.py test/*.py setup.py
	pylint rhasspyhermes/*.py test/*.py setup.py
	mypy rhasspyhermes/*.py test/*.py setup.py
	yamllint .

dist:
	python3 setup.py sdist

test:
	coverage run -m unittest test
	coverage report -m
	coverage xml

venv:
	rm -rf .venv/
	python3 -m venv .venv
	.venv/bin/pip3 install wheel setuptools
	.venv/bin/pip3 install -r requirements_all.txt
