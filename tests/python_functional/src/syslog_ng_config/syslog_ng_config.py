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
import copy
import logging
import random

from src.common.operations import cast_to_list
from src.common.random_id import get_unique_id
from src.driver_io.file.file_io import FileIO
from src.syslog_ng_config.renderer import ConfigRenderer
from src.syslog_ng_config.statement_group import StatementGroup
from src.syslog_ng_config.statements.destinations.file_destination import FileDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import AmqpDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import Collectd
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import ElasticsearchHttp
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import Graphite
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import Graylog2
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import HttpDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import JavaDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import KafkaDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import MongodbDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import NetworkDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import NetworkLoadBalancer
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import PipeDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import ProgramDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import PseudofileDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import PythonDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import RedisDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import RiemannDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import Slack
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import SmtpDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import SnmpdestDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import SqlDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import StompDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import SyslogDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import Tcp6Destination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import TcpDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import Telegram
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import Udp6Destination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import UdpDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import UnixDgramDestination
from src.syslog_ng_config.statements.destinations.rest_of_the_destinations import UnixStreamDestination
from src.syslog_ng_config.statements.filters.filter import Filter
from src.syslog_ng_config.statements.logpath.logpath import LogPath
from src.syslog_ng_config.statements.parsers.parser import Parser
from src.syslog_ng_config.statements.sources.example_msg_generator_source import ExampleMsgGeneratorSource
from src.syslog_ng_config.statements.sources.file_source import FileSource
from src.syslog_ng_config.statements.sources.rest_of_the_sources import DefaultNetworkDrivers
from src.syslog_ng_config.statements.sources.rest_of_the_sources import DiskqSourceSource
from src.syslog_ng_config.statements.sources.rest_of_the_sources import LinuxAudit
from src.syslog_ng_config.statements.sources.rest_of_the_sources import Mbox
from src.syslog_ng_config.statements.sources.rest_of_the_sources import NetworkSource
from src.syslog_ng_config.statements.sources.rest_of_the_sources import Nodejs
from src.syslog_ng_config.statements.sources.rest_of_the_sources import Osquery
from src.syslog_ng_config.statements.sources.rest_of_the_sources import PipeSource
from src.syslog_ng_config.statements.sources.rest_of_the_sources import ProgramSource
from src.syslog_ng_config.statements.sources.rest_of_the_sources import PythonFetcherSource
from src.syslog_ng_config.statements.sources.rest_of_the_sources import PythonSource
from src.syslog_ng_config.statements.sources.rest_of_the_sources import RandomGeneratorSource
from src.syslog_ng_config.statements.sources.rest_of_the_sources import Snmptrap
from src.syslog_ng_config.statements.sources.rest_of_the_sources import StdinSource
from src.syslog_ng_config.statements.sources.rest_of_the_sources import SyslogSource
from src.syslog_ng_config.statements.sources.rest_of_the_sources import SystemdJournalSource
from src.syslog_ng_config.statements.sources.rest_of_the_sources import Tcp6Source
from src.syslog_ng_config.statements.sources.rest_of_the_sources import TcpSource
from src.syslog_ng_config.statements.sources.rest_of_the_sources import Udp6Source
from src.syslog_ng_config.statements.sources.rest_of_the_sources import UdpSource
from src.syslog_ng_config.statements.sources.rest_of_the_sources import UnixDgramSource
from src.syslog_ng_config.statements.sources.rest_of_the_sources import UnixStreamSource
from src.syslog_ng_config.statements.sources.rest_of_the_sources import WildcardFileSource

logger = logging.getLogger(__name__)


