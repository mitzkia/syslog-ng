import itertools
import os
import sys

sys.path.append(os.path.join("../../contrib/config_option_database"))

from utils.ConfigOptions import get_driver_options  # noqa: E402

def generate_options_and_values_for_driver(expected_context, expected_driver):
    option_value_type_to_value_map = {
        "<arrow>": "=>",
        "<float>": 12.34,
        "<nonnegative-integer>": 4567,
        "<number>": 1234,
        "<path>": "'/tmp/a'",
        "<positive-integer>": 6789,
        "<string-list>": "aaa bbb ccc",
        "<string-or-number>": "teszt",
        "<string>": "'almafa'",
        "<template-content>": "'$MSG\n'",
        "<yesno>": "yes",
        "check-hostname": "check-hostname",
        "persist-only": "persist-only",
        "syslog": "'syslog'",
        "<string> <string-or-number>": '"counter", 11',
        "<string> <arrow> <string-or-number>": '"counter" => 11',
    }

    option_name_to_value_map = {
        'default-facility': "'kern'",
        'default-level': "'emerg'",
        'default-priority': "'emerg'",
        'default-severity': "'emerg'",
        "cipher-suite": "ECDHE-RSA-AES256-SHA",
        "client-sigalgs": "'RSA-PSS+SHA256:ed25519'",
        "curve-list": "'secp384r1:prime256v1'",
        "ecdh-curve-list": "'secp384r1:prime256v1'",
        "encoding": "'UTF-8'",
        "flags": "'no-parse'",
        "format": "'syslog'",
        "interface": "lo",
        "ip-protocol": 4,
        "ip": "127.0.0.1",
        "localip": "localhost",
        "localport": "30001",
        "mark-mode": "'internal'",
        "multi-line-garbage": "'test message'",
        "multi-line-mode": "'regexp'",
        "multi-line-prefix": "'test'",
        "multi-line-suffix": "'message'",
        "on-error": "fallback-to-string",
        "option": '"template", "$(format-json --scope dot_nv_pairs)"',
        "port": "30001",
        "setup": "'pwd'",
        "shutdown": "'pwd'",
        "sigalgs": "'RSA-PSS+SHA256:ed25519'",
        "ssl-options": "no-sslv2, no-sslv3, no-tlsv1",
        "startup": "'pwd'",
        "teardown": "'pwd'",
        "tls12-and-older": "'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256'",
        "tls13": "'TLS_CHACHA20_POLY1305_SHA256:TLS_AES_256_GCM_SHA384'",
        "truncate-size-ratio": 1,
        "transport": "tcp",
        "values": '"HOST" => "host$(iterate $(+ 1 $_) 0)"',
    }

    options = []

    def generate_option_properties_for_driver(expected_context, expected_driver):
        for context, driver, option_names, option_types, block_names in get_driver_options():
            if context == expected_context and driver == expected_driver:
                yield option_names, option_types, block_names

    def get_option_value(option_name, option_type):
        if option_type == "":
            return ""
        if option_name in option_name_to_value_map:
            return option_name_to_value_map[option_name]
        else:
            return option_value_type_to_value_map[option_type]

    def build_option_block(block_names, option_and_value):
        option_block = {}
        def update_option_block(option_block, subkey):
            option_block.update({subkey: {}})
            return option_block[subkey]

        for index, block_name in enumerate(block_names, start=1):
            if option_block == {}:
                working_option_block = update_option_block(option_block, block_name)
            else:
                working_option_block = update_option_block(working_option_block, block_name)
            if index == len(block_names):
                working_option_block.update(option_and_value)
        return option_block

    for option_names, option_types, block_names in generate_option_properties_for_driver(expected_context, expected_driver):
        if len(option_types) == 1:
            option_type = option_types[0]
        else:
            option_type = " ".join(option_types)
        for option_name in option_names.split("/"):
            if not block_names:
                options.append({option_name: get_option_value(option_name, option_type)})
            else:
                result_option_block = build_option_block(block_names, {option_name: get_option_value(option_name, option_type)})
                options.append(result_option_block)

    return options


def generate_id_name(param):
    def stringify_parameter(param):
        return repr(param).replace("{", "").replace("}", "").replace("'", "").replace(":", "").replace('"', "").replace(" ", "_")
    return stringify_parameter(param)