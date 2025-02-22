from game.errors import *
from enum import Enum

class Shuffle(Enum):
    NONE: int = -1
    DUMP: int = 0

class Effect(Enum):
    NONE: int = 0
    PEEK: int = 1
    SWAP: int = 2
    SPY: int = 3

class Deck:
    def __init__(self):
        self._cards: list = list()

class Card:
    def __init__(self, value: int = 0):
        self._value = value

    def effect(self) -> Effect | None:
        if self._value in (7, 8):
            return Effect.PEEK
        elif self._value in (9, 10):
            return Effect.SPY
        elif self._value in (11, 12):
            return Effect.SWAP
