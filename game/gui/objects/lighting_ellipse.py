from game.gui.objects import BaseObject
from pylix.algebra import Vector
import pygame


class LightingEllipse(BaseObject):
    def __init__(self, position, width, height, color, diffusion: int, alpha: int):
        super().__init__(position, color)
        self._size = Vector([width, height])
        self._diffusion = diffusion
        self._alpha = alpha

    def draw(self, surface):
        for i in range(self._diffusion):
            RectVector: Vector = self._size - Vector(dimension=2, default_value=i)
            alpha = (self._alpha - self._diffusion) + i
            ellipse = pygame.Surface((RectVector[0] * 2, RectVector[1] * 2), pygame.SRCALPHA)
            pygame.draw.ellipse(
                ellipse,
                (*self._color.get_data(), alpha),
                pygame.Rect(RectVector[0],
                            RectVector[1],
                            RectVector[0],
                            RectVector[1])
            )
            surface.blit(ellipse, (self._position[0] - RectVector[0], self._position[1] - RectVector[1]))

    def set_position_from_center(self, pos: Vector):
        self._position = pos - .5 * self._size
