PYTHON = python # On Ubuntu, change to python3.

all:
	$(PYTHON) familytree.py
	cd output; make