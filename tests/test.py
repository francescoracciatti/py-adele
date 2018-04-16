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
sys.path.append('../src/parser/')

import unittest

from src.parser.lexer import Keyword, Punctuation, Literal


class TestPyAdele(unittest.TestCase):
    """ This class contains the entire set of tests for PyAdele. """

    def test_uniqueness_tokens(self):
        """ Tests the uniqueness of all the tokens. """
        intersection = set.union(
            set(Keyword.tokens()) & set(Punctuation.tokens()),
            set(Keyword.tokens()) & set(Literal.tokens()),
            set(Literal.tokens()) & set(Punctuation.tokens()) )
        if any(intersection):
            self.fail("Duplicated token(s): " + str(intersection))

    def test_uniqueness_lexemes(self):
        """ Tests the uniqueness of all the lexemes. """
        intersection = set.union(
            set(Keyword.lexemes()) & set(Punctuation.lexemes()),
            set(Keyword.lexemes()) & set(Literal.lexemes()),
            set(Literal.lexemes()) & set(Punctuation.lexemes()) )
        if any(intersection):
            self.fail("Duplicated keywords(s): " + str(intersection))

    def test_minimal(self):
        """ TODO TBI 
        
        To perform the test it is necessary to have:
          + xml writer
          + xml comparator
          + xml comparison source
        """
        pass


if __name__ == '__main__':
    unittest.main()