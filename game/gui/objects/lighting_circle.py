from useful_utility.algebra import Vector

from game.gui.objects import BaseObject
import pygame


class LightingCircle(BaseObject):
    def __init__(self, position: Vector, color: Vector, radius: float, diffusion: int, alpha: int):
        super().__init__(position, color)
        self._radius = radius
        self._diffusion = diffusion
        self._alpha = alpha

    def draw(self, surface):
        for i in range(self._diffusion):
            radius = (self._radius - i)
            alpha = (self._alpha - self._diffusion) + i
            circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (*self._color.get_data(), alpha), (radius, radius), radius)
            surface.blit(circle_surface, (self._position[0] - radius, self._position[1] - radius))

