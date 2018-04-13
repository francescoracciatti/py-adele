#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" The main module of Py-ADeLe.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""

import logging

# TODO to parametrize
log_level = logging.DEBUG
log_path = ""
log_name = "log"


# Creates a logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Creates a formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Creates a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Creates a file handler
file_handler = logging.FileHandler(log_path + log_name + '.log', mode='a', encoding='utf-8')
file_handler.setLevel(log_level)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

from enum import unique, Enum

if __name__ == '__main__':
    logger.info("Py-ADeLe is running ...")
    logger.info("Done")

