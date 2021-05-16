import logging
import sys


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Logger:
    @classmethod
    def log_warning(cls, msg):
        logging.warning(bcolors.WARNING + " " + str(msg) + bcolors.ENDC)
        print(msg, file=sys.stderr)

    @classmethod
    def log_error(cls, msg):
        logging.error(msg)
        print(msg, file=sys.stderr)

    @classmethod
    def log_debug(cls, msg):
        logging.debug(msg)
        print(msg, file=sys.stderr)
