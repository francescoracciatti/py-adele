# -*- coding: utf-8 -*-
""" This module contains the ADeLe's lexing rules.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""


import logging

from ply import lex

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
    MODEL               = 'model'
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
tokens = Keyword.tokens() + Punctuation.tokens() + Literal.tokens()

# The reserved keywords
reserved = Keyword.reverse_map()



# Tokenizers for the puncutation
t_ASSIGN        = Punctuation.ASSIGN.lexeme
t_ASSIGN_ADD    = Punctuation.ASSIGN_ADD.lexeme
t_ASSIGN_SUB    = Punctuation.ASSIGN_SUB.lexeme
t_ASSIGN_MUL    = Punctuation.ASSIGN_MUL.lexeme
t_ASSIGN_DIV    = Punctuation.ASSIGN_DIV.lexeme
t_ASSIGN_MOD    = Punctuation.ASSIGN_MOD.lexeme
t_NOT_EQUAL_TO  = Punctuation.NOT_EQUAL_TO.lexeme
t_EQUAL_TO      = Punctuation.EQUAL_TO.lexeme
t_GR_EQ_THAN    = Punctuation.GR_EQ_THAN.lexeme
t_LS_EQ_THAN    = Punctuation.LS_EQ_THAN.lexeme
t_GR_THAN       = Punctuation.GR_THAN.lexeme
t_LS_THAN       = Punctuation.LS_THAN.lexeme
t_ADD           = Punctuation.ADD.lexeme
t_SUB           = Punctuation.SUB.lexeme
t_MUL           = Punctuation.MUL.lexeme
t_DIV           = Punctuation.DIV.lexeme
t_MOD           = Punctuation.MOD.lexeme
t_EXP           = Punctuation.EXP.lexeme
t_NEG           = Punctuation.NEG.lexeme
t_LOGIC_AND     = Punctuation.LOGIC_AND.lexeme
t_LOGIC_OR      = Punctuation.LOGIC_OR.lexeme
t_ROUND_L       = Punctuation.ROUND_L.lexeme
t_ROUND_R       = Punctuation.ROUND_R.lexeme
t_BRACK_L       = Punctuation.BRACK_L.lexeme
t_BRACK_R       = Punctuation.BRACK_R.lexeme
t_CURVY_L       = Punctuation.CURVY_L.lexeme
t_CURVY_R       = Punctuation.CURVY_R.lexeme
t_COMMA         = Punctuation.COMMA.lexeme
t_COLON         = Punctuation.COLON.lexeme
t_SEMICOLON     = Punctuation.SEMICOLON.lexeme


# Token parsing rule for chars
def t_LITERAL_CHAR(t):
    r"\'.\'"
    t.value = t.value.replace("'", "")
    return t


# Token parsing rule for float numbers
def t_LITERAL_FLOAT(t):
    r'-?\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        logger.critical("float number [" + str(t.value) + "] badly defined")
        raise
    return t


# Token parsing rule for signed integer numbers
def t_LITERAL_INTEGER(t):
    r'-?\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        logger.critical("integer number [" + str(t.value) + "] badly defined")
        raise
    return t


# Token parsing rule for strings
def t_LITERAL_STRING(t):
    r'\"([^\\"]|(\\.))*\"'
    t.value = t.value.replace('\"', '')
    return t


# Token parsing rule for identifiers
def t_LITERAL_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    # Checks if the identifier is a reserved keyword
    t.type = reserved.get(t.value, Literal.LITERAL_IDENTIFIER.lexeme)
    return t


# Token parsing rule to ignore tab occurrences
t_ignore = ' \t'

 
# Token parsing rule to ignore comments
def t_comment(t):
    r'\#.*'
    pass


# Token parsing rule to track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Token parsing rule for wrong statement or characters
def t_error(t):
    msg = "illegal character '" + str(t.value[0]) + "' - line " + str(t.lexer.lineno)
    logger.critical(msg)
    raise RuntimeError(msg)


# Builds the lexer
lexer = lex.lex()

