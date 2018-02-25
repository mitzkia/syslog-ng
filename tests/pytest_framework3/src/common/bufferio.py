class BufferIO(object):
    def __init__(self):
        self.buffer = ""
        self.msg_list = []

    def buffering_messages(self, read):
        content = read()
        if content:
            self.buffer += content

    def parsing_messages(self, parse_rule="\n"):
        if parse_rule == "\n":
            for chunk in self.buffer.splitlines(keepends=True):
                if chunk.endswith(parse_rule):
                    self.msg_list.append(chunk)
                    self.buffer = self.buffer.replace(chunk, "", 1)

    def pop_msg(self, read):
        self.buffering_messages(read)
        self.parsing_messages()
        return self.msg_list.pop(0)

    def pop_msgs(self, read, counter=0):
        self.buffering_messages(read)
        self.parsing_messages()
        if counter == 0:
            counter = len(self.msg_list)

        temp_list = []
        if counter > len(self.msg_list):
            assert False

        for index in range(0, counter):
            temp_list.append(self.msg_list[index])

        for index in range(0, counter):
            self.msg_list.pop(0)
        return temp_list

    def peek_msg(self, message):
        pass

    def peek_msgs(self, read, counter=0):
        if counter == 0:
            counter = len(self.msg_list)
        temp_list = []

        self.buffering_messages(read)
        self.parsing_messages()

        for index in range(0, counter):
            temp_list.append(self.msg_list[index])

        return temp_list
