from typing import Optional
import time

from pylix.algebra import Vector
from pylix.errors.decorator import TODO
from typing_extensions import override

from game.deck import DiscardPile, Shuffle
from game.deck import Card as logCard
from game.event_handler import LogicEvent, LogicEvents
from game.gui.animation import AnimationHandler
from game.gui.objects import Ellipse, Card, Button, Text
from game.logic import CaboLogic
from game.logic.logic import DrawOptions
from game.logic.w_ai_logic import LogicWAI
from game.enemies import BaseEnemy
from game.gui.panels import Panel
from game.gui import globals


def card_name_from_value(value) -> str:
    if 0 <= value <= 9:
        return f"Karte-0{str(value)}.png"
    if 10 <= value <= 13:
        return f"Karte-{str(value)}.png"
    return f"Karte-Rueck.png"


class GamePanel(Panel):
    def __init__(self, player_count, ai_count, player_pos, ai_pos, cards):
        """

        :param player_count: ALL players including AI
        :param ai_count: AI count
        :param player_pos: Are 3 or 4 active
        :param ai_pos: is AI on 2, 3, 4
        :param cards: How many cards
        """
        super().__init__()
        self._player_count: int = player_count
        self._human_count: int = player_count - ai_count
        self._ai_count: int = ai_count
        self._player_pos: tuple[bool, bool] = player_pos
        self._ai_pos: tuple[bool, bool, bool] = ai_pos
        self._has_ai: bool = any(self._ai_pos)
        self._cards: int = cards
        # 1 -> Human, 0 -> AI
        self._order: list = [1]
        self._order.append(1 if not self._ai_pos[0] else 0)

        if any(self._player_pos):
            if all(self._player_pos):
                self._order.append(1 if not self._ai_pos[1] else 0)
                self._order.append(1 if not self._ai_pos[2] else 0)
            elif self._player_pos[0]:
                self._order.append(1 if not self._ai_pos[1] else 0)
            else:
                self._order.append(1 if not self._ai_pos[2] else 0)

        self._logic = CaboLogic(self._player_count, self._cards) if self._ai_count == 0 else LogicWAI(self._human_count,
                                                                                                      self._cards,
                                                                                                      self._ai_count)
        temp_players: list = [*self._logic.get_players()]
        self._start_ai: int = -1
        if self._has_ai:
            for player in temp_players:
                if isinstance(player, BaseEnemy):
                    self._start_ai = player.get_pid()
                    break
        del temp_players

        self._mask_gui_logic: dict[int, int] = dict()
        human_i: int = 0
        ai_i: int = self._start_ai
        for i, player in enumerate(self._order):
            if player == 1:
                self._mask_gui_logic[i + 1] = human_i
                human_i += 1
            if player == 0:
                self._mask_gui_logic[i + 1] = ai_i
                ai_i += 1

        self._mask_logic_gui: dict = {v: k for k, v in self._mask_gui_logic.items()}

        # ------------------------------ finish logic init -------------------------------------------------------------
        self._card_scale_deck: float = .2
        self._card_scale_player: float = .19
        self._active_player_gui: int = 1
        self._active_player_logic: int = 0
        self._round_counter: int = 1

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

        c1 = Card(Vector([350, 150]), "Karte-Rueck.png", self._card_scale_deck)
        c1.set_position_from_center(Vector(default_value=-200))
        self.add_object(c1)

        self._c2 = Card(Vector([350, 150]), "Karte-Rueck.png", self._card_scale_deck)
        self._deck_center_position = self._middlePoint + 0.75 * Vector((self._c2.get_size()[0], 0))
        self._c2.set_position_from_center(self._deck_center_position)
        self.add_object(self._c2)

        self._extra_player_positions = [*self._player_pos]
        self._middle_point_pos1: Vector = Vector([globals.SIZE[0] / 2, globals.SIZE[1]])
        self._middle_point_pos2: Vector = Vector([globals.SIZE[0] / 2, 0])
        self._middle_point_pos3: Vector = Vector([globals.SIZE[0], globals.SIZE[1] / 2])
        self._middle_point_pos4: Vector = Vector([0, globals.SIZE[1] / 2])
        self._pos1: list = list()
        self._pos2: list = list()
        self._pos3: list = list()
        self._pos4: list = list()

        self._animation1 = list()
        self._animation2 = list()
        self._animation3 = list()
        self._animation4 = list()

        self._cabo = False
        self._cabo_caller = -1
        self._handcard: Optional[Card] = None
        self._handcard_pos: Vector = self._middlePoint + Vector([0, 100])
        self._animation_handcard: list = list()
        self._discard_pos: Vector = self._middlePoint - Vector((0.75 * self._c2.get_size()[0], 0))

        self._all_options: list = list()
        self.create_all_options()
        self._phase_1_options: list = [self._all_options[0], self._all_options[1], self._all_options[2]]
        self._phase_2_options: list = [self._all_options[3], self._all_options[4]]

        self._other_ani = list()
        self._swap_selected = list()

        self.set_player_cards()
        self.set_player_card_location()
        self.update_cards()

    def is_active_player_gui_ai(self) -> bool:
        return self._order[self._active_player_logic] == 0

    def phase_1(self, temp=""):
        print("Phase 1:")
        print(self._active_player_logic)
        print(self.is_active_player_gui_ai())
        print(temp)
        if self._logic.event_handler.has_event(LogicEvents.EMPTY_DECK):
            self._logic.event_handler.remove_event_by_kind(LogicEvents.EMPTY_DECK)
            self._logic.restock_deck(Shuffle.DUMP)
        if self.is_active_player_gui_ai() and self._round_counter not in [1, 2]:
            self._ai(self._active_player_logic)
            return
        elif self.is_active_player_gui_ai():
            print("Ai and in round 1, 2")
            print(self._active_player_logic)
            print(self._pos1)
            print(self._pos2)
            print(self._pos3)
            print(self._pos4)
            self.next_player()
            return
        if self._active_player_gui == self._cabo_caller:
            self.end_game()
            return
        if self._round_counter in [1, 2]:
            self.phase_3()
            return
        if self._round_counter == 3 and self._active_player_gui == 1:
            self.draw_from_deck()
            return
        self.update_options(self._phase_1_options[self._cabo:])

    def _ai(self, id_):
        self._logic.ai_phase1(id_)
        self._logic.ai_phase2(id_)
        events = self._logic.get_events()
        if len(events) == 0:
            self.next_player()
            return

        for event in events:
            assert isinstance(event, LogicEvent)
            if event.get_kind() == LogicEvents.PEEK_EFFECT:
                self._logic.ai_phase3(id_)
                self._logic.remove_event(event.get_eid())
            elif event.get_kind() == LogicEvents.SPY_EFFECT:
                self._logic.ai_phase4(id_)
                self._logic.remove_event(event.get_eid())
            elif event.get_kind() == LogicEvents.SWAP_EFFECT:
                self._logic.ai_phase5(id_)
            else:
                self.next_player()

    def phase_2(self):
        self.update_options(self._phase_2_options)

    def delete_options(self):
        to_delete: list = list()
        for index in range(len(self._objekte) - 1, -1, -1):
            if isinstance(self._objekte[index], Button) and self._objekte[index].get_identifier() == "option":
                to_delete.append(index)
        for i in to_delete:
            self._objekte.pop(i)

    def update_options(self, options):
        self.delete_options()
        for option in options:
            self._objekte.append(option)

    def create_all_options(self):
        option_color = (1 / 5) * (4 * globals.BRIGHT_COLOR + 1 * globals.BACKGROUND_COLOR)
        text_color = Vector(dimension=3)
        hover_color = globals.HOVER_COLOR
        font_size = 23
        cabo: Button = Button(
            Vector(),
            100, font_size,
            option_color,
            "Cabo",
            20,
            text_color=text_color,
            identifier="option",
            pos_from_center=self._handcard_pos + Vector([-110, 130]),
            hover_color=hover_color
        )
        cabo.add_event_listener(self.cabo)
        self._all_options.append(cabo)
        draw_from_deck: Button = Button(
            Vector(),
            100, font_size,
            option_color,
            "Deck",
            20,
            text_color=text_color,
            identifier="option",
            pos_from_center=self._handcard_pos + Vector([0, 130]),
            hover_color=hover_color
        )
        draw_from_deck.add_event_listener(self.draw_from_deck)
        self._all_options.append(draw_from_deck)
        draw_from_discard_pile: Button = Button(
            Vector(),
            100, font_size,
            option_color,
            "Ablagestapel",
            20,
            text_color=text_color,
            identifier="option",
            pos_from_center=self._handcard_pos + Vector([110, 130]),
            hover_color=hover_color
        )
        draw_from_discard_pile.add_event_listener(self.draw_from_discard)
        self._all_options.append(draw_from_discard_pile)
        card_to_discard: Button = Button(
            Vector(),
            100, font_size,
            option_color,
            "Wegwerfen",
            20,
            text_color=text_color,
            identifier="option",
            pos_from_center=self._handcard_pos + Vector([-100, 130]),
            hover_color=hover_color
        )
        card_to_discard.add_event_listener(self.throw_away)
        self._all_options.append(card_to_discard)
        swap_with_self: Button = Button(
            Vector(),
            100, font_size,
            option_color,
            "Tauschen",
            20,
            text_color=text_color,
            identifier="option",
            pos_from_center=self._handcard_pos + Vector([100, 130]),
            hover_color=hover_color
        )
        swap_with_self.add_event_listener(self.swap_self)
        self._all_options.append(swap_with_self)

    def draw_from_deck(self):
        self._logic.draw(self._active_player_logic, DrawOptions.GAME_DECK)
        self.create_handcard(self._logic[self._active_player_logic].get_active_card().get_value())
        self.phase_2()

    def draw_from_discard(self):
        discard_pile: DiscardPile = self._logic.get_discard_pile()
        all_ = discard_pile.get_all()
        if len(all_) > 1:
            card: logCard = all_[1]
            last_top_name = card_name_from_value(card.get_value())
            self._objekte[2].set_name(last_top_name)
        else:
            self._objekte[2] = Card(Vector([350, 150]), "Karte-Rueck.png", self._card_scale_deck,
                                    pos_from_center=Vector(default_value=-200))
        self._logic.draw(self._active_player_logic, DrawOptions.DISCARD_PILE)
        self.create_handcard(self._logic[self._active_player_logic].get_active_card().get_value())
        self.phase_2()

    def cabo(self):
        self._cabo = True
        self._cabo_caller = self._active_player_gui
        self._objekte.append(Text(Vector(), Vector(dimension=3), "Cabo has been called!", 30,
                                  pos_from_center=self._middlePoint, identifier="cabo_text"))
        self.delete_options()
        a = AnimationHandler(
            Vector(),
            Vector(default_value=1),
            globals.EASE_IN_OUT,
            2,
            0
        )
        a.on_finished(self.cabo_notified)
        a.start()
        self._other_ani.append(a)

    def cabo_notified(self):
        to_delete: list = list()
        for index in range(len(self._objekte) - 1, -1, -1):
            if isinstance(self._objekte[index], Text) and self._objekte[index].get_identifier() == "cabo_text":
                to_delete.append(index)
        for i in to_delete:
            self._objekte.pop(i)
        self._logic.cabo(self._active_player_logic)
        self.next_player()

    def swap_self(self):
        temp = Card(Vector(), "Karte-00.png", self._card_scale_player)
        card_width = temp.get_size()[0]
        card_height = temp.get_size()[1]
        del temp
        for i in range(self._cards):
            b = Button(
                Vector(),
                card_width + 5, 100,
                globals.BACKGROUND_COLOR,
                "t",
                card_height,
                identifier="swap_self",
                pos_from_center=self._pos1[i].get_center()
            )
            b.add_event_listener(self.swappy_selfy, i)
            self._objekte.append(b)
        self.delete_options()
        self.update_cards()

    def swappy_selfy(self, card):
        to_delete: list = list()
        for index in range(len(self._objekte) - 1, -1, -1):
            if isinstance(self._objekte[index], (Button, Card)) and self._objekte[index].get_identifier() == "swap_self":
                to_delete.append(index)
        for i in to_delete:
            self._objekte.pop(i)
        self._logic.swap_self(self._active_player_logic, card)
        self._handcard = None
        self.next_player()

    @TODO
    def end_game(self):
        ...

    def throw_away(self):
        self._logic.discard(self._active_player_logic)
        self.delete_options()
        self.move_handcard_discard()
        events = self._logic.get_events()
        if len(events) == 0:
            self.next_player()
            return

        for event in events:
            assert isinstance(event, LogicEvent)
            if event.get_kind() == LogicEvents.PEEK_EFFECT:
                self.phase_3()
                self._logic.remove_event(event.get_eid())
            elif event.get_kind() == LogicEvents.SPY_EFFECT:
                self.phase_4()
                self._logic.remove_event(event.get_eid())
            elif event.get_kind() == LogicEvents.SWAP_EFFECT:
                self.phase_5()
            else:
                self.next_player()

    def phase_3(self):
        peek_buttons: list = list()
        temp = Card(Vector(), "Karte-00.png", self._card_scale_player)
        card_width = temp.get_size()[0]
        card_height = temp.get_size()[1]
        del temp
        print("Phase 3:")
        print(self._active_player_logic)
        print(self._pos1)
        for i in range(self._cards):
            print(self._pos1)
            b = Button(
                Vector(),
                card_width + 5, 100,
                globals.BACKGROUND_COLOR,
                "t",
                card_height,
                identifier="peek",
                pos_from_center=self._pos1[i].get_center()
            )
            b.add_event_listener(self.peek, i)
            peek_buttons.append(b)
            self._objekte.append(peek_buttons[-1])
        self.update_cards()

    def peek(self, card_num):
        self.end_peek()
        see_card: Card = Card(
            Vector(),
            card_name_from_value(self.get_hidden_card_val(self._active_player_logic, card_num)),
            self._card_scale_player,
            pos_from_center=self._pos1[card_num].get_center() - Vector([0, self._pos1[card_num].get_size()[1] / 2]),
            identifier="peek"
        )
        self._objekte.append(see_card)
        a = AnimationHandler(
            Vector(),
            Vector(default_value=1),
            globals.EASE_IN_OUT,
            3,
            0
        )
        a.on_finished(self.next_player)
        a.on_finished(self.end_peek)
        a.start()
        self._other_ani.append(a)

    def end_peek(self):
        to_delete: list = list()
        for index in range(len(self._objekte) - 1, -1, -1):
            if isinstance(self._objekte[index], (Button, Card)) and self._objekte[index].get_identifier() == "peek":
                to_delete.append(index)
        for i in to_delete:
            self._objekte.pop(i)

    def get_hidden_card_val(self, player, card) -> int:
        return self._logic.get_players()[player].get_hidden_cards()[card].get_value()

    def phase_4(self):
        spy_buttons: list = list()
        temp = Card(Vector(), "Karte-00.png", self._card_scale_player)
        card_width = temp.get_size()[0]
        card_height = temp.get_size()[1]
        del temp
        player_list = self._pos1
        all_ = [[self._pos2, False, 2], [self._pos3, False, 1], [self._pos4, False, 3]]
        for player in range(self._player_count - 1):
            spy_buttons.append(list())

            player_list = list()
            p = 0
            for list_ in all_:
                if len(list_[0]) == 0 or list_[1]:
                    continue
                player_list = list_[0]
                p = list_[2]
                list_[1] = True
                break

            for card in range(self._cards):
                width = card_width + 5 if p in [0, 2] else card_height + 15
                height = card_height if p in [0, 2] else (card_width + 5) / 2
                b = Button(
                    Vector(),
                    width, 100,
                    globals.BACKGROUND_COLOR,
                    "t",
                    height,
                    identifier="spy",
                    pos_from_center=player_list[card].get_center()
                )
                b.add_event_listener(self.spy, card, player_list, p)
                spy_buttons[player].append(b)
                self._objekte.append(spy_buttons[player][-1])
        self.update_cards()

    def spy(self, card, player_list, p):
        self.end_spy()
        enemy_player = (self._active_player_logic + p) % self._player_count
        position = player_list[card].get_center()
        if p == 1:
            position -= Vector([player_list[card].get_size()[1] / 2, 0])
        elif p == 2:
            position += Vector([0, player_list[card].get_size()[1] / 2])
        elif p == 3:
            position += Vector([player_list[card].get_size()[1] / 2, 0])
        see_card: Card = Card(
            Vector(),
            card_name_from_value(self.get_hidden_card_val(enemy_player, card)),
            self._card_scale_player,
            pos_from_center=position,
            identifier="spy"
        )
        self._objekte.append(see_card)
        a = AnimationHandler(
            Vector(),
            Vector(default_value=1),
            globals.EASE_IN_OUT,
            3,
            0
        )
        a.on_finished(self.next_player)
        a.on_finished(self.end_spy)
        a.start()
        self._other_ani.append(a)

    def end_spy(self):
        to_delete: list = list()
        for index in range(len(self._objekte) - 1, -1, -1):
            if isinstance(self._objekte[index], (Button, Card)) and self._objekte[index].get_identifier() == "spy":
                to_delete.append(index)
        for i in to_delete:
            self._objekte.pop(i)

    def phase_5(self):
        spy_buttons: list = list()
        temp = Card(Vector(), "Karte-00.png", self._card_scale_player)
        card_width = temp.get_size()[0]
        card_height = temp.get_size()[1]
        del temp
        all_ = [[self._pos2, False, 2], [self._pos3, False, 1], [self._pos4, False, 3], [self._pos1, False, 0]]
        for player in range(self._player_count):
            spy_buttons.append(list())
            player_list = list()
            p = 0
            for list_ in all_:
                if len(list_[0]) == 0 or list_[1]:
                    continue
                player_list = list_[0]
                p = list_[2]
                list_[1] = True
                break

            for card in range(self._cards):
                width = card_width + 5 if p in [0, 2] else card_height
                height = card_height if p in [0, 2] else card_width + 5
                identifier = "swap_other" if p in [1, 2, 3] else "swap_self"
                b = Button(
                    Vector(),
                    width, 100,
                    globals.BACKGROUND_COLOR,
                    "t",
                    height,
                    identifier=identifier,
                    pos_from_center=player_list[card].get_center()
                )
                b.add_event_listener(self.swap, card, player_list, p, identifier)
                spy_buttons[player].append(b)
                self._objekte.append(spy_buttons[player][-1])
        self.update_cards()

    def swap(self, card, player_list, p, identifier):
        self.delete_swap(identifier)
        if len(self._swap_selected) < 1:
            self._swap_selected.append((card, player_list, p, identifier))
            return
        self._swap_selected.append((card, player_list, p, identifier))
        player_id = self._active_player_logic
        enemy_id = (self._active_player_logic + p) % self._player_count
        card_player = self._swap_selected[0][0] if self._swap_selected[0][3] == "swap_self" else self._swap_selected[1][0]
        card_enemy = self._swap_selected[0][0] if self._swap_selected[0][3] == "swap_other" else self._swap_selected[1][0]

        self._logic._swap_effect(player_id, enemy_id, card_player, card_enemy)
        self._swap_selected = list()
        self.next_player()

    def delete_swap(self, ident):
        to_delete: list = list()
        for index in range(len(self._objekte) - 1, -1, -1):
            if isinstance(self._objekte[index], (Button, Card)) and self._objekte[index].get_identifier() == ident:
                to_delete.append(index)
        for i in to_delete:
            self._objekte.pop(i)

    def move_handcard_discard(self):
        i = self._objekte.index(self._handcard)
        name_card = self._handcard.get_name()
        self._objekte[2] = Card(Vector(), name_card, self._card_scale_deck,
                                pos_from_center=self._discard_pos, identifier="discard_top")
        self._handcard = None
        self._objekte.pop(i)

    def next_player(self):
        self._active_player_gui += 1
        self._active_player_logic += 1
        if self._active_player_logic == self._player_count:
            self._active_player_gui = 1
            self._active_player_logic = 0
            self._round_counter += 1

        temp_pos1 = [*self._pos1]
        temp_pos2 = [*self._pos2]
        temp_pos3 = [*self._pos3]
        temp_pos4 = [*self._pos4]

        self._pos4 = [*temp_pos1]
        self._pos1 = [*temp_pos3]
        self._pos3 = [*temp_pos2]
        self._pos2 = [*temp_pos4]

        while len(self._pos1) == 0:
            temp_pos1 = [*self._pos1]
            temp_pos2 = [*self._pos2]
            temp_pos3 = [*self._pos3]
            temp_pos4 = [*self._pos4]
            self._pos4 = [*temp_pos1]
            self._pos1 = [*temp_pos3]
            self._pos3 = [*temp_pos2]
            self._pos2 = [*temp_pos4]

        self.re_reset_player_cards()
        self.update_cards()
        self.set_player_card_location()
        self.phase_1()

    def create_handcard(self, value):
        self._handcard = Card(self._handcard_pos, card_name_from_value(value), self._card_scale_deck)
        self._handcard.set_position_from_center(self._handcard_pos)
        self.update_cards()

    def re_reset_player_cards(self):
        temp_pos1 = [*self._pos1]
        temp_pos2 = [*self._pos2]
        temp_pos3 = [*self._pos3]
        temp_pos4 = [*self._pos4]

        self._pos1 = list()
        self._pos2 = list()
        self._pos3 = list()
        self._pos4 = list()

        self._animation1 = list()
        self._animation2 = list()
        self._animation3 = list()
        self._animation4 = list()

        for _ in temp_pos1:
            self._pos1.append(Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player))

        for _ in temp_pos2:
            self._pos2.append(Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player))

        for _ in temp_pos3:
            self._pos3.append(Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player, rotation=90))

        for _ in temp_pos4:
            self._pos4.append(Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player, rotation=-90))

        del temp_pos1
        del temp_pos2
        del temp_pos3
        del temp_pos4

    def set_player_cards(self):
        self._pos1: list = list()
        self._pos2: list = list()
        self._pos3: list = list()
        self._pos4: list = list()

        self._animation1 = list()
        self._animation2 = list()
        self._animation3 = list()
        self._animation4 = list()

        for _ in range(self._cards):
            self._pos1.append(Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player))
            self._pos2.append(Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player))
            if self._extra_player_positions[0]:
                self._pos3.append(
                    Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player, rotation=90))
            if self._extra_player_positions[1]:
                self._pos4.append(
                    Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player, rotation=-90))

    def set_player_card_location(self):
        temp: Card = Card(Vector(dimension=2), "Karte-Rueck.png", self._card_scale_player)
        #                                   Summe der Kartenbreiten          Summe der Abstände zwischen den Karten
        card_width = temp.get_size()[0]
        card_height = temp.get_size()[1]
        gap_width = .2 * temp.get_size()[0]
        total_card_width: float = temp.get_size()[0] * self._cards + gap_width * (self._cards - 1)
        del temp

        offset_non_changing: float = 0

        if len(self._pos1) > 0:
            offset_x: float = total_card_width / 2 - card_width / 2
            offset_y: float = offset_non_changing
            for i, card in enumerate(self._pos1):
                card.set_position_from_center(
                    self._middle_point_pos1 - Vector([offset_x, offset_y]) + Vector([0, card_height / 2])
                )
                self._animation1.append(AnimationHandler(
                    self._middle_point_pos1 - Vector([offset_x, offset_y]) + Vector([0, card_height / 2]),
                    self._middle_point_pos1 - Vector([offset_x, offset_y]),
                    globals.EASE_IN_OUT,
                    0.9,
                    0
                ))
                self._animation1[-1].start()

                offset_x -= card_width + gap_width
            if self._round_counter in [1, 2] and not self._has_ai:
                self._animation1[-1].on_finished(self.phase_1, "from_the_location_func")
            elif self._round_counter == 1 and self._active_player_gui == 1:
                self._animation1[-1].on_finished(self.phase_1, "from_the_location_func")

        if len(self._pos2) > 0:
            offset_x: float = total_card_width / 2 - card_width / 2
            offset_y: float = offset_non_changing
            for i, card in enumerate(self._pos2):
                card.set_position_from_center(
                    self._middle_point_pos2 - Vector([offset_x, offset_y]) - Vector([0, card_height / 2]))

                self._animation2.append(AnimationHandler(
                    self._middle_point_pos2 - Vector([offset_x, offset_y]) - Vector([0, card_height / 2]),
                    self._middle_point_pos2 - Vector([offset_x, offset_y]),
                    globals.EASE_IN_OUT,
                    0.9,
                    0
                ))
                self._animation2[-1].start()

                offset_x -= card_width + gap_width

        if len(self._pos3) > 0:
            offset_x: float = offset_non_changing
            offset_y: float = total_card_width / 2 - card_width / 2
            for i, card in enumerate(self._pos3):
                card.set_position_from_center(
                    self._middle_point_pos3 + Vector([offset_x, offset_y]) + Vector([card_height / 2, 0]))

                self._animation3.append(AnimationHandler(
                    self._middle_point_pos3 + Vector([offset_x, offset_y]) + Vector([card_height / 2, 0]),
                    self._middle_point_pos3 + Vector([offset_x, offset_y]),
                    globals.EASE_IN_OUT,
                    0.9,
                    0
                ))
                self._animation3[-1].start()

                offset_y -= card_width + gap_width

        if len(self._pos4) > 0:
            offset_x: float = 0
            offset_y: float = total_card_width / 2 - card_width / 2
            for i, card in enumerate(self._pos4):
                card.set_position_from_center(
                    self._middle_point_pos4 - Vector([offset_x, offset_y]) - Vector([card_height / 2, 0]), )

                self._animation4.append(AnimationHandler(
                    self._middle_point_pos4 - Vector([offset_x, offset_y]) - Vector([card_height / 2, 0]),
                    self._middle_point_pos4 - Vector([offset_x, offset_y]),
                    globals.EASE_IN_OUT,
                    0.9,
                    0
                ))
                self._animation4[-1].start()

                offset_y -= card_width + gap_width

    def update_cards(self):
        saved_index = 4
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

        if self._handcard is not None:
            self._objekte.append(self._handcard)

    @override
    def update_animation(self, dt):

        for i, a in enumerate(self._other_ani):
            if a.update(dt) == -1:
                continue

        for i, a in enumerate(self._animation1):
            if a.update(dt) == -1:
                continue
            self._pos1[i].set_position_from_center(a.get_current_animation_step())
            self._pos1[i].set_angle(a.get_current_animation_rotation())

        for i, a in enumerate(self._animation2):
            if a.update(dt) == -1:
                continue

            self._pos2[i].set_position_from_center(a.get_current_animation_step())
            self._pos2[i].set_angle(a.get_current_animation_rotation())

        for i, a in enumerate(self._animation3):
            if a.update(dt) == -1:
                continue

            self._pos3[i].set_position_from_center(a.get_current_animation_step())
            self._pos3[i].set_angle(a.get_current_animation_rotation())

        for i, a in enumerate(self._animation4):
            if a.update(dt) == -1:
                continue

            self._pos4[i].set_position_from_center(a.get_current_animation_step())
            self._pos4[i].set_angle(a.get_current_animation_rotation())
