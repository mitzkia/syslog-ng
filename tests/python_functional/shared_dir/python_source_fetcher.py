from syslogng import LogFetcher
from syslogng import LogMessage

class PythonSourceFetcherTestClass(LogFetcher):
    def init(self, options):
        return True

    def fetch(self):
        return LogFetcher.FETCH_NOT_CONNECTED, LogMessage()