class SyslogNgConfig(object):
    def __init__(self, version):
        self.__raw_config = None
        self.__syslog_ng_config = {
            "version": version,
            "includes": [],
            "global_options": {},
            "statement_groups": [],
            "logpath_groups": [],
        }
        self.randoms = []
        self.port_allocator = PortAllocator()

    @staticmethod
    def stringify(s):
        return '"' + s.replace('\\', "\\\\").replace('"', '\\"').replace('\n', '\\n') + '"'

    def set_raw_config(self, raw_config):
        self.__raw_config = raw_config

    def write_config(self, config_path):
        if self.__raw_config:
            rendered_config = self.__raw_config
        else:
            rendered_config = ConfigRenderer(self.__syslog_ng_config).get_rendered_config()
        logger.info("Generated syslog-ng config\n{}\n".format(rendered_config))
        FileIO(config_path).rewrite(rendered_config)

    def set_version(self, version):
        self.__syslog_ng_config["version"] = version

    def get_version(self):
        return self.__syslog_ng_config["version"]

    def add_include(self, include):
        self.__syslog_ng_config["includes"].append(include)

    def update_global_options(self, **options):
        self.__syslog_ng_config["global_options"].update(options)

    def create_dummy_source(self):
        options = {}
        return FileSource(file_name=None, **options)

    def create_dummy_destination(self):
        options = {}
        return FileDestination(file_name=None, **options)

    def create_file_source(self, file_name=None, **options):
        return FileSource(file_name, **options)

    def create_fifo_source(self, file_name=None, **options):
        return PipeSource(file_name, **options)

    def create_pipe_source(self, file_name=None, **options):
        return PipeSource(file_name, **options)

    def create_stdin_source(self, **options):
        return StdinSource(**options)

    def create_wildcard_file_source(self, base_dir=None, filename_pattern=None, **options):
        return WildcardFileSource(base_dir, filename_pattern, **options)

    def create_example_msg_generator_source(self, **options):
        return ExampleMsgGeneratorSource(**options)

    def create_python_fetcher_source(self, class_uri=None, class_package_path=None, **options):
        return PythonFetcherSource(class_uri, class_package_path, **options)

    def create_tcp_source(self, ip=None, port=None, **options):
        return TcpSource(self.port_allocator, ip, port, **options)

    def create_unix_stream_source(self, file_name=None, **options):
        return UnixStreamSource(file_name, **options)

    def create_network_source(self, ip=None, port=None, **options):
        return NetworkSource(self.port_allocator, ip, port, **options)

    def create_udp_source(self, ip=None, port=None, **options):
        return UdpSource(self.port_allocator, ip, port, **options)

    def create_tcp6_source(self, ip=None, port=None, **options):
        return Tcp6Source(self.port_allocator, ip, port, **options)

    def create_example_diskq_source_source(self, file=None, **options):
        return DiskqSourceSource(file, **options)

    def create_unix_dgram_source(self, file_name=None, **options):
        return UnixDgramSource(file_name, **options)

    def create_python_source(self, class_uri=None, class_package_path=None, **options):
        return PythonSource(class_uri, class_package_path, **options)

    def create_systemd_journal_source(self, **options):
        return SystemdJournalSource(**options)

    def create_program_source(self, file_name=None, **options):
        return ProgramSource(file_name, **options)

    def create_udp6_source(self, ip=None, port=None, **options):
        return Udp6Source(self.port_allocator, ip, port, **options)

    def create_syslog_source(self, ip=None, port=None, **options):
        return SyslogSource(self.port_allocator, ip, port, **options)

    def create_example_random_generator_source(self, bytes=None, **options):
        return RandomGeneratorSource(bytes, **options)

    def create_default_network_drivers_source(self, upd_port=None, tcp_port=None, rfc5424_tcp_port=None, **options):
        return DefaultNetworkDrivers(self.port_allocator, upd_port, tcp_port, rfc5424_tcp_port, **options)

    def create_linux_audit_source(self, **options):
        return LinuxAudit(**options)

    def create_mbox_source(self, filename=None, **options):
        return Mbox(filename, **options)

    def create_nodejs_source(self, **options):
        return Nodejs(**options)

    def create_osquery_source(self, **options):
        return Osquery(**options)

    def create_snmptrap_source(self, filename=None, **options):
        return Snmptrap(filename, **options)

    def create_filter(self, **options):
        return Filter(**options)

    def create_app_parser(self, **options):
        return Parser("app-parser", **options)

    def create_syslog_parser(self, **options):
        return Parser("syslog-parser", **options)

    def create_file_destination(self, file_name=None, **options):
        return FileDestination(file_name, **options)

    def create_fifo_destination(self, file_name=None, **options):
        return PipeDestination(file_name, **options)

    def create_pipe_destination(self, file_name=None, **options):
        return PipeDestination(file_name, **options)

    def create_pseudofile_destination(self, file_name=None, template=None, **options):
        return PseudofileDestination(file_name, template, **options)

    def create_amqp_destination(self, username=None, password=None, **options):
        return AmqpDestination(username, password, **options)

    def create_smtp_destination(self, sender=None, to=None, subject=None, body=None, **options):
        return SmtpDestination(sender, to, subject, body, **options)

    def create_kafka_c_destination(self, topic=None, **options):
        return KafkaDestination(topic, **options)

    def create_udp_destination(self, ip=None, port=None, **options):
        return UdpDestination(self.port_allocator, ip, port, **options)

    def create_java_destination(self, **options):
        return JavaDestination(**options)

    def create_sql_destination(self, columns=None, values=None, **options):
        return SqlDestination(columns, values, **options)

    def create_mongodb_destination(self, host=None, port=None, **options):
        return MongodbDestination(host, port, **options)

    def create_redis_destination(self, command=None, host=None, port=None, **options):
        return RedisDestination(command, host, port, **options)

    def create_program_destination(self, file_name=None, **options):
        return ProgramDestination(file_name, **options)

    def create_python_destination(self, class_uri=None, class_package_path=None, **options):
        return PythonDestination(class_uri, class_package_path, **options)

    def create_tcp6_destination(self, ip=None, port=None, **options):
        return Tcp6Destination(self.port_allocator, ip, port, **options)

    def create_tcp_destination(self, ip=None, port=None, **options):
        return TcpDestination(self.port_allocator, ip, port, **options)

    def create_stomp_destination(self, **options):
        return StompDestination(**options)

    def create_unix_stream_destination(self, file_name=None, **options):
        return UnixStreamDestination(file_name, **options)

    def create_riemann_destination(self, server=None, port=None, **options):
        return RiemannDestination(server, port, **options)

    def create_udp6_destination(self, ip=None, port=None, **options):
        return Udp6Destination(self.port_allocator, ip, port, **options)

    def create_network_destination(self, ip=None, port=None, **options):
        return NetworkDestination(self.port_allocator, ip, port, **options)

    def create_snmp_destination(self, host=None, **options):
        return SnmpdestDestination(host, **options)

    def create_http_destination(self, **options):
        return HttpDestination(**options)

    def create_syslog_destination(self, ip=None, port=None, **options):
        return SyslogDestination(self.port_allocator, ip, port, **options)

    def create_unix_dgram_destination(self, file_name=None, **options):
        return UnixDgramDestination(file_name, **options)

    def create_collectd_destination(self, plugin=None, type=None, **options):
        return Collectd(plugin, type, **options)

    def create_elasticsearch_http_destination(self, url=None, index=None, type=None, timeout=None, **options):
        return ElasticsearchHttp(url, index, type, timeout, **options)

    def create_graphite_destination(self, **options):
        return Graphite(**options)

    def create_graylog2_destination(self, **options):
        return Graylog2(**options)

    def create_network_load_balancer_destination(self, targets=None, **options):
        return NetworkLoadBalancer(targets, **options)

    def create_slack_destination(self, hook_url=None, timeout=None, **options):
        return Slack(hook_url, timeout, **options)

    def create_telegram_destination(self, bot_id=None, chat_id=None, timeout=None, **options):
        return Telegram(bot_id, chat_id, timeout, **options)

    def create_logpath(self, statements=None, flags=None):
        logpath = self.__create_logpath_with_conversion(statements, flags)
        self.__syslog_ng_config["logpath_groups"].append(logpath)
        return logpath

    def create_inner_logpath(self, statements=None, flags=None):
        inner_logpath = self.__create_logpath_with_conversion(statements, flags)
        return inner_logpath

    def create_statement_group(self, statements):
        statement_group = StatementGroup(statements)
        self.__syslog_ng_config["statement_groups"].append(statement_group)
        return statement_group

    def __create_statement_group_if_needed(self, item):
        if isinstance(item, (StatementGroup, LogPath)):
            return item
        else:
            return self.create_statement_group(item)

    def __create_logpath_with_conversion(self, items, flags):
        return self.__create_logpath_group(map(self.__create_statement_group_if_needed, cast_to_list(items)), flags)

    @staticmethod
    def __create_logpath_group(statements=None, flags=None):
        logpath = LogPath()
        if statements:
            logpath.add_groups(statements)
        if flags:
            logpath.add_flags(cast_to_list(flags))
        return logpath

    def create_source_by_name(self, driver_name, custom_option_list):
        return self.create_statement_by_name("source", driver_name, custom_option_list)

    def create_destination_by_name(self, driver_name, custom_option_list):
        return self.create_statement_by_name("destination", driver_name, custom_option_list)

    def create_statement_by_name(self, driver_type, driver_name, custom_option_list):
        copied_option_values = copy.deepcopy(custom_option_list)
        if copied_option_values and "positional" in copied_option_values:
            positional_value = copied_option_values["positional"]
            created_driver = getattr(self, "create_{}_{}".format(driver_name, driver_type))(positional_value)
        elif copied_option_values and "positional" not in copied_option_values:
            created_driver = getattr(self, "create_{}_{}".format(driver_name, driver_type))(**copied_option_values)
        else:
            created_driver = getattr(self, "create_{}_{}".format(driver_name, driver_type))()
        return created_driver

    def generate_uniq_persist_name_for_driver(self, driver):
        if "persist_name" not in driver.options:
            driver.options.update({"persist_name": "{}_{}_{}".format(driver.group_type, driver.driver_name, get_unique_id())})

    def create_log_statements_for_various_sources(self, driver_name, constructed_option):
        src = self.create_source_by_name(driver_name, constructed_option)
        self.generate_uniq_persist_name_for_driver(src)
        dst = self.create_file_destination()
        self.create_logpath(statements=[src, dst])
        return src, dst

    def create_log_statements_for_various_destinations(self, driver_name, constructed_option):
        src = self.create_file_source()
        dst = self.create_destination_by_name(driver_name, constructed_option)
        self.generate_uniq_persist_name_for_driver(dst)
        self.create_logpath(statements=[src, dst])
        return src, dst

    def filter_driver(self, driver_name):
        filtered_driver_list = ["openbsd", "sun_stream", "sun_streams", "pacct", "systemd_syslog"]  # sources
        filtered_driver_list += ['elasticsearch2', 'hdfs', 'kafka_java', 'loggly', 'logmatic']  # destinations

        if driver_name in filtered_driver_list:
            raise FilteredDriver

    def create_multidriver_config(self, parent_drivers, driver_type, constructed_option=None):
        self.add_include("scl.conf")
        for driver_name in parent_drivers:
            try:
                self.filter_driver(driver_name)
                if driver_type == "source":
                    src, dst = self.create_log_statements_for_various_sources(driver_name, constructed_option)
                elif driver_type == "destination":
                    src, dst = self.create_log_statements_for_various_destinations(driver_name, constructed_option)
                else:
                    logger.error("Not yet supported driver_type:{}".format(driver_type))
                if src.driver_name == "file":
                    src.write_log("<34>Oct 11 22:14:15 mymachine su: 'su root' failed for lonvick on /dev/pts/8\n", 101)

            except FilteredDriver:
                pass


class FilteredDriver(Exception):
    pass


class PortAllocator(object):
    def __init__(self):
        self.allocated_ports = set()

    def allocate_random_port(self):
        while True:
            random_port = random.randrange(1024, 65535)

            if random_port not in self.allocated_ports:
                self.allocated_ports.add(random_port)
                return random_port

    def allocate_port(self, port):
        self.allocated_ports.add(port)
