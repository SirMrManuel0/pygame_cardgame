from enum import Enum

class Types(Enum):
    INT: tuple = (int,)
    FLOAT: tuple = (float,)
    NUMBER: tuple = (*INT, *FLOAT)
    LIST: tuple = (list,)
    TUPLE: tuple = (tuple,)
    LISTS: tuple = (*LIST, )

class CaboCodes(Enum):
    NONE: int = 0

class CaboError(Exception):
    """
    A custom exception for errors in the Cabo application.
    """

    def __init__(self, code, msg="", wrong=None, right=None, err: str = "Error"):
        if wrong is not None:
            msg += f"\nWrong: {wrong}"
        if right is not None:
            msg += f"\nRight (Pattern): {right}"
        self.wrong = wrong
        self.right = right
        self.msg = msg
        super().__init__(f"{err} {code}: {msg}")

class ArgumentCodes(Enum):
    NONE: int = 0
    ZERO: int = 1
    LIST_LAYER_NOT_INT_FLOAT: int = 2
    OUT_OF_RANGE: int = 3
    NOT_INT_FLOAT: int = 4
    NOT_INT: int = 5
    NOT_LIST_NP_ARRAY: int = 6
    NOT_POSITIV: int = 7
    LIST_LAYER_NOT_INT_FLOAT_LIST: int = 8
    NOT_MATRIX_NP_ARRAY: int = 9
    NOT_PATH: int = 10
    LIST_NOT_STRING: int = 11
    MISSING_RESSOURCE_ENTRY: int = 12
    NOT_STRING: int = 13
    NOT_CARD: int = 14
    NOT_GAME_DECK: int = 15
    TOO_SMALL: int = 16
    NOT_SHUFFLE: int = 17
    NOT_EFFECT: int = 18
    NOT_DRAW_OPTIONS: int = 19
    NOT_LOGIC_EVENTS: int = 20


class ArgumentError(CaboError):
    """
        A custom exception for argument-related errors in the Cabo application.

        Attributes:
            code (ArgumentCodes): An error code identifying the type of error.
            msg (str, optional): A custom error message. If not provided, a default message is used.
            wrong_argument (any, optional): The incorrect argument that caused the error.
            right_argument (any, optional): The expected correct argument or pattern.
        """

    def __init__(self, code: ArgumentCodes, msg="", wrong_argument=None, right_argument=None):
        super().__init__(code, msg, wrong_argument, right_argument, "Argument Error")

class StateError(CaboError):
    """
        A custom exception for errors related to the state of the Cabo application.

        Attributes:
            code (int): An error code identifying the type of error.
            msg (str, optional): A custom error message. If not provided, a default message is used.
    """
    ...
