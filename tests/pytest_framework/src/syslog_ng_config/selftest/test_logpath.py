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
from src.syslog_ng_config.logpath import LogPaths

class FakeSrc:
    def get_statement_id(self):
        return "src_123"

class FakeSrc2:
    def get_statement_id(self):
        return "src_456"

class FakeDst:
    def get_statement_id(self):
        return "dst_123"

class FakeDst2:
    def get_statement_id(self):
        return "dst_456"

def test_register_logpath_node():
    logpath = LogPaths()
    syslog_ng_config = {"logpaths": {}}
    logpath.register_logpath_node(root_node=syslog_ng_config["logpaths"], sources=[FakeSrc()], destinations=[FakeDst()])
    assert syslog_ng_config == {
        'logpaths': {
            logpath.node_id: {
                'flags': [],
                'sources': ['src_123'],
                'destinations': ['dst_123'],
                'filters': [],
                'templates': [],
                'rewrites': []
            }
        }
    }

def test_add_sources():
    logpath = LogPaths()
    syslog_ng_config = {"logpaths": {}}
    logpath.register_logpath_node(root_node=syslog_ng_config["logpaths"], sources=[FakeSrc()], destinations=[FakeDst()])
    logpath.add_sources(sources=[FakeSrc2()])
    assert syslog_ng_config == {
        'logpaths': {
            logpath.node_id: {
                'flags': [],
                'sources': ['src_123', 'src_456'],
                'destinations': ['dst_123'],
                'filters': [],
                'templates': [],
                'rewrites': []
            }
        }
    }


def test_add_destinations():
    logpath = LogPaths()
    syslog_ng_config = {"logpaths": {}}
    logpath.register_logpath_node(root_node=syslog_ng_config["logpaths"], sources=[FakeSrc()], destinations=[FakeDst()])
    logpath.add_destinations(destinations=[FakeDst2()])
    assert syslog_ng_config == {
        'logpaths': {
            logpath.node_id: {
                'flags': [],
                'sources': ['src_123'],
                'destinations': ['dst_123', 'dst_456'],
                'filters': [],
                'templates': [],
                'rewrites': []
            }
        }
    }

# def test_add_flags():
#     logpath = LogPaths()
#
# def test_update_logpath_statement_list():
#     logpath = LogPaths()
