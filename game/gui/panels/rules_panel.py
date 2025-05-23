from game.gui.panels import Panel
from game.gui.objects import Rectangle
from game.gui.objects import Text
from game.gui.objects import Button
from game.gui.objects import Ghost
from pylix.algebra import Vector
from game.gui import globals

class RulesPanel(Panel):
    def __init__(self):
        super().__init__()

        self.ghost = Ghost()
        self.add_object(self.ghost)

        backButton = Button(
            Vector([35, 35]),
            100, 30,
            Vector([250, 241, 230]),
            "Zurück",
            20
        )

        self.add_object(backButton)

        title = Text(Vector([10, 20]), Vector([255, 255, 255]), "Cabuh!", 100)
        title.center_absolute_x()

        self.add_object(title)

    def update_animation(self, dt):
        self.ghost.update_animation(dt)


