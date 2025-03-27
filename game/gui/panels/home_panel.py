from game.gui.panels import Panel
from game.gui.objects import Rectangle
from game.gui.objects import Text
from game.gui.objects import Button
from useful_utility.algebra import Vector
from game.gui import globals

class HomePanel(Panel):
    def __init__(self):
        super().__init__()

        # self.add_object(Rectangle(Vector([10, 10]), 100, 100, Vector([100, 10, 10])))

        # a = Text(Vector([0, 20]), Vector([100, 100, 10]), "Cabuuuuh!", 100)
        # a.centerX()

        # self.add_object(a)

        btn = Button(Vector([10, 10]), 100, 100, Vector([0, 200, 0]), "Hello")
        self.add_object(btn)

