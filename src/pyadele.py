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
sys.path.append('./src/util/')
import logging
import logging.config

import json

from parser.grammar import parser
from shell.options import get_command_line_arguments
from shell.service import validate_argument
from model.interpreter import Interpreter

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
        source, output, interpreter = validate_argument(argument)

        # Opens the source file
        with open(source, 'r') as filesource:
            sourcecode = filesource.read()
        
        # Parses the source file and builds the attack scenario
        logger.info("Parsing ...")
        scenario = parser.parse(sourcecode)
        logger.info("Done")
      
        # Interprets and writes the attack scenario
        logger.info("Interpreting ...")
        outputcode = Interpreter.interpret(scenario, interpreter)
        logger.info("Done")
        
        
        # Writes the output file
        with open(output, 'w') as fileoutput:
            fileoutput.write(outputcode)

        logger.info("Done")
    except Exception as e:
        logger.critical(e, exc_info=True)
        sys.exit(1)

