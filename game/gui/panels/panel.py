import pygame
import game
import game.gui as gui
from typing import Self


class Panel:
    def __init__(self):
        self._objekte: list = list()
        self._events = dict()

    def add_object(self, object):
        self._objekte.append(object)

    def get_events(self):
        return {k: v for k, v in self._events.items()}

    def __iter__(self) -> iter:
        return iter(self._objekte)


