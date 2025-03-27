from game.gui.objects import Rectangle
from game.gui.objects import Text
from useful_utility.algebra import Vector
import pygame
from game.gui import globals

class Button(Rectangle):
    def __init__(self, position, width, height, color, text):
        super().__init__(position, width, height, color)
        self._text = Text(position, Vector([255, 255, 255]), text, height)

    def draw(self, surface):
        self._text.draw(surface)
        