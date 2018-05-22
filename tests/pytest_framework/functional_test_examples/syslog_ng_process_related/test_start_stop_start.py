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

def test_start_reload_stop_start(tc):
    config = tc.new_config()
    file_source = config.get_file_source({"file_path": "input"})
    file_destination = config.get_file_destination({"file_path": "output"})
    config.create_logpath(sources=[file_source], destinations=[file_destination])

    bsd_message = tc.new_bsd_message().build()
    file_source.write_message(bsd_message)

    syslog_ng = tc.new_syslog_ng()
    syslog_ng.start(config)

    file_source.write_message(bsd_message)

    syslog_ng.reload()
    syslog_ng.stop()

    file_source.write_message(bsd_message)

    syslog_ng.start()

    message_counter = 3
    output_messages = file_destination.read_all_messages()
    expected_output_messages = bsd_message.remove_priority().build(message_counter)
    assert output_messages == expected_output_messages[0].get_messages(message_counter)
