import pygame
import game
import game.gui as gui

class Window:
    def __init__(self, dimension, title: str):
        self._events = dict()
        self._dimension: gui.Dimension = dimension
        self._alive = True
        self._title = title
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self._dimension.get_dimensions())

        pygame.display.set_caption(self._title)

        if game.is_dark():
            pygame.display.set_icon(pygame.image.load(game.get_path_resource("icons", "purple")))



    def add_event(self, event_type: int, func):
        if event_type in self._events:
            self._events[event_type].append(func)
        else:
            self._events[event_type] = [func]


    def draw(self):
        # Zeichnen Methoden
        ...

    def update(self):
        ...

    def run(self):
        while self._alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._alive = False
                    break

                if event.type in self._events:
                    for func in self._events[event.type]:
                        func()

            pygame.display.flip()

            self._clock.tick(60)

        pygame.quit()

    def get_screen(self):
        return self._screen