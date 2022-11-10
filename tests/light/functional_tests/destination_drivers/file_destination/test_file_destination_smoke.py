import pytest

from functional_tests.parametrize_testcases import generate_id_name
from functional_tests.parametrize_testcases import generate_options_and_values_for_driver
from src.common.file import copy_shared_file


@pytest.mark.parametrize("option_and_value", generate_options_and_values_for_driver("destination", "file"), ids=generate_id_name)
def test_file_destination_smoke(config, syslog_ng, bsd_formatter, log_message, option_and_value):
    # print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    # print(option_and_value)
    config.update_global_options(stats_level=5)
    generator_source = config.create_example_msg_generator_source(num=1, template=config.stringify(bsd_formatter.format_message(log_message)))

    if option_and_value == {'': ''}:
        file_destination = config.create_file_destination(file_name="output.log")
    else:
        file_destination = config.create_file_destination(file_name="output.log", **option_and_value)

    if option_and_value == {'disk-buffer': ''}:
        file_destination.options["disk-buffer"] = ""
    elif list(option_and_value.keys())[0] == "disk-buffer":
        file_destination.options["disk-buffer"].update({"disk-buf-size": "1M"})
    elif list(option_and_value.keys())[0] == "class":
        copy_shared_file("sngexample.py")

    config.create_logpath(statements=[generator_source, file_destination])

    syslog_ng.start(config)
    syslog_ng.reload(config)

    assert file_destination.read_log() != ""
    assert file_destination.get_query()["written"] != 0
