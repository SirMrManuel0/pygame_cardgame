import pygame

import game.gui
from game.logic import CaboLogic
import game.gui as gui

class GuiHandler:
    def __init__(self, instant_run: bool = True, sizes=None) -> None:
        pygame.init()
        self._base_dimension = gui.Dimension((700 * game.gui.PHI, 700))

        self._current_window = None

        if instant_run:
            self.run()



    def run(self) -> None:
        home_window = gui.Window(self._base_dimension, "Cabo")
        pygame.draw.rect(home_window.get_screen(), (255, 0, 0), (350, 250, 100, 100))
        home_window.run()