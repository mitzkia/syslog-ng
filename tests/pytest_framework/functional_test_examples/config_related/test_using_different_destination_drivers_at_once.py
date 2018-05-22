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

def test_using_different_destination_drivers_at_once(tc):
    config = tc.new_config()
    config.add_global_options({"stats_level": 3})
    file_source = config.get_file_source({"file_path": "input"})
    file_destination = config.get_file_destination({"file_path": "output"})
    pipe_destination = config.get_pipe_destination({"file_path": "pipe-output"})
    config.create_logpath(sources=[file_source], destinations=[file_destination, pipe_destination])

    bsd_message = tc.new_bsd_message().program("random_program1").build()
    file_source.write_message(bsd_message)

    syslog_ng = tc.new_syslog_ng()
    syslog_ng.start(config)

    result = config.read_all_destinations()
    assert result == {
        "file": bsd_message.remove_priority().build().get_message(),
        "pipe": bsd_message.remove_priority().build().get_message()
    }

    all_counters = config.get_all_counters()
    expected_counters = {
        "processed": 1,
        "written": 1,
        "queued": 0,
        "dropped": 0,
        "memory_usage": 0
    }
    assert all_counters == {
        "file": expected_counters,
        "pipe": expected_counters
    }
