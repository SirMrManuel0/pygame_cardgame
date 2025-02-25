import os
import json
import numpy as np

from game.errors import ArgumentError, assertion
from game.gui import GuiHandler

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

def get_path_resource(*way) -> str:
    """
    Returns the absolute path of a ressource.
    The input should be the order of keys, under which the path is saved in resource.json.

    :param: way
    :return: abs path to ressource
    """
    assertion.assert_type_list(way, str, 2, msg=f"Only strings can be in the way.",  right_arg=["ex", "ample"])

    with open(get_path_abs("..\\resources\\resources.json"), "r", encoding="utf-8") as js:
        look_up: dict = json.load(js)
    sub_path: dict = look_up
    for i, step in enumerate(way):
        if isinstance(sub_path, dict) and step not in sub_path:
            raise ArgumentError(3,
                                msg=f"There is no entry in 'resources.json' for '{step}' in order of '{way[:i+1]}'" +
                                    "\nOr there are too many args.",
                                wrong_argument=way)
        sub_path = sub_path[step]
    assertion.assert_type(sub_path, str, 4, msg=f"There is no given path for this request in 'resources.json'")
    return get_path_abs(os.path.join("..\\resources", "\\" + str(sub_path)))

def rnd(x: float) -> float:
    return float(np.round(x, 8))

def run() -> None:
    GuiHandler()
