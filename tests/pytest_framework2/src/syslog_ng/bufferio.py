class DriverIO(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_object = None

    def read(self):
        # print("read file - start")
        if not self.file_object:
            self.file_object = open(self.file_path, 'r')
        # print("read file - end")
        return self.file_object.read()

    def write(self, message="test message\n"):
        # print("write file - start")
        with open(self.file_path, 'a') as file_object:
            file_object.write(message)
        # print("write file - end")


class FDestinationDriver(object):
    def __init__(self, file_path):
        self.bufferio = BufferIO()
        self.driverio = DriverIO(file_path)

    def pop_msg(self):
        return self.bufferio.pop_msg(self.driverio.read)

    def pop_msgs(self, counter):
        return self.bufferio.pop_msgs(self.driverio.read, counter)

    def peek_msg(self, message="message 1"):
        return self.bufferio.peek_msg(message)

    def peek_msgs(self):
        pass


class BufferIO(object):
    def __init__(self):
        self.buffer = ""
        self.msg_list = []

    def buffering_messages(self, read):
        # print("BBBBbuffering messages - start, buffer: [%s], msg_list: [%s]" % (self.buffer, self.msg_list))
        content = read()
        if content:
            self.buffer += content
        # print("BBBBbuffering messages - end, buffer: [%s], msg_list: [%s]" % (self.buffer, self.msg_list))

    def parsing_messages(self, parse_rule="\n"):
        # print("PPPPPparse messages - start, buffer: [%s], msg_list: [%s]" % (self.buffer, self.msg_list))
        if parse_rule == "\n":
            for chunk in self.buffer.splitlines(keepends=True):
                if chunk.endswith(parse_rule):
                    self.msg_list.append(chunk)
                    self.buffer = self.buffer.replace(chunk, "", 1)
        # print("PPPPPparse messages - end, buffer: [%s], msg_list: [%s]" % (self.buffer, self.msg_list))

    def pop_msg(self, read):
        # print("11111pop msg - start")
        self.buffering_messages(read)
        self.parsing_messages()
        # print("11111pop msg - end")
        return self.msg_list.pop(0)

    def pop_msgs(self, read, counter):
        # print("2222pop msgs - start")
        self.buffering_messages(read)
        self.parsing_messages()
        temp_list = []
        if counter > len(self.msg_list):
            assert False

        # save elements for returning
        for index in range(0, counter):
            temp_list.append(self.msg_list[index])

        # drop elements from list
        for index in range(0, counter):
            self.msg_list.pop(0)

        # print("2222pop msgs - end")
        return temp_list

    def peek_msg(self, message):
        pass

d_io = DriverIO("b.txt")
d_io.write("message 1\n")
d_io.write("message 2\n")
d_io.write("message 3\n")
print("Read messages:\n%s" % d_io.read())
fd = FDestinationDriver("b.txt")
print("popped msg1: %s" % fd.pop_msg()) # read message 1
print("popped msg2: %s" % fd.pop_msg()) # read message 2
d_io.write("message 4\n")
d_io.write("message 5\n")
d_io.write("message 6")
print("popped msg3: %s" % fd.pop_msg()) # read message 3
print("popped msg4: %s" % fd.pop_msg()) # read message 4
print("popped msgs1: %s" % fd.pop_msgs(counter=1))  # read message 5
d_io.write("\nmessage 7\n")
print("popped msgs2: %s" % fd.pop_msgs(counter=2))  # read message 6-7
# print("popped msg5: %s" % fd.pop_msg()) # read message
