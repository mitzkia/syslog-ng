from src.parameters.test_case import TestCaseParameters


def test_testcase_parameters(request):
    tcp = TestCaseParameters(request)
    assert set(list(tcp.testcase_parameters)) == {'testcase_name', 'dir_paths', 'file_paths', 'loglevel'}
    assert set(list(tcp.testcase_parameters['dir_paths'])) == {'working_dir', 'relative_working_dir'}
    assert set(list(tcp.testcase_parameters['file_paths'])) == {'report_file', 'testcase_file'}
