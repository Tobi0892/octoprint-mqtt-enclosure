import logging
from logging.handlers import TimedRotatingFileHandler


class LOG:

    def __init__(self, logfile):
        self.logfile = logfile
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler = TimedRotatingFileHandler(self.logfile, when="midnight", interval=1, encoding='utf8')
        handler.suffix = "%Y%m%d"
        handler.setFormatter(formatter)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)

    def info(self, message):
        self.logger.info(message)
