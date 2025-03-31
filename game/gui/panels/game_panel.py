from game.gui.panels import Panel
from game.gui.objects import Rectangle
from game.gui.objects import Text
from game.gui.objects import Button
from game.gui.objects import Circle
from game.gui.objects import Ellipse
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

        light_ellipse_in_the_middle_of_the_screen_that_lays_below_the_cards = Ellipse(
            self._middlePoint,
            420,
            270,
            Vector([248, 244, 228])
        )
        light_ellipse_in_the_middle_of_the_screen_that_lays_below_the_cards.set_position_from_center(self._middlePoint)

        self.add_object(light_ellipse_in_the_middle_of_the_screen_that_lays_below_the_cards)

        c1 = Card(Vector([350, 150]), "Karte-11.png", 0.2)
        c1.set_position_from_center(self._middlePoint - Vector((0.75 * c1.get_size()[0], 0)))
        self.add_object(c1)

        c2 = Card(Vector([350, 150]), "Karte-Rueck.png", 0.2)
        c2.set_position_from_center(self._middlePoint + 0.75 * Vector((c2.get_size()[0], 0)))
        self.add_object(c2)

        start_button = Button(
            Vector([0, 0]),
            250, 40,
            Vector([62, 76, 84]),
            "Play!",
            40,
            text_color=Vector([255, 255, 255])
        )
        start_button.set_position_from_center(self._middlePoint)
        self.add_object(start_button)
