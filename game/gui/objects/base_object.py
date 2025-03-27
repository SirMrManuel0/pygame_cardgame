from useful_utility.algebra import Vector


class BaseObject:
    def __init__(self, position, color):
        self._position = position
        self._color = color

    def rotate(self):
        ...

    def set_color(self, color):
        self._color = color

    def draw():
        ...
