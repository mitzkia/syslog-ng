import sys

class DummyPythonDest(object):
    def init(self, msg):
        sys.stderr.write("\n>>>>Hello from python module\n\n")
        return True

    def send(self, msg):
        print('queue', msg)
        return True