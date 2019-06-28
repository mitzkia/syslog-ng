#!/usr/bin/env python
#############################################################################
# Copyright (c) 2015-2018 Balabit
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
from pathlib2 import Path

import src.testcase_parameters.testcase_parameters as tc_parameters
from src.common.random_id import get_unique_id
from src.driver_io.file.file_io import FileIO
from src.message_reader.single_line_parser import SingleLineParser
from src.syslog_ng_config.statements.destinations.destination_reader import DestinationReader
from src.syslog_ng_ctl.syslog_ng_ctl import SyslogNgCtl


class DriverStatsHandler(object):
    def __init__(self, group_type, driver_name):
        if group_type == "destination":
            statement_short_name = "dst"
        elif group_type == "source":
            statement_short_name = "src"

        self.component = "{}.{}".format(statement_short_name, driver_name)
        self.syslog_ng_ctl = SyslogNgCtl(tc_parameters.INSTANCE_PATH)

    def build_query_pattern(self):
        return self.build_pattern(delimiter=".")

    def build_stats_pattern(self):
        return self.build_pattern(delimiter=";")

    def build_pattern(self, delimiter):
        return "{}{}".format(
            self.component,
            delimiter,
        )

    def parse_result(self, result, result_type):
        statistical_elements = ["memory_usage", "written", "processed", "dropped", "queued", "stamp"]
        parsed_output = {}
        for stat_element in statistical_elements:
            for line in result:
                if stat_element in line:
                    if result_type == "query":
                        parsed_output.update({stat_element: int(line.split(".")[-1].split("=")[-1])})
                    elif result_type == "stats":
                        parsed_output.update({stat_element: int(line.split(".")[-1].split(";")[-1])})
                    else:
                        raise Exception("Unknown result_type: {}".format(result_type))
        return parsed_output

    def filter_stats_result(self, stats_result, stats_pattern):
        filtered_list = []
        for stats_line in stats_result:
            if stats_pattern in stats_line:
                filtered_list.append(stats_line)
        return filtered_list

    def get_query(self):
        query_pattern = self.build_query_pattern()
        query_result = self.syslog_ng_ctl.query(pattern="*{}*".format(query_pattern))['stdout'].splitlines()

        return self.parse_result(result=query_result, result_type="query")

    def get_stats(self):
        stats_pattern = self.build_stats_pattern()
        stats_result = self.syslog_ng_ctl.stats()['stdout'].splitlines()

        filtered_stats_result = self.filter_stats_result(stats_result, stats_pattern)
        return self.parse_result(result=filtered_stats_result, result_type="stats")


class FileDestination(object):
    def __init__(self, file_name=None, **options):
        self.driver_name = "file"
        self.group_type = "destination"
        self.options = options
        if file_name is not None:
            if file_name == "":
                self.positional_option = "''"
            elif file_name == "auto":
                self.positional_option = Path(tc_parameters.WORKING_DIR, "output_fd_{}.log".format(get_unique_id()))
            else:
                self.positional_option = Path(tc_parameters.WORKING_DIR, file_name)
        self.destination_reader = DestinationReader(FileIO, SingleLineParser)
        self.stats_handler = DriverStatsHandler(group_type=self.group_type, driver_name=self.driver_name)

    def get_path(self):
        return self.positional_option

    def set_path(self, pathname):
        self.positional_option = Path(tc_parameters.WORKING_DIR, pathname)
        self.destination_reader.construct_driver_io(self.positional_option)

    def read_log(self):
        return self.destination_reader.read_logs(self.get_path(), counter=1)[0]

    def read_logs(self, counter):
        return self.destination_reader.read_logs(self.get_path(), counter=counter)

    def get_stats(self):
        return self.stats_handler.get_stats()

    def get_query(self):
        return self.stats_handler.get_query()
