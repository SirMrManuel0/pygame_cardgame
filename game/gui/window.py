import pygame
import game
import game.gui as gui
from game.gui.panels import *
from game.errors import *
import webbrowser


class Window:
    def __init__(self, dimension, title: str):
        self._events = dict()
        self._dimension: gui.Dimension = dimension
        self._alive = True
        self._title = title
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self._dimension.get_dimensions(), pygame.SRCALPHA)
        self._allPanels = [HomePanel(), PreGamePanel(), RulesPanel()]
        self._panel = self._allPanels[0]
        self._cursorImg = pygame.image.load(game.get_path_resource("cursor", "Cursor"))
        self._cursorImg = pygame.transform.scale(self._cursorImg, (22, 22))
        self._cursorImgRect = self._cursorImg.get_rect()

        def back_to_home_panel():
            self._panel = self._allPanels[0]

        def home_panel_button1_function_listener():
            self._panel = self._allPanels[1]

        def home_panel_button3_function_listener():
            self._panel = self._allPanels[2]

        def home_panel_button4_function_listener():
            webbrowser.open('https://github.com/SirMrManuel0/pygame_cardgame')

        self._allPanels[0].get_object(1).add_event_listener(home_panel_button1_function_listener)
        self._allPanels[0].get_object(2).add_event_listener(home_panel_button1_function_listener)
        self._allPanels[0].get_object(4).add_event_listener(home_panel_button4_function_listener)
        self._allPanels[0].get_object(3).add_event_listener(home_panel_button3_function_listener)
        self._allPanels[1].get_object(0).add_event_listener(back_to_home_panel)
        self._allPanels[2].get_object(0).add_event_listener(back_to_home_panel)

        pygame.display.set_caption(self._title)
        pygame.display.set_icon(pygame.image.load(game.get_path_resource("icons", "purple")))

    def add_event(self, event_type: int, func):
        if event_type in self._events:
            self._events[event_type].append(func)
        else:
            self._events[event_type] = [func]

    def draw(self):
        self._panel.draw(self._screen)
        assertion.assert_is_not_none(self._panel, ArgumentError, code=ArgumentCodes.NONE)

    def update(self):
        self._panel.update()

    def event(self, event):
        self._panel.event(event)

    def run(self):
        while self._alive:

            for event in pygame.event.get():
                self.event(event)
                if event.type == pygame.QUIT:
                    self._alive = False
                    break

                if event.type in self._events:
                    for func in self._events[event.type]:
                        func()

            self._screen.fill(gui.globals.BACKGROUND_COLOR.get_data())
            light: list = list(gui.globals.COLOR_OF_LIGHT.get_data())
            light.append(0)
            pygame.draw.circle(self._screen, light, pygame.mouse.get_pos(), 30)

            oneIsHovered = False
            for object_ in self._panel:
                if type(object_).__name__ == "Button":
                    if object_.is_hovered():
                        oneIsHovered = True

            self.draw()
            self.update()

            if oneIsHovered:
                self._cursorImgRect.center = pygame.mouse.get_pos()
                self._screen.blit(self._cursorImg, self._cursorImgRect)
                pygame.mouse.set_visible(False)
            else:
                pygame.mouse.set_visible(True)

            # run loop
            pygame.display.flip()

            self._clock.tick(60)

        pygame.quit()

    def get_screen(self):
        return self._screen
