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
from src.common.find_in_content import find_regexp_in_content


def test_message_payload(tc):
    config = tc.new_config()
    file_source = config.get_file_source({"file_path": "input", "keep_hostname": "yes"})
    file_destination = config.get_file_destination({"file_path": "output"})
    config.create_logpath(sources=[file_source], destinations=[file_destination])

    test_message = "my favorite custom test message"
    file_source.write(test_message)

    syslog_ng = tc.new_syslog_ng()
    syslog_ng.start(config)

    dst_file_messages = file_destination.read()
    dst_file_content = "".join(dst_file_messages)
    assert find_regexp_in_content(".*{}$".format(test_message), dst_file_content) is True
