from src.syslog_ng.syslogng import SyslogNg
from src.parameters.syslog_ng_parameters import SyslogNgParameters
from src.parameters.testcase_parameters import TestCaseParameters


# tests
def test_syslog_ng_start_command_syntax_check(tc_unittest):
    syslog_ng_object = instantiate_syslog_ng(tc_unittest, instance_name="server")


# helper functions
def instantiate_syslog_ng(tc_unittest, instance_name):
    return SyslogNg(tc_unittest.logger_factory, tc_unittest.syslog_ng_parameters, instance_name)


### testable functions:
# dump_config
# dump_console_log
# get_syslog_ng_pid
# get_syslog_ng_process
# get_syslog_ng_start_command
# handle_config_syntax_check_result
# handle_if_syslog_ng_already_killed
# handle_syslog_ng_reload_process_result
# handle_syslog_ng_start_process_result
# handle_syslog_ng_stop_process_result
# __init__
# is_core_file_exist
# reload
# reload_syslog_ng_process
# restart
# run_syntax_check_on_config
# run_syslog_ng_process
# start
# stop
# stop_syslog_ng_process
# wait_for_console_messages
# wait_for_syslog_ng_reload
# wait_for_syslog_ng_start
# wait_for_syslog_ng_stop


# def stub_dependencies_for_syslog_ng_parameters(syslog_ng_parameters_object):
#     when(syslog_ng_parameters_object.testcase_context).getfixturevalue(*args).thenReturn("/tmp")
#     fake_fd = open("/tmp/fake_path", 'w')
#     when(syslog_ng_parameters_object).open_file_for_write(*args).thenReturn(fake_fd)
#     fake_fd.close()
#     return syslog_ng_parameters_object


# def test_syslog_ng_start(tc_unittest):
#     testcase_parameters = TestCaseParameters(tc_unittest.testcase_context)
#     syslog_ng_parameters = SyslogNgParameters(tc_unittest.testcase_context, testcase_parameters)
#     syslog_ng_parameters = stub_dependencies_for_syslog_ng_parameters(syslog_ng_parameters)
#     syslog_ng_object = SyslogNg(tc_unittest.logger_factory, syslog_ng_parameters, "server")
#     syntax_check_command_elements = ["syslog-ng -Fedtv --no-caps --enable-core", "slng_config_server.conf", "slng_persist_server.persist", "slng_pid_server.pid"]
#     for command_element in syntax_check_command_elements:
#         assert command_element in syslog_ng_object.get_syslog_ng_start_command(syntax_check=True)