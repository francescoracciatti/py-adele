# -*- coding: utf-8 -*-
""" This module contains the facilities to support the definition
of the lexemes.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""


from enum import unique, Enum
from types import DynamicClassAttribute
from typing import Tuple, Dict

@unique
class Lexeme(Enum):
    """ Supports the definition of lexemes.

    This class make it possible to map a token onto the related lexeme,
    by ensuring the uniqueness of both the tokens and the lexemes.
    """

    @DynamicClassAttribute
    def token(self) -> str:
        """ The token of the Lexeme member. """
        return self.name

    @DynamicClassAttribute
    def lexeme(self) -> str:
        """ The lexeme of the Lexeme member. """
        return self.value

    @classmethod
    def tokens(cls) -> Tuple[str, ...]:
        """ Gets the tuple containing the tokens of Lexeme. """
        return tuple(e.name for e in cls)

    @classmethod
    def lexemes(cls) -> Tuple[str, ...]:
        """ Gets the tuple containing the lexemes of Lexeme. """
        return tuple(e.value for e in cls)

    @classmethod
    def reverse_map(cls) -> Dict[str, str]:
        """ Gets the reverse map of Lexeme. """
        d: Dict[str, str] = {}
        for e in cls:
            d[e.value] = e.name
        return d

