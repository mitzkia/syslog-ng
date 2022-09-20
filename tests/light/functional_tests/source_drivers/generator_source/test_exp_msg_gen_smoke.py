import pytest

from functional_tests.parametrize_testcases import generate_options_and_values_for_driver
from functional_tests.parametrize_testcases import generate_id_name

@pytest.mark.parametrize("option_and_value", generate_options_and_values_for_driver("source", "example-msg-generator"), ids=generate_id_name)
def test_example_msg_generator_source_smoke(config, syslog_ng, option_and_value):

    config.update_global_options(stats_level=5)
    example_msg_generator_source = config.create_example_msg_generator_source(**option_and_value)

    file_destination = config.create_file_destination(file_name="output.log")
    config.create_logpath(statements=[example_msg_generator_source, file_destination])

    syslog_ng.start(config)
    syslog_ng.reload(config)

    assert file_destination.read_log() != ""
    assert file_destination.get_query()["written"] != 0