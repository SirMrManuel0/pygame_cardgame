import pygame

import game
import game.gui as gui
from game.gui import globals


class GuiHandler:
    def __init__(self, instant_run: bool = True, sizes=None) -> None:
        pygame.init()
        pygame.mixer.init()

        pygame.mixer.music.load(game.get_path_resource("music", "background"))

        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=-1, start=0.0)

        self._base_dimension = gui.Dimension(globals.SIZE)

        # Play music (loop=-1 means it will loop indefinitely)
        pygame.mixer.music.play(loops=-1, start=0.0)

        self._window = gui.Window(self._base_dimension, "Cabuh!")

        if instant_run:
            self.run()

    def run(self) -> None:
        self._window.run()
