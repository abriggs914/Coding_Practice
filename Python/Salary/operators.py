from enum import Enum


class Operators(Enum):
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, n, f):
        self.n = n
        self.f = f

    ADDITION = "+", lambda a, b: a + b
    SUBTRACTION = "-", lambda a, b: a - b
    MULTIPLICATION = "*", lambda a, b: a * b
    DIVISION = "/", lambda a, b: a / b
    POWER = "^", lambda a, b: a ** b