from typing import override

from game.gui.objects import Rectangle
from game.gui.objects import Text
from pylix.algebra import Vector
import pygame
from game.gui import globals


class Button(Rectangle):
    def __init__(self, position, width, font_size, color, text, margin_top_bottom,
                 text_color=Vector([0, 0, 0]), hover_color=globals.HOVER_COLOR, identifier=None,
                 pos_from_center: Vector | None = None):
        super().__init__(position, width, font_size, color)

        self._text = Text(Vector([position[0], position[1]]), text_color, text, font_size)
        self._size[1] = self._text.get_text_object().get_height() + margin_top_bottom
        self._hovered = False
        self._clicked = False
        self._identifier = identifier

        self._text.set_position(
            self._text._position[0] + (self._size[0] / 2) - (self._text.get_text_object().get_width() / 2),
            self._text._position[1] + (self._size[1] / 2) - (self._text.get_text_object().get_height() / 2)
        )
        self._color_ = color
        self._hover_color = hover_color
        if pos_from_center is not None:
            self.set_position_from_center(pos_from_center)

    def get_identifier(self):
        return self._identifier

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self._color.get_data(),
            pygame.Rect(self._position[0],
                        self._position[1],
                        self._size[0],
                        self._size[1]),
            0,
            5
        )

        self._text.draw(surface)

    @override
    def click_listener(self):
        for i in self._clickListener:
            if len(i[1]) > 0:
                i[0](*i[1])
                continue
            i[0]()

    @override
    def add_event_listener(self, func, *args):
        self._clickListener.append([func, args])

    def update(self):
        pos = pygame.mouse.get_pos()
        # print("Grainca lijevo : " , (pos[0] > self._position[0]))
        # print("Grainca desno : " , (pos[0] < self._position[0] + self._size[0]))
        # print("Grainca gore : " , pos[1] > self._position[1])
        # print("Grainca dole : ", (pos[1] < self._position[1] + self._size[1]))

        if (pos[0] > self._position[0]) and (pos[0] < self._position[0] + self._size[0]) and (
                pos[1] > self._position[1]) and (pos[1] < self._position[1] + self._size[1]):
            self._hovered = True
        else:
            self._hovered = False

        if self._hovered:
            self.set_color(self._hover_color)
        else:
            self.set_color(self._color_)

    def change_color(self, color):
        self._color_ = color

    def is_hovered(self):
        return self._hovered

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and self._hovered:
            self.click_listener()

    def set_position_from_center(self, pos: Vector):
        self._position = pos - .5 * self._size

        self._text.set_position(
            self._position[0] + (self._size[0] / 2) - (self._text.get_text_object().get_width() / 2),
            self._position[1] + (self._size[1] / 2) - (self._text.get_text_object().get_height() / 2)
        )
