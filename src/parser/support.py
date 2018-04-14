# -*- coding: utf-8 -*-
""" This module contains the infrastructure to support the definition of tokens.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""


from enum import unique, Enum


@unique
class Token(Enum):
    """ Supports the definition of pairs <TOKEN, KEYWORD>.

    This class make it possible to map a token onto the related keyword,
    by ensuring the uniqueness of both the tokens and the keywords.
    """

    @classmethod
    def tokens(cls):
        """ Gets the tokens of the current instance. """
        return _get_tuple_names_from_enum(cls)

    @classmethod
    def keywords(cls):
        """ Gets the keywords of the current instance. """
        return _get_tuple_values_from_enum(cls)

    @classmethod
    def reverse_map(cls):
        """ Gets the reverse map of the current instance. """
        return _get_dict_value_to_name_from_enum(cls)


def _get_tuple_names_from_enum(cls):
    """ Gets the tuple of the names from the given Enum class. """
    return tuple(e.name for e in cls)


def _get_tuple_values_from_enum(cls):
    """ Gets the tuple of the values from the given Enum class. """
    return tuple(e.value for e in cls)


def _get_dict_value_to_name_from_enum(cls):
    """
    Gets the dictionary mapping the values onto the related names
    from the given Enum class.
    """
    d = {}
    for e in cls:
        d[e.value] = e.name
    return d

