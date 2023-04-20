import pprint
import sys
from datetime import datetime


class Logger:
    def __init__(self):
        pass

    @staticmethod
    def stdout(*value: object):
        print(datetime.now(), *value)

    @staticmethod
    def stderr(*value: object):
        print(datetime.now(), *value, file=sys.stderr)


def error(*value: object):
    Logger.stderr("[ERROR\t]", *value)


def info(*value: object):
    Logger.stdout("[INFO\t]", *value)


def debug(*value: object):
    Logger.stdout("[DEBUG\t]", *value)


def pretty(*value: object):
    pprint.pprint(datetime.now(), *value)
