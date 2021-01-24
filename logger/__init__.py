# -*-coding:utf-8-*-
import logging
import os, sys
import time, datetime


# reportPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))+"\\report\\log_"+time.strftime("%Y-%m-%d_%H-%M-%S")+".log"
class Logger(object):
    def _now(self):
        return str(datetime.datetime.now()).split(".")[0]

    def debug(self, message):
        print(self._now() + "-[DEBUG]-" + message)

    def info(self, message):
        print(self._now() + "-[INFO]-" + message)

    def warn(self, message):
        print(self._now() + "-[WARN]-" + message, file=sys.stderr)

    def error(self, message):
        print(self._now() + "-[ERROR]-" + message, file=sys.stderr)

    def critical(self, message):
        print(self._now() + "-[CRITICAL]-" + message, file=sys.stderr)


Logger = Logger()
