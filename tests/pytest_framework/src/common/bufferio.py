from src.common.blocking import wait_until_true

class BufferIO(object):
    def __init__(self):
        self.buffer = ""
        self.msg_list = []
        self.final_msg_list = []

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

    def buffer_and_parse(self, read, counter):
        self.buffering_messages(read)
        self.parsing_messages()
        print("BBBB A FELPARSEOLT UZENETEK: %s" % self.msg_list)
        print("BBBB A FELPARSEOLT UZENETEK DBSZAMA: %s" % len(self.msg_list))
        print("BBBB ENNYI DB UZENETET VARUNK: %s" % counter)
        print("MEGJOTT A MEGFELELO SZAMU UZENET: %s" % (len(self.msg_list) >= counter))
        return len(self.msg_list) >= counter

    def pop_msg(self, read):
        a = self.pop_msgs(read, counter=1)
        if isinstance(a, list) and len(a)!=0:
            return a[0]
        return ""

    def pop_msgs(self, read, counter=0):

        print("EZAFONTOSSSSSSSSSSSSSSSS: %s" % self.peek_msgs(read))
        result = wait_until_true(self.buffer_and_parse, read, counter, monitoring_time=1)
        print("Frompopmsgs-result-innerwaituntil: %s" % result)
        print("EZAFONTOSSSSSSSSSSSSSSSS2: %s" % self.peek_msgs(read))
        import sys
        sys.exit(1)

        if counter == 0:
            counter = len(self.msg_list)
        self.final_msg_list = self.msg_list[0:counter]
        self.msg_list = self.msg_list[counter:]
        return self.final_msg_list

    def peek_msg(self, read):
        return self.peek_msgs(read, counter=0)[0]

    def peek_msgs(self, read, counter=0):
        assert wait_until_true(self.buffer_and_parse, read, counter), "We have less messages than expected"

        return self.msg_list[0:counter]
