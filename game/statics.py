import os
from game import ArgumentError

def get_path_abs(relative_path: str) -> str:
    """
    Returns the absolute path of a file or folder relative to scripts.py.

    :param relative_path: Relative path to the file or folder.
    :return: Absolute path.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the executing script
    abs_path = os.path.join(script_dir, relative_path)
    abs_path = os.path.abspath(abs_path)
    if not os.path.exists(abs_path):
        raise ArgumentError(1, msg=f"Path '{abs_path}' does not exists.", wrong_argument=relative_path)
    return abs_path

def get_path_resource(path: str) -> str:
    """
    Returns the absolute path of a ressource.
    The input path should consider the relative start to be in resources.

    :param path:
    :return: abs path to ressource
    """
    return get_path_abs(os.path.join("..\\resources", path))

def run() -> None:
    ...