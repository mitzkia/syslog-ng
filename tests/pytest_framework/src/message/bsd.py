import re


class BSD(object):
    def __init__(self, logger_factory):
        self.logger = logger_factory.create_logger("BSD")

    @staticmethod
    def create_bsd_message(generated_message_parts, add_newline=False):
        message = ""
        if "priority" in generated_message_parts:
            message += "<%s>" % generated_message_parts["priority"]
        if "bsd_timestamp" in generated_message_parts:
            message += "%s " % generated_message_parts["bsd_timestamp"]
        if "hostname" in generated_message_parts:
            message += "%s " % generated_message_parts["hostname"]
        if "program" in generated_message_parts:
            message += "%s" % generated_message_parts["program"]
        if "pid" in generated_message_parts:
            message += "[%s]: " % generated_message_parts["pid"]
        if "message" in generated_message_parts:
            message += "%s" % (generated_message_parts["message"])
        if add_newline and not generated_message_parts["message"].endswith("\n"):
            message += "\n"
        if "regexp" in generated_message_parts.values():
            return re.compile(message)
        return message
