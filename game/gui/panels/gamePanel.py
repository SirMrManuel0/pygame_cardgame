from game.gui.panels import Panel
from game.gui.objects import Rectangle
from game.gui.objects import Text
from game.gui.objects import Button
from game.gui.objects import Card
from useful_utility.algebra import Vector
from game.logic.logic import CaboLogic
from game.gui import globals

class GamePanel(Panel):
    def __init__(self):
        super().__init__()
        self.gameLogic = CaboLogic()
        # self.add_object(Rectangle(Vector([10, 10]), 100, 100, Vector([100, 10, 10])))

        # a = Text(Vector([0, 20]), Vector([100, 100, 10]), "Cabuuuuh!", 100)
        # a.centerX()

        # self.add_object(a)

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

        c1 = Card(Vector([350, 150]), "Karte-11.png")
        self.add_object(c1)

        c2 = Card(Vector([650, 150]), "Karte-Rueck.png")
        self.add_object(c2)

