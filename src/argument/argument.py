# -*- coding: utf-8 -*-
""" The command line argument parsing facilities of Py-ADeLe.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""

import os
from enum import unique, Enum
from argparse import ArgumentParser
from types import DynamicClassAttribute
import logging


from model.writer import Writer 


# Creates a logger
logger = logging.getLogger(__name__)


@unique
class Option(Enum):
    """ The command line options. """
    SOURCE  = 's'
    WRITER  = 'w'
    OUTPUT  = 'o'
    FORCE   = 'f'

    @DynamicClassAttribute
    def short(self):
        """ The short code. """
        return '-{}'.format(self._name_.lower())

    @DynamicClassAttribute
    def long(self):
        """ The long code. """
        return '--{}'.format(self._name_.lower())

    @DynamicClassAttribute
    def metavar(self):
        """ The meta variable. """
        return '\"{}\"'.format(self._name_.upper())

    @DynamicClassAttribute
    def option(self):
        """ The name of the option. """
        return self._name_.lower()

    @classmethod
    def options(cls):
        """ Gets the options. """
        return tuple(e.option for e in cls)


class Argument(object):
    """ The arguments from the command line. """
    
    def __init__(self, source, writer, output, force):
        self.source = source
        self.writer = writer
        self.output = output
        self.force = force


def get_command_line_arguments():
    """ Gets the command line arguments. """

    epilog = 'Usage: python pyadele.py {} {} {} {} [{} {}] [{}]'.format(
        Option.SOURCE.short,
        'paht/to/source',
        Option.WRITER.short,
        'output-writer',
        Option.OUTPUT.short,
        'path/to/output',
        Option.FORCE.short)
    argparser = ArgumentParser(epilog=epilog)
    argparser.add_argument(Option.SOURCE.short, 
                           Option.SOURCE.long,
                           metavar=Option.SOURCE.metavar,
                           default='',
                           help="The path to the source file to be processed. Mandatory.")
    argparser.add_argument(Option.WRITER.short, 
                           Option.WRITER.long,
                           metavar=Option.WRITER.metavar,
                           default='',
                           help="The writer of the output file. Mandatory.")
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
    arguments = argparser.parse_args().__dict__

    # Checks if the arguments exist
    for option in Option.options():
        if arguments.get(option, None) is None:
            msg = "Cannot recognize the argument for the option {}".format(option)
            logger.critical(msg)
            argparser.error(msg)

    # The source file is mandatory
    source = arguments[Option.SOURCE.option] 
    if not source:
        msg = "Source file is missing"
        logger.critical(msg)
        argparser.error(msg)

    # Validates the writer, which is mandatory
    writer = arguments[Option.WRITER.option]
    if not writer:
        msg = "Writer is missing"
        logger.critical(msg)
        argparser.error(msg)
    if not Writer.exist(writer):
        msg = "Writer {} not recognized".format(writer)
        logger.critical(msg)
        argparser.error(msg)

    # Buils the output filename if it is missing 
    output = arguments[Option.OUTPUT.option]
    if not output:
        output = '{}.{}'.format(
            os.path.splitext(source)[0],
            writer)
        logger.info("Output filename is missing, using {}".format(output))

    # Gets the force flag
    force = arguments[Option.FORCE.option]

    return Argument(source, writer, output, force)

