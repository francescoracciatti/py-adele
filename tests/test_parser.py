#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" The unit test for the parsing engine of Py-ADeLe.

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
sys.path.append('../src/util/')

import unittest

from src.parser.grammar import *

class TestParser(unittest.TestCase):
    """ Full test set for the parsing engine of PyADeLe. """

    def setUp(self):
        unittest.TestCase.setUp(self)

    def test_redefinition_variable_same_line(self):
        """ Tests the guard on the already defined variables on the same line. """
        try:
            with open('source/test-guard-variable-declaration-same-line.adele', 'r') as filesource:
                sourcecode = filesource.read()
            scenario = parser.parse(sourcecode)
        except RuntimeAssertError:
            return

    def test_redefinition_variable_same_scope(self):
        """ Tests the guard on the already defined variables in the same scope. """
        try:
            with open('source/test-guard-variable-declaration-same-scope.adele', 'r') as filesource:
                sourcecode = filesource.read()
            scenario = parser.parse(sourcecode)
        except RuntimeAssertError:
            return

    def test_complete_scenario(self):
        """ Tests the working complete scenario."""
        with open('source/test-complete.adele', 'r') as filesource:
            sourcecode = filesource.read()
        scenario = parser.parse(sourcecode)

    def tearDown(self):
        unittest.TestCase.tearDown(self)


if __name__ == '__main__':
    unittest.main()