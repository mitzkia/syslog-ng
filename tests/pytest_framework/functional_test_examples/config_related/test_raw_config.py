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

from src.driver_io.file.file_io import FileIO
from src.common.find_in_content import is_number_of_occurences_in_content

def test_raw_config(tc):
    config = tc.new_config()
    src_file = tc.new_file_path(prefix="input")
    dst_file = tc.new_file_path(prefix="output")
    syslog_ng = tc.new_syslog_ng()
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
    };""" % (syslog_ng.get_version(), src_file, dst_file, dst_file, dst_file, dst_file, dst_file, dst_file)
    config.set_raw_config(raw_config)

    input_content = """almafa
belafa
celafa
test
belafa magja
belafa termese
belafa levele
"""
    FileIO(tc.logger_factory, file_path=src_file).write(content=input_content)

    syslog_ng.start(config)

    output_messages = FileIO(tc.logger_factory, file_path=dst_file).read()

    assert is_number_of_occurences_in_content("^>>>>ALMA<<<<.*almafa$", output_messages) is True
    assert is_number_of_occurences_in_content("^>>>>BELA MAG<<<<.*belafa magja$", output_messages) is True
    assert is_number_of_occurences_in_content("^>>>>BELA TERMES<<<<.*belafa termese$", output_messages) is True
    assert is_number_of_occurences_in_content("^>>>>BELA LEVEL<<<<.*belafa levele$", output_messages) is True
    assert is_number_of_occurences_in_content("^>>>>CELA<<<<.*celafa$", output_messages) is True
    assert is_number_of_occurences_in_content("^>>>>XXXX<<<<.*test$", output_messages) is True
    assert is_number_of_occurences_in_content("^.*belafa$", output_messages) is False
