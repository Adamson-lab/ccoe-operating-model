PY ?= python3
export PYTHONPATH := src

.PHONY: all validate test docs diagrams demo clean
all: validate test diagrams docs

validate:
	$(PY) -m ccoe validate

test:
	$(PY) -m unittest discover -s tests -v

docs:
	$(PY) -m ccoe raci-md
	$(PY) -m ccoe adr-index
	$(PY) -m ccoe catalog
	$(PY) -m ccoe scorecard

diagrams:
	$(PY) tools/gen_diagrams.py

demo:  ## good plan passes, bad plan is blocked (exit code 1 expected)
	$(PY) -m ccoe check-plan tests/fixtures/plan_good.json
	-$(PY) -m ccoe check-plan tests/fixtures/plan_bad.json --today 2026-11-24
