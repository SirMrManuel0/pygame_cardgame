from game.gui.objects import BaseObject
from useful_utility.algebra import Vector
import pygame


class Ellipse(BaseObject):
    def __init__(self, position, width, height, color):
        super().__init__(position, color)
        self._size = Vector([width, height])

    def draw(self, surface):
        pygame.draw.ellipse(
            surface,
            self._color.get_data(),
            pygame.Rect(self._position[0],
                        self._position[1],
                        self._size[0],
                        self._size[1])
        )

    def set_position_from_center(self, pos: Vector):
        self._position = pos - .5 * self._size
