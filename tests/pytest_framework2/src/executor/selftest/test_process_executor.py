from subprocess import PIPE
from src.executor.process_executor import ProcessExecutor
from src.executor.process_common import ProcessCommon


def test_process_executor_start_stop(tc_unittest):
    process_common = ProcessCommon(tc_unittest.logger_factory)
    process_executor = ProcessExecutor(tc_unittest.logger_factory)
    python_command = ["python3", "-c", "'import time; time.sleep(3)'"]
    process_object = process_executor.start_process(python_command, PIPE, PIPE)
    assert process_object.is_running() is True
    assert process_common.is_pid_in_process_list(process_object.pid) is True
    process_executor.stop_process(process_object)
    assert process_object.is_running() is False
    assert process_common.is_pid_in_process_list(process_object.pid) is False
