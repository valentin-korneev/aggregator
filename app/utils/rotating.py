from logging.handlers import TimedRotatingFileHandler
from time import time


class RotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=0, utc=False, atTime=None, errors=None, maxBytes=0):
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc, atTime, errors)
        self.maxBytes = maxBytes

    def shouldRollover(self, record):
        if self.stream is None:
            self.stream = self._open()
        if self.maxBytes > 0:
            msg = f'{self.format(record)}' + chr(10)
            self.stream.seek(0, 2)
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1
        if int(time()) >= self.rolloverAt:
            return 1
        return 0