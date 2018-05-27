# -*- coding: utf-8 -*-
""" This module contains the Object-Oriented Model of ADeLe.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""


from enum import unique, Enum
from types import DynamicClassAttribute
from typing import List, Any
from builtins import type

from util.utils import baserepr, basestr


class Container(object):
    """ The base class to build containers. """
    pass


class SimpleStatement(object):
    """ The base class to model compound statements. """
    pass


class CompoundStatement(object):
    """ The base class to model compound statements. """
    pass


class Literal(Container):
    """ Models a literal. 
    
    Literals contain literal values.
    """
    
    # The prefix to build the identifier of literals 
    PREFIX: str = '_'
    
    def __init__(self, type: str, value: str) -> None:
        self.identifier: str = '{}{}'.format(self.PREFIX, value)
        self.type: str = type
        self.value: str = value

    def __str__(self):
        return basestr(self)
    
    def __repr__(self):
        return baserepr(self)


class Variable(Container):
    """ Models a variable. 
    
    Variables contain references (throug identifiers) to other variables or literals, 
    does not contain literal values.
    """
    
    def __init__(self, identifier: str, type: str, reference: str) -> None:
        self.identifier: str = identifier
        self.type: str = type
        self.reference: str = reference

    def __str__(self):
        return basestr(self)
    
    def __repr__(self):
        return baserepr(self)


@unique
class ISO(Enum):
    """ ISO measure units. """
    TIME: str = 's'
    LENGTH: str = 'm'
    ANGLE: str = 'rad'

    @DynamicClassAttribute
    def symbol(self) -> str:
        """ The measure unit related symbol. """
        return self.value


class Configuration(CompoundStatement):
    """ Models the configuration compound statement. """

    def __init__(self, actions: List[Any]) -> None:
        self.actions: List[Any] = actions
        
    def __str__(self):
        return basestr(self)
    
    def __repr__(self):
        return baserepr(self)


class SetUnitTime(SimpleStatement):
    """ Models the action 'setUnitTime'. """
    
    def __init__(self, reference: str) -> None:
        self.reference: str = reference

    def __str__(self):
        return basestr(self)
    
    def __repr__(self):
        return baserepr(self)


class SetUnitLength(SimpleStatement):
    """ Models the action 'setUnitLength'. """
    
    def __init__(self, reference: str) -> None:
        self.reference: str = reference

    def __str__(self):
        return basestr(self)
    
    def __repr__(self):
        return baserepr(self)


class SetUnitAngle(SimpleStatement):
    """ Models the action 'setUnitAngle'. """
    
    def __init__(self, reference: str) -> None:
        self.reference: str = reference

    def __str__(self):
        return basestr(self)
    
    def __repr__(self):
        return baserepr(self)


class SetTimeStart(SimpleStatement):
    """ Models the action 'setTimeStart'. """
    
    def __init__(self, reference: str) -> None:
        self.reference: str = reference

    def __str__(self):
        return basestr(self)
    
    def __repr__(self):
        return baserepr(self)


class Attack(CompoundStatement):
    """ Models the attack compound statement. """
    
    # TODO To be implemented, this is a stub
    
    def __str__(self):
        return basestr(self)
    
    def __repr__(self):
        return baserepr(self)


class Scenario(CompoundStatement):
    """ Models the whole scenario compound statement. 
    
    It contains the configuration and the list of the attacks. 
    """

    # TODO To be developed, this is a stub        

    def __init__(self,
                 configuration: Configuration = None,
                 attack: Attack = None) -> None:
        self.configuration: Configuration = configuration
        self.attack: Attack = attack

    def __str__(self):
        return basestr(self)
    
    def __repr__(self):
        return baserepr(self)

