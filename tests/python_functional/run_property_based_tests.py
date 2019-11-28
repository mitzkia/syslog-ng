#!/usr/bin/env python3
import argparse
import os
import shlex
import shutil
import sys
from pathlib import Path

import pytest
from utils.ConfigOptions import get_driver_options

from syslog_ng_tests.property_based.option_type_and_hypothesis_strategy_mapping import STRATEGY_MAPPING_BY_OPTION_NAME
from syslog_ng_tests.property_based.option_type_and_hypothesis_strategy_mapping import STRATEGY_MAPPING_BY_OPTION_TYPE

sys.path.append(os.path.join("../../contrib/config_option_database"))


PROPERTY_BASED_TESTS_RELATIVE_PATH = "syslog_ng_tests/property_based/"


class FilteredOption(Exception):
    pass


class PropertyTestGenerator:
    def __init__(self, max_examples, user_filters, database_meta):
        self.max_examples = max_examples

        self.blacklist_options = user_filters["blacklist_options"]
        self.blacklist_drivers = user_filters["blacklist_drivers"]
        self.blacklist_blocks = user_filters["blacklist_blocks"]

        self.whitelist_options = user_filters["whitelist_options"]
        self.whitelist_drivers = user_filters["whitelist_drivers"]
        self.whitelist_blocks = user_filters["whitelist_blocks"]

        self.option_database = database_meta["option_database"]
        self.db_type = database_meta["db_type"]
        self.testcase_names = []
        self.testcase_contents = []

        self.add_hardcoded_blacklist_drivers()
        self.add_hardcoded_blacklist_blocks()
        self.add_hardcoded_blacklist_options()

    def add_hardcoded_blacklist_drivers(self):
        pass
        # self.blacklist_drivers.extend(["openbsd", "sun_stream", "sun_streams", "pacct", "systemd_syslog"])  # sources
        # self.blacklist_drivers.extend(['elasticsearch2', 'hdfs', 'kafka_java', 'loggly', 'logmatic'])  # destinations
        # self.blacklist_drivers.extend(['apache_accesslog_parser_vhost', 'checkpoint_parser', 'cisco_timestamp_parser', 'ewmm_parser', 'extract_solaris_msgid', 'iptables_parser', 'netskope_parser', 'sudo_parser', 'websense_parser', 'windows_eventlog_parser', 'add_contextual_data', 'csv_parser', 'date_parser', 'db_parser', 'geoip2', 'grouping_by', 'json_parser', 'kv_parser', 'linux_audit_parser', 'map_value_pairs', 'python', 'snmptrapd_parser', 'syslog_parser', 'tags_parser', 'xml'])  # parsers
        # self.blacklist_drivers.extend(['credit_card_hash'])  # rewrites

    def add_hardcoded_blacklist_blocks(self):
        self.blacklist_blocks.extend(["attributes", "rekey", "config", "option", "failover", "failback", "tls", "type", "value_pairs", "disk_buffer", "hook_commands"])

    def add_hardcoded_blacklist_options(self):
        self.blacklist_options.extend(["multi_line_garbage", "multi_line_prefix", "persist_name", "disk_buffer", "force_directory_polling", "recursive", "positional", "interface", "workers", "localip"])

    def generate_pbts_for_database(self, write_testcase_content=True):
        for option_item in self.option_database:
            try:
                option_name, option_types, block_names, parent_drivers = self.get_fields_for_option_item(option_item)

                self.filter_by_blacklist_whitelist_options(option_name)
                selected_parent_drivers = self.filter_list_items_by_blacklist_or_whitelist(
                    property_list=parent_drivers,
                    blacklist_elements=self.blacklist_drivers,
                    whitelist_elements=self.whitelist_drivers,
                )
                selected_block_names = self.filter_list_items_by_blacklist_or_whitelist(
                    property_list=block_names,
                    blacklist_elements=self.blacklist_blocks,
                    whitelist_elements=self.whitelist_blocks,
                )

                testcase_name = self.construct_testcase_name(option_types, option_name, selected_block_names)
                testcase_content = self.construct_testcase_content(testcase_name, option_name, option_types, selected_block_names, selected_parent_drivers)
                self.save_testcase_name_and_content(testcase_name, testcase_content)

                print(testcase_name)

                if write_testcase_content:
                    self.write_testcase_content_to_disk(testcase_name, testcase_content)
            except FilteredOption:
                pass

    def save_testcase_name_and_content(self, testcase_name, testcase_content):
        self.testcase_names.append(testcase_name)
        self.testcase_contents.append(testcase_content)

    def get_fields_for_option_item(self, option_item):
        return option_item["option_name"], option_item["option_types"], option_item["block_names"], option_item["parent_drivers"]

    def filter_by_blacklist_whitelist_options(self, option_name):
        if self.blacklist_options and option_name in self.blacklist_options:
            raise FilteredOption
        if self.whitelist_options and option_name not in self.whitelist_options:
            raise FilteredOption

    def filter_list_items_by_blacklist_or_whitelist(self, property_list, blacklist_elements, whitelist_elements):
        if property_list == []:
            return property_list
        filtering_result = None
        if whitelist_elements:
            filtering_result = list(set(property_list).intersection(whitelist_elements))
        elif blacklist_elements:
            filtering_result = list(set(property_list).difference(blacklist_elements))
        else:
            return property_list
        if filtering_result == []:
            raise FilteredOption
        return filtering_result

    def construct_testcase_name(self, option_types, option_name, block_names):
        testcase_name = "test_{}_".format(self.db_type)
        if block_names:
            testcase_name += "{}_".format("_".join(block_names))
        testcase_name += "{}_".format(option_name)
        normalized_option_types = [item.replace("<", "").replace(">", "").replace(":", "colon") for item in option_types]
        testcase_name += "_".join(normalized_option_types)
        return testcase_name

    def write_testcase_content_to_disk(self, testcase_name, testcase_content):
        if testcase_content:
            testcase_path = Path(PROPERTY_BASED_TESTS_RELATIVE_PATH, self.db_type, "{}.py".format(testcase_name))
            with open(testcase_path, "w") as file_object:
                file_object.write(testcase_content)

    def construct_testcase_content(self, testcase_name, option_name, option_types, block_names, parent_drivers):
        testcase_content = ""
        testcase_content += self.construct_testcase_imports(option_types)
        testcase_content += self.construct_hypothesis_decorators(option_name, option_types)
        testcase_content += self.construct_testcase_definition(option_types, testcase_name)
        testcase_content += self.construct_testcase_action(option_name, option_types, block_names, parent_drivers)
        return testcase_content

    def construct_testcase_imports(self, option_types):
        testcase_imports = """
import random
import string
from hypothesis.provisional import domains, ip4_addr_strings, ip6_addr_strings, urls
from hypothesis.strategies import one_of, text, floats, integers, sampled_from, just, lists
from hypothesis import given, Verbosity, settings
from syslog_ng_tests.property_based.conftest import setup_workspace, get_syslog_ng_and_config_objects, build_option
from syslog_ng_tests.property_based.option_type_and_hypothesis_strategy_mapping import template_functions, time_zones
from src.syslog_ng.syslog_ng_cli import SyslogNgSyntaxError
"""
        return testcase_imports

    def construct_hypothesis_decorators(self, option_name, option_types):
        hypothesis_decorators = """
@settings(max_examples={}, verbosity=Verbosity.verbose, database=None, deadline=None)
@given({})
""".format(self.max_examples, self.build_hypothesis_strategy(option_name, option_types))
        return hypothesis_decorators

    def build_hypothesis_strategy(self, option_name, option_types):
        strategies = ""
        if option_name in STRATEGY_MAPPING_BY_OPTION_NAME:
            strategies += STRATEGY_MAPPING_BY_OPTION_NAME[option_name]
        else:
            for option_type in option_types:
                if strategies != "":
                    strategies += ", "
                if option_type in STRATEGY_MAPPING_BY_OPTION_TYPE:
                    strategies += STRATEGY_MAPPING_BY_OPTION_TYPE[option_type]
                else:
                    strategies += "just('{}')".format(option_type)
        return strategies

    def construct_testcase_definition(self, option_types, testcase_name):
        testcase_definition = "def {}(request, {}):".format(testcase_name, self.construct_tested_value_for_testcase_definition(len(option_types)))
        return testcase_definition

    def construct_tested_value_for_testcase_definition(self, counter):
        constructed_string = ""
        for i in range(1, counter + 1):
            if constructed_string != "":
                constructed_string += ", "
            constructed_string += "tested_value_{}".format(i)
        return constructed_string

    def construct_testcase_action(self, option_name, option_types, block_names, parent_drivers):
        testcase_action = """
    testcase_parameters = setup_workspace(request)
    config, syslog_ng = get_syslog_ng_and_config_objects(request, testcase_parameters)

    constructed_option = build_option('{}', {}, {})
    config.create_multidriver_config(parent_drivers={}, driver_type='{}', constructed_option=constructed_option)

    syslog_ng.start(config)
    syslog_ng.stop()
""".format(option_name, block_names, self.construct_tested_value_for_testcase_definition(len(option_types)), parent_drivers, self.db_type)
        return testcase_action


