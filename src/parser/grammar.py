# -*- coding: utf-8 -*-
""" This module contains the AML's parsing engine.

Author:
    Francesco Racciatti

Copyright (C) 2018

"""

import logging
from enum import unique, Enum
from mypy_extensions import NoReturn
from typing import List, Any

from ply import yacc
from ply.yacc import YaccProduction

from lexer import *
from model.oom import *
from mypy import scope


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


class RuntimeAssertError(Exception):
    """ Exception caused by an assetion failing. """

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
    """ The type of the YACC production. """
    ACTION = 'action'
    IDENTIFIER = 'identifier'


class ScopeHandler(object):
    """ Handles the variables' scopes. """

    # Codes the actual scope
    scopes: List[int] = list()

    # The current scope
    current_scope: int = -1;

    @classmethod
    def open_scope(cls) -> None:
        """ Opens a new scope. """
        # Enlarges the list
        if ( cls.current_scope + 1 == len(cls.scopes) ):
            cls.scopes.append(-1)
        # Points-to the actual scope just opened
        cls.current_scope += 1
        # Update its identifier
        cls.scopes[cls.current_scope] += 1

    @classmethod
    def close_scope(cls) -> None:
        """ Closes a previous opened scope. """
        # Points to the actual scope (outer) 
        cls.current_scope -= 1

    @classmethod
    def get_current_scope_identifier(cls) -> str:
        """ Gets the identifier of the current scope. """
        if len(cls.scopes) == 0 or cls.current_scope < 0:
            return None
        scope_identifier = ''
        for i in range(0, cls.current_scope + 1):
            scope_identifier += str(cls.scopes[i]) 
        return scope_identifier

    @classmethod
    def get_scope_identifier(cls, scope: int) -> str:
        """ Gets the identifier of the current scope. """
        if len(cls.scopes) == 0 or cls.current_scope < 0:
            return None
        scope_identifier = ''
        for i in range (0, scope + 1):
            scope_identifier += str(cls.scopes[i])
        return scope_identifier

    @classmethod
    def get_global_scope_identifier(cls) -> str:
        """ Gets the global scope coded as string. """
        return '0'


class SymbolTable(object):
    """ Models a symbol table for a single scope. """

    # The symbol table, maps the identifier onto the related object
    symbol_table: Dict[str, Any] = dict()

    def store_literal(self, type: Keyword, value: str) -> Literal:
        """ Stores the given literal and returns its identifier. """
        symbol = Literal(type.lexeme, value)
        self.symbol_table[symbol.identifier] = symbol
        return symbol

    def store_variable(self, scope: str, identifier: str, type: Keyword, value: str) -> Variable:
        """ Stores the given variable and returns its identifier. """
        symbol = Variable(scope, identifier, type.lexeme, value)
        self.symbol_table[identifier] = symbol
        return symbol

    def retrieve(self, identifier: str) -> Any:
        """ Retrieves the symbol having the given identifier. """
        return self.symbol_table.get(identifier, None)

 
class GlobalSymbolTable(object):
    """ Models a multi scope symbol table to support scoped variables.
        
    Shadowing is not admitted.
    """
    
    # The multi scoped symbol table, maps a scope onto the related symbol table
    global_symbol_table: Dict[str, SymbolTable] = dict()

    @classmethod
    def store_literal(cls, type: Keyword, value: str) -> Literal:
        """ Stores the given literal into the global scope' symbol table. """
        scope = ScopeHandler.get_global_scope_identifier()
        if cls.global_symbol_table.get(scope, None) is None:
            cls.global_symbol_table[scope] = SymbolTable()
        symbol_table = cls.global_symbol_table[scope]
        return symbol_table.store_literal(type, value)

    @classmethod
    def store_variable(cls, scope: str, identifier: str, type: Keyword, value: str) -> Variable:
        """ Defines the given symbol. """
        if cls.global_symbol_table.get(scope, None) is None:
            cls.global_symbol_table[scope] = SymbolTable()
        symbol_table = cls.global_symbol_table[scope]
        return symbol_table.store_variable(scope, identifier, type, value)

    @classmethod
    def retrieve(cls, scope: str, identifier: str) -> Any:
        """ Retrieves the symbol having the given identifier. """
        symbol_table = cls.global_symbol_table.get(scope, None)
        if symbol_table is None:
            return None
        return symbol_table.retrieve(identifier)


