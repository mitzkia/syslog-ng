import re


class IETF(object):
    def __init__(self, logger_factory):
        self.logger = logger_factory.create_logger("IETF")

    @staticmethod
    def create_ietf_message(generated_message_parts):
        message = ""
        if "priority" in generated_message_parts:
            message += "<%s>" % generated_message_parts["priority"]
        if "syslog_protocol_version" in generated_message_parts:
            message += "%s " % generated_message_parts["syslog_protocol_version"]
        if "iso_timestamp" in generated_message_parts:
            message += "%s " % generated_message_parts["iso_timestamp"]
        if "hostname" in generated_message_parts:
            message += "%s " % generated_message_parts["hostname"]
        if "program" in generated_message_parts:
            message += "%s " % generated_message_parts["program"]
        if "pid" in generated_message_parts:
            message += "%s " % generated_message_parts["pid"]
        if "message_id" in generated_message_parts:
            message += "%s " % generated_message_parts["message_id"]
        if "sdata" in generated_message_parts:
            message += '[meta sequenceId="-"] '
        if "message" in generated_message_parts:
            message += "%s" % (generated_message_parts["message"])
        if not generated_message_parts["message"].endswith("\n"):
            message += "\n"
        message_length = len(message.encode('utf-8'))
        message = "%d %s" % (message_length, message)
        if "regexp" in generated_message_parts.values():
            return re.compile(message)
        return message
