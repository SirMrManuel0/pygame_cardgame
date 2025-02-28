import pygame

from game.logic import CaboLogic
from game.gui import Dimension

class GuiHandler:
    def __init__(self, instant_run: bool = True, sizes: Dimension = Dimension()) -> None:
        pygame.init()

        if instant_run:
            self.run()

    def run(self) -> None:
        ...
