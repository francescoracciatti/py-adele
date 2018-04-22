# -*- coding: utf-8 -*-
""" This module contains the AML's parsing engine.

Author:
    Francesco Racciatti

Copyright (C) 2018

"""

import logging

from ply import yacc

from lexer import *
from model.model import Scenario, Configuration


logger = logging.getLogger(__name__)


class Associativity(object):
    """ Operator associativity. """
    LEFT    = 'left'
    RIGHT   = 'right'


# Parsing rules precedence and associativity
precedence = (
    (Associativity.LEFT, Punctuation.ADD.token, Punctuation.SUB.token),
    (Associativity.LEFT, Punctuation.MUL.token, Punctuation.DIV.token),
    (Associativity.LEFT, Punctuation.EXP.token)
)


class Global(object):
    """ Contains the global data structures which support the parsing engine. """
    
    # The configuration of the scenario
    configuration = Configuration()


# Handles syntax errors
def p_error(p):
    raise RuntimeError("Wrong syntax for the token '{}' - line {}".format(
        str(p.value), p.lineno))


# Handles empty productions
def p_empty(p):
    '''
    empty :
    '''
    pass


# Catches the scenario's compound statement, which is the entry point
def p_compound_statement_scenario(p):
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

