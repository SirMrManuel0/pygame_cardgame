from game.gui.objects import Rectangle
from game.gui.objects import Text
from useful_utility.algebra import Vector, Matrix
from game.gui.objects import BaseObject
import pygame

import os
from game.gui import globals


class Card(BaseObject):
    def __init__(self, position, name, scale_size, rotation=0):
        super().__init__(position, Vector([0, 0, 0]))
        self._img = pygame.image.load("./resources/cards/" + name)
        self._img = pygame.transform.scale(self._img, (
            self._img.get_rect().size[0] * scale_size, self._img.get_rect().size[1] * scale_size)
        )
        self._img = pygame.transform.rotate(self._img, rotation)

        self._size = Vector([self._img.get_rect().size[0], self._img.get_rect().size[1]])

    def draw(self, screen):
        screen.blit(self._img, (self._position[0], self._position[1]))

    def set_position_from_center(self, pos: Vector):
        self._position = pos - .5 * self._size

    def get_size(self):
        return self._size
