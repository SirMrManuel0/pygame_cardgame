import pygame

from game.logic import CaboLogic
import game.gui as gui

class GuiHandler:
    def __init__(self, instant_run: bool = True, sizes=None) -> None:
        pygame.init()
        self._base_dimension = gui.Dimension((500, 600))

        self._current_window = None

        if instant_run:
            self.run()

    def run(self) -> None:
        home_window = gui.Window(self._base_dimension, "Cabo")
        home_window.run()
