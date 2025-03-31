from useful_utility.algebra import Vector


class BaseObject:
    def __init__(self, position, color):
        self._position = position
        self._color = color
        self._clickListener = []

    def rotate(self):
        ...

    def set_color(self, color):
        self._color = color

    def draw(self):
        ...

    def update(self):
        ...

    def clickListener(self):
        for i in self._clickListener:
            i()

    def addEventListener(self, func):
        self._clickListener.append(func)