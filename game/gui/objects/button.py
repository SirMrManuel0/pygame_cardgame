from game.gui.objects import Rectangle
from game.gui.objects import Text
from useful_utility.algebra import Vector
import pygame
import os
from game.gui import globals

class Button(Rectangle):
    def __init__(self, position, width, fontSize, color, text, marginTopBottom):
        super().__init__(position, width, fontSize, color)

        self._text = Text(Vector([position[0], position[1]]), Vector([0, 0, 0]), text, fontSize)
        self._size[1] = self._text.getTextObject().get_height() + marginTopBottom
        self._hoverd = False

        self._text.setPosition(
            self._text._position[0] + (self._size[0] / 2) - (self._text.getTextObject().get_width() / 2),
            self._text._position[1] + (self._size[1] / 2) - (self._text.getTextObject().get_height() / 2)
        )

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

    def update(self):
        pos = pygame.mouse.get_pos()

        #print("Grainca lijevo : " , (pos[0] > self._position[0]))
        #print("Grainca desno : " , (pos[0] < self._position[0] + self._size[0]))
        #print("Grainca gore : " , pos[1] > self._position[1])
        #print("Grainca dole : ", (pos[1] < self._position[1] + self._size[1]))

        if (pos[0] > self._position[0]) and (pos[0] < self._position[0] + self._size[0]) and (pos[1] > self._position[1]) and (pos[1] < self._position[1] + self._size[1]):
            self._hoverd = True
        else:
            self._hoverd = False

        if self._hoverd:
            self.set_color(Vector([166, 132, 38]))
        else:
            self.set_color(Vector([250, 241, 230]))

        if pygame.mouse.get_pressed()[0] and self._hoverd:
            self.clickListener()


    def isHoverd(self):
        return self._hoverd

