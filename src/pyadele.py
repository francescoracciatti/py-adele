#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" The main module of Py-ADeLe.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""


import os
import sys 
sys.path.append('./src/')
sys.path.append('./src/parser/')
#from argparse import ArgumentParser
#from enum import unique, Enum
#from types import DynamicClassAttribute

import logging

from parser.grammar import parser
from argument.argument import get_command_line_arguments

# TODO handle the version number 
__version__ = '2.0.0'


# TODO argparse
LOG_LEVEL = logging.DEBUG
log_path = ""
log_name = "log"
target = 'tests/sources/test-complete.adele'


# Creates a logger
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

# Creates a formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

# Creates a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Creates a file handler
file_handler = logging.FileHandler(log_path + log_name + '.log', mode='a', encoding='utf-8')
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


if __name__ == '__main__':
    logger.info("Py-ADeLe is running")

    # Retrieves the command line arguments
    arguments = get_command_line_arguments(sys.argv[1:])

    # Opens the source file
    with open(target, 'r') as f:
        logger.info("Target: {}".format(target))
        source = f.read()
    try:
        # Parses the source file and builds the attack scenario
        logger.info("Parsing ...")
        scenario = parser.parse(source)
    except SyntaxError as e:
        logger.critical("Sintax error: " + str(e))
    except RuntimeError as e:
        logger.critical("Parsing error: " + str(e))
    except:
        logger.critical("Generic error: " + str(e))
        raise
    logger.info("Parsing done")
    
    # TODO Builds the bytecode
    
    logger.info("Done")



