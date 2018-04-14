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
    def get_list_tokens(cls):
        """ Gets the list of the tokens. """
        return _get_list_names_from_enum(cls)

    @classmethod
    def get_list_keywords(cls):
        """ Gets the list of the keywords. """
        return _get_list_values_from_enum(cls)

    @classmethod
    def get_dict_keyword_to_token(cls):
        """ Gets the dict mapping the (unique) keywords onto the related (unique) tokens. """
        return _get_dict_value_to_name_from_enum(cls)


def _get_list_names_from_enum(cls):
    """ Gets the list of the names from the given Enum class. """
    return [e.name for e in cls]

def _get_list_values_from_enum(cls):
    """ Gets the list of the values from the given Enum class. """
    return [e.value for e in cls]

def _get_dict_value_to_name_from_enum(cls):
    """
    Gets the dictionary mapping the values onto the related names
    from the given Enum class.
    """
    d = {}
    for e in cls:
        d[e.value] = e.name
    return d
