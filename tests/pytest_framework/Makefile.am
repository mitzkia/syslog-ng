export top_srcdir

pytest-self-check:
	@virtualenv -p python3 $(top_srcdir)/tests/pytest_framework/
	@source $(top_srcdir)/tests/pytest_framework/bin/activate
	@python3 -m pip install -r $(top_srcdir)/tests/pytest_framework/requirements.txt
	@python3 -m pytest $(top_srcdir)/tests/pytest_framework/src

pytest-check:
	@virtualenv -p python3 $(top_srcdir)/tests/pytest_framework/
	@source $(top_srcdir)/tests/pytest_framework/bin/activate
	@python3 -m pip install -r $(top_srcdir)/tests/pytest_framework/requirements.txt
	@python3 -m pytest $(top_srcdir)/tests/pytest_framework/functional_tests/ --installdir=$(top_srcdir)/install

.PHONY: pytest-self-check pytest-check
