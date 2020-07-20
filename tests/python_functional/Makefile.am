export top_srcdir

EXTRA_DIST += \
	tests/python_functional/CMakeLists.txt

PYTEST_SUBDIR=
PYTEST_UNITTEST_SUBDIR=$(top_srcdir)/tests/python_functional/src/$(PYTEST_SUBDIR)
PYTEST_FUNCTEST_SUBDIR=$(top_srcdir)/tests/python_functional/functional_tests/$(PYTEST_SUBDIR)
PYTEST_VERBOSE=false
PYTEST_VERBOSITY_ARGS=-o log_cli=$(PYTEST_VERBOSE) --showlocals --verbosity=3
PYTEST_SELF_CHECK_DEFAULT_ARGS=$(PYTEST_VERBOSITY_ARGS) $(PYTEST_UNITTEST_SUBDIR)
PYTEST_CHECK_DEFAULT_ARGS=$(PYTEST_VERBOSITY_ARGS) $(PYTEST_FUNCTEST_SUBDIR)

pytest-self-check:
	@${PYTHON} -m pytest $${PYTEST_ARGS:-$(PYTEST_SELF_CHECK_DEFAULT_ARGS)}

pytest-check:
	@${PYTHON} -m pytest --installdir=${prefix} $${PYTEST_ARGS:-$(PYTEST_CHECK_DEFAULT_ARGS)}

pytest-linters:
	@find $(top_srcdir)/tests/python_functional/ -name "*.py" \
		-not -path "*reports*" \
		-not -path "*tox*" \
		-print0 | xargs -0 \
		pre-commit run --show-diff-on-failure --config=$(top_srcdir)/tests/python_functional/.pre-commit-config.yaml --files

.PHONY: pytest-self-check pytest-check pytest-linters
