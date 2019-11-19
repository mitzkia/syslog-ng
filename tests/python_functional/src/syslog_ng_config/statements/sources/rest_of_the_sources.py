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

from src.syslog_ng_config.statements.statement_option_handler import StatementOptionHandler
from src.syslog_ng_config.statements.sources.source_driver import SourceDriver


# File Based
class PipeSource(SourceDriver):
    def __init__(self, file_name, **options):
        self.driver_name = "pipe"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["file_name"])
        self.set_path(file_name)

        super(PipeSource, self).__init__(option_handler=self.option_handler)

    def set_path(self, new_file_name):
        self.option_handler.set_path(new_file_name, "input")

    def get_path(self):
        return self.option_handler.get_positional_option_values()[0]


class ProgramSource(SourceDriver):
    def __init__(self, file_name, **options):
        self.driver_name = "program"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["file_name"])
        self.set_path(file_name)

        super(ProgramSource, self).__init__(option_handler=self.option_handler)

    def set_path(self, new_file_name):
        self.option_handler.set_path(new_file_name, "input")

    def get_path(self):
        return self.option_handler.get_positional_option_values()[0]


class WildcardFileSource(SourceDriver):
    def __init__(self, base_dir, filename_pattern, **options):
        self.driver_name = "wildcard_file"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["base_dir", "filename_pattern"], mandatory=True, driver_io=False, positional=False)
        self.set_base_dir(base_dir)
        self.set_filename_pattern(filename_pattern)

        super(WildcardFileSource, self).__init__(option_handler=self.option_handler)

    def set_base_dir(self, new_base_dir):
        self.option_handler.set_base_dir(new_base_dir)

    def set_filename_pattern(self, new_filename_pattern):
        self.option_handler.set_filename_pattern(new_filename_pattern)


# Local Socket Based
class TcpSource(SourceDriver):
    def __init__(self, port_allocator, ip, port, **options):
        self.driver_name = "tcp"
        self.port_allocator = port_allocator
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["ip", "port"], mandatory=True, driver_io=True, positional=False)
        self.set_ip(ip)
        self.set_port(port)

        super(TcpSource, self).__init__(option_handler=self.option_handler)

    def set_ip(self, new_ip):
        self.option_handler.set_ip(new_ip)

    def set_port(self, new_port):
        self.option_handler.set_port(self.port_allocator, new_port)


class Tcp6Source(SourceDriver):
    def __init__(self, port_allocator, ip, port, **options):
        self.driver_name = "tcp6"
        self.port_allocator = port_allocator
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["ip", "port"], mandatory=True, driver_io=True, positional=False)
        self.set_ip(ip)
        self.set_port(port)

        super(Tcp6Source, self).__init__(option_handler=self.option_handler)

    def set_ip(self, new_ip):
        self.option_handler.set_ip(new_ip, ipversion=6)

    def set_port(self, new_port):
        self.option_handler.set_port(self.port_allocator, new_port)


class NetworkSource(SourceDriver):
    def __init__(self, port_allocator, ip, port, **options):
        self.driver_name = "network"
        self.port_allocator = port_allocator
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["ip", "port"], mandatory=True, driver_io=True, positional=False)
        self.set_ip(ip)
        self.set_port(port)

        super(NetworkSource, self).__init__(option_handler=self.option_handler)

    def set_ip(self, new_ip):
        self.option_handler.set_ip(new_ip)

    def set_port(self, new_port):
        self.option_handler.set_port(self.port_allocator, new_port)


class SyslogSource(SourceDriver):
    def __init__(self, port_allocator, ip, port, **options):
        self.driver_name = "syslog"
        self.port_allocator = port_allocator
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["ip", "port"], mandatory=True, driver_io=True, positional=False)
        self.set_ip(ip)
        self.set_port(port)

        super(SyslogSource, self).__init__(option_handler=self.option_handler)

    def set_ip(self, new_ip):
        self.option_handler.set_ip(new_ip)

    def set_port(self, new_port):
        self.option_handler.set_port(self.port_allocator, new_port)


class UdpSource(SourceDriver):
    def __init__(self, port_allocator, ip, port, **options):
        self.driver_name = "udp"
        self.port_allocator = port_allocator
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["ip", "port"], mandatory=True, driver_io=True, positional=False)
        self.set_ip(ip)
        self.set_port(port)

        super(UdpSource, self).__init__(option_handler=self.option_handler)

    def set_ip(self, new_ip):
        self.option_handler.set_ip(new_ip)

    def set_port(self, new_port):
        self.option_handler.set_port(self.port_allocator, new_port)


class Udp6Source(SourceDriver):
    def __init__(self, port_allocator, ip, port, **options):
        self.driver_name = "udp6"
        self.port_allocator = port_allocator
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["ip", "port"], mandatory=True, driver_io=True, positional=False)
        self.set_ip(ip)
        self.set_port(port)

        super(Udp6Source, self).__init__(option_handler=self.option_handler)

    def set_ip(self, new_ip):
        self.option_handler.set_ip(new_ip, ipversion=6)

    def set_port(self, new_port):
        self.option_handler.set_port(self.port_allocator, new_port)