class CurrentScope(object):
    """ Supports the parsing engine by containing the current entities. """
        
    # The list of the actions contained in the current scope
    actions: List[Any] = list()
    
    # The list of the literals contained in the current scope
    identifiers: List[Any] = list()
    
    @classmethod
    def append(cls, entity: Any, type: ProductionType) -> None:
        """ Appends the given entity of the given type to the related data structure. """
        if type == ProductionType.ACTION:
            cls.actions.append(entity)
        elif type == ProductionType.IDENTIFIER:
            cls.identifiers.append(entity)
        else:
            raise UnrecognizedError("Cannot append the entity {}, unrecognized type {}".format(entity, type))

    @classmethod
    def get(cls, type: ProductionType) -> List[Any]:
        """ Gets the given production type related list. """
        if type == ProductionType.ACTION:
            return cls.actions
        elif type == ProductionType.IDENTIFIER:
            return cls.identifiers
        else:
            raise UnrecognizedError("Cannot get the data for the type {}".format(type))

    @classmethod
    def clean(cls, type: ProductionType = None) -> None:
        """ Cleans the data structures of the current scope. """
        if type == ProductionType.ACTION:
            cls.actions = list()
        elif type == ProductionType.IDENTIFIER:
            cls.identifiers = list()
        else:
            cls.actions = list()
            cls.identifiers = list()


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


# Catches a curvy left bracket
def p_curvy_left(p: YaccProduction) -> None:
    '''
    curvy_left : CURVY_L
    '''
    ScopeHandler.open_scope()


# Catches a curvy right bracket
def p_curvy_right(p: YaccProduction) -> None:
    '''
    curvy_right : CURVY_R
    '''
    ScopeHandler.close_scope()


# Catches a literal boolean
def p_literal_boolean(p: YaccProduction) -> Literal:
    '''
    literal_boolean : TRUE
                    | FALSE
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = GlobalSymbolTable.store_literal(Keyword.BOOLEAN, p[1])


# Catches a literal char
def p_literal_char(p: YaccProduction) -> Literal:
    '''
    literal_char : LITERAL_CHAR
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = GlobalSymbolTable.store_literal(Keyword.CHAR, p[1])


# Catches a literal integer
def p_literal_integer(p: YaccProduction) -> Literal:
    '''
    literal_integer : LITERAL_INTEGER
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = GlobalSymbolTable.store_literal(Keyword.INTEGER, p[1])


# Catches a literal float
def p_literal_float(p: YaccProduction) -> Literal:
    '''
    literal_float : LITERAL_FLOAT
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = GlobalSymbolTable.store_literal(Keyword.FLOAT, p[1])


# Catches a literal string
def p_literal_string(p: YaccProduction) -> Literal:
    '''
    literal_string : LITERAL_STRING
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = GlobalSymbolTable.store_literal(Keyword.STRING, p[1])


# Catches an 8 bit unsigned integer
def p_literal_uint8(p: YaccProduction) -> Literal:
    '''
    literal_uint8 : UINT8
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = GlobalSymbolTable.store_literal(Keyword.UINT8, p[1])


# Catches a 16 bit unsigned integer
def p_literal_uint16(p: YaccProduction) -> Literal:
    '''
    literal_uint16 : UINT16
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = GlobalSymbolTable.store_literal(Keyword.UINT16, p[1])


# Catches a 32 bit unsigned integer
def p_literal_uint32(p: YaccProduction) -> Literal:
    '''
    literal_uint32 : UINT32
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = GlobalSymbolTable.store_literal(Keyword.UINT32, p[1])


# Catches a 64 bit unsigned integer
def p_literal_uint64(p: YaccProduction) -> Literal:
    '''
    literal_uint64 : UINT64
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = GlobalSymbolTable.store_literal(Keyword.UINT64, p[1])


# Catches an 8 bit signed integer
def p_literal_sint8(p: YaccProduction) -> Literal:
    '''
    literal_sint8 : SINT8
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = GlobalSymbolTable.store_literal(Keyword.SINT8, p[1])


