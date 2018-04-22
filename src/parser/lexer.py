# -*- coding: utf-8 -*-
""" This module contains the ADeLe's lexing rules.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""


import logging
from typing import Tuple, Dict, Any
from mypy_extensions import NoReturn

from ply import lex
from ply.lex import LexToken, Lexer

from lexeme import Lexeme


logger = logging.getLogger(__name__)


class Keyword(Lexeme):
    """ The ADeLe's keywords. """
    # Unscoped types
    BOOLEAN             = 'boolean'
    CHAR                = 'char'
    INTEGER             = 'integer'
    FLOAT               = 'float'
    STRING              = 'string'
    # Scoped types, when the size does really matter
    UINT8               = 'uint8'
    UINT16              = 'uint16'
    UINT32              = 'uint32'
    UINT64              = 'uint64'
    SINT8               = 'sint8'
    SINT16              = 'sint16'
    SINT32              = 'sint32'
    SINT64              = 'sint64'
    FLOAT32             = 'float32'
    FLOAT64             = 'float64'
    # Generic message
    MESSAGE             = 'message'
    # Boolean values
    FALSE               = 'false'
    TRUE                = 'true'
    # Configuration
    SET_UNIT_TIME       = 'setUnitTime'
    SET_UNIT_LENGTH     = 'setUnitLength'
    SET_UNIT_ANGLE      = 'setUnitAngle'
    SET_TIME_START      = 'setTimeStart'
    SET_TIME_END        = 'setUnitTime'
    # Actions
    ELEMENT_MISPLACE    = 'elementMisplace'
    ELEMENT_ROTATE      = 'elementRotate'
    ELEMENT_DECEIVE     = 'elementDeceive'
    ELEMENT_DISABLE     = 'elementDisable'
    ELEMENT_ENABLE      = 'elementEnable'
    ELEMENT_DESTROY     = 'elementDestroy'
    MESSAGE_WRITE       = 'messageWrite'
    MESSAGE_READ        = 'messageRead'
    MESSAGE_FORWARD     = 'messageForward'
    MESSAGE_INJECT      = 'messageInject'
    MESSAGE_CREATE      = 'messageCreate'
    MESSAGE_CLONE       = 'messageClone'
    MESSAGE_DROP        = 'messageDrop'
    # Statements
    SCENARIO            = 'scenario'
    AT                  = 'at'
    FOREACH             = 'foreach'
    FROM                = 'from'
    FOR                 = 'for'
    IF                  = 'if'
    ELSE                = 'else'
    # Containers
    LIST                = 'list'
    RANGE               = 'range'
    # Accessors
    IN                  = 'in'
    # WellKnown values
    CAPTURED            = 'CAPTURED'
    SELF                = 'SELF'
    START               = 'START'
    END                 = 'END'
    TX                  = 'TX'
    RX                  = 'RX'
    # Time
    HOUR                = 'h'
    MINUTE              = 'min'
    SECOND              = 's'
    SECOND_MILLI        = 'ms'
    SECOND_MICRO        = 'us'


class Punctuation(Lexeme):
    """ The ADeLe's punctuation. """
    # Basic assignment operator
    ASSIGN              = r'='
    # Compound assignment operators
    ASSIGN_ADD          = r'\+='
    ASSIGN_SUB          = r'-='
    ASSIGN_MUL          = r'\*='
    ASSIGN_DIV          = r'/='
    ASSIGN_MOD          = r'%='
    # Comparison operators
    NOT_EQUAL_TO        = r'!='
    EQUAL_TO            = r'=='
    GR_EQ_THAN          = r'>='
    LS_EQ_THAN          = r'<='
    GR_THAN             = r'>'
    LS_THAN             = r'<'
    # Basic operators
    ADD                 = r'\+'
    SUB                 = r'-'
    MUL                 = r'\*'
    DIV                 = r'/'
    MOD                 = r'%'
    EXP                 = r'\^'
    NEG                 = r'!'
    # Logical operators
    LOGIC_AND           = r'\&\&'
    LOGIC_OR            = r'\|\|'
    # Parenthesis
    ROUND_L             = r'\('
    ROUND_R             = r'\)'
    BRACK_L             = r'\['
    BRACK_R             = r'\]'
    CURVY_L             = r'\{'
    CURVY_R             = r'\}'
    # Other punctuation
    SEMICOLON           = r'\;'
    COMMA               = r'\,'
    COLON               = r'\:'


class Literal(Lexeme):
    """ Supports the tokenization of literal values. """
    LITERAL_IDENTIFIER  = 'LITERAL_IDENTIFIER'
    LITERAL_INTEGER     = 'LITERAL_INTEGER'
    LITERAL_STRING      = 'LITERAL_STRING'
    LITERAL_FLOAT       = 'LITERAL_FLOAT'
    LITERAL_CHAR        = 'LITERAL_CHAR'


