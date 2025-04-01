from game.gui.panels import Panel
from game.gui.objects import Button
from game.gui.objects import Ellipse
from game.gui.objects import Card
from useful_utility.algebra import Vector
from game.logic.logic import CaboLogic
from game.gui import globals


class PreGamePanel(Panel):
    def __init__(self):
        super().__init__()
        self.gameLogic = CaboLogic()
        self._card_scale_deck: float = .2
        self._card_scale_player: float = .19
        # self.add_object(Rectangle(Vector([10, 10]), 100, 100, Vector([100, 10, 10])))

        # a = Text(Vector([0, 20]), Vector([100, 100, 10]), "Cabuuuuh!", 100)
        # a.centerX()

        # self.add_object(a)

        second_light: Ellipse = Ellipse(
            self._middlePoint,
            460,
            310,
            globals.DIFFUSED_LIGHT
        )
        second_light.set_position_from_center(self._middlePoint)
        self.add_object(second_light)

        light_ellipse_in_the_middle_of_the_screen_that_lays_below_the_cards = Ellipse(
            self._middlePoint,
            420,
            270,
            globals.COLOR_OF_LIGHT
        )
        light_ellipse_in_the_middle_of_the_screen_that_lays_below_the_cards.set_position_from_center(self._middlePoint)

        self.add_object(light_ellipse_in_the_middle_of_the_screen_that_lays_below_the_cards)

        c1 = Card(Vector([350, 150]), "Karte-11.png", self._card_scale_deck)
        c1.set_position_from_center(self._middlePoint - Vector((0.75 * c1.get_size()[0], 0)))
        self.add_object(c1)

        c2 = Card(Vector([350, 150]), "Karte-Rueck.png", self._card_scale_deck)
        c2.set_position_from_center(self._middlePoint + 0.75 * Vector((c2.get_size()[0], 0)))
        self.add_object(c2)

        start_button = Button(
            Vector([0, 0]),
            250, 40,
            globals.BACKGROUND_COLOR,
            "Play!",
            40,
            text_color=Vector([255, 255, 255])
        )
        start_button.set_position_from_center(self._middlePoint)
        self.add_object(start_button)

        #           pos2
        # pos4      deck        pos3
        #           pos1
        self._cards: int = 4
        self._players: int = 2
        self._middle_point_pos1: Vector = Vector([globals.SIZE[0] / 2, globals.SIZE[1]])
        self._middle_point_pos2: Vector = Vector([globals.SIZE[0] / 2, 0])
        self._middle_point_pos3: Vector = Vector([globals.SIZE[0], globals.SIZE[1] / 2])
        self._middle_point_pos4: Vector = Vector([0, globals.SIZE[1] / 2])
        self._pos1: list = [
            Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player),
            Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player),
            Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player),
            Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player)
        ]
        self._pos2: list = [
            Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player),
            Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player),
            Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player),
            Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player)
        ]
        self._pos3: list = list()
        self._pos4: list = list()
        self.set_player_card_location()
        self.update_cards()

    def set_player_cards(self):
        ...

    def set_player_card_location(self):
        temp: Card = Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player)
        #                                   Summe der Kartenbreiten          Summe der Abstände zwischen den Karten
        card_width = temp.get_size()[0]
        gap_width = .2 * temp.get_size()[0]
        total_card_width: float = temp.get_size()[0] * self._cards + gap_width * (self._cards - 1)
        del temp

        offset_non_changing: float = 0

        if len(self._pos1) > 0:
            offset_x: float = total_card_width / 2 - card_width / 2
            offset_y: float = offset_non_changing
            for card in self._pos1:
                card.set_position_from_center(self._middle_point_pos1 - Vector([offset_x, offset_y]))
                offset_x -= card_width + gap_width

        if len(self._pos2) > 0:
            offset_x: float = total_card_width / 2 - card_width / 2
            offset_y: float = offset_non_changing
            for card in self._pos2:
                card.set_position_from_center(self._middle_point_pos2 - Vector([offset_x, offset_y]))
                offset_x -= card_width + gap_width

        if len(self._pos3) > 0:
            offset_x: float = offset_non_changing
            offset_y: float = total_card_width / 2 - card_width / 2
            for card in self._pos3:
                card.set_position_from_center(self._middle_point_pos3 - Vector([offset_x, offset_y]))
                offset_x -= card_width + gap_width

        if len(self._pos4) > 0:
            offset_x: float = offset_non_changing
            offset_y: float = total_card_width / 2 - card_width / 2
            for card in self._pos4:
                card.set_position_from_center(self._middle_point_pos4 - Vector([offset_x, offset_y]))
                offset_x -= card_width + gap_width

    def update_cards(self):
        card_counter: int = 0
        saved_index: int = -1
        for i, object_ in enumerate(self._objekte):
            if not isinstance(object_, Card):
                continue
            card_counter += 1
            if card_counter <= 2:
                continue

            saved_index: int = i
            break

        while saved_index < len(self._objekte) and isinstance(self._objekte[saved_index], Card):
            self._objekte.pop(saved_index)

        for card in self._pos1:
            self._objekte.append(card)

        for card in self._pos2:
            self._objekte.append(card)

        for card in self._pos3:
            self._objekte.append(card)

        for card in self._pos4:
            self._objekte.append(card)