# Catches a 16 bit signed integer
def p_literal_sint16(p: YaccProduction) -> Literal:
    '''
    literal_sint16 : SINT16
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = GlobalSymbolTable.store_literal(Keyword.SINT16, p[1])


# Catches a 32 bit signed integer
def p_literal_sint32(p: YaccProduction) -> Literal:
    '''
    literal_sint32 : SINT32
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = GlobalSymbolTable.store_literal(Keyword.SINT32, p[1])


# Catches a 64 bit unsigned integer
def p_literal_sint64(p: YaccProduction) -> Literal:
    '''
    literal_sint64 : SINT64
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = GlobalSymbolTable.store_literal(Keyword.SINT64, p[1])


# Catches a 32 bit floating point
def p_literal_float32(p: YaccProduction) -> Literal:
    '''
    literal_float32 : FLOAT32
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = GlobalSymbolTable.store_literal(Keyword.FLOAT32, p[1])


# Catches a 64 bit floating point
def p_literal_float64(p: YaccProduction) -> Literal:
    '''
    literal_float64 : FLOAT64
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = GlobalSymbolTable.store_literal(Keyword.FLOAT64, p[1])


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
    scenario_compound_statement : SCENARIO curvy_left scenario_block_content curvy_right
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    p[0] = p[3]

# >>>
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
#<<<

# Catches the configuration's compound statement
def p_configuration_compound_statement(p: YaccProduction) -> Configuration:
    '''
    configuration_compound_statement : CONFIGURATION curvy_left configuration_block_content curvy_right
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


def assert_not_already_declared(identifier: str, lineno: int) -> None:
    """ Raises a runtime error if the identifier was already declared. """
    # Checks the given identifier in the support data structure for the current scope
    if identifier in CurrentScope.get(ProductionType.IDENTIFIER):
        raise RuntimeAssertError("The identifier '{}' was already declared - line {}".format(
                identifier, lineno))
    # Checks the given identifier in the current scope and the outer ones 
    for scope in range(0, ScopeHandler.current_scope + 1):
        scope_identifier = ScopeHandler.get_scope_identifier(scope)
        if GlobalSymbolTable.retrieve(scope_identifier, identifier) is not None:
            raise RuntimeAssertError("The identifier '{}' was already declared - line {}".format(
                identifier, lineno))


# Catches an identifier used in declarations
def p_declaration_identifier(p: YaccProduction) -> None:
    '''
    declaration_identifier : LITERAL_IDENTIFIER
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    assert_not_already_declared(p[1], p.lineno(1))
    CurrentScope.append(p[1], ProductionType.IDENTIFIER)


# Catches a set of identifiers used in declarations
def p_declaration_identifier_set(p: YaccProduction) -> None:
    '''
    declaration_identifier_set : declaration_identifier
                               | declaration_identifier COMMA declaration_identifier_set
    '''
    logger.debug("Yacc production: {}".format(p[1:]))


# Catches the declaration of boolean variables
def p_declaration_boolean_set(p: YaccProduction) -> None:
    '''
    declaration_boolean_set : BOOLEAN declaration_identifier_set semicolons
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    # Stores the declared variable into the symbol table
    scope_identifier = ScopeHandler.get_current_scope_identifier()
    for identifier in CurrentScope.get(ProductionType.IDENTIFIER):
        GlobalSymbolTable.store_variable(scope_identifier, identifier, Keyword.BOOLEAN, None)
    CurrentScope.clean(ProductionType.IDENTIFIER)


# Catches the declaration of char variables
def p_declaration_char_set(p: YaccProduction) -> None:
    '''
    declaration_char_set : CHAR declaration_identifier_set semicolons
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    # Stores the declared variable into the symbol table
    scope_identifier = ScopeHandler.get_current_scope_identifier()
    for identifier in CurrentScope.get(ProductionType.IDENTIFIER):
        GlobalSymbolTable.store_variable(scope_identifier, identifier, Keyword.CHAR, None)
    CurrentScope.clean(ProductionType.IDENTIFIER)


# Catches the declaration of integer variables
def p_declaration_integer_set(p: YaccProduction) -> None:
    '''
    declaration_integer_set : INTEGER declaration_identifier_set semicolons
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    # Stores the declared variable into the symbol table
    scope_identifier = ScopeHandler.get_current_scope_identifier()
    for identifier in CurrentScope.get(ProductionType.IDENTIFIER):
        GlobalSymbolTable.store_variable(scope_identifier, identifier, Keyword.INTEGER, None)
    CurrentScope.clean(ProductionType.IDENTIFIER)


