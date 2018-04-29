# -*- coding: utf-8 -*-
""" The command line argument parser of Py-ADeLe.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""


import os
import logging
from enum import unique, Enum
from types import DynamicClassAttribute
from typing import Tuple, List
from argparse import ArgumentParser


# Creates a logger
logger = logging.getLogger(__name__)


@unique
class Option(Enum):
    """ The command line options. """
    SOURCE          = 's'
    INTERPRETER     = 'i'
    OUTPUT          = 'o'
    FORCE           = 'f'

    @DynamicClassAttribute
    def short(self) -> str:
        """ The short code. """
        return '-{}'.format(self.name.lower())

    @DynamicClassAttribute
    def long(self) -> str:
        """ The long code. """
        return '--{}'.format(self.name.lower())

    @DynamicClassAttribute
    def metavar(self) -> str:
        """ The meta variable. """
        return '\"{}\"'.format(self.name.upper())

    @DynamicClassAttribute
    def option(self) -> str:
        """ The name of the option. """
        return self.name.lower()

    @classmethod
    def options(cls) -> Tuple[str, ...]:
        """ Gets the options. """
        return tuple(e.option for e in cls)


class Argument(object):
    """ Wraps the full set of arguments passed by the command line. """

    def __init__(self,
                 source: str = None,
                 interpreter: str = None,
                 output: str = None,
                 force: str = None) -> None:
        self.source: str = source
        self.interpreter: str = interpreter
        self.output: str = output
        self.force: str = force

    def __str__(self):
        str = '{}: '.format(self.__class__.__name__)
        for k in self.__dict__.keys():
           str += '[{}: {}] '.format(k, self.__dict__[k]) 
        return str


def get_command_line_arguments(args: List[str]) -> Argument:
    """ Parses and returns the command line arguments. """

    epilog = 'Usage: python pyadele.py {} {} {} {} [{} {}] [{}]'.format(
        Option.SOURCE.short,
        'paht/to/source',
        Option.INTERPRETER.short,
        'interpreter',
        Option.OUTPUT.short,
        'path/to/output',
        Option.FORCE.short)
    argparser = ArgumentParser(epilog=epilog)
    argparser.add_argument(Option.SOURCE.short,
                           Option.SOURCE.long,
                           metavar=Option.SOURCE.metavar,
                           default='',
                           help="The path to the source file to be processed. It is Mandatory.")
    argparser.add_argument(Option.INTERPRETER.short,
                           Option.INTERPRETER.long,
                           metavar=Option.INTERPRETER.metavar,
                           default='',
                           help="The interpreter of the parsing engine. It is Mandatory.")
    argparser.add_argument(Option.OUTPUT.short,
                           Option.OUTPUT.long,
                           metavar=Option.OUTPUT.metavar,
                           default='',
                           help="[Optional] The path to the output file.")
    argparser.add_argument(Option.FORCE.short,
                           Option.FORCE.long,
                           action='store_true',
                           default=False,
                           dest=Option.FORCE.option,
                           help="[Optional] Forces the overwrite of the output file.")

    # Parses the arguments
    arguments = argparser.parse_args(args).__dict__

    # Checks if the arguments exist
    for option in Option.options():
        if arguments.get(option, None) is None:
            msg = "Cannot recognize the argument for the option {}".format(option)
            logger.critical(msg)
            argparser.error(msg)

    # The (path to the) source file is mandatory
    source = arguments[Option.SOURCE.option]
    if not source:
        msg = "The (path to the) source file is missing"
        logger.critical(msg)
        argparser.error(msg)

    # The interpreter is mandatory
    interpreter = arguments[Option.INTERPRETER.option]
    if not interpreter:
        msg = "The interpreter is missing ()"
        logger.critical(msg)
        argparser.error(msg)

    # The (path to the) output file is not mandatory
    output = arguments[Option.OUTPUT.option]

    # The force overwrite flag is not mandatory
    force = arguments[Option.FORCE.option]

    return Argument(source, interpreter, output, force)

