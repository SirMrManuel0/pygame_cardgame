import pygame

import game.gui
from game.logic import CaboLogic
import game.gui as gui
from game.gui import globals


class GuiHandler:
    def __init__(self, instant_run: bool = True, sizes=None) -> None:
        pygame.init()
        self._base_dimension = gui.Dimension(globals.SIZE)

        self._window = gui.Window(self._base_dimension, "Cabuh!")

        if instant_run:
            self.run()

    def run(self) -> None:
        self._window.run()
