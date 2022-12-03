import pytest

from src.common.file import copy_shared_file


def configure_network_source(config, port_allocator, testcase_parameters, pp_type):
    if pp_type == "tls":
        server_key_path = copy_shared_file(testcase_parameters, "server.key")
        server_cert_path = copy_shared_file(testcase_parameters, "server.crt")
        transport = '"proxied-tls-passthrough"'
        network_source = config.create_network_source(
            ip="localhost",
            port=port_allocator(),
            transport=transport,
            flags="no-parse",
            tls={
                "key-file": server_key_path,
                "cert-file": server_cert_path,
                "peer-verify": '"optional-untrusted"',
            },
        )
    else:
        transport = '"proxied-tcp"'
        network_source = config.create_network_source(ip="localhost", port=port_allocator(), transport=transport, flags="no-parse")
    return network_source


def set_loggen_parameter(pp_type, loggen_input_method, testcase_parameters):
    if pp_type == "non_tls" and loggen_input_method == "native":
        loggen_custom_options = {
            "inet": True,
        }
    if pp_type == "non_tls" and loggen_input_method == "file":
        loggen_input_file_path = copy_shared_file(testcase_parameters, "proxy_protocol_v2_input/pp_test_message")
        loggen_custom_options = {
            "inet": True,
            "dont_parse": True,
            "read_file": loggen_input_file_path,
            "loop_reading": True,
        }
    if pp_type == "tls" and loggen_input_method == "native":
        loggen_custom_options = {
            "use_ssl": True,
            "proxied_tls_passthrough": True,
        }
    if pp_type == "tls" and loggen_input_method == "file":
        loggen_input_file_path = copy_shared_file(testcase_parameters, "proxy_protocol_v2_input/pp_test_message")
        loggen_custom_options = {
            "use_ssl": True,
            "proxied_tls_passthrough": True,
            "dont_parse": True,
            "read_file": loggen_input_file_path,
            "loop_reading": True,
        }
    return loggen_custom_options


@pytest.mark.parametrize("pp_version", [1, 2])
# @pytest.mark.parametrize("pp_version", [1])
@pytest.mark.parametrize("pp_type", ["non_tls", "tls"])
# @pytest.mark.parametrize("pp_type", ["non_tls"])
@pytest.mark.parametrize("loggen_input_method", ["native", "file"])
# @pytest.mark.parametrize("loggen_input_method", ["native"])
# @pytest.mark.parametrize("loggen_message_counter", [1, 2, 5, 10])
@pytest.mark.parametrize("loggen_message_counter", [2])
def test_pp_acceptance(config, syslog_ng, loggen, port_allocator, testcase_parameters, pp_version, pp_type, loggen_input_method, loggen_message_counter):
    config.update_global_options(stats_level=1)
    network_source = configure_network_source(config, port_allocator, testcase_parameters, pp_type)
    TEMPLATE = r'"${PROXIED_SRCIP} ${PROXIED_DSTIP} ${PROXIED_SRCPORT} ${PROXIED_DSTPORT} ${PROXIED_IP_VERSION} ${MESSAGE}\n"'
    file_destination = config.create_file_destination(file_name="output.log", template=TEMPLATE)
    config.create_logpath(statements=[network_source, file_destination])

    syslog_ng.start(config)

    loggen_custom_options = set_loggen_parameter(pp_type, loggen_input_method, testcase_parameters)
    loggen.start(
        debug=True,
        target=network_source.options["ip"],
        port=network_source.options["port"],
        proxied=pp_version,
        number=loggen_message_counter,
        **loggen_custom_options,
    )

    output_log = file_destination.read_logs(counter=loggen_message_counter - 1)
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA: input msg num: %s vs written: %s vs arrived lines: %s" % (loggen_message_counter, file_destination.get_stats()["written"], len(output_log)))
