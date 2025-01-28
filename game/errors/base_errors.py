class CaboError(Exception):
    def __init__(self, code: int, msg=None):
        self.code = code
        super().__init__(f"Error {code}: {msg}")

class ArgumentError(CaboError):
    def __init__(self, code: int, msg=None, wrong_argument=None, right_argument=None):
        if msg is None and (wrong_argument is not None or right_argument is not None):
            msg: str = f"Argument Error!\nWrong Argument: {wrong_argument}\nRight Argument: {right_argument}"
        if msg is not None and (wrong_argument is not None or right_argument is not None):
            msg += f"\nWrong Argument: {wrong_argument}\nRight Argument: {right_argument}"
        self.wrong_argument = wrong_argument
        self.right_argument = right_argument
        self.msg = msg
        super().__init__(code, msg)

class StateError(CaboError):
    ...
