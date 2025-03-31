from game.gui.objects import BaseObject
from useful_utility.algebra import Vector
import pygame


class Circle(BaseObject):
    def __init__(self, position, color, radius):
        super().__init__(position, color)
        self._radius = radius

    def draw(self, surface):
        pygame.draw.circle(surface, self._color.get_data(), self._position.get_data(), self._radius)

