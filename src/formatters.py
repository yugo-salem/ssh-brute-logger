from json import dumps
import logging


class JsonFormatter(logging.Formatter):
    def format(self, record):
        return dumps([
            self.formatTime(record, self.datefmt),
            record.msg,
        ])
