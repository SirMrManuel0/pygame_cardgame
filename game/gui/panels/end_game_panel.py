from game.gui.panels import Panel
from game.gui.objects import Rectangle
from game.gui.objects import Text
from game.gui.objects import Button
from game.gui.objects import Ghost
from pylix.algebra import Vector
from game.gui import globals
from game.gui.objects import Fireworks
import pygame
import sys

class EndPanel(Panel):

    def update_animation(self, dt):
        self._firework.update_animation(dt)
        self._firework2.update_animation(dt)
        self.ghost.update_animation(dt)

    def __init__(self):
        super().__init__()

        self._card_sum = 39
        self._number_of_rounds = 23

        self.ghost = Ghost()
        self.add_object(self.ghost)

        self._firework = Fireworks(
            min(round((50 - self._card_sum) * (self._number_of_rounds / 4)), 200),
            Vector([100, globals.SIZE[1] + 10]),
            Vector([100, 120])
        )
        self.add_object(self._firework)


        self._firework2 = Fireworks(
            min(round((50 - self._card_sum) * (self._number_of_rounds / 4)), 200),
            Vector([globals.SIZE[0] - 100, globals.SIZE[1] + 10]),
            Vector([60, 80])
        )
        self.add_object(self._firework2)

        gameEnded = Text(Vector([0, 100]), Vector([255, 255, 255]), "Game ended!", 80)
        gameEnded.center_absolute_x()
        self.add_object(gameEnded)




        margin = 300
        margin2 = 100
        marginTop = 20

        winnerText= Text(Vector([globals.SIZE[0] / 2 - margin, 180 + marginTop]), Vector([255, 255, 255]), "Winner : ", 30)
        self.add_object(winnerText)
        winner = Text(Vector([globals.SIZE[0] / 2 + margin2, 180 + marginTop]), Vector([255, 255, 255]), "Immanuel Kant", 40)
        self.add_object(winner)

        caboCalledText = Text(Vector([globals.SIZE[0] / 2 - margin, 220 + marginTop]), Vector([255, 255, 255]), "Cabo was called by : ", 30)
        self.add_object(caboCalledText)
        caboCalled = Text(Vector([globals.SIZE[0] / 2 + margin2, 220 + marginTop]), Vector([255, 255, 255]), "Friedrich Nietzsche", 40)
        self.add_object(caboCalled)

        gameDuarationText = Text(Vector([globals.SIZE[0] / 2 - margin, 260 + marginTop]), Vector([255, 255, 255]), "Game duration : ", 30)
        self.add_object(gameDuarationText)
        gameDuaration = Text(Vector([globals.SIZE[0] / 2 + margin2, 260 + marginTop]), Vector([255, 255, 255]), "20s", 40)
        self.add_object(gameDuaration)

        numberOfRoundsText = Text(Vector([globals.SIZE[0] / 2 - margin, 300 + marginTop]), Vector([255, 255, 255]), "Number of rounds : ", 30)
        self.add_object(numberOfRoundsText)
        numberOfRounds = Text(Vector([globals.SIZE[0] / 2 + margin2, 300 + marginTop]), Vector([255, 255, 255]), "5", 40)
        self.add_object(numberOfRounds)

        winningSumText = Text(Vector([globals.SIZE[0] / 2 - margin, 340 + marginTop]), Vector([255, 255, 255]), "Card sum of the winner : ", 30)
        self.add_object(winningSumText)
        winningSum = Text(Vector([globals.SIZE[0] / 2 + margin2, 340 + marginTop]), Vector([255, 255, 255]), "2", 40)
        self.add_object(winningSum)

        self._exitButton = Button(
            Vector([globals.SIZE[0] / 2 - 110, 340 + marginTop + 90]),
            100, 30,
            Vector([255, 98, 66]),
            "Exit",
            20
        )
        self._exitButton.add_event_listener(lambda: sys.exit())

        self.add_object(self._exitButton)

        self.new_game_button = Button(
            Vector([globals.SIZE[0] / 2, 340 + marginTop + 90]),
            140, 30,
            Vector([125, 245, 183]),
            "New Game",
            20
        )
        self.add_object(self.new_game_button)