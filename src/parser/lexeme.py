# -*- coding: utf-8 -*-
""" This module contains the facilities to support the definition
of the lexemes.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""


from enum import unique, Enum
from types import DynamicClassAttribute


@unique
class Lexeme(Enum):
    """ Supports the definition of lexemes.

    This class make it possible to map a token onto the related lexeme,
    by ensuring the uniqueness of both the tokens and the lexemes.
    """

    @DynamicClassAttribute
    def token(self):
        """ The token of the Lexeme member. """
        return self._name_

    @DynamicClassAttribute
    def lexeme(self):
        """ The lexeme of the Lexeme member. """
        return self._value_

    @classmethod
    def tokens(cls):
        """ Gets the tokens of Lexeme. """
        return _get_tuple_names_from_enum(cls)

    @classmethod
    def lexemes(cls):
        """ Gets the lexemes of Lexeme. """
        return _get_tuple_values_from_enum(cls)

    @classmethod
    def reverse_map(cls):
        """ Gets the reverse map of Lexeme. """
        return _get_dict_value_to_name_from_enum(cls)


def _get_tuple_names_from_enum(cls):
    """ Gets the tuple of the names from the given Enum instance. """
    return tuple(e.name for e in cls)


def _get_tuple_values_from_enum(cls):
    """ Gets the tuple of the values from the given Enum instance. """
    return tuple(e.value for e in cls)


def _get_dict_value_to_name_from_enum(cls):
    """
    Gets the dictionary mapping the values onto the related names
    from the given Enum instance.
    """
    d = {}
    for e in cls:
        d[e.value] = e.name
    return d

