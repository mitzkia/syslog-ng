import re
import socket


class BSDMessage(object):
    def __init__(self):
        self.default_message_parts = {
            "priority": "38",
            "bsd_timestamp": "Jun  1 08:05:04",
            "hostname": socket.gethostname(),
            "program": "testprogram",
            "pid": "9999",
            "message": "test message - árvíztűrő tükörfúrógép"
        }
        self.bsd_timestamp_regexp_pattern = "[a-zA-Z]{3} ([0-9]{2}| [0-9]{1}) [0-9]{2}:[0-9]{2}:[0-9]{2}"

    @staticmethod
    def construct_message(message_parts):
        message = ""
        if "priority" in message_parts:
            message += "<{}>".format(message_parts["priority"])
        if "bsd_timestamp" in message_parts:
            message += "{} ".format(message_parts["bsd_timestamp"])
        if "hostname" in message_parts:
            message += "{} ".format(message_parts["hostname"])
        if "program" in message_parts:
            message += "{}".format(message_parts["program"])
        if "pid" in message_parts:
            message += "[{}]: ".format(message_parts["pid"])
        if "message" in message_parts:
            message += "{}".format(message_parts["message"])
        if not message_parts["message"].endswith("\n"):
            message += "\n"
        return message

    def construct_regexp_message(self, message_parts):
        return re.compile(self.construct_message(message_parts))
