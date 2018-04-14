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
from src.parser.keyword import Keyword, Punctuation


class TestPyAdele(unittest.TestCase):
    """ This class contains the entire set of tests of PyAdele. """

    def test_token_uniqueness(self):
        """ Tests the uniqueness of all the tokens. """
        intersection = set(Keyword.get_list_tokens()).intersection(set(Punctuation.get_list_tokens()))
        if any(intersection):
            self.fail("Duplicated token(s): " + str(intersection))

    def test_keyword_uniqueness(self):
        """ Tests the uniqueness of all the keywords. """
        intersection = set(Keyword.get_list_keywords()).intersection(set(Punctuation.get_list_keywords()))
        if any(intersection):
            self.fail("Duplicated keywords(s): " + str(intersection))

if __name__ == '__main__':
    unittest.main()