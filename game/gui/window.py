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
        self._screen = pygame.display.set_mode(self._dimension.get_dimensions())
        self._allPanels = [HomePanel(), GamePanel(), RulesPanel()]
        self._backgroundImage =  pygame.image.load("./resources/images/background.jpg")
        self._backgroundImageRect = self._backgroundImage.get_rect()
        self._panel = self._allPanels[0]
        self._cursorImg = pygame.image.load("./resources/cursor/cursor.png")
        self._cursorImg  = pygame.transform.scale(self._cursorImg, (22, 22))
        self._cursorImgRect = self._cursorImg.get_rect()

        def backToHomePanel():
            self._panel = self._allPanels[0]

        def homePanelButton1FunctionListener():
            self._panel = self._allPanels[1]

        def homePanelButton3FunctionListener():
            self._panel = self._allPanels[2]

        def homePanelButton4FunctionListener():
            webbrowser.open('https://github.com/SirMrManuel0/pygame_cardgame')

        self._allPanels[0].get_object(1).addEventListener(homePanelButton1FunctionListener)
        self._allPanels[0].get_object(2).addEventListener(homePanelButton1FunctionListener)
        self._allPanels[0].get_object(4).addEventListener(homePanelButton4FunctionListener)
        self._allPanels[0].get_object(3).addEventListener(homePanelButton3FunctionListener)
        self._allPanels[1].get_object(0).addEventListener(backToHomePanel)
        self._allPanels[2].get_object(0).addEventListener(backToHomePanel)


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



    def run(self):
        while self._alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._alive = False
                    break

                if event.type in self._events:
                    for func in self._events[event.type]:
                        func()

            self._screen.fill((0, 0, 0))
            self._screen.blit(self._backgroundImage, self._backgroundImageRect)

            oneIsHoverd = False
            for object in self._panel:
                if type(object).__name__ == "Button":
                    if (object.isHoverd()):
                        oneIsHoverd = True

            self.draw()
            self.update()

            if oneIsHoverd:
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