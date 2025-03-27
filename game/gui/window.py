import pygame
import game
import game.gui as gui
from game.gui.panels import *
from game.errors import *


class Window:
    def __init__(self, dimension, title: str):
        self._events = dict()
        self._dimension: gui.Dimension = dimension
        self._alive = True
        self._title = title
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self._dimension.get_dimensions())
        self._panel = None

        self.update(HomePanel())
        self.draw()

        pygame.display.set_caption(self._title)

        pygame.display.set_icon(pygame.image.load(game.get_path_resource("icons", "purple")))

    def add_event(self, event_type: int, func):
        if event_type in self._events:
            self._events[event_type].append(func)
        else:
            self._events[event_type] = [func]

    def draw(self):
        assertion.assert_is_not_none(self._panel, ArgumentError, code=ArgumentCodes.NONE)

        for objekt in self._panel:
            objekt.draw(self._screen)

    def update(self, panel):
        self._panel = panel

    def run(self):
        while self._alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._alive = False
                    break

                if event.type in self._events:
                    for func in self._events[event.type]:
                        func()

            # run loop
            pygame.display.flip()

            self._clock.tick(60)

        pygame.quit()

    def get_screen(self):
        return self._screen