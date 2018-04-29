#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" The main module of Py-ADeLe.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""


import sys
sys.path.append('./src/')
sys.path.append('./src/model/')
sys.path.append('./src/parser/')
sys.path.append('./src/shell/')
import logging

from parser.grammar import parser
from shell.options import get_command_line_arguments
from shell.service import validate_argument


# TODO handle the version number
__version__ = '2.0.0'


# TODO argparse
LOG_LEVEL = logging.DEBUG
log_path = ""
log_name = "log"


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
    try:
        # Retrieves the command line arguments
        argument = get_command_line_arguments(sys.argv[1:])
        logger.info(argument)

        # Validates the arguments
        source, output = validate_argument(argument)
    
        # TODO remove
        # Bypass the command line call
        source = 'tests/source/test-complete.adele'
    
        # Opens the source file
        with open(source, 'r') as f:
            code = f.read()
        
        # Parses the source file and builds the attack scenario
        logger.info("Parsing ...")
        scenario = parser.parse(code)
        logger.info("Parsing done")
      
      
        # Interprets and writes the attack scenario
    
        logger.info("Done")
    except Exception as e:
        logger.critical(e)
        raise

