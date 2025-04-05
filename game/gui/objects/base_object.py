from pylix.algebra import Vector


class BaseObject:
    def __init__(self, position = Vector(dimension=2), color = Vector(dimension=3)):
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

    def click_listener(self):
        for i in self._clickListener:
            i()

    def add_event_listener(self, func):
        self._clickListener.append(func)

    def event(self, event):
        ...

    def update(self):
        ...

    def clickListener(self):
        for i in self._clickListener:
            i()

    def addEventListener(self, func):
        self._clickListener.append(func)
