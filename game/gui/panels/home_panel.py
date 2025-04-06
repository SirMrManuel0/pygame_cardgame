from game.gui.panels import Panel
from game.gui.objects import Rectangle
from game.gui.objects import Text
from game.gui.objects import Button
from game.gui.objects import Ghost
from pylix.algebra import Vector
from game.gui import globals
import webbrowser


class HomePanel(Panel):
    def __init__(self):
        super().__init__()

        # self.add_object(Rectangle(Vector([10, 10]), 100, 100, Vector([100, 10, 10])))

        # a = Text(Vector([0, 20]), Vector([100, 100, 10]), "Cabuuuuh!", 100)
        # a.centerX()

        # self.add_object(a)

        self.ghost = Ghost()
        self.add_object(self.ghost)

        title = Text(Vector([10, 20]), Vector([255, 255, 255]), "Cabuh!", 100)
        title.center_absolute_x()

        self.add_object(title)

        self.start_btn = Button(
            Vector([globals.SIZE[0] / 2 - 200, 250]),
            400, 30,
            Vector([250, 241, 230]),
            "Play!",
            20
        )
        self.add_object(self.start_btn)

        self.anleitung_btn = Button(
            Vector([globals.SIZE[0] / 2 - 200, 330]),
            400, 30,
            Vector([250, 241, 230]),
            "Anleitungen",
            20
        )
        self.anleitung_btn.add_event_listener(lambda : webbrowser.open("http://www.smiling-monster.de/spiele/smg007/download/SMG-Cabo-DE.pdf"))
        self.add_object(self.anleitung_btn)

        btn3 = Button(
            Vector([globals.SIZE[0] / 2 - 200, 410]),
            400, 30,
            Vector([250, 241, 230]),
            "Check out the code",
            20
        )
        btn3.add_event_listener(lambda : webbrowser.open("https://github.com/SirMrManuel0/pygame_cardgame"))
        self.add_object(btn3)

        text = Text(Vector([10, globals.SIZE[1] - 20]), Vector([255, 255, 255]), "Ein Spiel von : Tarik, Louis & Vito",
                    20)
        self.add_object(text)

    def update_animation(self, dt):
        self.ghost.update_animation(dt)