class UnixStreamSource(SourceDriver):
    def __init__(self, file_name, **options):
        self.driver_name = "unix_stream"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["file_name"])
        self.set_socket_path(file_name)

        super(UnixStreamSource, self).__init__(option_handler=self.option_handler)

    def set_socket_path(self, new_file_name):
        self.option_handler.set_socket_path(new_file_name, "input")


class UnixDgramSource(SourceDriver):
    def __init__(self, file_name, **options):
        self.driver_name = "unix_dgram"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["file_name"])
        self.set_socket_path(file_name)

        super(UnixDgramSource, self).__init__(option_handler=self.option_handler)

    def set_socket_path(self, new_file_name):
        self.option_handler.set_socket_path(new_file_name, "input")


# Language Bindings
class PythonFetcherSource(SourceDriver):
    def __init__(self, class_uri, class_package_path, **options):
        self.driver_name = "python_fetcher"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["class"], mandatory=True, driver_io=False, positional=False)
        self.set_class_path(class_uri, class_package_path)

        super(PythonFetcherSource, self).__init__(option_handler=self.option_handler)

    def set_class_path(self, new_class_uri, new_class_package_path):
        self.option_handler.set_python_fetcher_class_path(new_class_uri, new_class_package_path)


class PythonSource(SourceDriver):
    def __init__(self, class_uri, class_package_path, **options):
        self.driver_name = "python"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["class"], mandatory=True, driver_io=False, positional=False)
        self.set_class_path(class_uri, class_package_path)

        super(PythonSource, self).__init__(option_handler=self.option_handler)

    def set_class_path(self, new_class_uri, new_class_package_path):
        self.option_handler.set_python_class_path(new_class_uri, new_class_package_path)


# Other
class SystemdJournalSource(SourceDriver):
    def __init__(self, **options):
        self.driver_name = "systemd_journal"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)

        super(SystemdJournalSource, self).__init__(option_handler=self.option_handler)


class DiskqSourceSource(SourceDriver):
    def __init__(self, file, **options):
        self.driver_name = "example_diskq_source"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["file"], mandatory=True, driver_io=True, positional=False)
        self.set_path(file)

        super(DiskqSourceSource, self).__init__(option_handler=self.option_handler)

    def set_path(self, new_file_name):
        self.option_handler.set_path(new_file_name, "input")


class RandomGeneratorSource(SourceDriver):
    def __init__(self, bytes, **options):
        self.driver_name = "example_random_generator"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["bytes"], mandatory=True, driver_io=False, positional=False)
        self.set_bytes(bytes)

        super(RandomGeneratorSource, self).__init__(option_handler=self.option_handler)

    def set_bytes(self, new_bytes):
        self.option_handler.set_bytes(new_bytes)


class StdinSource(SourceDriver):
    def __init__(self, **options):
        self.driver_name = "stdin"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)

        super(StdinSource, self).__init__(option_handler=self.option_handler)


# SCL
class DefaultNetworkDrivers(SourceDriver):
    def __init__(self, port_allocator, upd_port, tcp_port, rfc5424_tcp_port, **options):
        self.driver_name = "default_network_drivers"
        self.port_allocator = port_allocator
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["udp_port", "tcp_port", "rfc5424_tcp_port"], mandatory=True, driver_io=True, positional=False)
        self.set_udp_port(upd_port)
        self.set_tcp_port(tcp_port)
        self.set_rfc5424_tcp_port(rfc5424_tcp_port)

        super(DefaultNetworkDrivers, self).__init__(option_handler=self.option_handler)

    def set_udp_port(self, new_upd_port):
        self.option_handler.set_port(self.port_allocator, new_upd_port, "udp_port")

    def set_tcp_port(self, new_tcp_port):
        self.option_handler.set_port(self.port_allocator, new_tcp_port, "tcp_port")

    def set_rfc5424_tcp_port(self, new_rfc5424_tcp_port):
        self.option_handler.set_port(self.port_allocator, new_rfc5424_tcp_port, "rfc5424_tcp_port")


class LinuxAudit(SourceDriver):
    def __init__(self, **options):
        self.driver_name = "linux_audit"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)

        super(LinuxAudit, self).__init__(option_handler=self.option_handler)


class Mbox(SourceDriver):
    def __init__(self, filename, **options):
        self.driver_name = "mbox"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["filename"], mandatory=True, driver_io=True, positional=False)
        self.set_filename(filename)

        super(Mbox, self).__init__(option_handler=self.option_handler)

    def set_filename(self, new_filename):
        self.option_handler.set_path(new_filename, "input")


class Nodejs(SourceDriver):
    def __init__(self, **options):
        self.driver_name = "nodejs"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)

        super(Nodejs, self).__init__(option_handler=self.option_handler)


class Osquery(SourceDriver):
    def __init__(self, **options):
        self.driver_name = "osquery"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)

        super(Osquery, self).__init__(option_handler=self.option_handler)


class Snmptrap(SourceDriver):
    def __init__(self, filename, **options):
        self.driver_name = "snmptrap"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["filename"], mandatory=True, driver_io=True, positional=False)
        self.set_filename(filename)

        super(Snmptrap, self).__init__(option_handler=self.option_handler)

    def set_filename(self, new_filename):
        self.option_handler.set_path(new_filename, "input")
