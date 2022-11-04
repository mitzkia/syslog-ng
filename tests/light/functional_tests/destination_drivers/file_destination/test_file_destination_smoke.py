import pytest

from functional_tests.parametrize_testcases import generate_id_name
from functional_tests.parametrize_testcases import generate_options_and_values_for_driver


@pytest.mark.parametrize("option_and_value", generate_options_and_values_for_driver("destination", "file"), ids=generate_id_name)
def test_file_source_smoke(config, syslog_ng, bsd_formatter, log_message, option_and_value):

    config.update_global_options(stats_level=5)
    generator_source = config.create_example_msg_generator_source(num=1, template=config.stringify(bsd_formatter.format_message(log_message)))

    file_destination = config.create_file_destination(file_name="output.log", **option_and_value)
    if list(option_and_value.keys())[0] == "disk-buffer":
        file_destination.options["disk-buffer"].update({"disk_buf_size": "1M"})

    config.create_logpath(statements=[generator_source, file_destination])

    syslog_ng.start(config)
    syslog_ng.reload(config)

    assert file_destination.read_log() != ""
    assert file_destination.get_query()["written"] != 0
