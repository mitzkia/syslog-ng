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


def test_snmp_destination_acceptance(config, syslog_ng):
    dummy_source = config.create_dummy_source()
    snmp_options = [
        {"version": "v2c"},
        {"host": "192.168.1.1"},
        {"trap-obj": "'.1.3.6.1.6.3.1.1.4.1.0', 'Objectid', '.1.3.6.1.4.1.18372.3.1.1.1.2.1'"},
        {"snmp-obj": "'.1.3.6.1.4.1.18372.3.1.1.1.1.1.0', 'Octetstring', 'Test SNMP trap'"},
        {"snmp-obj": "'.1.3.6.1.4.1.18372.3.1.1.1.1.2.0', 'Octetstring', 'admin'"},
        {"snmp-obj": "'.1.3.6.1.4.1.18372.3.1.1.1.1.3.0', 'Ipaddress', '192.168.1.1'"},
    ]
    snmp_destination = config.create_snmp_destination(options=snmp_options)

    config.create_logpath(statements=[dummy_source, snmp_destination])

    syslog_ng.start(config)
