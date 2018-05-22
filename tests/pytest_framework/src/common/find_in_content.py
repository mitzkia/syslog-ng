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

import re

def is_number_of_occurences_in_content(regexp, content, counter=1):
    regexp_pattern = re.compile(regexp)
    return counter == len(list(filter(regexp_pattern.match, content.splitlines(True))))

def grep_in_content(regexp, content):
    regexp_pattern = re.compile(regexp)
    for content_line in content.splitlines(True):
        if re.search(regexp_pattern, content_line) is not None:
            return content_line
    return None
