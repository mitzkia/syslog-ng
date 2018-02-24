import re


class BSD(object):
    def __init__(self, logger_factory):
        self.logger = logger_factory.create_logger("BSD")

    def create_bsd_message(self, generated_message_parts):
        # NEEEEM jo, itt nem lehet 2 fv, 
        # nezzuk vegig megegyszer a teszteset oldalrol, onnan lehet 2 fv-t hivni
        message = "<{}> {} {} {}[{}]: {}".format(
            generated_message_parts['priority'],
            generated_message_parts['bsd_timestamp'],
            generated_message_parts['hostname'],
            generated_message_parts['program'],
            generated_message_parts['pid'],
            generated_message_parts['message'],
            )
        if not generated_message_parts["message"].endswith("\n"):
            message += "\n"
        return message

    def create_regexp_bsd_message(self, generated_message_parts):
        bsd_message = self.create_bsd_message(generated_message_parts)
        return re.compile(bsd_message)