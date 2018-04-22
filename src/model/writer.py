# -*- coding: utf-8 -*-
""" This module contains the writers of the Object-Oriented Model of ADeLe.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""

from enum import Enum, unique


@unique
class Writer(Enum):
    """ The type of writers for the output file. """
    XML     = 'xml'

    @classmethod
    def exist(cls, writer: str) -> bool:
        """ Checks if the given writer exists. """
        if writer.lower() in tuple(e.value for e in cls):
            return True
        return False

