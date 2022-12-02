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

from src.common.file import copy_shared_file

TEMPLATE = r'"${PROXIED_SRCIP} ${PROXIED_DSTIP} ${PROXIED_SRCPORT} ${PROXIED_DSTPORT} ${PROXIED_IP_VERSION} ${MESSAGE}\n"'
INPUT_MESSAGES = "PROXY TCP4 1.1.1.1 2.2.2.2 3333 4444\r\n" \
                 "message 0\n" \
                 "message 1\n" \
                 "message 2\n"
EXPECTED_MESSAGE0 = "1.1.1.1 2.2.2.2 3333 4444 4 message 0\n"
EXPECTED_MESSAGE1 = "1.1.1.1 2.2.2.2 3333 4444 4 message 1\n"
EXPECTED_MESSAGE2 = "1.1.1.1 2.2.2.2 3333 4444 4 message 2\n"


@pytest.mark.parametrize(
    "pp_version", [
        ("proxy-protocol-v1"),
        ("proxy-protocol-v2"),
    ], ids=["pp_v1", "pp_v2"],
)
def test_pp_reload(config, syslog_ng, loggen, port_allocator, testcase_parameters, pp_version):
    network_source = config.create_network_source(ip="localhost", port=port_allocator(), transport='"proxied-tcp"', flags="no-parse")
    file_destination = config.create_file_destination(file_name="output.log", template=TEMPLATE)
    config.create_logpath(statements=[network_source, file_destination])

    syslog_ng.start(config)

    if pp_version == "proxy-protocol-v1":
        network_source.write_log(INPUT_MESSAGES, rate=1)
    else:
        loggen_input_file_path = copy_shared_file(testcase_parameters, "proxy_protocol_v2_input/message0_message1_message2_input")
        loggen.start(
            target=network_source.options["ip"],
            port=network_source.options["port"],
            inet=True,
            stream=True,
            dont_parse=True,
            permanent=True,
            rate=1,
            read_file=loggen_input_file_path,
        )

    # With the current loggen implementation there is no way to properly timing messages.
    # Here I made an assumption that with rate=1, there will be messages which will arrive
    # into syslog-ng AFTER the reload. Timing the reload after the first message arrives.

    # Note: The worst case scenario in case of extreme slowness in the test environment, is
    # that syslog-ng will receive all the messages before reload. In this case the test will
    # not fill it's purpose, and do not test if the headers are reserved between reloads.
    # But at least the test wont be flaky, it will pass in this corner case too.

    assert file_destination.read_log() == EXPECTED_MESSAGE0

    syslog_ng.reload(config)

    assert file_destination.read_log() == EXPECTED_MESSAGE1
    assert file_destination.read_log() == EXPECTED_MESSAGE2
