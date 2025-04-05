from game.errors import *
from enum import Enum

class Shuffle(Enum):
    """
    Enum to define the different shuffle possibilities.
    """
    NONE: int = -1
    DUMP: int = 0

class Effect(Enum):
    """
    The effects of the cards. This enum is only used by deck and children.
    """
    NONE: int = 0
    PEEK: int = 1
    SWAP: int = 2
    SPY: int = 3

class Deck:
    """
    Parent of all decks.
    """
    def __init__(self):
        self._cards: list = list()

    def __iter__(self):
        """
        To make the deck iterable.
        """
        return self._cards

class Card:
    """
    Element of decks.
    """
    def __init__(self, value: int = 0):
        """
        :param value: The card value between 0 and 13
        """
        # Argument validation
        assertion.assert_types(value, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_range(value, -1, 13, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
        self._value = value

    def get_value(self):
        return self._value

    def effect(self) -> Effect:
        """
        Returns the enum of the card effect.
        """
        if self._value in (7, 8):
            return Effect.PEEK
        elif self._value in (9, 10):
            return Effect.SPY
        elif self._value in (11, 12):
            return Effect.SWAP
        return Effect.NONE
