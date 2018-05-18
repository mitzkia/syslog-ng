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
from src.driver_io.file_based.file_interface import FileInterface
from src.common.find_in_content import find_regexp_in_content


def test_raw_config(tc):
    fileio = FileInterface(tc.logger_factory)
    config = tc.new_config()
    src_file = tc.new_file_path(prefix="input")
    dst_file = tc.new_file_path(prefix="output")
    raw_config = """@version: %s
    log {
        source { file("%s" flags(no-parse) ); };
        if (message("almafa")) {
                destination { file("%s" persist-name('aaa') template(">>>>ALMA<<<< $ISODATE $HOST $MSGHDR$MSG\n")); };
        } elif (message("belafa")) {
                if (message("magja")) {
                        destination { file("%s" persist-name('bbb1') template(">>>>BELA MAG<<<< $ISODATE $HOST $MSGHDR$MSG\n")); };
                } elif (message("termese")) {
                        destination { file("%s" persist-name('bbb2') template(">>>>BELA TERMES<<<< $ISODATE $HOST $MSGHDR$MSG\n")); };
                } elif (message("levele")) {
                        destination { file("%s" persist-name('bbb3') template(">>>>BELA LEVEL<<<< $ISODATE $HOST $MSGHDR$MSG\n")); };
                };
        } elif (message("celafa")) {
                destination { file("%s" persist-name('ccc') template(">>>>CELA<<<< $ISODATE $HOST $MSGHDR$MSG\n")); };
        } else {
                destination { file("%s" persist-name('xxx') template(">>>>XXXX<<<< $ISODATE $HOST $MSGHDR$MSG\n")); };
        };
    };""" % (
        config.syslog_ng_version, src_file, dst_file, dst_file, dst_file, dst_file, dst_file, dst_file
    )
    config.set_raw_config(raw_config)

    fileio.write_content(file_path=src_file, content="almafa")
    fileio.write_content(file_path=src_file, content="belafa")
    fileio.write_content(file_path=src_file, content="celafa")
    fileio.write_content(file_path=src_file, content="test")
    fileio.write_content(file_path=src_file, content="belafa magja")
    fileio.write_content(file_path=src_file, content="belafa termese")
    fileio.write_content(file_path=src_file, content="belafa levele")

    syslog_ng = tc.new_syslog_ng()
    syslog_ng.start(config)

    dst_file_messages = fileio.read_content(file_path=dst_file, expected_message_counter=6)

    dst_file_content = "".join(dst_file_messages)
    assert find_regexp_in_content("^>>>>ALMA<<<<.*almafa$", dst_file_content) is True
    assert find_regexp_in_content("^>>>>BELA MAG<<<<.*belafa magja$", dst_file_content) is True
    assert find_regexp_in_content("^>>>>BELA TERMES<<<<.*belafa termese$", dst_file_content) is True
    assert find_regexp_in_content("^>>>>BELA LEVEL<<<<.*belafa levele$", dst_file_content) is True
    assert find_regexp_in_content("^>>>>CELA<<<<.*celafa$", dst_file_content) is True
    assert find_regexp_in_content("^>>>>XXXX<<<<.*test$", dst_file_content) is True
    assert find_regexp_in_content("^.*belafa$", dst_file_content) is False
