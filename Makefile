.ONESHELL:

venv: 
	pip install --upgrade pip
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

clean-all: clean
# TODO clean app running files

clean-venv:
	rm -rf venv

clean-test:
# TODO clean test env
	
clean: clean-venv clean-test
	rm -rf profile/*
	find . -name __pycache__  -prune -exec rm -rf {} \;

test: clean-test venv
# TODO setup test env first
	. venv/bin/activate
	pytest -s -W ignore::DeprecationWarning
	
