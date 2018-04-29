#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" The unit test for Py-ADeLe.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""


import sys
sys.path.append('../')
sys.path.append('../src/')
sys.path.append('../src/model/')
sys.path.append('../src/parser/')
sys.path.append('../src/shell/')

import unittest

from src.parser.lexer import Keyword, Punctuation, Literal


class TestLexer(unittest.TestCase):
    """ Full test set for the Lexer of PyAdele. """

    def setUp(self):
        unittest.TestCase.setUp(self)

    def test_lexer_ensure_uniqueness_tokens(self):
        """ Tests the uniqueness of all the tokens. """
        intersection = set.union(
            set(Keyword.tokens()) & set(Punctuation.tokens()),
            set(Keyword.tokens()) & set(Literal.tokens()),
            set(Literal.tokens()) & set(Punctuation.tokens()) )
        if any(intersection):
            self.fail("Duplicated token(s): " + str(intersection))

    def test_lexer_ensure_uniqueness_lexemes(self):
        """ Tests the uniqueness of all the lexemes. """
        intersection = set.union(
            set(Keyword.lexemes()) & set(Punctuation.lexemes()),
            set(Keyword.lexemes()) & set(Literal.lexemes()),
            set(Literal.lexemes()) & set(Punctuation.lexemes()) )
        if any(intersection):
            self.fail("Duplicated keywords(s): " + str(intersection))

    def tearDown(self):
        unittest.TestCase.tearDown(self)


if __name__ == '__main__':
    unittest.main()