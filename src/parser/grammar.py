# -*- coding: utf-8 -*-
""" This module contains the AML's parsing engine.

Author:
    Francesco Racciatti

Copyright (C) 2018

"""

import logging
from mypy_extensions import NoReturn
from typing import List, Any

from ply import yacc
from ply.yacc import YaccProduction

from lexer import *
from model.oom import *
from enum import unique, Enum
from _ast import keyword
from builtins import property


logger = logging.getLogger(__name__)


class UnrecognizedError(Exception):
    """ Exception caused by an unrecognized entity. """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message : str = message

    def __str__(self):
        return basestr(self)
    
    def __repr__(self):
        return baserepr(self)


class InvalidArgumentError(Exception):
    """ Exception caused by an invalid argument. """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message : str = message

    def __str__(self):
        return basestr(self)
    
    def __repr__(self):
        return baserepr(self)


class Associativity(object):
    """ Operator associativity. """
    LEFT: str = 'left'
    RIGHT: str = 'right'


@unique
class ProductionType(Enum):
    """ The type of the production by Yacc. """
    ACTION = 'action'


class SymbolTable(object):
    """ Models the global symbol table. """

    # The global symbol table
    symbol_table: Dict[str, Any] = dict()
    
    @classmethod
    def store(cls, identifier: str, type: Keyword, value: str) -> str:
        """ Defines the given symbol. """
        if identifier is None:
            symbol = Literal(type.lexeme, value)
        else:
            symbol = Variable(identifier, type.lexeme, value)
        cls.symbol_table[symbol.identifier] = symbol
        return symbol

    @classmethod
    def retrieve(cls, identifier: str) -> Any:
        """ Retrieves the symbol having the given identifier. """
        return symbol_table.get(identifier, None)


class CurrentScope(object):
    """ Supports the parsing engine to build the current scope representation. """
        
    # The list of the actions contained in the current scope
    actions: List[Any] = list()
    
    @classmethod
    def append(cls, entity: Any, type: ProductionType) -> None:
        """ Appends the given entity of the given type to the related data structure. """
        if type == ProductionType.ACTION:
            cls.actions.append(entity)
        else:
            raise UnrecognizedError("Cannot append the entity {}, unrecognized type {}".format(entity, type))

    @classmethod
    def get(cls, type: ProductionType) -> List[Any]:
        """ Gets the given production type related list. """
        if type == ProductionType.ACTION:
            return cls.actions
        else:
            raise UnrecognizedError("Cannot get the data for the type {}".format(type))

    @classmethod
    def clean(cls) -> None:
        """ Cleans the data structures of the current scope. """
        cls.actions = list()


# Handles syntax errors
def p_error(p: YaccProduction) -> NoReturn:
    raise RuntimeError("Wrong syntax for the token '{}' - line {}".format(
        str(p.value), p.lineno))


# Handles empty productions
def p_empty(p: YaccProduction) -> None:
    '''
    empty :
    '''
    logger.debug("Yacc production: {}".format(p[1:]))


# Catches a number of semicolons 
def p_semicolons(p: YaccProduction) -> None:
    '''
    semicolons : SEMICOLON
               | SEMICOLON semicolons
    '''
    logger.debug("Yacc production: {}".format(p[1:]))


# Catches a literal integer
def p_literal_integer(p: YaccProduction) -> Literal:
    '''
    literal_integer : LITERAL_INTEGER
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = SymbolTable.store(None, Keyword.INTEGER, p[1])


# Catches a literal string
def p_literal_string(p: YaccProduction) -> Literal:
    '''
    literal_string : LITERAL_STRING
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = SymbolTable.store(None, Keyword.STRING, p[1])


# Catches a literal float
def p_literal_float(p: YaccProduction) -> Literal:
    '''
    literal_float : LITERAL_FLOAT
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = SymbolTable.store(None, Keyword.FLOAT, p[1])


# Catches a literal char
def p_literal_char(p: YaccProduction) -> Literal:
    '''
    literal_char : LITERAL_CHAR
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = SymbolTable.store(None, Keyword.CHAR, p[1])
    

