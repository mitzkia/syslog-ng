import socket

class MessageInterface(object):
    def __init__(self, logger_factory):
        self.bsd_message = BSDMessage(logger_factory)

    def construct_bsd_messages(self, used_message_parts, message_counter):
        self.validate_message_parts(used_message_parts, self.bsd_message.default_message_part)
        merged_message_parts = self.set_message_parts()
        bsd_messages = ""
        for counter in range(1, message_counter+1):
            bsd_messages += self.bsd_message.construct_message(merged_message_parts)

        return bsd_messages

    def construct_ietf_messages(self):
        return ""

    def validate_message_parts(self, message_parts):
        pass

    def set_message_parts(self):
        pass

class BSDMessage:
    def __init__(self, logger_factory):
        self.default_message_parts = {
            "priority": "38",
            "bsd_timestamp": "Jun  1 08:05:04",
            "hostname": socket.gethostname(),
            "program": "testprogram",
            "pid": "9999",
            "message": "test \u00c1\u00c9\u0150\u00da\u0170\u00d3\u00dc-\u00e1\u00e1\u00e9\u00fa\u00f3\u00f6 message"
        }
    
    def construct_message(self, message_parts):
        pass

class IETFMessage:
    def __init__(self, logger_factory):
        self.default_message_parts = {
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

    def construct_message(self):
        pass
