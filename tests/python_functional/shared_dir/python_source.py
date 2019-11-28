from syslogng import LogSource


class PythonSourceTestClass(LogSource):
    def init(self, options):
        return True

    def run(self):
        pass

    def request_exit(self):
        pass
