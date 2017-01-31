#!/bin/bash -xe
#############################################################################
# Copyright (c) 2009-2016 Balabit
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

git clone https://github.com/balabit/syslog-ng.git
cd /syslog-ng
pip install -r requirements.txt
./autogen.sh
mkdir build
cd /syslog-ng/build
../configure --enable-debug --with-jsonc=internal --with-mongoc=internal --with-librabbitmq-client=internal --with-ivykis=internal --prefix=/install
make V=1
make install
make check
