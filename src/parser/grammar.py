# -*- coding: utf-8 -*-
""" This module contains the AML's parsing engine.

Author:
    Francesco Racciatti

Copyright (C) 2018

"""

import logging
from mypy_extensions import NoReturn
from typing import Any

from ply import yacc
from ply.yacc import YaccProduction

from lexer import *
from model.model import Scenario, Configuration


logger = logging.getLogger(__name__)


class Associativity(object):
    """ Operator associativity. """
    LEFT: str   = 'left'
    RIGHT: str  = 'right'


class Global(object):
    """ Contains the global data structures which support the parsing engine. """
    
    # The configuration of the scenario
    configuration: Configuration = Configuration()


# Handles syntax errors
def p_error(p: YaccProduction) -> NoReturn:
    raise RuntimeError("Wrong syntax for the token '{}' - line {}".format(
        str(p.value), p.lineno))


# Handles empty productions
def p_empty(p: YaccProduction) -> None:
    '''
    empty :
    '''
    pass


# Catches the scenario's compound statement, which is the entry point
def p_compound_statement_scenario(p: YaccProduction) -> Any:
    '''
    compound_statement_scenario : SCENARIO CURVY_L empty CURVY_R
    '''
    p[0] = None

#    '''
#    compound_statement_scenario : SCENARIO CURVY_L compound_statement_content_scenario CURVY_R
#    '''
#    p[0] = p[3]


# Catches the content of the scenario's compound statement
#def p_compound_statement_content_scenario(p):
#    '''
    
#    compound_statement_content_scenario : empty                             empty
#                                        | SEMICOLON                         empty
#                                        | compound_statement_configuration  empty
#                                        | compound_statement_attack         empty
#                                        | compound_statement_configuration  compound_statement_attack
#                                        | compound_statement_attack         compound_statement_configuration
#    '''
#    pass




# Builds the parser end define the entry point
parser = yacc.yacc(start='compound_statement_scenario')

