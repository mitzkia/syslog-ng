import pytest
from src.testcase.setup_testcase import SetupTestCase, SetupUnitTestCase
from datetime import datetime


def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true", help="Also run @slow tests.")
    parser.addoption("--loglevel", action="store", default="info",
                     help="Set loglevel for test runs. Available loglevels: ['info', 'error', 'debug']. Default loglevel: info")

    parser.addoption("--installpath", action="store",
                     help="Set installpath for installed syslog-ng. Used when installmode is: custom. Example path: '/home/user/syslog-ng/installdir/'")
    parser.addoption("--reports", action="store", default=get_current_date(),
                     help="Path for report files folder. Default form: 'reports/<current_date>'")


@pytest.fixture
def reports(request):
    return request.config.getoption("--reports")


@pytest.fixture
def installpath(request):
    return request.config.getoption("--installpath")


@pytest.fixture
def loglevel(request):
    return request.config.getoption("--loglevel")


@pytest.fixture
def runslow(request):
    return request.config.getoption("--runslow")


@pytest.fixture
def tc(request):
    return SetupTestCase(request)

@pytest.fixture
def tc_unittest(request):
    return SetupUnitTestCase(request)

def get_current_date():
    return 'reports/' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
