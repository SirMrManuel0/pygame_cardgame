import pygame
import game
import game.gui as gui
from typing import Self
from game.gui import globals
from useful_utility.algebra import Vector

class Panel:
    def __init__(self):
        self._objekte: list = list()
        self._middlePoint = Vector(globals.SIZE) / 2

    def add_object(self, object_):
        self._objekte.append(object_)

    def get_object(self, index):
        return self._objekte[index]

    def update(self):
        for i in self._objekte:
            i.update()

    def update_animation(self, dt):
        ...

    def draw(self, screen):
        for i in self._objekte:
            i.draw(screen)

    def get_objects(self):
        return self._objekte

    def __iter__(self) -> iter:
        return iter(self._objekte)

    def event(self, event):
        for i in self._objekte:
            i.event(event)
