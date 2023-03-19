import pprint
import sys


class Logger:
    def __init__(self):
        pass

    @staticmethod
    def stdout(*value: object):
        return print(*value)

    @staticmethod
    def stderr(*value: object):
        return print(*value, file=sys.stderr)

    @staticmethod
    def pretty(*value: object):
        return pprint.pprint(*value)


def stdout(*value: object):
    return Logger.stdout("# ", *value)


def debug(*value: object):
    return Logger.stdout("[DEBUG]", *value)


def info(*value: object):
    return Logger.stdout("[INFO]", *value)


def pretty(*value: object):
    return Logger.pretty(*value)


def error(*value: object):
    return Logger.stderr("[ERROR]", *value)
