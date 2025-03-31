import pygame
import game
import game.gui as gui
from typing import Self


class Panel:
    def __init__(self):
        self._objekte: list = list()

    def add_object(self, object):
        self._objekte.append(object)

    def get_object(self, index):
        return self._objekte[index]

    def update(self):
        for i in self._objekte:
            i.update()

    def draw(self, screen):
        for i in self._objekte:
            i.draw(screen)

    def get_objects(self):
        return self._objekte

    def __iter__(self) -> iter:
        return iter(self._objekte)


