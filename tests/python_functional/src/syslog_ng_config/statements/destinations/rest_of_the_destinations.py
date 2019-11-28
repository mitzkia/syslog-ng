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
from pathlib2 import Path

from src.syslog_ng_config.statements.destinations.destination_driver import DestinationDriver
from src.syslog_ng_config.statements.statement_option_handler import StatementOptionHandler
#
# import src.testcase_parameters.testcase_parameters as tc_parameters
# from src.common.operations import copy_shared_file
#
# from src.syslog_ng_config.statements.option_handlers.basic import BasicOptionHandler
# from src.syslog_ng_config.statements.option_handlers.path_based import StatementOptionHandler(self.options)
# from src.syslog_ng_config.statements.option_handlers.path_based import get_working_dir_for_driver
# from src.syslog_ng_config.statements.option_handlers.path_based import OptionPathHandler


DEFAULT_REMOTE_HOST_ADDRESS = DEFAULT_LOCALHOST_ADDRESS = "127.0.0.1"
DEFAULT_LOCALHOST_IPV6_ADDRESS = "::1"


# File Based
class PipeDestination(DestinationDriver):
    def __init__(self, file_name, **options):
        self.driver_name = "pipe"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["file_name"])
        self.set_path(file_name)

        super(PipeDestination, self).__init__(option_handler=self.option_handler)

    def set_path(self, new_file_name):
        self.option_handler.set_path(new_file_name, "output")

    def get_path(self):
        return self.option_handler.get_positional_option_values()[0]


class ProgramDestination(DestinationDriver):
    def __init__(self, file_name, **options):
        self.driver_name = "program"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["file_name"])
        self.set_path(file_name)

        super(ProgramDestination, self).__init__(option_handler=self.option_handler)

    def set_path(self, new_file_name):
        self.option_handler.set_path(new_file_name, "output")

    def get_path(self):
        return self.option_handler.get_positional_option_values()[0]


class PseudofileDestination(DestinationDriver):
    def __init__(self, file_name, template, **options):
        self.driver_name = "pseudofile"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["file_name"])
        self.option_handler.register_option_list(["template"], mandatory=True, driver_io=False, positional=False)
        self.set_path(file_name)
        self.set_template(template)

        super(PseudofileDestination, self).__init__(option_handler=self.option_handler)

    def set_path(self, new_file_name):
        self.option_handler.set_path(new_file_name, "output")
        Path(self.option_handler.get_path()).touch()

    def set_template(self, new_template):
        self.option_handler.set_template(new_template)


# Local Socket Based
class TcpDestination(DestinationDriver):
    def __init__(self, port_allocator, ip, port, **options):
        self.driver_name = "tcp"
        self.port_allocator = port_allocator
        self.options = options
        self.options["ip"] = DEFAULT_LOCALHOST_ADDRESS
        self.options["port"] = port_allocator.allocate_random_port()

        self.option_handler = StatementOptionHandler()
        self.option_handler.init_options(self.options)
        self.option_handler.set_option_property("ip", is_driverio=True, is_positional=True)

        super(TcpDestination, self).__init__(option_handler=self.option_handler)

    def set_ip(self, new_ip):
        self.option_handler.set_ip(new_ip)

    def set_port(self, new_port):
        self.port_allocator(new_port)


class Tcp6Destination(DestinationDriver):
    def __init__(self, port_allocator, ip, port, **options):
        self.driver_name = "tcp6"
        self.port_allocator = port_allocator
        self.options = options

        self.options["ip"] = DEFAULT_LOCALHOST_IPV6_ADDRESS
        self.options["port"] = port_allocator.allocate_random_port()

        self.option_handler = StatementOptionHandler()
        self.option_handler.init_options(self.options)
        self.option_handler.set_option_property("ip", is_driverio=True, is_positional=True)

        super(Tcp6Destination, self).__init__(option_handler=self.option_handler)

    def set_ip(self, new_ip):
        self.option_handler.set_ip(new_ip, ipversion=6)

    def set_port(self, new_port):
        self.option_handler.set_port(self.port_allocator, new_port)