# Catches the declaration of float variables
def p_declaration_float_set(p: YaccProduction) -> None:
    '''
    declaration_float_set : FLOAT declaration_identifier_set semicolons
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    # Stores the declared variable into the symbol table
    scope_identifier = ScopeHandler.get_current_scope_identifier()
    for identifier in CurrentScope.get(ProductionType.IDENTIFIER):
        GlobalSymbolTable.store_variable(scope_identifier, identifier, Keyword.FLOAT, None)
    CurrentScope.clean(ProductionType.IDENTIFIER)


# Catches the declaration of string variables
def p_declaration_string_set(p: YaccProduction) -> None:
    '''
    declaration_string_set : STRING declaration_identifier_set semicolons
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    # Stores the declared variable into the symbol table
    scope_identifier = ScopeHandler.get_current_scope_identifier()
    for identifier in CurrentScope.get(ProductionType.IDENTIFIER):
        GlobalSymbolTable.store_variable(scope_identifier, identifier, Keyword.STRING, None)
    CurrentScope.clean(ProductionType.IDENTIFIER)


# Catches the declaration of uint8 variables
def p_declaration_uint8_set(p: YaccProduction) -> None:
    '''
    declaration_uint8_set : UINT8 declaration_identifier_set semicolons
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    # Stores the declared variable into the symbol table
    scope_identifier = ScopeHandler.get_current_scope_identifier()
    for identifier in CurrentScope.get(ProductionType.IDENTIFIER):
        GlobalSymbolTable.store_variable(scope_identifier, identifier, Keyword.UINT8, None)
    CurrentScope.clean(ProductionType.IDENTIFIER)


# Catches the declaration of uint16 variables
def p_declaration_uint16_set(p: YaccProduction) -> None:
    '''
    declaration_uint16_set : UINT16 declaration_identifier_set semicolons
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    # Stores the declared variable into the symbol table
    scope_identifier = ScopeHandler.get_current_scope_identifier()
    for identifier in CurrentScope.get(ProductionType.IDENTIFIER):
        GlobalSymbolTable.store_variable(scope_identifier, identifier, Keyword.UINT16, None)
    CurrentScope.clean(ProductionType.IDENTIFIER)


# Catches the declaration of uint32 variables
def p_declaration_uint32_set(p: YaccProduction) -> None:
    '''
    declaration_uint32_set : UINT32 declaration_identifier_set semicolons
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    # Stores the declared variable into the symbol table
    scope_identifier = ScopeHandler.get_current_scope_identifier()
    for identifier in CurrentScope.get(ProductionType.IDENTIFIER):
        GlobalSymbolTable.store_variable(scope_identifier, identifier, Keyword.UINT32, None)
    CurrentScope.clean(ProductionType.IDENTIFIER)


# Catches the declaration of uint64 variables
def p_declaration_uint64_set(p: YaccProduction) -> None:
    '''
    declaration_uint64_set : UINT64 declaration_identifier_set semicolons
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    # Stores the declared variable into the symbol table
    scope_identifier = ScopeHandler.get_current_scope_identifier()
    for identifier in CurrentScope.get(ProductionType.IDENTIFIER):
        GlobalSymbolTable.store_variable(scope_identifier, identifier, Keyword.UINT64, None)
    CurrentScope.clean(ProductionType.IDENTIFIER)


# Catches the declaration of sint8 variables
def p_declaration_sint8_set(p: YaccProduction) -> None:
    '''
    declaration_sint8_set : SINT8 declaration_identifier_set semicolons
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    # Stores the declared variable into the symbol table
    scope_identifier = ScopeHandler.get_current_scope_identifier()
    for identifier in CurrentScope.get(ProductionType.IDENTIFIER):
        GlobalSymbolTable.store_variable(scope_identifier, identifier, Keyword.SINT8, None)
    CurrentScope.clean(ProductionType.IDENTIFIER)


# Catches the declaration of sint16 variables
def p_declaration_sint16_set(p: YaccProduction) -> None:
    '''
    declaration_sint16_set : SINT16 declaration_identifier_set semicolons
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    # Stores the declared variable into the symbol table
    scope_identifier = ScopeHandler.get_current_scope_identifier()
    for identifier in CurrentScope.get(ProductionType.IDENTIFIER):
        GlobalSymbolTable.store_variable(scope_identifier, identifier, Keyword.SINT16, None)
    CurrentScope.clean(ProductionType.IDENTIFIER)


