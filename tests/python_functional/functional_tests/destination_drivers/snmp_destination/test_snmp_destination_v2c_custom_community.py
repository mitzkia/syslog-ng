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


CISCO_TIMETICKS = '97881'

OBJ_OID = "1.3.6.1.4.1.2682.1.4.5.1.1.99.1.1.6"
TRAP_OID = "1.3.6.1.6.3.1.1.4.1.0"
TRAP_DATA = "1.3.6.1.4.1.9.9.41.2.0.1"

input_log = "<38>Feb 11 21:27:22 testhost testprogram[9999]: test message\n"
expected_logs = [
    '.{} = Timeticks: ({}) 0:16:18.81'.format(OBJ_OID, CISCO_TIMETICKS),
    '.{} = OID: .{}'.format(TRAP_OID, TRAP_DATA),
]


@pytest.mark.snmp
def test_snmp_dest_v2_custom_community(config, syslog_ng, snmptrapd):
    # create source driver config
    file_source = config.create_file_source(file_name="input.log")

    # create destination driver config
    snmp_objs = (
        "'{}','Timeticks','{}'".format(OBJ_OID, CISCO_TIMETICKS),
    )

    trap_obj = "'.{}','Objectid','{}'".format(TRAP_OID, TRAP_DATA)

    snmp_destination = config.create_snmp_destination(
        host="'127.0.0.1'",
        port=snmptrapd.get_port(),
        version="'v2c'",
        snmp_obj=snmp_objs,
        trap_obj=trap_obj,
        community="'testcommunity'",
    )

    config.create_logpath(statements=[file_source, snmp_destination])
    config.update_global_options(keep_hostname="yes")
    file_source.write_log(input_log)

    syslog_ng.start(config)

    received_traps = snmptrapd.get_traps()
    for exp_log in expected_logs:
        assert exp_log in received_traps