# The parsing entry point
def p_entry_point(p: YaccProduction) -> Scenario:
    '''
    entry_point : empty
                | scenario_compound_statement
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = p[1]


# Catches the scenario's compound statement
def p_scenario_compound_statement(p: YaccProduction) -> Scenario:
    '''
    scenario_compound_statement : SCENARIO CURVY_L scenario_block_content CURVY_R
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = p[3]


# Catches the scenario's block content
def p_scenario_block_content(p: YaccProduction) -> Scenario:
    '''
    scenario_block_content : empty empty
                           | configuration_compound_statement empty
                           | attack_compound_statement empty
                           | configuration_compound_statement attack_compound_statement
                           | attack_compound_statement configuration_compound_statement
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    # TODO add the symbol table
    # TODO add the expression table
    # Builds the scenario
    if isinstance(p[1], Configuration):
        p[0] = Scenario(p[1], p[2])
    elif isinstance(p[1], Attack):
        p[0] = Scenario(p[2], p[1])
    else: # Empty block content
        p[0] = Scenario(None, None)
    # TODO clean the current scope


# Catches the configuration's compound statement
def p_configuration_compound_statement(p: YaccProduction) -> Configuration:
    '''
    configuration_compound_statement : CONFIGURATION CURVY_L configuration_block_content CURVY_R
    '''
    # Scans the current scope's list to build the configuration
    logger.debug("Yacc production: {}".format(p[1:]))
    configuration = Configuration(CurrentScope.get(ProductionType.ACTION))
    CurrentScope.clean()
    p[0] = configuration


# Catches the configuration's block content
def p_configuration_block_content(p: YaccProduction) -> None:
    '''
    configuration_block_content : configuration_action_set
    '''
    # Supports the looping of the parser inside the configuration block
    logger.debug("Yacc production: {}".format(p[1:]))


# Catches the set of actions contained inside the configuration's block 
def p_configuration_action_set(p: YaccProduction) -> None:
    '''
    configuration_action_set : configuration_action
                             | configuration_action configuration_action_set
    '''
    # Fills the current scope with the configuration's actions
    logger.debug("Yacc production: {}".format(p[1:]))
    CurrentScope.append(p[1], ProductionType.ACTION)


# Catches the configuration actions
def p_configuration_action(p: YaccProduction) -> Any:
    '''
    configuration_action : action_set_unit_time
                         | action_set_unit_length
                         | action_set_unit_angle
                         | action_set_time_start
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = p[1]


# Catches the action 'setUnitTime'
def p_action_set_unit_time(p: YaccProduction) -> SetUnitTime:
    '''
    action_set_unit_time : SET_UNIT_TIME ROUND_L literal_string ROUND_R semicolons
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = SetUnitTime(p[3].identifier)


# Catches the action 'setUnitLength'
def p_action_set_unit_length(p: YaccProduction) -> SetUnitLength:
    '''
    action_set_unit_length : SET_UNIT_LENGTH ROUND_L literal_string ROUND_R semicolons
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = SetUnitLength(p[3].identifier)


# Catches the action 'setUnitAngle'
def p_action_set_unit_angle(p: YaccProduction) -> SetUnitAngle:
    '''
    action_set_unit_angle : SET_UNIT_ANGLE ROUND_L literal_string ROUND_R semicolons
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = SetUnitAngle(p[3].identifier)


# Catches the action 'setTimeStart'
def p_action_set_time_start(p: YaccProduction) -> SetTimeStart:
    '''
    action_set_time_start : SET_TIME_START ROUND_L literal_float ROUND_R semicolons
                          | SET_TIME_START ROUND_L literal_integer ROUND_R semicolons
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    # Time cannot be negative
    if p[3].value < 0.0:
        raise InvalidArgumentError("Time cannot be negative, line {}".format(p.lineno(1)))
    p[0] = SetTimeStart(p[3].identifier)


# Catches the attack's compound statement
def p_attack_compound_statement(p: YaccProduction) -> None:
    '''
    attack_compound_statement : ATTACK CURVY_L empty CURVY_R
    '''
    # TODO this is a stub, to be implemented
    pass


# Builds the parser end define the entry point
parser = yacc.yacc(start='entry_point')