# Catches the declaration of sint32 variables
def p_declaration_sint32_set(p: YaccProduction) -> None:
    '''
    declaration_sint32_set : SINT32 declaration_identifier_set semicolons
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    # Stores the declared variable into the symbol table
    scope_identifier = ScopeHandler.get_current_scope_identifier()
    for identifier in CurrentScope.get(ProductionType.IDENTIFIER):
        GlobalSymbolTable.store_variable(scope_identifier, identifier, Keyword.SINT32, None)
    CurrentScope.clean(ProductionType.IDENTIFIER)


# Catches the declaration of sint64 variables
def p_declaration_sint64_set(p: YaccProduction) -> None:
    '''
    declaration_sint64_set : SINT64 declaration_identifier_set semicolons
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    # Stores the declared variable into the symbol table
    scope_identifier = ScopeHandler.get_current_scope_identifier()
    for identifier in CurrentScope.get(ProductionType.IDENTIFIER):
        GlobalSymbolTable.store_variable(scope_identifier, identifier, Keyword.SINT64, None)
    CurrentScope.clean(ProductionType.IDENTIFIER)


# Catches the declaration of float32 variables
def p_declaration_float32_set(p: YaccProduction) -> None:
    '''
    declaration_float32_set : FLOAT32 declaration_identifier_set semicolons
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    # Stores the declared variable into the symbol table
    scope_identifier = ScopeHandler.get_current_scope_identifier()
    for identifier in CurrentScope.get(ProductionType.IDENTIFIER):
        GlobalSymbolTable.store_variable(scope_identifier, identifier, Keyword.FLOAT32, None)
    CurrentScope.clean(ProductionType.IDENTIFIER)


# Catches the declaration of float64 variables
def p_declaration_float64_set(p: YaccProduction) -> None:
    '''
    declaration_float64_set : FLOAT64 declaration_identifier_set semicolons
    '''
    logger.debug("Yacc production: {}".format(p[1:]))
    # Stores the declared variable into the symbol table
    scope_identifier = ScopeHandler.get_current_scope_identifier()
    for identifier in CurrentScope.get(ProductionType.IDENTIFIER):
        GlobalSymbolTable.store_variable(scope_identifier, identifier, Keyword.FLOAT64, None)
    CurrentScope.clean(ProductionType.IDENTIFIER)


# Catches the declaration of a set of homogeneous variables
def p_declaration_homogeneous_variable_set(p: YaccProduction) -> None:
    '''
    declaration_homogeneous_variable_set : declaration_boolean_set
                                         | declaration_char_set
                                         | declaration_integer_set
                                         | declaration_float_set
                                         | declaration_string_set
                                         | declaration_uint8_set
                                         | declaration_uint16_set
                                         | declaration_uint32_set
                                         | declaration_uint64_set
                                         | declaration_sint8_set
                                         | declaration_sint16_set
                                         | declaration_sint32_set
                                         | declaration_sint64_set
                                         | declaration_float32_set
                                         | declaration_float64_set
    '''
    logger.debug("Yacc production: {}".format(p[1:]))


# Catches the declaration of a set of heterogeneous variables
def p_declaration_heterogeneous_variable_set(p: YaccProduction) -> None:
    '''
    declaration_heterogeneous_variable_set : declaration_homogeneous_variable_set
                                           | declaration_homogeneous_variable_set declaration_heterogeneous_variable_set
    '''
    logger.debug("Yacc production: {}".format(p[1:]))


# >>>
# Catches the attack's compound statement
def p_attack_compound_statement(p: YaccProduction) -> None:
    '''
    attack_compound_statement : ATTACK curvy_left empty curvy_right
                              | ATTACK curvy_left declaration_heterogeneous_variable_set curvy_right
    '''
    # TODO this is a stub, to be implemented
    pass
#<<<

# Builds the parser end define the entry point
parser = yacc.yacc(start='entry_point')

