import pytest

from functional_tests.parametrize_testcases import generate_options_and_values_for_driver
from functional_tests.parametrize_testcases import generate_id_name

@pytest.mark.parametrize("option_and_value", generate_options_and_values_for_driver("source", "file"), ids=generate_id_name)
def test_file_source_smoke(config, syslog_ng, bsd_formatter, log_message, option_and_value):

    config.update_global_options(stats_level=5)
    if list(option_and_value.keys())[0] != "":
        file_source = config.create_file_source(file_name="input.log", **option_and_value)
    else:
        file_source = config.create_file_source(file_name=list(option_and_value.values())[0].replace("'", ""))
    if list(option_and_value.keys())[0] in ["multi-line-prefix", "multi-line-suffix", "multi-line-garbage"]:
        file_source.options["multi-line-mode"] = "'regexp'"
    if list(option_and_value.keys())[0] == "multi-line-mode":
        file_source.options["multi-line-prefix"] = "'test'"
    if list(option_and_value.keys())[0] == "pad-size":
        file_source.options["pad-size"] = 10
    file_destination = config.create_file_destination(file_name="output.log")
    config.create_logpath(statements=[file_source, file_destination])

    syslog_ng.start(config)
    file_source.write_log(bsd_formatter.format_message(log_message), 5)
    syslog_ng.reload(config)

    assert file_destination.read_log() != ""
    assert file_destination.get_query()["written"] != 0
