class CaboError(Exception):
    """
    A custom exception for errors in the Cabo application.

    Attributes:
        code (int): An error code identifying the type of error.
        msg (str, optional): An optional error message.
    """
    def __init__(self, code: int, msg=None):
        self.code = code
        super().__init__(f"{code}: {msg}")

class ArgumentError(CaboError):
    """
        A custom exception for argument-related errors in the Cabo application.

        Attributes:
            code (int): An error code identifying the type of error.
            msg (str, optional): A custom error message. If not provided, a default message is used.
            wrong_argument (any, optional): The incorrect argument that caused the error.
            right_argument (any, optional): The expected correct argument or pattern.
        """
    def __init__(self, code: int, msg=None, wrong_argument=None, right_argument=None):
        if msg is None:
            msg: str = f"Argument Error!"
        if wrong_argument is not None:
            msg += f"\nWrong Argument: {wrong_argument}"
        if right_argument is not None:
            msg += f"\nRight Argument (Pattern): {right_argument}"
        self.wrong_argument = wrong_argument
        self.right_argument = right_argument
        self.msg = msg
        super().__init__(code, msg)

class StateError(CaboError):
    """
        A custom exception for errors related to the state of the Cabo application.

        Attributes:
            code (int): An error code identifying the type of error.
            msg (str, optional): A custom error message. If not provided, a default message is used.
    """
    ...
