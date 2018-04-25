# -*- coding: utf-8 -*-
""" This module contains the Object-Oriented Model of ADeLe.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""

from enum import unique, Enum
from types import DynamicClassAttribute
from typing import List
from math import inf


@unique
class ISO(Enum):
    """ ISO measure units. """
    TIME: str       = 's'
    LENGTH: str     = 'm'
    ANGLE: str      = 'rad'

    @DynamicClassAttribute
    def symbol(self) -> str:
        """ The measure unit related symbol. """
        return self.value


# The start time
ABSOLUTE_REFERENCE_TIME_START: float = 0.0

# The end time
ABSOLUTE_REFERENCE_TIME_END: float = inf


class Configuration(object):
    """ Models the configuration compound statement. """

    def __init__(self,
                 unit_time: str     = ISO.TIME.symbol,
                 unit_length: str   = ISO.LENGTH.symbol,
                 unit_angle: str    = ISO.ANGLE.symbol,
                 time_start: float  = ABSOLUTE_REFERENCE_TIME_START,
                 time_end: float    = ABSOLUTE_REFERENCE_TIME_END) -> None:
        self.unit_time: str     = unit_time
        self.unit_length: str   = unit_length
        self.unit_angle: str    = unit_angle
        self.time_start: float  = time_start
        self.time_end: float    = time_end


class Attack(object):
    """ Models the attack compound statement. """
    pass



class Scenario(object):
    """ Models the whole scenario compound statement. """

    def __init__(self,
                 configuration: Configuration   = None,
                 list_attack: List[Attack]      = None) -> None:
        self.configuration: Configuration = configuration

