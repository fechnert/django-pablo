
DEBUG = 30
INFO = 20
WARNING = 10
ERROR = 0

class PabloLogger(object):
    """Own logging mechanism to set and use loglevels independent of django logging settings"""

    def __init__(self, loglevel=ERROR):
        self.loglevel = loglevel

    def debug(self, message):
        self.log(DEBUG, message)

    def info(self, message):
        self.log(INFO, message)

    def warning(self, message):
        self.log(WARNING, message)

    def error(self, message):
        self.log(ERROR, message)

    def log(self, level, message):
        if level <= self.loglevel:
            print(message)


logger = PabloLogger()
