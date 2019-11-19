#!/usr/bin/env python
#############################################################################
# Copyright (c) 2015-2019 Balabit
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# As an additional exemption you are allowed to compile & link against the
# OpenSSL libraries as published by the OpenSSL project. See the file
# COPYING for details.
#
#############################################################################
import os
import re
from datetime import datetime

import pytest
import src.testcase_parameters.testcase_parameters as tc_parameters
from pathlib2 import Path
from src.common.operations import copy_file
from src.common.pytest_operations import calculate_testcase_name
from src.syslog_ng.syslog_ng import SyslogNg
from src.syslog_ng.syslog_ng_paths import SyslogNgPaths
from src.syslog_ng_config.syslog_ng_config import SyslogNgConfig
from src.testcase_parameters.testcase_parameters import TestcaseParameters


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")


def calculate_working_dir(pytest_config_object, testcase_name):
    report_dir = Path(Path.cwd(), "reports/", get_current_date())
    return Path(report_dir, calculate_testcase_name(testcase_name))


def setup_workspace(request):
    tc_parameters.WORKING_DIR = working_dir = calculate_working_dir(request.config, request.node.name)
    tc_parameters.RELATIVE_WORKING_DIR = relative_working_dir = working_dir.relative_to(Path.cwd())
    request.node.user_properties.append(("working_dir", working_dir))
    request.node.user_properties.append(("relative_working_dir", relative_working_dir))
    testcase_parameters = TestcaseParameters(request)  # We need to manually instantiate TestcaseParameters() otherwise it will used from cache
    if not testcase_parameters.get_working_dir().exists():
        testcase_parameters.get_working_dir().mkdir(parents=True)
    copy_file(testcase_parameters.get_testcase_file(), testcase_parameters.get_working_dir())
    return testcase_parameters


def get_syslog_ng_and_config_objects(request, testcase_parameters):
    config = SyslogNgConfig(request.getfixturevalue("version"))
    instance_paths = SyslogNgPaths(testcase_parameters).set_syslog_ng_paths("server")
    syslog_ng = SyslogNg(instance_paths, testcase_parameters)
    request.addfinalizer(lambda: syslog_ng.stop())
    return config, syslog_ng


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    yield


collected_hypothesis_reports = ""
collection_of_started_testcases = []
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    global collected_hypothesis_reports, collection_of_started_testcases
    report = (yield).get_result()
    working_dirs = []
    if hasattr(item, "hypothesis_report_information") and report.when == "teardown":
        for line in item.hypothesis_report_information:
            if line.startswith("Trying example:") or line.startswith("Falsifying example:"):
                collection_of_started_testcases.append(line)
        for (dirpath, dirnames, filenames) in os.walk("reports/"):
            for filename in filenames:
                full_path = Path(dirpath, filename)
                working_dir = str(full_path.parent)
                if working_dir not in working_dirs:
                    working_dirs.append(working_dir)

        if len(collection_of_started_testcases) == len(working_dirs):
            working_dirs = sorted(working_dirs)
            collected_hypothesis_reports = ""
            started_testcases_and_working_dirs = zip(collection_of_started_testcases, working_dirs)
            new_data = (' : Working Dir '.join(item) for item in started_testcases_and_working_dirs)
            for elem in new_data:
                collected_hypothesis_reports += elem + "\n"
        else:
            # probably the reports/ dir is not empty
            raise Exception


def pytest_terminal_summary(terminalreporter):
    """ This function merges two information in one final report,
    - on one side we have collected_hypothesis_reports where testcase names are linked with working dirs
    - on the other side we have testcases with linked failure reports
    - final report will contains testcase name + actual hypothesis value + working dir + testcase failure
    """
    print("\n\n-------------------------------------------------------------------PROPERTY BASED TESTS FAILURES SUMMARY-------------------------------------------------------------------")
    final_report = ""
    collected_hypothesis_reports_list = collected_hypothesis_reports.splitlines()

    if "failed" in terminalreporter.stats:
        for testcase_item in terminalreporter.stats['failed']:
            for item in testcase_item.sections[0]:
                actual_tc = None
                actual_traceback = None
                for line in item.splitlines():
                    if "Trying example" in line:
                        actual_tc = line
                    if re.search("^[^(Trying example)]", line) is not None:
                        actual_traceback = line

                    if actual_tc and actual_traceback:
                        for line in collected_hypothesis_reports_list:
                            if actual_tc in line:
                                del collected_hypothesis_reports_list[collected_hypothesis_reports_list.index(line)]
                                line = re.sub(r'request=.*>>, ', '', line).replace(":", "\n")
                                final_report += line + " \n Failure reason: " + actual_traceback + "\n"
                                final_report += "\n------------------------------------------\n"
                                break
                        actual_tc = None
                        actual_traceback = None

    terminalreporter.write_line(final_report)
    with open("property_based_report.log", "w") as file_object:
        file_object.write(final_report)


def build_option(option_name, block_names, *tested_option_values):
    if len(tested_option_values) == 1:
        if tested_option_values[0] in ["yes", "no", "on", "off"] or not isinstance(tested_option_values[0], str):
            return {option_name: tested_option_values[0]}
        else:
            option_value = '"{}"'.format(tested_option_values[0])
            return {option_name: option_value}

    concatenated_tested_option_values = " "
    for value in tested_option_values:
        concatenated_tested_option_values += str(value) + " "
    builded_tested_option = {option_name: concatenated_tested_option_values}

    # if block_names:
    #     for parent_option in reversed(block_names):
    #         builded_tested_option = {parent_option: builded_tested_option}

    return builded_tested_option
