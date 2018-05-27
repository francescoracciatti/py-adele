# -*- coding: utf-8 -*-
""" The utilities of Py-ADeLe.

Author:
    Francesco Racciatti

Copyright 2018 Francesco Racciatti

"""


from typing import Any


def baserepr(cls: Any) -> str:
    """ Provides the string representation of the given class. """
    s = '<{}:{{'.format(cls.__class__.__name__)
    for idx, key in enumerate(cls.__dict__.keys()):
        if idx != 0:
            s += ', '
        s += '{}: {}'.format(key, cls.__dict__[key])
    s += '}>'
    return s


def basestr(cls: Any) -> str:
    """ Stringifies the given class. """
    return baserepr(cls)

