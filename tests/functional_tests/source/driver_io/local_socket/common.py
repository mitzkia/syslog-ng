import socket
import psutil
from source.testdb.common.common import wait_till_function_not_true


class LocalSocketCommon(object):
    def __init__(self, testdb_logger):
        self.testdb_logger = testdb_logger
        self.log_writer = testdb_logger.set_logger("LocalSocketCommon")

    def generate_socket_for_type(self, driver_name):
        if driver_name in ["tcp", "network", "syslog"]:
            return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif driver_name in ["tcp6"]:
            return socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        elif driver_name in ["udp"]:
            return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        elif driver_name in ["udp6"]:
            return socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        elif driver_name in ["unix-stream"]:
            return socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        elif driver_name in ["unix-dgram"]:
            return socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    def is_socket_already_used(self, client_address):
        for psutil_socket in psutil.net_connections('all'):
            if psutil_socket.laddr == client_address:
                self.log_writer.error("Checking socket usage, socket is already used. client address: [%s], self object id: [%s]" % (str(client_address), hex(id(self))))
                return True
        self.log_writer.info("Checking socket usage, socket is not used yet. client address: [%s], self object id: [%s]" % (str(client_address), hex(id(self))))
        return False

    def get_socket_status(self, client_address):
        for psutil_socket in psutil.net_connections('all'):
            if psutil_socket.laddr == client_address:
                self.log_writer.info("Reporting socket status, client address: [%s], status: [%s]" % (client_address, psutil_socket))
                return psutil_socket.status
        self.log_writer.error("Reporting socket status, Socket is not used. client address: [%s]" % str(client_address))
        return False

    def is_socket_state_established(self, client_address):
        return self.get_socket_status(client_address) == "ESTABLISHED"

    def is_socket_state_listening(self, client_address):
        return self.get_socket_status(client_address) == "LISTEN"

    def is_socket_state_none(self, client_address):
        return self.get_socket_status(client_address) == "NONE"

    def wait_for_socket_listening(self, driver_name, client_address):
        self.log_writer.info("Wait for socket listening, socket type [%s], client address: [%s]" % (driver_name, client_address))
        if driver_name in ["udp", "udp6", "unix-stream", "unix-dgram"]:
            socket_listening_result = wait_till_function_not_true(self.is_socket_state_none, client_address, monitoring_time=1)
            self.testdb_logger.write_message_based_on_value(logsource=self.log_writer, message="Socket [%s] with client address [%s] listening result" % (driver_name, client_address), value=socket_listening_result)
            if not socket_listening_result:
                assert False
        else:
            socket_listening_result = wait_till_function_not_true(self.is_socket_state_listening, client_address, monitoring_time=1)
            self.testdb_logger.write_message_based_on_value(logsource=self.log_writer, message="Socket [%s] with client address [%s] listening result" % (driver_name, client_address), value=socket_listening_result)
            if not socket_listening_result:
                assert False
