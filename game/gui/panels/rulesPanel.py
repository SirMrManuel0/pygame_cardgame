from game.gui.panels import Panel
from game.gui.objects import Rectangle
from game.gui.objects import Text
from game.gui.objects import Button
from useful_utility.algebra import Vector
from game.gui import globals

class RulesPanel(Panel):
    def __init__(self):
        super().__init__()

        backButton = Button(
            Vector([35, 35]),
            100, 30,
            Vector([250, 241, 230]),
            "Zurück",
            20
        )

        self.add_object(backButton)

        title = Text(Vector([10, 20]), Vector([255, 255, 255]), "Cabooo", 100)
        title.centerAbsoluteX()

        self.add_object(title)

