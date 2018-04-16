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
    (Associativity.LEFT, Punctuation.EXP.token),
    #(Associativity.RIGHT, 'USUB', 'UNEG')
)


class Global(object):
    """ Contains the global data structures which support the parsing engine. """
    
    # The configuration of the scenario
    configuration = Configuration()


# Handles syntax errors
def p_error(p):
    raise RuntimeError("wrong syntax for the token '{}' - line {}".format(
        str(p.value), p.lineno))


# Catches the entry point
def p_attack(p):
    '''
    scenario : SCENARIO CURVY_L CURVY_R
    '''
    scenario = Scenario()
    scenario.configuration = Global.configuration
    p[0] = scenario


# Builds the parser
parser = yacc.yacc(start=Keyword.SCENARIO.lexeme)

