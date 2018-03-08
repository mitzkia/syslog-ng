from mockito import when, args
from src.parameters.test_case import TestCaseParameters
from src.parameters.syslog_ng import SyslogNgParameters


def stub_dependencies_for_syslog_ng_parameters(syslog_ng_parameters_object):
    when(syslog_ng_parameters_object.testcase_context).getfixturevalue(*args).thenReturn("/tmp/for_unittest")
    return syslog_ng_parameters_object


def check_keys_for_instance_name_in_syslog_ng_parameters(instance_parameters):
    assert set(list(instance_parameters)) == {'binary_file_paths', 'dir_paths', 'file_paths'}
    assert set(list(instance_parameters['dir_paths'])) == {'install_dir', 'libjvm_dir', 'working_dir'}
    assert set(list(instance_parameters['file_paths'])) == {'config_path', 'persist_path', 'pid_path', 'control_socket_path'}


def test_set_instance_parameters(request):
    tcp = TestCaseParameters(request)
    syslog_ng_parameters_object = SyslogNgParameters(request, tcp)
    syslog_ng_parameters_object = stub_dependencies_for_syslog_ng_parameters(syslog_ng_parameters_object)

    instance_name = "test"
    instance_parameters = syslog_ng_parameters_object.set_instance_parameters(instance_name)
    check_keys_for_instance_name_in_syslog_ng_parameters(instance_parameters)


def test_set_instance_parameters_with_different_instances(request):
    tcp = TestCaseParameters(request)
    syslog_ng_parameters_object = SyslogNgParameters(request, tcp)
    syslog_ng_parameters_object = stub_dependencies_for_syslog_ng_parameters(syslog_ng_parameters_object)

    instance_name = "test"
    instance_name2 = "test2"

    instance_parameters = syslog_ng_parameters_object.set_instance_parameters(instance_name)
    check_keys_for_instance_name_in_syslog_ng_parameters(instance_parameters)

    instance_parameters2 = syslog_ng_parameters_object.set_instance_parameters(instance_name2)
    check_keys_for_instance_name_in_syslog_ng_parameters(instance_parameters2)

    assert set(list(syslog_ng_parameters_object.syslog_ng_parameters)) == {instance_name, instance_name2}
