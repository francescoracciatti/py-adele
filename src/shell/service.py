# -*- coding: utf-8 -*-
""" The service module of Py-ADeLe.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""


import os
import sys
import logging
from enum import unique, IntEnum
from typing import Tuple

from options import Argument
from model.interpreter import Interpreter
from util.utils import baserepr, basestr


# Creates the logger
logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """ Exception caused by a validation error. """

    @unique
    class Code(IntEnum):
        """ The error codes. """
        NOT_EXIST: int = 1
        NOT_FILE: int = 2
        NOT_SUPPORTED: int = 3


class Choose(object):
    """ Wraps the choose (yes/no). """
    YES: str = 'yes'
    NO: str = 'no'


def validate_argument(argument: Argument) -> Tuple[str, str]:
    """ Validates the given arguments and returns the paths to the
    source file and output file.
    """
    # Checks if the source file exists
    if not os.path.exists(argument.source):
        raise ValidationError("The source file '{}' does not exist".format(argument.source),
                              ValidationError.Code.NOT_EXIST)
    if not os.path.isfile(argument.source):
        raise ValidationError("The (source) path '{}' does not refer a file".format(argument.source),
                              ValidationError.Code.NOT_FILE)

    # Checks if the parser supports the current interpreter
    if not Interpreter.exist(argument.interpreter):
        raise ValidationError("The interpreter '{}' is not supported".format(argument.interpreter),
                              ValidationError.Code.NOT_SUPPORTED)

    # Checks if the output file already exists and if it can be overwritten
    if argument.output is None or not argument.output:
        argument.output = '{}.{}'.format(
            os.path.splitext(argument.source)[0],
            argument.interpreter.lower())
        logger.info("The (path to the) output file is missing, using default: '{}'".format(argument.output))
    if os.path.exists(argument.output):
        if os.path.isfile(argument.output):
            if argument.force is False:
                logger.info("The output file '{}' already exists, overwrite?".format(argument.output))
                overwrite = str()
                input_msg = '[{}/{}]'.format(Choose.YES, Choose.NO)
                while overwrite.lower() not in (Choose.YES.lower(), Choose.NO.lower()):
                    overwrite = input(input_msg)
                    logger.info("{} > {}".format(input_msg, overwrite))
                if overwrite.lower() == Choose.NO.lower():
                    logger.info("Cannot overwrite the output file, will not proceed.")
                    sys.exit(0)
                logger.info("The file '{}' will be overwritten".format(argument.output))
            else:
                logger.info("The file '{}' will be overwritten (force overwrite)".format(argument.output))
        else:
            raise ValidationError("The (output) path '{}' does not refer a file".format(argument.output),
                                  ValidationError.Code.NOT_FILE)

    return [argument.source, argument.output, argument.interpreter]

