#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" The unit test for the validate argument function of Py-ADeLe.

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

from src.shell.options import Argument
from src.shell.service import ValidationError, validate_argument


class TestValidateArgument(unittest.TestCase):
    """ Full test set for the validate argument function of PyADeLe. """

    def setUp(self):
        unittest.TestCase.setUp(self)

    def test_validation_when_source_file_does_not_exist_then_raise_validation_exception(self):
        """ Tests the validation function when the source file does not exist. """
        argument = Argument('source/unexisting-file', 'xml', '', False)
        with self.assertRaises(ValidationError) as e:
            validate_argument(argument)
        self.assertEqual(e.exception.code, ValidationError.Code.NOT_EXIST)

    def test_validation_when_source_file_is_not_a_file_then_raise_validation_exception(self):
        """ Tests the validation function when the source path does not refer a file. """
        argument = Argument('source', 'xml', '', False)
        with self.assertRaises(ValidationError) as e:
            validate_argument(argument)
        self.assertEqual(e.exception.code, ValidationError.Code.NOT_FILE)

    def test_validation_when_interpreter_not_supported_then_raise_validation_exception(self):
        """ Tests the validation function when the interpreter is not supported. """
        argument = Argument('source/empty.adele', 'unexisting-interpreter', '', False)
        with self.assertRaises(ValidationError) as e:
            validate_argument(argument)
        self.assertEqual(e.exception.code, ValidationError.Code.NOT_SUPPORTED)

    def test_validation_when_output_file_is_not_a_file_without_force_overwrite_then_raise_validation_exception(self):
        """ Tests the validation function when the output path does not refer a file,
        without the force overwrite option. """
        argument = Argument('source/empty.adele', 'xml', 'source', False)
        with self.assertRaises(ValidationError) as e:
            validate_argument(argument)
        self.assertEqual(e.exception.code, ValidationError.Code.NOT_FILE)

    def test_validation_when_output_file_is_not_a_file_with_force_overwrite_then_raise_validation_exception(self):
        """ Tests the validation function when the output path does not refer a file,
        without the force overwrite option. """
        argument = Argument('source/empty.adele', 'xml', 'source', True)
        with self.assertRaises(ValidationError) as e:
            validate_argument(argument)
        self.assertEqual(e.exception.code, ValidationError.Code.NOT_FILE)

    def tearDown(self):
        unittest.TestCase.tearDown(self)


if __name__ == '__main__':
    unittest.main()