import re
import socket


class IETFMessage(object):
    def __init__(self):
        self.default_message_parts = {
            "priority": "38",
            "syslog_protocol_version": "1",
            "iso_timestamp": "2017-06-01T08:05:04+02:00",
            "hostname": socket.gethostname(),
            "program": "testprogram",
            "pid": "9999",
            "message_id": "-",
            "sdata": '[meta sequenceId="1"]',
            "message": "test message - árvíztűrő tükörfúrógép"
        }
        self.iso_timestamp_regexp_pattern = "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}+[0-9]{2}:[0-9]{2}"
        self.bom_pattern = '\ufeff'

    def construct_message(self, message_parts):
        message = ""
        if "priority" in message_parts:
            message += "<{}>".format(message_parts["priority"])
        if "syslog_protocol_version" in message_parts:
            message += "{} ".format(message_parts["syslog_protocol_version"])
        if "iso_timestamp" in message_parts:
            message += "{} ".format(message_parts["iso_timestamp"])
        if "hostname" in message_parts:
            message += "{} ".format(message_parts["hostname"])
        if "program" in message_parts:
            message += "{} ".format(message_parts["program"])
        if "pid" in message_parts:
            message += "{} ".format(message_parts["pid"])
        if "message_id" in message_parts:
            message += "{} ".format(message_parts["message_id"])
        if "sdata" in message_parts:
            message += '{} '.format(message_parts["sdata"])
        if "message" in message_parts:
            message += "{}{}".format(self.bom_pattern, message_parts["message"])
        if not message_parts["message"].endswith("\n"):
            message += "\n"
        message_length = len(message.encode('utf-8'))
        message = "{} {}".format(message_length, message)
        return message

    def construct_regexp_message(self, message_parts):
        return re.compile(self.construct_message(message_parts))
