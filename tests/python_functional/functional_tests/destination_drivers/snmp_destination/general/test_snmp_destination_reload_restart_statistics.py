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

from src.helpers.snmptrapd.conftest import *  # noqa:F403, F401

@pytest.mark.snmp
def test_snmp_dest_reload_restart_stat(config, syslog_ng, syslog_ng_ctl, snmptrapd, snmp_test_params):
    input_message_counter = 1
    # example_msg_generator source generates a new message on start
    output_message_counter = 1
    stats_message_counter = 1
    generator_source = config.create_example_msg_generator_source(num=input_message_counter)
    snmp_destination = config.create_snmp_destination(
        host=snmp_test_params.get_ip_address(),
        port=snmptrapd.get_port(),
        snmp_obj=snmp_test_params.get_basic_snmp_obj(),
        trap_obj=snmp_test_params.get_basic_trap_obj()
    )
    config.create_logpath(statements=[generator_source, snmp_destination])

    syslog_ng.start(config)

    received_traps = snmptrapd.get_traps()
    assert received_traps == snmp_test_params.get_expected_basic_trap()
    assert any(snmp_test_params.get_default_community() in line for line in snmptrapd.get_raw_traps())

    assert snmp_destination.get_query() == {'written': stats_message_counter, 'processed': stats_message_counter, 'dropped': 0, 'queued': 0}
    assert snmp_destination.get_stats() == {'written': stats_message_counter, 'processed': stats_message_counter, 'dropped': 0, 'queued': 0}

    syslog_ng.restart(config)
    # example_msg_generator source generates a new message on start (re-start happend)
    output_message_counter = 2 # snmptrapd output file was appended with second message
    stats_message_counter = 1 # new message was registered in stats

    received_traps = snmptrapd.get_traps()
    assert received_traps == output_message_counter * snmp_test_params.get_expected_basic_trap()
    assert any(snmp_test_params.get_default_community() in line for line in snmptrapd.get_raw_traps())

    assert snmp_destination.get_query() == {'written': stats_message_counter, 'processed': stats_message_counter, 'dropped': 0, 'queued': 0}
    assert snmp_destination.get_stats() == {'written': stats_message_counter, 'processed': stats_message_counter, 'dropped': 0, 'queued': 0}

    syslog_ng.reload(config)
    # example_msg_generator source generates a new message on reload
    output_message_counter = 3 # snmptrapd output file was appended with third message
    stats_message_counter = 2 # new message was registered in stats

    received_traps = snmptrapd.get_traps()
    assert received_traps == output_message_counter * snmp_test_params.get_expected_basic_trap()
    assert any(snmp_test_params.get_default_community() in line for line in snmptrapd.get_raw_traps())

    assert snmp_destination.get_query() == {'written': stats_message_counter, 'processed': stats_message_counter, 'dropped': 0, 'queued': 0}
    assert snmp_destination.get_stats() == {'written': stats_message_counter, 'processed': stats_message_counter, 'dropped': 0, 'queued': 0}

