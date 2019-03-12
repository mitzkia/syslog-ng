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
import socket

import pytest

input_log = "<38>Feb 11 21:27:22 testprogram[9999]: test message\n"
expected_log = "Feb 11 21:27:22 {} testprogram[9999]: test message\n".format(socket.gethostname())


@pytest.mark.parametrize(
    "input_log, expected_log, counter",
    [(input_log, expected_log, 1), (input_log, expected_log, 10)],
    ids=["with_one_log", "with_ten_logs"],
)
def test_pipe_acceptance(config, syslog_ng, input_log, expected_log, counter):
    pipe_source = config.create_pipe_source(file_name="input.log")
    pipe_destination = config.create_pipe_destination(file_name="output.log")
    config.create_logpath(statements=[pipe_source, pipe_destination])

    syslog_ng.start(config)
    pipe_source.write_log(input_log, counter)
    assert pipe_destination.read_logs(counter) == [expected_log] * counter
