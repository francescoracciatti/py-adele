#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" The unit test for the validations of the arguments of Py-ADeLe.

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
from unittest import mock

from src.shell.options import Argument
from src.shell.service import SourceFileNotFoundError, NotAFileError, UnrecognizedInterpreterError, validate_argument


class TestArguments(unittest.TestCase):
    """ Full test set for the validate argument function of PyADeLe. """

    def setUp(self):
        unittest.TestCase.setUp(self)

    def test_validation_when_source_file_does_not_exist_then_raise_exception(self):
        """ Tests the validation function when the source file does not exist. """
        argument = Argument('source/unexisting-file', 'xml', '', False)
        with self.assertRaises(SourceFileNotFoundError) as e:
            validate_argument(argument)

    def test_validation_when_source_file_is_not_a_file_then_raise_exception(self):
        """ Tests the validation function when the source path does not refer a file. """
        argument = Argument('source', 'xml', '', False)
        with self.assertRaises(NotAFileError) as e:
            validate_argument(argument)

    def test_validation_when_interpreter_not_supported_then_raise_exception(self):
        """ Tests the validation function when the interpreter is not supported. """
        argument = Argument('source/empty.adele', 'unexisting-interpreter', '', False)
        with self.assertRaises(UnrecognizedInterpreterError) as e:
            validate_argument(argument)

    def test_validation_when_output_file_is_not_a_file_without_force_overwrite_then_raise_exception(self):
        """ Tests the validation function when the output path does not refer a file,
        without the force overwrite option. """
        argument = Argument('source/empty.adele', 'xml', 'source', False)
        with self.assertRaises(NotAFileError) as e:
            validate_argument(argument)

    def test_validation_when_output_file_is_not_a_file_with_force_overwrite_then_raise_exception(self):
        """ Tests the validation function when the output path does not refer a file,
        without the force overwrite option. """
        argument = Argument('source/empty.adele', 'xml', 'source', True)
        with self.assertRaises(NotAFileError) as e:
            validate_argument(argument)

    def test_validation_when_output_file_exists_with_force_overwrite(self):
        """ Tests the validation function when the output path refers a file,
        with the force overwrite option. """
        source = 'source/empty.adele'
        interpreter = 'xml'
        output = 'source/empty.xml'
        argument = Argument(source, interpreter, output, True)
        validate_argument(argument)
        self.assertEqual(argument.source, source)
        self.assertEqual(argument.interpreter, interpreter)
        self.assertEqual(argument.output, output)
    
    @mock.patch('src.shell.service.input', create=True)
    def test_validation_when_output_file_exists_check_overwrite_yes(self, mocked_input):
        """ Tests the validation function when the output path refers a file,
        without the force overwrite option, with the mocked input function (passes yes). """
        mocked_input.side_effect = ['yes']
        source = 'source/empty.adele'
        interpreter = 'xml'
        output = 'source/empty.xml'
        argument = Argument(source, interpreter, output, False)
        validate_argument(argument)
        self.assertEqual(argument.source, source)
        self.assertEqual(argument.interpreter, interpreter)
        self.assertEqual(argument.output, output)
    
    @mock.patch('src.shell.service.input', create=True)
    def test_validation_when_output_file_exists_check_overwrite_no(self, mocked_input):
        """ Tests the validation function when the output path refers a file,
        without the force overwrite option, with the mocked input function (passes no). """
        mocked_input.side_effect = ['no']
        argument = Argument('source/empty.adele', 'xml', 'source/empty.xml', False)
        with self.assertRaises(SystemExit) as e:
            validate_argument(argument)

    def tearDown(self):
        unittest.TestCase.tearDown(self)


if __name__ == '__main__':
    unittest.main()

