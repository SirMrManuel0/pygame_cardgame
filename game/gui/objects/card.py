from game.gui.objects import Rectangle
from game.gui.objects import Text
from pylix.algebra import Vector, Matrix
from game.gui.objects import BaseObject
import pygame

import os
from game.gui import globals


class Card(BaseObject):
    def __init__(self, position, name, scale_size, rotation=0, pos_from_center=None, identifier=None):
        super().__init__(position, Vector([0, 0, 0]))
        self._rotation = rotation
        self._name = name
        self._scale_size = scale_size
        self._img = pygame.image.load("./resources/cards/" + name)
        self._img = pygame.transform.scale(self._img, (
            self._img.get_rect().size[0] * scale_size, self._img.get_rect().size[1] * scale_size)
                                           )
        self._img = pygame.transform.rotate(self._img, rotation)

        self._size = Vector([self._img.get_rect().size[0], self._img.get_rect().size[1]])
        self._identifier = identifier

        if pos_from_center is not None:
            self.set_position_from_center(pos_from_center)

    def get_identifier(self):
        return self._identifier

    def get_center(self) -> Vector:
        return self._position + (.5 * self._size)

    def draw(self, screen):
        screen.blit(self._img, (self._position[0], self._position[1]))

    def set_position_from_center(self, pos: Vector):
        self._position = pos - (.5 * self._size)

    def get_size(self):
        return self._size

    def get_name(self) -> str:
        return self._name

    def set_angle(self, angle):
        self._img = pygame.image.load("./resources/cards/" + self._name)
        self._img = pygame.transform.scale(self._img, (
            self._img.get_rect().size[0] * self._scale_size, self._img.get_rect().size[1] * self._scale_size)
                                           )
        center = [*self._img.get_rect().center]
        self._img = pygame.transform.rotate(self._img, self._rotation + angle)

        self._size = Vector([self._img.get_rect().size[0], self._img.get_rect().size[1]])
        self.set_position_from_center(self._position + Vector(center))

    def __str__(self):
        return f"Card at {hex(id(self))}: {self._position}"

    def __repr__(self):
        return f"Card at {hex(id(self))}: {self._position}"