def cleanup_test_dir_for_db_type(db_type):
    shutil.rmtree("{}/{}".format(PROPERTY_BASED_TESTS_RELATIVE_PATH, db_type), ignore_errors=True)
    Path(PROPERTY_BASED_TESTS_RELATIVE_PATH, db_type).mkdir()


def validate_properties(context, parent_driver, option_name, option_types, block_names):
    assert isinstance(context, str)
    assert isinstance(parent_driver, str)
    assert isinstance(option_name, str)
    assert isinstance(option_types, tuple)
    assert isinstance(block_names, tuple)


def get_normalized_properties(parent_driver, option_name, option_types, block_names):
    normalized_parent_driver = [parent_driver.split("/")[0].replace("-", "_")]

    option_name = option_name if option_name else "positional"
    normalized_option_name = option_name.split("/")[0].replace("-", "_").replace("<", "typed_").replace(">", "")

    option_types = option_types if option_types else ('<empty>',)
    normalized_option_types = [item.replace("<n/a>", "<unknown>").replace("-", "_") for item in option_types]

    normalized_block_names = [item.split("/")[0].replace("-", "_") for item in block_names]

    return normalized_parent_driver, normalized_option_name, normalized_option_types, normalized_block_names


def update_parent_driver_for_option_if_needed(options_context_node, option):
    for item in options_context_node:
        if option['option_name'] == item['option_name'] and option['option_types'] == item['option_types'] and option['block_names'] == item['block_names']:
            item['parent_drivers'].append(option['parent_drivers'][0])
            return True
    return False


