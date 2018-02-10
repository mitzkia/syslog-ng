import copy
import socket
import time
from src.message.bsd import BSD
from src.message.ietf import IETF


class MessageInterface(object):
    def __init__(self, logger_factory):
        self.logger = logger_factory.create_logger("MessageInterface")
        self.default_bsd_message_parts = {
            "priority": "38",
            "bsd_timestamp": "Jun  1 08:05:04",
            "hostname": socket.gethostname(),
            "program": "testprogram",
            "pid": "9999",
            "message": "test \u00c1\u00c9\u0150\u00da\u0170\u00d3\u00dc-\u00e1\u00e1\u00e9\u00fa\u00f3\u00f6 message"
        }
        self.default_ietf_message_parts = {
            "priority": "38",
            "syslog_protocol_version": "1",
            "iso_timestamp": "2017-06-01T08:05:04+02:00",
            "hostname": socket.gethostname(),
            "program": "testprogram",
            "pid": "9999",
            "message_id": "-",
            "sdata": '[meta sequenceId="1"]',
            "message": "test \u00c1\u00c9\u0150\u00da\u0170\u00d3\u00dc-\u00e1\u00e1\u00e9\u00fa\u00f3\u00f6 message"
        }
        self.bsd_syslog = BSD(logger_factory=logger_factory)
        self.ietf_syslog = IETF(logger_factory=logger_factory)

# Interface for BSDSyslog
    def create_bsd_message(self, defined_bsd_message_parts=None, add_newline=True, counter=1):
        self.validate_defined_message_parts(defined_message_parts=defined_bsd_message_parts, default_message_parts=self.default_bsd_message_parts)
        generated_bsd_message_parts = self.set_message_parts(defined_message_parts=defined_bsd_message_parts, default_message_parts=self.default_bsd_message_parts, counter=counter)
        return self.bsd_syslog.create_bsd_message(generated_message_parts=generated_bsd_message_parts, add_newline=add_newline)

    def create_multiple_bsd_messages(self, defined_bsd_message_parts=None, message_counter=2, add_newline=True):
        messages = ""
        for actual_counter in range(1, message_counter + 1):
            messages += self.create_bsd_message(defined_bsd_message_parts=defined_bsd_message_parts, add_newline=add_newline, counter=actual_counter)
        return messages

# Interface for IETFSyslog
    def create_ietf_message(self, defined_ietf_message_parts=None, add_newline=True, counter=1):
        self.validate_defined_message_parts(defined_message_parts=defined_ietf_message_parts, default_message_parts=self.default_ietf_message_parts)
        generated_ietf_message_parts = self.set_message_parts(defined_message_parts=defined_ietf_message_parts, default_message_parts=self.default_ietf_message_parts, counter=counter)
        return self.ietf_syslog.create_ietf_message(generated_message_parts=generated_ietf_message_parts, add_newline=add_newline)

    def create_multiple_ietf_messages(self, defined_ietf_message_parts=None, message_counter=2, add_newline=True):
        messages = ""
        for actual_counter in range(1, message_counter + 1):
            messages += self.create_ietf_message(defined_ietf_message_parts=defined_ietf_message_parts, add_newline=add_newline, counter=actual_counter)
        return messages

# Other
    def validate_defined_message_parts(self, defined_message_parts, default_message_parts):
        if defined_message_parts and (set(defined_message_parts) - set(default_message_parts.keys())):
            raise Exception("Found unknown log message part: %s" % defined_message_parts)

    @staticmethod
    def set_message_parts(defined_message_parts, default_message_parts, counter=1):
        generated_message_parts = copy.deepcopy(default_message_parts)
        for message_part in default_message_parts.keys():
            if defined_message_parts:
                if (message_part == "bsd_timestamp") and (message_part in defined_message_parts.keys()) and (defined_message_parts[message_part] == "current"):
                    generated_message_parts[message_part] = time.strftime("%b %-d %H:%M:%S")
                elif (message_part == "bsd_timestamp") and (message_part in defined_message_parts.keys()) and (defined_message_parts[message_part] == "regexp"):
                    generated_message_parts[message_part] = '[a-zA-Z]{3} ([0-9]{2}| [0-9]{1}) [0-9]{2}:[0-9]{2}:[0-9]{2}'
                    generated_message_parts['regexp'] = 'regexp'
                elif (message_part in defined_message_parts.keys()) and (defined_message_parts[message_part] != "skip"):
                    generated_message_parts[message_part] = defined_message_parts[message_part]
                elif (message_part in defined_message_parts.keys()) and (defined_message_parts[message_part] == "skip"):
                    generated_message_parts.pop(message_part)
        generated_message_parts['message'] += " - %s" % counter
        return generated_message_parts
