import copy
from src.message.bsd_message import BSDMessage
from src.message.ietf_message import IETFMessage


class MessageInterface(object):
    def __init__(self, logger_factory):
        self.logger = logger_factory.create_logger("MessageInterface")
        self.bsd_message = BSDMessage()
        self.ietf_message = IETFMessage()
        self.custom_message_pattern = {
            "hostname": "random_hostname",
            "program": "random_program",
        }

    def construct_bsd_messages(self, message_parts, message_counter=1):
        return self.construct_messages(self.bsd_message, message_parts, message_counter)

    def construct_ietf_messages(self, message_parts, message_counter=1):
        return self.construct_messages(self.ietf_message, message_parts, message_counter)

    def construct_messages(self, message_format, message_parts, message_counter):
        self.validate_message_parts(message_parts, message_format.default_message_parts)
        merged_message_parts = self.set_message_parts(message_parts, message_format.default_message_parts)
        messages = []
        for _actual_counter in range(1, message_counter + 1):
            if ("meta" in merged_message_parts.keys()) and (merged_message_parts['meta'] == "regexp"):
                messages.append(message_format.construct_regexp_message(merged_message_parts))
            else:
                messages.append(message_format.construct_message(merged_message_parts))
        if ("meta" in merged_message_parts.keys()) and (merged_message_parts['meta'] == "regexp"):
            return messages
        else:
            return "".join(messages)

    def construct_messages_with_various_message_parts(self, message_part, message_part_counter):
        various_message_parts = []
        for counter in range(1, message_part_counter + 1):
            various_message_parts.append("{}-{}".format(self.custom_message_pattern[message_part], counter))
        generated_messages = []
        for various_message_part in various_message_parts:
            generated_messages.append(
                self.construct_messages(self.bsd_message, {message_part: various_message_part}, message_counter=1))
        return generated_messages

    @staticmethod
    def validate_message_parts(message_parts, default_message_parts):
        if message_parts and (set(message_parts) - set(default_message_parts)):
            raise Exception("Found unknown message part in: {}".format(message_parts))

    def set_message_parts(self, message_parts, default_message_parts):
        merged_message_parts = copy.deepcopy(default_message_parts)
        for message_part_name, message_part_value in message_parts.items():
            if message_part_value == "skip":
                merged_message_parts.pop(message_part_name)
            elif (message_part_name == "bsd_timestamp") and (message_part_value == "regexp"):
                merged_message_parts[message_part_name] = self.bsd_message.bsd_timestamp_regexp_pattern
                merged_message_parts['meta'] = "regexp"
            else:
                merged_message_parts[message_part_name] = message_part_value
        return merged_message_parts
