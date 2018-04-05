This Pull Request will introduce a new python based test-framework for syslog-ng.

 * The Pull Request is still in Work-In-Progress state, but I wanted to show the actual progress (from my point of view the current status is not so far from the end).
 * After a discussion with some colleagues we have agreed that the best way to handle this PR is a one commit PR (Review and make review changes are easier in this case).
 * From change to change I will force push this PR (branch) and will update the current status.

## The aim of the test-framework

 * To give a tool into developers hand where they can write even an end2end testcases for some features
 * To replace an old python based functional tests (under tests/functional/)

## Actual status

Remaining tasks with the framework (before the PR is finished):
- [ ] General changes:
    - [x] PR should PASS on Travis
    - [x] Framework should be run in virtualenv
    - [x] Add basic usages with make targets
    - [ ] Framework should be run inside dbld's docker image
    - [ ] Generate a class diagramm
    - [ ] Generate a flow chart
- [ ] Internal API related changes:
    - [x] Improve self coverage, now ~84%, expected above ~80%
    - [x] Improve API under syslog_ng_config/
    - [x] Cleanup code in various modules
    - [x] Added pylintrc file
    - [ ] Pass on pylint check (self pylintrc)
    - [ ] remove unnecessary comments
- [ ] Functional testcase related changes
    - [ ] write valuable testcases

## Restrictions on the framework

 * The framework started with: file source and file destination driver support. After the API is stabilized driver support can be extended iteratively.
 * Parallel running. When we start pytest with parallel running for even one testcase it will fail in teardown phase.

## How to use the framework

1, Dependencies:
 * The test-framework was built on top of Python3 support
 * The root directory of test-framework contains a requirements.txt file which contains framework dependencies.

2, Usage with make:
 * Here you cannot use custom pytest commands (yet).
 * Here you do not need to install requirements.txt, it will installed automatically inside a virtualenv
 * This mode has only 2 hardcoded commands:
   * `$ make pytest-check` This command runs all functional tests under "functional_tests/" dir without verbose console log
   * `$ make pytest-self-check` This command runs all self tests for test-framework

3, Usage without make:
 * Here you can use your favorite pytest commands
 * Here you must define your syslog-ng install path after: "--installdir" option
 * Example1: A standard start for all functional tests with verbose output on console
   * `$ cd tests/pytest_framework`
   * `$ python3 -m pytest --verbose --showlocals -s functional_tests/ --installdir=[syslog-ng install path]`
 * Example2: Start only special testcase (or testcases) which are matching on "pattern from testcase"
   * `$ cd tests/pytest_framework`
   * `$ python3 -m pytest --verbose --showlocals -s functional_tests/ -k [pattern from testcase] --installdir=[syslog-ng install path]`

4, Reporting:
 * The framework uses capabilities of the builtin `logging` module.
 * Available log levels: INFO (default), DEBUG, ERROR
 * Console log:
   * Pytest display verbose log from testcases when it was started with: "--verbose --showlocals -s"
   * Without this start arguments pytest will not log anything on console, only if there is an error in testcase
 * File log:
   * Self unit-tests are not, but functional-tests are using a separate report directory which contains followings:
     * syslog-ng related files: config, pid, persist, ctl, console stdout/stderr, core file, backtrace file
     * source-destination related files: input/output files
     * testcase related files: full testcase log, also a started testcase
