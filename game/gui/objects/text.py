from game.gui.objects import BaseObject
from pylix.algebra import Vector
import pygame
from game.gui import globals


class Text(BaseObject):
    def __init__(self, position, color, text, font_size, pos_from_center=None, identifier=None):
        super().__init__(position, color)
        self._font = pygame.font.SysFont('freesanbold.ttf', font_size)
        self._text = self._font.render(text, True, color.get_data())
        self._textRect = self._text.get_rect()
        self._identifier = identifier
        if pos_from_center is None:
            self._textRect.center = (
                int(self._position[0] + self._text.get_width() / 2),
                int(self._position[1] + self._text.get_height() / 2)
            )
        else:
            self._textRect.center = (
                int(pos_from_center[0]),
                int(pos_from_center[1])
            )

    def get_identifier(self):
        return self._identifier

    def center_absolute_x(self):
        self._textRect.center = (int(globals.SIZE[0] / 2), int(self._position[1] + self._text.get_height() / 2))

    def draw(self, surface):
        surface.blit(self._text, self._textRect)

    def get_text_object(self):
        return self._text

    def set_position(self, x, y):
        self._position[0] = x
        self._position[1] = y

        self._textRect.center = (
            int(self._position[0] + self._text.get_width() / 2),
            int(self._position[1] + self._text.get_height() / 2)
        )

    def set_position_from_center(self, pos: Vector):
        self._position = pos - .5 * Vector([self._text.get_width(), self._text.get_height()])
        self.set_position(self._position[0], self._position[1])

    def change_text(self, new_text):
        self._text = self._font.render(new_text, True, self._color.get_data())
        self._textRect = self._text.get_rect()
        self._textRect.center = (
            int(self._position[0] + self._text.get_width() / 2), int(self._position[1] + self._text.get_height() / 2))
