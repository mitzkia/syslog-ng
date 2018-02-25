from src.driver_io.file_based.wait_for_event import FileWaitForEvent


class SlngConsoleHandler(object):
    def __init__(self, logger_factory, process_commands):
        self.logger_factory = logger_factory
        self.process_commands = process_commands
        self.logger = logger_factory.create_logger("SlngConsoleHandler")
        self.syslog_ng_start_message = ["syslog-ng starting up;"]
        self.syslog_ng_stop_message = ["syslog-ng shutting down"]
        self.syslog_ng_reload_messages = [
            "New configuration initialized",
            "Configuration reload request received, reloading configuration",
            "Configuration reload finished"
        ]
        self.stderr_file = None

    def wait_for_start_message(self, external_tool=None):
        return self.wait_for_console_message(messages=self.syslog_ng_start_message, external_tool=external_tool)

    def wait_for_reload_message(self, external_tool=None):
        return self.wait_for_console_message(messages=self.syslog_ng_reload_messages, external_tool=external_tool)

    def wait_for_stop_message(self, external_tool=None):
        return self.wait_for_console_message(messages=self.syslog_ng_stop_message, external_tool=external_tool)

    def wait_for_console_message(self, messages, external_tool=None):
        if not self.stderr_file:
            if not external_tool:
                self.stderr_file = FileWaitForEvent(self.logger_factory, self.process_commands['start']['stderr'])
            else:
                self.stderr_file = FileWaitForEvent(self.logger_factory, self.process_commands[external_tool]['stderr'])
        result = []
        for message in messages:
            found_message_in_console_log = self.stderr_file.wait_for_message(expected_message=message)
            # print("Message: %s" % message)
            # print("Found or not: %s" % found_message_in_console_log)
            result.append(found_message_in_console_log)
        return all(result)
