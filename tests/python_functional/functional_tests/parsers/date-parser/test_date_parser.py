#!/usr/bin/env python
#############################################################################
# Copyright (c) 2021 Balabit
# Copyright (c) 2021 Micek
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
import time

import src.testcase_parameters.testcase_parameters as tc_parameters

INPUT_MESSAGES = """CET +01 +02 +03 +04 +05 +06 PDT EDT M\n\
CET +01 +02 +03 +04 +05 +06 PDT EDT M\n\
CET +01 +02 +03 +04 +05 +06 PDT EDT M\n\
CET +01 +02 +03 +04 +05 +06 PDT EDT M\n\
CET +01 +02 +03 +04 +05 +06 PDT EDT M\n\
CET +01 +02 +03 +04 +05 +06 PDT EDT M\n\
CET +01 +02 +03 +04 +05 +06 PDT EDT M\n\
CET +01 +02 +03 +04 +05 +06 PDT EDT M\n\
CET +01 +02 +03 +04 +05 +06 PDT EDT M\n\
CET +01 +02 +03 +04 +05 +06 PDT EDT M\n\
CET +01 +02 +03 +04 +05 +06 PDT EDT M\n\
CET +01 +02 +03 +04 +05 +06 PDT EDT M\n\
CET +01 +02 +03 +04 +05 +06 PDT EDT M\n\
CET +01 +02 +03 +04 +05 +06 PDT EDT M\n\
CET +01 +02 +03 +04 +05 +06 PDT EDT M\n\
CET +01 +02 +03 +04 +05 +06 PDT EDT M\n\
CET +01 +02 +03 +04 +05 +06 PDT EDT M\n\
CET +01 +02 +03 +04 +05 +06 PDT EDT M\n\
CET +01 +02 +03 +04 +05 +06 PDT EDT M\n\
CET +01 +02 +03 +04 +05 +06 PDT EDT M\n\
CET +01 +02 +03 +04 +05 +06 PDT EDT M\n"""


def test_date_parser(config, syslog_ng, loggen, port_allocator):
    network_source = config.create_network_source(ip="localhost", port=port_allocator())
    date_parsers = []
    for _ in range(0, 10):
        date_parsers.append(config.create_date_parser(format='"%z %z %z %z %z %z %z %z %z %z"'))

    config.create_logpath(statements=[network_source] + date_parsers)

    syslog_ng.start(config, stderr=False, debug=False, trace=False, verbose=False, startup_debug=False)

    loggen_intput_file_path = os.path.join(tc_parameters.WORKING_DIR, "loggen_input.txt")
    with open(loggen_intput_file_path, 'w') as file_object:
        file_object.write(INPUT_MESSAGES)

    time.sleep(1)
    loggen.start(target=network_source.options["ip"], port=network_source.options["port"], inet=True, syslog_proto=True, read_file=loggen_intput_file_path, loop_reading=True, dont_parse=True, rate=10000000, active_connections=100)
    time.sleep(3)

    loggen.stop()
