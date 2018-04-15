# -*- coding: utf-8 -*-
""" This module contains the Object-Oriented Model of ADeLe.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""

# The default units of measurement for the time, space and angle
DEFAULT_UNIT_TIME = 'second'
DEFAULT_UNIT_SPACE = 'meter'
DEFAULT_UNIT_ANGLE = 'rad'

# The current unit of measurement for the time, space and angle
UNIT_TIME = DEFAULT_UNIT_TIME
UNIT_SPACE = DEFAULT_UNIT_SPACE
UNIT_ANGLE = DEFAULT_UNIT_ANGLE


def setUnitTime(unit_time):
    """ Sets the measurement unit for the time. """
    UNIT_TIME = unit_time


def setUnitSpace(unit_space):
    """ Sets the measurement unit for the space. """
    UNIT_SPACE = unit_space


def setUnitAngle(unit_angle):
    """ Sets the measurement unit for the angle. """
    UNIT_ANGLE = unit_angle


class Configuration(object):
    """ Models the current configuration. """
    
    def __init__(self):
        self.unit_time = UNIT_TIME
        self.unit_space = UNIT_SPACE
        self.unit_angle = UNIT_ANGLE

