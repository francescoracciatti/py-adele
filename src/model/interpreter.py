# -*- coding: utf-8 -*-
""" This module contains the interpreters of Py-ADeLe.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""

from enum import Enum, unique


@unique
class Interpreter(Enum):
    """ The type of interpreters for the output file. """
    XML     = 'xml'
#    JSON    = 'json'
#    YAML    = 'yaml'

    @classmethod
    def exist(cls, interpreter: str) -> bool:
        """ Checks if the given writer exists. """
        if interpreter.lower() in tuple(e.value.lower() for e in cls):
            return True
        return False

