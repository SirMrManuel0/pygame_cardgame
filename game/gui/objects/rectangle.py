from game.gui.objects import BaseObject
from useful_utility.algebra import Vector
import pygame


class Rectangle(BaseObject):
    def __init__(self, position, width, height, color):
        super().__init__(position, color)
        print(width)
        self._size = Vector([width, height])

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self._color.get_data(),
            pygame.Rect(self._position[0],
                        self._position[1],
                        self._size[0],
                        self._size[1])
        )
