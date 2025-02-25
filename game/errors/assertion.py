from game.errors import ArgumentError, StateError, CaboError


def assert_type(var, type, code: int, msg: str = None, right_arg=None) -> None:
    if not isinstance(var, type):
        raise ArgumentError(code, wrong_argument=var, right_argument=right_arg, msg=msg)


def assert_range(var: float | int, start: float | int, end: float | int, code: int, msg: str = None,
                 right_arg=None) -> None:
    if var < start or var > end:
        raise ArgumentError(code, wrong_argument=var, right_argument=right_arg, msg=msg)


def assert_below(var: float | int, max_: int | float, code: int, msg: str = None, right_arg=None) -> None:
    if var >= max_:
        raise ArgumentError(code, wrong_argument=var, right_argument=right_arg, msg=msg)


def assert_above(var: float | int, min_: int | float, code: int, msg: str = None, right_arg=None) -> None:
    if var <= min_:
        raise ArgumentError(code, wrong_argument=var, right_argument=right_arg, msg=msg)


def assert_equals(var, equaled, code: int, msg: str = None, right_arg=None) -> None:
    if var != equaled:
        raise ArgumentError(code, wrong_argument=var, right_argument=right_arg, msg=msg)

