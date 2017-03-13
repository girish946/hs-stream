"""Helper functions """

from __future__ import print_function
import sys
from clint.textui import colored


def info(msg):
    """ Green Colored info message """
    print(colored.green("[INFO]: {0}".format(msg)))


def warn(msg):
    """ Yellow Colored info message """
    print(colored.yellow("[WARN]: {0}".format(msg)))


def err(msg):
    """ Red Colored info message """
    print(colored.red("[ERROR]: {0}".format(msg)))


def debug(msg):
    """ Debugging """
    print(colored.cyan("[DEBUG]: {0}".format(msg)))


def sysexit(msg, color='red'):
    """ Helper exit function """
    if color == 'red':
        msg = colored.red("[EXIT]: {0}".format(msg))
    elif color == 'green':
        msg = colored.green("[EXIT]: {0}".format(msg))
    sys.exit(msg)
