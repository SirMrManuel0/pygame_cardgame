from useful_utility.algebra import Vector

from game.gui.panels import Panel
from game.gui.objects import Button
from game.gui.objects import Ellipse
from game.gui.objects import Card
from game.logic.logic import CaboLogic
from game.gui import globals
from game.gui.objects import Text


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

        add_button_width = 50
        self._add_pos3_button = Button(
            Vector([0, 0]),
            add_button_width, 20,
            globals.BRIGHT_COLOR,
            "Add",
            20
        )
        self._add_pos3_button.set_position_from_center(Vector([globals.SIZE[0] - add_button_width, globals.SIZE[1] / 2]))
        self._add_pos3_button.add_event_listener(self.add_player_3)
        self.add_object(self._add_pos3_button)

        self._minus_pos3_button = Button(
            Vector(dimension=2),
            add_button_width + 5, 20,
            globals.BRIGHT_COLOR,
            "Remove",
            20
        )

        self._ai_pos3_button = Button(
            Vector(dimension=2),
            add_button_width, 20,
            globals.BRIGHT_COLOR,
            "AI",
            20
        )
        self._minus_pos3_button.set_position_from_center(Vector([
            globals.SIZE[0] - add_button_width * 3,
            globals.SIZE[1] / 2 - 20
        ]))
        self._ai_pos3_button.set_position_from_center(Vector([
            globals.SIZE[0] - add_button_width * 3,
            globals.SIZE[1] / 2 + 20
        ]))
        self._minus_pos3_button.add_event_listener(self.remove_pos3)
        self._ai_pos3_button.add_event_listener(self.make_pos3_ai)

        self._add_pos4_button = Button(
            Vector([0, 0]),
            add_button_width, 20,
            globals.BRIGHT_COLOR,
            "Add",
            20
        )
        self._add_pos4_button.set_position_from_center(Vector([add_button_width, globals.SIZE[1] / 2]))
        self._add_pos4_button.add_event_listener(self.add_player_4)
        self.add_object(self._add_pos4_button)

        self._minus_pos4_button = Button(
            Vector(dimension=2),
            add_button_width + 5, 20,
            globals.BRIGHT_COLOR,
            "Remove",
            20
        )

        self._ai_pos4_button = Button(
            Vector(dimension=2),
            add_button_width, 20,
            globals.BRIGHT_COLOR,
            "AI",
            20
        )
        self._minus_pos4_button.set_position_from_center(Vector([add_button_width * 3, globals.SIZE[1] / 2 - 20]))
        self._ai_pos4_button.set_position_from_center(Vector([add_button_width * 3, globals.SIZE[1] / 2 + 20]))
        self._minus_pos4_button.add_event_listener(self.remove_pos4)
        self._ai_pos4_button.add_event_listener(self.make_pos4_ai)

        temp_card = Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player)
        card_height = temp_card.get_size()[1]
        del temp_card

        cards_button_width, cards_button_font_size, cards_button_margin = 30, 50, 0
        text_color = globals.BRIGHT_COLOR
        hover_color = 1/5 * (3 * globals.BACKGROUND_COLOR + 2 * globals.HOVER_COLOR)
        self._plus_cards = Button(
            Vector(dimension=2),
            cards_button_width, cards_button_font_size,
            globals.BACKGROUND_COLOR,
            "+",
            cards_button_margin,
            text_color=text_color,
            hover_color=hover_color
        )
        self._minus_cards = Button(
            Vector(dimension=2),
            cards_button_width, cards_button_font_size,
            globals.BACKGROUND_COLOR,
            "-",
            cards_button_margin,
            text_color=text_color,
            hover_color=hover_color
        )
        self._plus_cards.set_position_from_center(Vector([
            self._middlePoint[0] + 90,
            globals.SIZE[1] - (card_height - 10)
        ]))
        self._minus_cards.set_position_from_center(Vector([
            self._middlePoint[0] - 90,
            globals.SIZE[1] - (card_height - 10)
        ]))
        self._plus_cards.add_event_listener(self.increase_cards)
        self._minus_cards.add_event_listener(self.decrease_cards)
        self._objekte.append(self._plus_cards)
        self._objekte.append(self._minus_cards)

        self._cards: int = 4

        self._cards_display = Text(
            Vector(),
            globals.BRIGHT_COLOR,
            str(self._cards),
            80
        )
        self._cards_display.set_position_from_center(Vector([
            self._middlePoint[0],
            globals.SIZE[1] - (card_height - 10)
        ]))
        self._objekte.append(self._cards_display)

        #           pos2
        # pos4      deck        pos3
        #           pos1
        self._players: int = 2
        # [self._pos3, self._pos4
        self._extra_player_positions: list = [False, False]
        self._middle_point_pos1: Vector = Vector([globals.SIZE[0] / 2, globals.SIZE[1]])
        self._middle_point_pos2: Vector = Vector([globals.SIZE[0] / 2, 0])
        self._middle_point_pos3: Vector = Vector([globals.SIZE[0], globals.SIZE[1] / 2])
        self._middle_point_pos4: Vector = Vector([0, globals.SIZE[1] / 2])
        self._pos1: list = list()
        self._pos2: list = list()
        self._pos3: list = list()
        self._pos4: list = list()
        self.set_player_cards()
        self.set_player_card_location()
        self.update_cards()

    def set_player_cards(self):
        self._pos1: list = list()
        self._pos2: list = list()
        self._pos3: list = list()
        self._pos4: list = list()
        for _ in range(self._cards):
            self._pos1.append(Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player))
            self._pos2.append(Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player))
            if self._extra_player_positions[0]:
                self._pos3.append(Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player, rotation=90))
            if self._extra_player_positions[1]:
                self._pos4.append(Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player, rotation=90))

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
                offset_y -= card_width + gap_width

        if len(self._pos4) > 0:
            offset_x: float = offset_non_changing
            offset_y: float = total_card_width / 2 - card_width / 2
            for card in self._pos4:
                card.set_position_from_center(self._middle_point_pos4 - Vector([offset_x, offset_y]))
                offset_y -= card_width + gap_width

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

    def add_player_3(self):
        self._players += 1
        self._extra_player_positions[0] = True
        self._objekte.remove(self._add_pos3_button)
        self._objekte.append(self._minus_pos3_button)
        self._objekte.append(self._ai_pos3_button)
        self.set_player_cards()
        self.set_player_card_location()
        self.update_cards()

    def add_player_4(self):
        self._objekte.remove(self._add_pos4_button)
        self._objekte.append(self._minus_pos4_button)
        self._objekte.append(self._ai_pos4_button)
        self._players += 1
        self._extra_player_positions[1] = True
        self.set_player_cards()
        self.set_player_card_location()
        self.update_cards()

    def remove_pos3(self):
        self._players -= 1
        self._extra_player_positions[0] = False
        self._objekte.append(self._add_pos3_button)
        self._objekte.remove(self._minus_pos3_button)
        self._objekte.remove(self._ai_pos3_button)
        self.set_player_cards()
        self.set_player_card_location()
        self.update_cards()

    def remove_pos4(self):
        self._players -= 1
        self._extra_player_positions[1] = False
        self._objekte.append(self._add_pos4_button)
        self._objekte.remove(self._minus_pos4_button)
        self._objekte.remove(self._ai_pos4_button)
        self.set_player_cards()
        self.set_player_card_location()
        self.update_cards()

    def make_pos3_ai(self):
        ...

    def make_pos4_ai(self):
        ...

    def increase_cards(self):
        ...

    def decrease_cards(self):
        ...