class NetworkDestination(DestinationDriver):
    def __init__(self, port_allocator, ip, port, **options):
        self.driver_name = "network"
        self.port_allocator = port_allocator
        self.options = options

        self.options["ip"] = DEFAULT_LOCALHOST_ADDRESS
        self.options["port"] = port_allocator.allocate_random_port()

        self.option_handler = StatementOptionHandler()
        self.option_handler.init_options(self.options)
        self.option_handler.set_option_property("ip", is_driverio=True, is_positional=True)

        super(NetworkDestination, self).__init__(option_handler=self.option_handler)

    def set_ip(self, new_ip):
        self.option_handler.set_ip(new_ip)

    def set_port(self, new_port):
        self.option_handler.set_port(self.port_allocator, new_port)


class SyslogDestination(DestinationDriver):
    def __init__(self, port_allocator, ip, port, **options):
        self.driver_name = "syslog"
        self.port_allocator = port_allocator
        self.options = options

        self.options["ip"] = DEFAULT_LOCALHOST_ADDRESS
        self.options["port"] = port_allocator.allocate_random_port()

        self.option_handler = StatementOptionHandler()
        self.option_handler.init_options(self.options)
        self.option_handler.set_option_property("ip", is_driverio=True, is_positional=True)

        super(SyslogDestination, self).__init__(option_handler=self.option_handler)

    def set_ip(self, new_ip):
        self.option_handler.set_ip(new_ip)

    def set_port(self, new_port):
        self.option_handler.set_port(self.port_allocator, new_port)


class UdpDestination(DestinationDriver):
    def __init__(self, port_allocator, ip, port, **options):
        self.driver_name = "udp"
        self.port_allocator = port_allocator
        self.options = options

        self.options["ip"] = DEFAULT_LOCALHOST_ADDRESS
        self.options["port"] = port_allocator.allocate_random_port()

        self.option_handler = StatementOptionHandler()
        self.option_handler.init_options(self.options)
        self.option_handler.set_option_property("ip", is_driverio=True, is_positional=True)

        super(UdpDestination, self).__init__(option_handler=self.option_handler)

    def set_ip(self, new_ip):
        self.option_handler.set_ip(new_ip)

    def set_port(self, new_port):
        self.option_handler.set_port(self.port_allocator, new_port)


class Udp6Destination(DestinationDriver):
    def __init__(self, port_allocator, ip, port, **options):
        self.driver_name = "udp6"
        self.port_allocator = port_allocator
        self.options = options

        self.options["ip"] = DEFAULT_LOCALHOST_IPV6_ADDRESS
        self.options["port"] = port_allocator.allocate_random_port()

        self.option_handler = StatementOptionHandler()
        self.option_handler.init_options(self.options)
        self.option_handler.set_option_property("ip", is_driverio=True, is_positional=True)

        super(Udp6Destination, self).__init__(option_handler=self.option_handler)

    def set_ip(self, new_ip):
        self.option_handler.set_ip(new_ip, ipversion=6)

    def set_port(self, new_port):
        self.option_handler.set_port(self.port_allocator, new_port)


class UnixDgramDestination(DestinationDriver):
    def __init__(self, file_name, **options):
        self.driver_name = "unix_dgram"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["file_name"])
        self.set_socket_path(file_name)

        super(UnixDgramDestination, self).__init__(option_handler=self.option_handler)

    def set_socket_path(self, new_file_name):
        self.option_handler.set_socket_path(new_file_name, "output")


class UnixStreamDestination(DestinationDriver):
    def __init__(self, file_name, **options):
        self.driver_name = "unix_stream"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["file_name"])
        self.set_socket_path(file_name)

        super(UnixStreamDestination, self).__init__(option_handler=self.option_handler)

    def set_socket_path(self, new_file_name):
        self.option_handler.set_socket_path(new_file_name, "output")


# Remote Socket Based
class SnmpdestDestination(DestinationDriver):
    def __init__(self, host, **options):
        self.driver_name = "snmp"
        self.options = options
        # self.options.update({"snmp_obj": "'.1.3.6.1.2.1.1.3.0', 'Timeticks', '97881'"})
        # self.options.update({"trap_obj": "'.1.3.6.1.6.3.1.1.4.1.0','Objectid', '.1.3.6.1.4.1.9.9.41.2.0.1'"})

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["host"], mandatory=True, driver_io=True, positional=False)
        self.set_host(host)

        super(SnmpdestDestination, self).__init__(option_handler=self.option_handler)

    def set_host(self, new_host):
        self.option_handler.set_host(new_host)


class HttpDestination(DestinationDriver):
    def __init__(self, **options):
        self.driver_name = "http"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)

        super(HttpDestination, self).__init__(option_handler=self.option_handler)


