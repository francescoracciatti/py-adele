# -*- coding: utf-8 -*-
""" This module contains the ADeLe's lexing rules.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""


import logging

from ply import lex

from tokens import Keyword, Punctuation, Literal 


logger = logging.getLogger(__name__)

# The tokens used by the tokenizer
tokens = Keyword.tokens() + Punctuation.tokens() + Literal.tokens()

# The reserved keywords
reserved = Keyword.reverse_map()
 
# Tokenizers for the puncutation
t_ASSIGN        = Punctuation.ASSIGN.value
t_ASSIGN_ADD    = Punctuation.ASSIGN_ADD.value
t_ASSIGN_SUB    = Punctuation.ASSIGN_SUB.value
t_ASSIGN_MUL    = Punctuation.ASSIGN_MUL.value
t_ASSIGN_DIV    = Punctuation.ASSIGN_DIV.value
t_ASSIGN_MOD    = Punctuation.ASSIGN_MOD.value
t_NOT_EQUAL_TO  = Punctuation.NOT_EQUAL_TO.value
t_EQUAL_TO      = Punctuation.EQUAL_TO.value
t_GR_EQ_THAN    = Punctuation.GR_EQ_THAN.value
t_LS_EQ_THAN    = Punctuation.LS_EQ_THAN.value
t_GR_THAN       = Punctuation.GR_THAN.value
t_LS_THAN       = Punctuation.LS_THAN.value
t_ADD           = Punctuation.ADD.value
t_SUB           = Punctuation.SUB.value
t_MUL           = Punctuation.MUL.value
t_DIV           = Punctuation.DIV.value
t_MOD           = Punctuation.MOD.value
t_EXP           = Punctuation.EXP.value
t_NEG           = Punctuation.NEG.value
t_LOGIC_AND     = Punctuation.LOGIC_AND.value
t_LOGIC_OR      = Punctuation.LOGIC_OR.value
t_ROUND_L       = Punctuation.ROUND_L.value
t_ROUND_R       = Punctuation.ROUND_R.value
t_BRACK_L       = Punctuation.BRACK_L.value
t_BRACK_R       = Punctuation.BRACK_R.value
t_CURVY_L       = Punctuation.CURVY_L.value
t_CURVY_R       = Punctuation.CURVY_R.value
t_COMMA         = Punctuation.COMMA.value
t_COLON         = Punctuation.COLON.value
t_SEMICOLON     = Punctuation.SEMICOLON.value
 
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
        logger.critical("float number badly defined")
        raise
    return t
 
# Token parsing rule for signed integer numbers
def t_LITERAL_INTEGER(t):
    r'-?\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        logger.critical("integer number badly defined")
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
    t.type = reserved.get(t.value, Literal.LITERAL_IDENTIFIER.value)
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
    t.lexer.skip(1)
    msg = "illegal character '" + str(t.value[0]) + "' - line " + str(t.lexer.lineno)
    logger.critical(msg)
    raise RuntimeError(msg)

# Builds the lexer
lexer = lex.lex()

