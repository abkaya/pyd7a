PYTHON=PYTHONPATH=. python
COVERAGE=$(shell which coverage)

MODULES=$(subst /,,$(subst d7a/,,$(sort $(dir $(wildcard d7a/*/)))))
TESTS=$(addprefix test-,${MODULES})

all: clean test coverage

test: ${TESTS}

test-%: 
	@echo "*** performing tests for d7-$(subst test-,,$@)"
	@$(PYTHON) $(COVERAGE) run --append d7a/$(subst test-,,$@)/test/all.py;

coverage:
	@echo "*** generating unittest coverage report (based on last test run)"
	@$(COVERAGE) report -m --omit '*__init__.py,*/test/*'

clean:
	@rm -f .coverage

.PHONY: all test clean test test-% coverage