# The tokens used by the tokenizer
tokens: Tuple[str, ...] = Keyword.tokens() + Punctuation.tokens() + Literal.tokens()


# The reserved keywords
reserved: Dict[str, str] = Keyword.reverse_map()


# Tokenizers for the puncutation
                    
t_ASSIGN: str           = Punctuation.ASSIGN.lexeme
t_ASSIGN_ADD: str       = Punctuation.ASSIGN_ADD.lexeme
t_ASSIGN_SUB: str       = Punctuation.ASSIGN_SUB.lexeme
t_ASSIGN_MUL: str       = Punctuation.ASSIGN_MUL.lexeme
t_ASSIGN_DIV: str       = Punctuation.ASSIGN_DIV.lexeme
t_ASSIGN_MOD: str       = Punctuation.ASSIGN_MOD.lexeme
t_NOT_EQUAL_TO: str     = Punctuation.NOT_EQUAL_TO.lexeme
t_EQUAL_TO: str         = Punctuation.EQUAL_TO.lexeme
t_GR_EQ_THAN: str       = Punctuation.GR_EQ_THAN.lexeme
t_LS_EQ_THAN: str       = Punctuation.LS_EQ_THAN.lexeme
t_GR_THAN: str          = Punctuation.GR_THAN.lexeme
t_LS_THAN: str          = Punctuation.LS_THAN.lexeme
t_ADD: str              = Punctuation.ADD.lexeme
t_SUB: str              = Punctuation.SUB.lexeme
t_MUL: str              = Punctuation.MUL.lexeme
t_DIV: str              = Punctuation.DIV.lexeme
t_MOD: str              = Punctuation.MOD.lexeme
t_EXP: str              = Punctuation.EXP.lexeme
t_NEG: str              = Punctuation.NEG.lexeme
t_LOGIC_AND: str        = Punctuation.LOGIC_AND.lexeme
t_LOGIC_OR: str         = Punctuation.LOGIC_OR.lexeme
t_ROUND_L: str          = Punctuation.ROUND_L.lexeme
t_ROUND_R: str          = Punctuation.ROUND_R.lexeme
t_BRACK_L: str          = Punctuation.BRACK_L.lexeme
t_BRACK_R: str          = Punctuation.BRACK_R.lexeme
t_CURVY_L: str          = Punctuation.CURVY_L.lexeme
t_CURVY_R: str          = Punctuation.CURVY_R.lexeme
t_COMMA: str            = Punctuation.COMMA.lexeme
t_COLON: str            = Punctuation.COLON.lexeme
t_SEMICOLON: str        = Punctuation.SEMICOLON.lexeme


# Token parsing rule for chars
def t_LITERAL_CHAR(t: LexToken) -> LexToken:
    r"\'.\'"
    t.value = t.value.replace("'", "")
    return t


# Token parsing rule for float numbers
def t_LITERAL_FLOAT(t: LexToken) -> LexToken:
    r'-?\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        logger.critical("float number [" + str(t.value) + "] badly defined")
        raise
    return t


# Token parsing rule for signed integer numbers
def t_LITERAL_INTEGER(t: LexToken) -> LexToken:
    r'-?\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        logger.critical("integer number [" + str(t.value) + "] badly defined")
        raise
    return t


# Token parsing rule for strings
def t_LITERAL_STRING(t: LexToken) -> LexToken:
    r'\"([^\\"]|(\\.))*\"'
    t.value = t.value.replace('\"', '')
    return t


# Token parsing rule for identifiers
def t_LITERAL_IDENTIFIER(t: LexToken) -> LexToken:
    r'[a-zA-Z][a-zA-Z_0-9]*'
    # Checks if the identifier is a reserved keyword
    t.type = reserved.get(t.value, Literal.LITERAL_IDENTIFIER.lexeme)
    return t


# Token parsing rule to ignore tab occurrences
t_ignore: str = ' \t'


# Token parsing rule to ignore comments
def t_comment(t: LexToken) -> None:
    r'\#.*'
    pass


# Token parsing rule to track line numbers
def t_newline(t: LexToken) -> None:
    r'\n+'
    t.lexer.lineno += len(t.value)


# Token parsing rule for wrong statement or characters
def t_error(t: LexToken) -> NoReturn:
    msg = "Illegal character '{}' - line {}".format(t.value[0], t.lexer.lineno)
    logger.critical(msg)
    raise RuntimeError(msg)


# Builds the lexer
lexer: Lexer = lex.lex()

