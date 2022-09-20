import pytest

from src.common.file import copy_shared_file

from functional_tests.parametrize_testcases import generate_options_and_values_for_driver
from functional_tests.parametrize_testcases import generate_id_name

@pytest.mark.parametrize("option_and_value", generate_options_and_values_for_driver("source", "network"), ids=generate_id_name)
def test_network_source_smoke(config, syslog_ng, bsd_formatter, log_message, port_allocator, testcase_parameters, option_and_value):

    config.update_global_options(stats_level=5)
    if list(option_and_value.keys())[0] not in ["ip", "localip", "port", "localport"]:
        network_source = config.create_network_source(ip="localhost", port=port_allocator(), **option_and_value)
        if list(option_and_value.keys())[0] == "tls":
            network_source.options["transport"] = "'tls'"
            server_key_path = copy_shared_file(testcase_parameters, "server.key")
            server_cert_path = copy_shared_file(testcase_parameters, "server.crt")
            network_source.options["tls"].update(
                {
                    "key-file": "'%s'" % server_key_path, 
                    "cert-file": "'%s'" % server_cert_path,
                    "peer-verify": "'optional-untrusted'",
                }
            )
            if "pkcs12-file" in list(option_and_value["tls"].keys()):
                server_pkcs12_path = copy_shared_file(testcase_parameters, "server.p12")
                network_source.options["tls"].update(
                    {
                        "pkcs12-file": "'%s'" % server_pkcs12_path,
                    }
                )
            if "dhparam-file" in list(option_and_value["tls"].keys()):
                dhparam_path = copy_shared_file(testcase_parameters, "dhparam.pem")
                network_source.options["tls"].update(
                    {
                        "dhparam-file": "'%s'" % dhparam_path,
                    }
                )
            if "ca-file" in list(option_and_value["tls"].keys()):
                ca_file_path = copy_shared_file(testcase_parameters, "ca.crt")
                network_source.options["tls"].update(
                    {
                        "ca-file": "'%s'" % ca_file_path,
                    }
                )
            # if "cacert" in list(option_and_value["tls"].keys()):
            #     cacert_path = copy_shared_file(testcase_parameters, "ca.crt")
            #     network_source.options["tls"].update(
            #         {
            #             "cacert": "'%s'" % cacert_path,
            #         }
            #     )
            # if "cert" in list(option_and_value["tls"].keys()):
            #     cert_path = copy_shared_file(testcase_parameters, "ca.crt")
            #     network_source.options["tls"].update(
            #         {
            #             "cert": "'%s'" % cert_path,
            #         }
            #     )
    elif list(option_and_value.keys())[0] in ["ip", "localip"]:
        network_source = config.create_network_source(port=port_allocator(), **option_and_value)
    else:
        network_source = config.create_network_source(**option_and_value)

    file_destination = config.create_file_destination(file_name="output.log")
    config.create_logpath(statements=[network_source, file_destination])

    syslog_ng.start(config)
    network_source.write_log(bsd_formatter.format_message(log_message), 1)
    syslog_ng.reload(config)

    assert file_destination.read_log() != ""
    assert file_destination.get_query()["written"] == 1