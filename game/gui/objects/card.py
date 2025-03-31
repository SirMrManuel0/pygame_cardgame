from game.gui.objects import Rectangle
from game.gui.objects import Text
from useful_utility.algebra import Vector
from game.gui.objects import BaseObject
import pygame

import os
from game.gui import globals

class Card(BaseObject):
    def __init__(self, position, name):
        super().__init__(position, Vector([0, 0, 0]))
        self._img = pygame.image.load("./resources/cards/" + name)
        self._img = pygame.transform.scale(self._img, (self._img.get_rect().size[0] * 0.3, self._img.get_rect().size[1] * 0.3))

    def draw(self, screen):
        screen.blit(self._img, (self._position[0], self._position[1]))

