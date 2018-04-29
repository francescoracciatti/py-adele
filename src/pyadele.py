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
sys.path.append('./src/model/')
sys.path.append('./src/parser/')
sys.path.append('./src/shell/')
import logging
import logging.config

import json

from parser.grammar import parser
from shell.options import get_command_line_arguments
from shell.service import validate_argument


# Logger configuration file
loggerconfig = 'src/log/logger.json'

# Gets the logger
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    if os.path.exists(loggerconfig):
        with open(loggerconfig, 'rt') as logger_config_file:
            config = json.load(logger_config_file)
        logging.config.dictConfig(config)
    else:
        print("Cannot find the logger configuration file, using default config")
        logging.basicConfig(level=logging.INFO)

    logger.info("Py-ADeLe is running")
    
    try:
        # Retrieves the command line arguments
        argument = get_command_line_arguments(sys.argv[1:])
        logger.info(argument)

        # Validates the arguments
        source, output = validate_argument(argument)

        # TODO remove, it bypasses the command line call
        source = 'tests/source/test-complete.adele'
    
        # Opens the source file
        with open(source, 'r') as filesource:
            sourcecode = filesource.read()
        
        # Parses the source file and builds the attack scenario
        logger.info("Parsing ...")
        scenario = parser.parse(sourcecode)
        logger.info("Parsing done")
      
        # Interprets and writes the attack scenario
        # TODO remove, it stubs the interpreter
        outputcode = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit..."
        
        # Writes the output file
        with open(output, 'w') as fileoutput:
            fileoutput.write(outputcode)

        logger.info("Done")
    except Exception as e:
        logger.critical(e, exc_info=True)
        raise