def update_context_node_with_option(options_context_node, option):
    if not update_parent_driver_for_option_if_needed(options_context_node, option):
        options_context_node.append(option)


def get_driver_options_property_style():
    options_db = {}
    for context, parent_driver, option_name, option_types, block_names in get_driver_options():
        validate_properties(context, parent_driver, option_name, option_types, block_names)
        normalized_parent_driver, normalized_option_name, normalized_option_types, normalized_block_names = get_normalized_properties(parent_driver, option_name, option_types, block_names)

        option = {
            'option_name': normalized_option_name,
            'option_types': normalized_option_types,
            'block_names': normalized_block_names,
            'parent_drivers': normalized_parent_driver,
        }
        options_context_node = options_db.setdefault(context, [])
        update_context_node_with_option(options_context_node, option)
    return options_db


def generate_property_based_tests(max_examples, user_filters):
    for db_type, db_values in get_driver_options_property_style().items():
        cleanup_test_dir_for_db_type(db_type)

        database_meta = {
            "option_database": db_values,
            "db_type": db_type,
        }
        property_test_generator = PropertyTestGenerator(max_examples, user_filters, database_meta)
        property_test_generator.generate_pbts_for_database()


def run_property_based_tests(installdir):
    start_pytest_cmd = "\
        --installdir={} \
        -lvvvs -r A \
        {}".format(installdir, PROPERTY_BASED_TESTS_RELATIVE_PATH)
    pytest.main(shlex.split(start_pytest_cmd))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--installdir", required=True)
    parser.add_argument("--max-examples", default=1)

    parser.add_argument('--blacklist-options', nargs='+', default=[])
    parser.add_argument('--blacklist-drivers', nargs='+', default=[])
    parser.add_argument('--blacklist-blocks', nargs='+', default=[])

    parser.add_argument('--whitelist-options', nargs='+', default=[])
    parser.add_argument('--whitelist-drivers', nargs='+', default=[])
    parser.add_argument('--whitelist-blocks', nargs='+', default=[])

    args = parser.parse_args()

    user_filters = {
        "blacklist_options": args.blacklist_options,
        "blacklist_drivers": args.blacklist_drivers,
        "blacklist_blocks": args.blacklist_blocks,

        "whitelist_options": args.whitelist_options,
        "whitelist_drivers": args.whitelist_drivers,
        "whitelist_blocks": args.whitelist_blocks,
    }

    generate_property_based_tests(args.max_examples, user_filters)
    run_property_based_tests(args.installdir)


if __name__ == "__main__":
    exit(main())
