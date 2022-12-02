#!/usr/bin/env python
#############################################################################
# Copyright (c) 2020 One Identity
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
import pytest

from src.common.blocking import wait_until_true

NUMBER_OF_MESSAGES = 10


@pytest.mark.parametrize(
    "pp_version", [
        ("proxy-protocol-v1"),
        ("proxy-protocol-v2"),
    ], ids=["pp_v1", "pp_v2"],
)
def test_pp_with_simple_tcp_connection(config, port_allocator, syslog_ng, loggen, testcase_parameters, pp_version):
    network_source = config.create_network_source(ip="localhost", port=port_allocator(), transport="proxied-tcp")
    file_destination = config.create_file_destination(file_name="output.log")
    config.create_logpath(statements=[network_source, file_destination])

    syslog_ng.start(config)

    loggen.start(network_source.options["ip"], network_source.options["port"], inet=True, stream=True, number=NUMBER_OF_MESSAGES)
    wait_until_true(lambda: loggen.get_sent_message_count() == NUMBER_OF_MESSAGES)

    # We could check the source side stats, too, but it is not yet implemented
    assert not file_destination.get_path().exists()