class RiemannDestination(DestinationDriver):
    def __init__(self, server, port, **options):
        self.driver_name = "riemann"
        self.options = options
        # self.options.update({"server": "127.0.0.1"})
        # self.options.update({"port": 8881})
        # self.__basic_option_handler = BasicOptionHandler(options=self.options)
        # super(RiemannDestination, self).__init__(self.__basic_option_handler)

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["server", "port"], mandatory=True, driver_io=True, positional=False)

        super(RiemannDestination, self).__init__(option_handler=self.option_handler)


class StompDestination(DestinationDriver):
    def __init__(self, **options):
        self.driver_name = "stomp"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)

        super(StompDestination, self).__init__(option_handler=self.option_handler)


class SqlDestination(DestinationDriver):
    def __init__(self, columns, values, **options):
        self.driver_name = "sql"
        self.options = options

        # if "columns" not in self.options:
        #     self.options.update({"columns": '"message  varchar(300)"'})
        # if "values" not in self.options:
        #     self.options.update({"values": "$MSGONLY"})

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["columns", "values"], mandatory=True, driver_io=True, positional=False)

        super(SqlDestination, self).__init__(option_handler=self.option_handler)


class MongodbDestination(DestinationDriver):
    def __init__(self, host, port, **options):
        self.driver_name = "mongodb"
        self.options = options
        # # nem derul ki a syntax-onlybol
        # self.options.update({"host": "127.0.0.1"})
        # self.options.update({"port": 8888})
        # # pelda uri:mongodb://myDBReader:D1fficultP%40ssw0rd@mongodb0.example.com:27017/admin
        # # self.__basic_option_handler = BasicOptionHandler(options=self.options)
        # # super(MongodbDestination, self).__init__(self.__basic_option_handler)

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["host", "port"], mandatory=True, driver_io=True, positional=False)

        super(MongodbDestination, self).__init__(option_handler=self.option_handler)


class RedisDestination(DestinationDriver):
    def __init__(self, command, host, port, **options):
        self.driver_name = "redis"
        self.options = options

        # self.options.update({"command": '"HINCRBY", "hosts", "$HOST", "1"'})
        # self.options.update({"host": '127.0.0.1'})
        # self.options.update({"port": 5555})

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["command", "host", "port"], mandatory=True, driver_io=True, positional=False)

        super(RedisDestination, self).__init__(option_handler=self.option_handler)


class AmqpDestination(DestinationDriver):
    def __init__(self, host, port, username, password, **options):
        self.driver_name = "amqp"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["host", "port"], mandatory=True, driver_io=True, positional=False)
        self.option_handler.register_option_list(["username", "password"], mandatory=True, driver_io=False, positional=False)

        super(AmqpDestination, self).__init__(option_handler=self.option_handler)

    def set_host(self, new_host):
        pass

    def set_port(self, new_host):
        pass

    def set_username(self, new_host):
        pass

    def set_pass(self, new_host):
        pass


class SmtpDestination(DestinationDriver):
    def __init__(self, sender, to, subject, body, **options):
        self.driver_name = "smtp"
        self.options = options

        # if "sender" not in self.options:
        #     self.options.update({"sender": "'sender@domain.com'"})
        # if "to" not in self.options:
        #     self.options.update({"to": "'to@domain.com'"})
        # if "subject" not in self.options:
        #     self.options.update({"subject": "'test'"})
        # if "body" not in self.options:
        #     self.options.update({"body": "'test'"})

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["sender", "to", "subject", "body"], mandatory=True, driver_io=True, positional=False)

        super(SmtpDestination, self).__init__(option_handler=self.option_handler)


class KafkaDestination(DestinationDriver):
    def __init__(self, topic, **options):
        self.driver_name = "kafka_c"
        self.options = options

        # if "topic" not in self.options:
        #     self.options.update({"topic": '"syslog-ng"'})
        # self.options.update({"flush_timeout_on_shutdown": 1})
        # self.options.update({"flush_timeout_on_reload": 1})

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["topic"], mandatory=True, driver_io=True, positional=False)

        super(KafkaDestination, self).__init__(option_handler=self.option_handler)


