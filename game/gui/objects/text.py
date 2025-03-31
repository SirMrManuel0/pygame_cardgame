from game.gui.objects import BaseObject
from useful_utility.algebra import Vector
import pygame
from game.gui import globals


class Text(BaseObject):
    def __init__(self, position, color, text, font_size):
        super().__init__(position, color)
        self._font = pygame.font.SysFont('freesanbold.ttf', font_size)
        self._text = self._font.render(text, True, color.get_data())
        self._textRect = self._text.get_rect()
        self._textRect.center = (self._position[0] + self._text.get_width() / 2, self._position[1] + self._text.get_height() / 2)

    def center_absolute_x(self):
        self._textRect.center = (globals.SIZE[0] / 2, self._position[1] + self._text.get_height() / 2)

    def draw(self, surface):
        surface.blit(self._text, self._textRect)

    def get_text_object(self):
        return self._text

    def set_position(self, x, y):
        self._position[0] = x
        self._position[1] = y

        self._textRect.center = (
            self._position[0] + self._text.get_width() / 2,
            self._position[1] + self._text.get_height() / 2
        )
