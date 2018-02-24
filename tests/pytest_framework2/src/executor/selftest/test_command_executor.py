import pytest
from src.executor.command_executor import CommandExecutor


@pytest.mark.parametrize("command, expected_exit_code, expected_stdout, expected_stderr", [
    (
        ["echo", "almafa"],
        0,
        "almafa\n",
        ""
    ),
    (
        ["grep", "almafa", "almafa"],
        2,
        "",
        "grep: almafa: No such file or directory\n"
    ),
])
def test_command_executor(tc_unittest, command, expected_exit_code, expected_stdout, expected_stderr):
    command_executor = CommandExecutor(tc_unittest.logger_factory)
    exit_code, stdout, stderr = command_executor.execute_command(command)
    assert [exit_code, stdout, stderr] == [expected_exit_code, expected_stdout, expected_stderr]
