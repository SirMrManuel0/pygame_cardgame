import pygame

from game.logic import CaboLogic
import game.gui as gui

class GuiHandler:
    def __init__(self, instant_run: bool = True, sizes=None) -> None:
        pygame.init()

        if instant_run:
            self.run()

    def run(self) -> None:
        ...
