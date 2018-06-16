# -*- coding: utf-8 -*-
""" This module contains the interpreters of Py-ADeLe.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""

import logging
from enum import unique, IntEnum
from typing import Any

from util.utils import baserepr, basestr
from oom import *


logger = logging.getLogger(__name__)


# The column width
INDENT_SPACE = ' ' * 4

# Prefix for the reserved attributes
ATTRIBUTE_RESERVED_PREFIX = '_'

# Tags' properties
PROPERTY_ENTITY = 'entity'
PROPERTY_LENGTH = 'length'
PROPERTY_INDEX = 'index'
PROPERTY_TYPE = 'type'

# Properties's values
PROPERTY_VALUE_OBJECT = 'object'
PROPERTY_VALUE_ATTRIBUTE = 'attribute'


class InterpretationError(Exception):
    """ Exception caused by an interpretation error. """

    @unique
    class Code(IntEnum):
        """ The error codes. """
        NOT_SUPPORTED = 1
        OBJECT_NOT_RECOGNIZED = 2


    def __init__(self, message: str, code: int = None) -> None:
        super().__init__(message)
        self.message : str = message
        self.code : int = code

    def __str__(self):
        return basestr(self)

    def __repr__(self):
        return baserepr(self)


class Interpreter(object):
    """ The interpret that builds the representation of the attack scenario. """

    @unique
    class Type(Enum):
        XML = 'xml'
#       JSON = 'json'
#       YAML = 'yaml'

    @classmethod
    def exist(cls, interpreter: str) -> bool:
        """ Checks if the given interpreter exists. """
        if interpreter.lower() in tuple(e.value.lower() for e in cls.Type):
            return True
        return False

    @classmethod
    def interpret(cls, scenario: Scenario, interpreter: str) -> str:
        """ Interprets the given scenario by using the requested interpreter. """
        if interpreter.lower() == cls.Type.XML.value.lower():
            return interpret_xml(scenario)
#        if interpreter.lower() == cls.Type.JSON.value.lower():
#            return interpret_json(scenario)
#        if interpreter.lower() == cls.Type.YAML.value.lower():
#            return interpret_yaml(scenario)
        else:
            raise InterpretationError("{} not supported".format(type),
                                      InterpretationError.Code.NOT_SUPPORTED)


def interpret_xml(statement: Any, indentation: int = 0, index: int = None) -> str:
    """ Provides the XML interpretation for the given scenario. """
    logger.debug("interpret_xml: statement [{}], indentation [{}]".format(
        statement.__class__.__name__,
        indentation))

    if statement is None:
        return ''

    xml = ''
    if indentation == 0:
        xml += '<?xml version="1.0"?>\n'

    if index is None:
        xml += '{}<{} {}="{}">\n'.format(
            INDENT_SPACE * indentation,
            statement.__class__.__name__,
            PROPERTY_ENTITY,
            PROPERTY_VALUE_OBJECT)
    else:
        xml += '{}<{} {}="{}" {}="{}">\n'.format(
            INDENT_SPACE * indentation,
            statement.__class__.__name__,
            PROPERTY_ENTITY,
            PROPERTY_VALUE_OBJECT,
            PROPERTY_INDEX,
            index)
    # Inspects the object's variables (discarding the reserved ones)
    for key in statement.__dict__.keys():
        if not key.startswith(ATTRIBUTE_RESERVED_PREFIX):
            logger.debug("attribute: {}".format(key))
            if isinstance(statement.__dict__[key], (int, float, bool, str)):
                logger.debug("type: int, float, bool, str")
                xml += '{}<{} {}="{}" {}="{}">\n'.format(
                    INDENT_SPACE * (indentation + 1),
                    key,
                    PROPERTY_ENTITY,
                    PROPERTY_VALUE_ATTRIBUTE,
                    PROPERTY_TYPE,
                    statement.__dict__[key].__class__.__name__)
                xml += '{}{}\n'.format(
                    INDENT_SPACE * (indentation + 2),
                    statement.__dict__[key])
            elif isinstance(statement.__dict__[key], (list, tuple)):
                logger.debug("type: list, tuple")
                xml += '{}<{} {}="{}" {}="{}" {}="{}">\n'.format(
                    INDENT_SPACE * (indentation + 1),
                    key,
                    PROPERTY_ENTITY,
                    PROPERTY_VALUE_ATTRIBUTE,
                    PROPERTY_TYPE,
                    statement.__dict__[key].__class__.__name__,
                    PROPERTY_LENGTH,
                    len(statement.__dict__[key]))
                for index, item in enumerate(statement.__dict__[key]):
                    xml += interpret_xml(item, indentation + 2, index)
            elif isinstance(statement.__dict__[key], dict):
                logger.debug("type: dict")
                xml += '{}<{} {}="{}" {}="{}" {}="{}">\n'.format(
                    INDENT_SPACE * (indentation + 1),
                    key,
                    PROPERTY_ENTITY,
                    PROPERTY_VALUE_ATTRIBUTE,
                    PROPERTY_TYPE,
                    statement.__dict__[key].__class__.__name__,
                    PROPERTY_LENGTH,
                    len(statement.__dict__[key]))
                for index, subkey in enumerate(statement.__dict__[key].keys()):
                    xml += interpret_xml(statement.__dict__[key][subkey], indentation + 2, index)
            else: # Anything else
                logger.debug("type: not built-in")
                xml += '{}<{} {}="{}" {}="{}">\n'.format(
                    INDENT_SPACE * (indentation + 1),
                    key,
                    PROPERTY_ENTITY,
                    PROPERTY_VALUE_ATTRIBUTE,
                    PROPERTY_TYPE,
                    statement.__dict__[key].__class__.__name__)
                xml += interpret_xml(statement.__dict__[key], indentation + 2)
            xml += '{}</{}>\n'.format(
                INDENT_SPACE * (indentation + 1),
                key)
    logger.debug("closing class name {}".format(statement.__class__.__name__))
    xml += '{}</{}>\n'.format(
        INDENT_SPACE * indentation,
        statement.__class__.__name__)
    return xml


#def interpret_json(scenario: Scenario) -> str:
#    """ Provides the YAML interpretation for the given scenario. """
#    return ''


#def interpret_yaml(scenario: Scenario) -> str:
#    """ Provides the JSON interpretation for the given scenario. """
#    return ''
