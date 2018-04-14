#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" The unit test for Py-ADeLe.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""


import unittest
import sys


sys.path.append('../')
sys.path.append('../src/')
sys.path.append('../src/parser/')
from src.parser.tokens import Keyword, Punctuation


class TestPyAdele(unittest.TestCase):
    """ This class contains the entire set of tests of PyAdele. """

    def test_token_uniqueness(self):
        """ Tests the uniqueness of all the tokens. """
        intersection = set(Keyword.tokens()).intersection(set(Punctuation.tokens()))
        if any(intersection):
            self.fail("Duplicated token(s): " + str(intersection))

    def test_keyword_uniqueness(self):
        """ Tests the uniqueness of all the keywords. """
        intersection = set(Keyword.keywords()).intersection(set(Punctuation.keywords()))
        if any(intersection):
            self.fail("Duplicated keywords(s): " + str(intersection))

if __name__ == '__main__':
    unittest.main()