# Language Bindings
class JavaDestination(DestinationDriver):
    def __init__(self, **options):
        self.driver_name = "java"
        self.options = options

        # self.options.update(
        #     {
        #         "class_path": '"{}/*.jar"'.format(get_working_dir_for_driver(self.driver_name, tc_parameters)),
        #         "class_name": '"com.balabit.javadestination.TestJavaDestination"',
        #         "option": '"init_return_value", "True"',
        #     }
        # )
        # copy_shared_file(Path("plain-jdst-test.jar"), destination_path=Path("."))
        # os.environ["LD_LIBRARY_PATH"] = "/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server/"
        # os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64/"

        # self.__basic_option_handler = BasicOptionHandler(options=self.options)
        # super(JavaDestination, self).__init__(self.__basic_option_handler)

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["host"], mandatory=True, driver_io=True, positional=False)

        super(JavaDestination, self).__init__(option_handler=self.option_handler)


class PythonDestination(DestinationDriver):
    def __init__(self, class_uri, class_package_path, **options):
        self.driver_name = "python"
        self.options = options
        # self.options.update({"class": "python_destination.PythonDestinationTestClass"})
        # copy_shared_file(Path("python_destination.py"))
        # os.environ["PYTHONPATH"] = str(get_working_dir_for_driver(self.driver_name, tc_parameters))

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["class"], mandatory=True, driver_io=True, positional=False)
        self.set_class_path(class_uri, class_package_path)

        super(PythonDestination, self).__init__(option_handler=self.option_handler)

    def set_class_path(self, new_class_uri, new_class_package_path):
        self.option_handler.set_python_class_path(new_class_uri, new_class_package_path)


# SCL
class Collectd(DestinationDriver):
    def __init__(self, plugin, type, **options):
        self.driver_name = "collectd"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["plugin", "type"], mandatory=True, driver_io=False, positional=False)
        self.set_plugin(plugin)
        self.set_type(type)

        super(Collectd, self).__init__(option_handler=self.option_handler)

    def set_plugin(self, new_plugin):
        self.option_handler.set_plugin(new_plugin)

    def set_type(self, new_type):
        self.option_handler.set_type(new_type)


class ElasticsearchHttp(DestinationDriver):
    def __init__(self, url, index, type, timeout, **options):
        self.driver_name = "elasticsearch_http"
        self.options = options
        # if "url" not in self.options:
        #     self.options.update({"url": "test"})
        # if "index" not in self.options:
        #     self.options.update({"index": "test"})
        # if "type" not in self.options:
        #     self.options.update({"type": "test"})
        # if "timeout" not in self.options:
        #     self.options.update({"timeout": 1})

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["url", "index", "type", "timeout"], mandatory=True, driver_io=True, positional=False)
        self.set_url(url)
        self.set_index(index)
        self.set_type(type)
        self.set_timeout(timeout)

        super(ElasticsearchHttp, self).__init__(option_handler=self.option_handler)


class Graphite(DestinationDriver):
    def __init__(self, **options):
        self.driver_name = "graphite"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)

        super(Graphite, self).__init__(option_handler=self.option_handler)


class Graylog2(DestinationDriver):
    def __init__(self, **options):
        self.driver_name = "graylog2"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)

        super(Graylog2, self).__init__(option_handler=self.option_handler)


class NetworkLoadBalancer(DestinationDriver):
    def __init__(self, targets, **options):
        self.driver_name = "network_load_balancer"
        self.options = options
        # if "targets" not in self.options:
        #     self.options.update({"targets": "127.0.0.1"})

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["targets"], mandatory=True, driver_io=True, positional=False)

        super(NetworkLoadBalancer, self).__init__(option_handler=self.option_handler)


class Slack(DestinationDriver):
    def __init__(self, hook_url, timeout, **options):
        self.driver_name = "slack"
        self.options = options
        # if "hook-url" not in self.options:
        #     self.options.update({"hook-url": "test"})
        # if "timeout" not in self.options:
        #     self.options.update({"timeout": 1})

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["hook_url", "timeout"], mandatory=True, driver_io=True, positional=False)

        super(Slack, self).__init__(option_handler=self.option_handler)


class Telegram(DestinationDriver):
    def __init__(self, bot_id, chat_id, timeout, **options):
        self.driver_name = "telegram"
        self.options = options
        # if "bot_id" not in self.options:
        #     self.options.update({"bot_id": "test"})
        # if "chat_id" not in self.options:
        #     self.options.update({"chat_id": "test"})
        # if "timeout" not in self.options:
        #     self.options.update({"timeout": 1})

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["bot_id", "chat_id", "timeout"], mandatory=True, driver_io=False, positional=False)

        super(Telegram, self).__init__(option_handler=self.option_handler)
