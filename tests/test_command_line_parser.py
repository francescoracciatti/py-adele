#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" The unit test for the command line parser of Py-ADeLe.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""


import sys
sys.path.append('../')
sys.path.append('../src/')
sys.path.append('../src/parser/')

import unittest

from src.commandline.option import get_command_line_arguments


class TestCommandLineParser(unittest.TestCase):
    """ Full test set for the command line parser of PyADeLe. """

    def setUp(self):
        unittest.TestCase.setUp(self)

    def test_all_arguments(self):
        """ Tests the correctness of the command line arguments parser
        by using the full arguments set.
        """
        cmd = ['-s', 'sources/empty.adele', '-i', 'xml', '-o', 'output', '-f']
        argument = get_command_line_arguments(cmd)
        self.assertEqual(argument.source, cmd[1])
        self.assertEqual(argument.interpreter, cmd[3])
        self.assertEqual(argument.output, cmd[5])
        self.assertTrue(argument.force)

    def test_guard_on_argument_unrecognizable(self):
        """ Tests the guard for unrecognizable arguments. """
        cmd = ['-s', 'sources/empty.adele', '-i', 'xml', '-o', 'output', '-u']
        with self.assertRaises(SystemExit) as e:
            get_command_line_arguments(cmd)
        self.assertEqual(e.exception.code, 2)

    def test_mandatory_arguments_only(self):
        """ Tests the correctness of the command line arguments parser
        by using only the mandatory arguments. 
        """
        cmd = ['-s', 'sources/empty.adele', '-i', 'xml']
        argument = get_command_line_arguments(cmd)
        self.assertEqual(argument.source, cmd[1])
        self.assertEqual(argument.interpreter, cmd[3])

    def test_guard_on_missing_argument_source(self):
        """ Tests the guard for the lack of the argument 'source'. """
        cmd = ['-i', 'xml']
        with self.assertRaises(SystemExit) as e:
            get_command_line_arguments(cmd)
        self.assertEqual(e.exception.code, 2)

    def test_guard_on_missing_argument_interpreter(self):
        """ Tests the guard for the lack of the argument 'interpreter'. """
        cmd = ['-s', 'sources/empty.adele']
        with self.assertRaises(SystemExit) as e:
            get_command_line_arguments(cmd)
        self.assertEqual(e.exception.code, 2)

    def tearDown(self):
        unittest.TestCase.tearDown(self)


if __name__ == '__main__':
    unittest.main()