# -*- coding: utf-8 -*-
""" This module contains the ADeLe's tokens and related keywords.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""

from support import Token


class Keyword(Token):
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


class Punctuation(Token):
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
