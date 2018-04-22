# -*- coding: utf-8 -*-
""" This module contains the Object-Oriented Model of ADeLe.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""

from enum import unique, Enum
from types import DynamicClassAttribute
from math import inf


@unique
class ISO(Enum):
    """ ISO measure units. """    
    TIME    = 's'
    LENGTH  = 'm'
    ANGLE   = 'rad'

    @DynamicClassAttribute
    def symbol(self):
        """ The unit symbol. """
        return self._value_


# The start time
ABSOLUTE_REFERENCE_TIME_START = 0.0

# The end time
ABSOLUTE_REFERENCE_TIME_END = inf


class Configuration(object):
    """ Models the configuration of the scenario. """

    def __init__(self,
                 unit_time = ISO.TIME.symbol,
                 unit_length = ISO.LENGTH.symbol,
                 unit_angle = ISO.ANGLE.symbol,
                 time_start = ABSOLUTE_REFERENCE_TIME_START,
                 time_end = ABSOLUTE_REFERENCE_TIME_END):
        self.unit_time = unit_time
        self.unit_length = unit_length
        self.unit_angle = unit_angle
        self.time_start = time_start
        self.time_end = time_end


class Scenario(object):
    """ Models the whole attack scenario. """

    def __init__(self, configuration = Configuration(), list_attack = []):
        self.configuration = configuration

