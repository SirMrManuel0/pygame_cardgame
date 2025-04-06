import pygame
import game
import game.gui as gui
from game.gui.panels.home_panel import HomePanel
from game.gui.panels.pre_game_panel import PreGamePanel
from game.gui.panels.rules_panel import RulesPanel
from game.gui.panels.game_panel import GamePanel
from game.gui.panels.end_game_panel import EndPanel
from game.errors.base_errors import *
import game.errors.assertion as assertion

class Window:

    def __init__(self, dimension, title: str):
        self._events = dict()
        self._dimension: gui.Dimension = dimension
        self._alive = True
        self._title = title
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self._dimension.get_dimensions(), pygame.SRCALPHA)
        self._allPanels = [HomePanel, PreGamePanel, RulesPanel, GamePanel, EndPanel]
        self._panel = None
        self._cursorImg = pygame.image.load(game.get_path_resource("cursor", "Cursor"))
        self._cursorImg = pygame.transform.scale(self._cursorImg, (22, 22))
        self._cursorImgRect = self._cursorImg.get_rect()

        self.createHomePanel()

        pygame.display.set_caption(self._title)
        pygame.display.set_icon(pygame.image.load(game.get_path_resource("icons", "purple")))

    def createHomePanel(self):
        self._panel = self._allPanels[0]()
        self._panel.start_btn.add_event_listener(self.createPreGamePanel)

    def createPreGamePanel(self):
        self._panel = self._allPanels[1]()
        self._panel.start_button.add_event_listener(self.createGamePanel)

    def createAnleitungPanel(self):
        self._panel = self._allPanels[2]()

    def createGamePanel(self):
        player_count, ai_count, player_pos, ai_pos, cards = self._panel.get_for_game()
        self._panel = self._allPanels[3](player_count, ai_count, player_pos, ai_pos, cards, self.create_end_game_panel)

    def create_end_game_panel(self):
        winner, cabo_caller, game_duration, number_of_rounds, sum_card_of_winner = self._panel.get_for_end_game()
        self._panel = self._allPanels[4](winner, cabo_caller, game_duration, number_of_rounds, sum_card_of_winner)

        self._panel.new_game_button.add_event_listener(self.createPreGamePanel)

    def add_event(self, event_type: int, func):
        if event_type in self._events:
            self._events[event_type].append(func)
        else:
            self._events[event_type] = [func]

    def draw(self):
        self._panel.draw(self._screen)
        assertion.assert_is_not_none(self._panel, ArgumentError, code=ArgumentCodes.NONE)

    def update(self, dt):
        self._panel.update()
        self._panel.update_animation(dt)

    def event(self, event):
        self._panel.event(event)

    def run(self):
        while self._alive:
            dt = self._clock.tick(gui.globals.FPS)

            for event in pygame.event.get():
                self.event(event)
                if event.type == pygame.QUIT:
                    self._alive = False
                    break

                if event.type in self._events:
                    for func in self._events[event.type]:
                        func()

            self._screen.fill(gui.globals.BACKGROUND_COLOR.get_data())

            oneIsHovered = False
            for object_ in self._panel:
                if type(object_).__name__ == "Button":
                    if object_.is_hovered():
                        oneIsHovered = True

            self.draw()
            self.update(dt / 1000)

            if oneIsHovered:
                self._cursorImgRect.center = pygame.mouse.get_pos()
                self._screen.blit(self._cursorImg, self._cursorImgRect)
                pygame.mouse.set_visible(False)
            else:
                pygame.mouse.set_visible(True)

            light: list = list(gui.globals.BRIGHT_COLOR.get_data())
            light.append(10)

            for i in range(20):
                radius: float = 30 + i
                circle = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(circle, light, (radius, radius), radius)
                self._screen.blit(circle, (pygame.mouse.get_pos()[0] - radius, pygame.mouse.get_pos()[1] - radius))

            # run loop
            pygame.display.flip()

        pygame.quit()

    def get_screen(self):
        return self._screen
