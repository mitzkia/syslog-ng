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


@pytest.mark.snmp
def test_snmp_dest_missing_trap_obj(config, syslog_ng, snmptrapd):
    # create source driver config
    file_source = config.create_file_source(file_name="input.log")

    # create destination driver config
    snmp_objs = (
        "'{}','Timeticks','{}'".format(OBJ_OID, CISCO_TIMETICKS),
    )

    snmp_destination = config.create_snmp_destination(
        host="'127.0.0.1'",
        port=snmptrapd.get_port(),
        version="'v2c'",
        snmp_obj=snmp_objs,
    )

    config.create_logpath(statements=[file_source, snmp_destination])
    config.update_global_options(keep_hostname="yes")

    # syslog/ng shall not start due to missing trap object in configuration
    with pytest.raises(Exception):
        syslog_ng.start(config)
