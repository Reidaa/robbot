import logging
import sys
from logging.handlers import TimedRotatingFileHandler

FORMAT = '%(asctime)s\t[%(levelname)s]\t%(message)s'
FORMATTER = logging.Formatter(FORMAT)
LOG_FILE = "robbot.log"

CONSOLE_HANDLER_STDOUT = logging.StreamHandler(sys.stdout)
CONSOLE_HANDLER_STDOUT.setFormatter(FORMATTER)

CONSOLE_HANDLER_STDERR = logging.StreamHandler(sys.stderr)
CONSOLE_HANDLER_STDERR.setFormatter(FORMATTER)

FILE_HANDLER = TimedRotatingFileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)


def get_console_handler(sterr: bool = False) -> logging.StreamHandler:
    if sterr:
        return CONSOLE_HANDLER_STDERR
    return CONSOLE_HANDLER_STDOUT


def get_file_handler() -> logging.FileHandler:
    return FILE_HANDLER


def get_logger(logger_name: str, stderr: bool = False) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler(stderr))
    logger.propagate = False
    return logger


def error(*value: object):
    get_logger(__name__).error(print_to_string(*value))


def warning(*value: object):
    get_logger(__name__).warning(print_to_string(*value))


def info(*value: object):
    get_logger(__name__).info(print_to_string(*value))


def debug(*value: object):
    get_logger(__name__).debug(print_to_string(*value))


def print_to_string(*args, **kwargs) -> str:
    newstr = ""
    for a in args:
        newstr += str(a) + ' '
    return newstr
