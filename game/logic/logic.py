# from game import get_path_abs, get_path_resource
from enum import Enum

from game.player import Player
from game.errors import *
from game.deck import GameDeck, DiscardPile, Card, Shuffle
from game.event_handler import LogicEvents, LogicEventHandler
from game.deck.base import Effect


class DrawOptions(Enum):
    DISCARD_PILE: int = 0
    GAME_DECK: int = 1
    CABO: int = 2


class CaboLogic:
    def __init__(self, player_count: int = 4, start_card_count: int = 4):
        assertion.assert_types(player_count, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_types(start_card_count, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_above(start_card_count, 0, ArgumentError, code=ArgumentCodes.TOO_SMALL)
        assertion.assert_above(player_count, 0, ArgumentError, code=ArgumentCodes.TOO_SMALL)
        self._game_deck: GameDeck = GameDeck()
        self._discard_pile: DiscardPile = DiscardPile()
        self._players: list = [Player(self._game_deck, cards=start_card_count, pid=i) for i in range(player_count)]
        self._player_count: int = player_count
        self.event_handler: LogicEventHandler = LogicEventHandler()

    def get_game_deck(self) -> GameDeck:
        return self._game_deck

    def get_discard_pile(self) -> DiscardPile:
        return self._discard_pile

    def get_players(self) -> list:
        return self._players

    def get_player_count(self) -> int:
        return self._player_count

    def get_player_hidden_cards(self) -> tuple:
        return tuple([tuple(player.get_hidden_cards()) for player in self._players])

    def get_player_hidden_card(self, pid: int, card: int) -> Card:
        assertion.assert_types(pid, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_types(card, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_is_positiv(pid, ArgumentError, code=ArgumentCodes.NOT_POSITIV)
        assertion.assert_is_positiv(card, ArgumentError, code=ArgumentCodes.NOT_POSITIV)
        return self._players[pid].get_hidden_card(card)

    def get_events(self) -> list:
        return self.event_handler.get_events()

    def remove_event(self, eid: int) -> None:
        self.event_handler.remove_event(eid)

    def clear_events(self) -> None:
        self.event_handler.clear_events()

    def draw(self, player_id: int, deck: DrawOptions = DrawOptions.GAME_DECK) -> None:
        assertion.assert_types(player_id, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_type(deck, DrawOptions, ArgumentError, code=ArgumentCodes.NOT_DRAW_OPTIONS)
        assertion.assert_is_positiv(player_id, ArgumentError, code=ArgumentCodes.NOT_POSITIV)

        card: Card = self._game_deck.draw() if deck == DrawOptions.GAME_DECK else self._discard_pile.draw()
        self._players[player_id].set_active_card(card)
        self.check_empty_deck()

    def discard(self, player_id: int) -> None:
        assertion.assert_types(player_id, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_is_positiv(player_id, ArgumentError, code=ArgumentCodes.NOT_POSITIV)
        card: Card = self._players[player_id].get_active_card()
        self._players[player_id].set_active_card(Card(-1))
        self._discard_pile.add(card)
        self._execute_effect(card.effect(), player_id)

    def restock_deck(self, kind: Shuffle) -> None:
        assertion.assert_type(kind, Shuffle, ArgumentError, code=ArgumentCodes.NOT_SHUFFLE)
        self._game_deck.update(self._discard_pile, kind)

    def swap_self(self, player_id: int, swaping_card: int) -> None:
        assertion.assert_types(player_id, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_types(swaping_card, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_is_positiv(player_id, ArgumentError, code=ArgumentCodes.NOT_POSITIV)
        assertion.assert_is_positiv(swaping_card, ArgumentError, code=ArgumentCodes.NOT_POSITIV)

        card: Card = self._players[player_id].get_active_card()
        card_swaped: Card = self._players[player_id].get_hidden_card(swaping_card)
        self._players[player_id].set_active_card(card_swaped)
        self._players[player_id].set_hidden_card(swaping_card, card)

    def _execute_effect(self, effect: Effect, player_id: int) -> None:
        assertion.assert_types(player_id, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_type(effect, Effect, ArgumentError, code=ArgumentCodes.NOT_EFFECT)
        assertion.assert_is_positiv(player_id, ArgumentError, code=ArgumentCodes.NOT_POSITIV)
        if effect == Effect.NONE:
            return
        ef_dict: dict = {
            Effect.PEEK: LogicEvents.PEEK_EFFECT,
            Effect.SPY: LogicEvents.SPY_EFFECT,
            Effect.SWAP: LogicEvents.SWAP_EFFECT
        }
        self.event_handler.add_event(ef_dict[effect], player_id)

    def _swap_effect(self, player_id: int, enemy_id: int, swap_card_player: int, swap_card_enemy: int) -> None:
        assertion.assert_types(player_id, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_types(enemy_id, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_types(swap_card_player, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_types(swap_card_enemy, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)

        assertion.assert_is_positiv(player_id, ArgumentError, code=ArgumentCodes.NOT_POSITIV)
        assertion.assert_is_positiv(enemy_id, ArgumentError, code=ArgumentCodes.NOT_POSITIV)
        assertion.assert_is_positiv(swap_card_player, ArgumentError, code=ArgumentCodes.NOT_POSITIV)
        assertion.assert_is_positiv(swap_card_enemy, ArgumentError, code=ArgumentCodes.NOT_POSITIV)

        card: Card = self._players[player_id].get_hidden_card(swap_card_player)
        card_swaped: Card = self._players[enemy_id].get_hidden_card(swap_card_enemy)
        self._players[player_id].set_hidden_card(swap_card_player, card_swaped)
        self._players[enemy_id].set_hidden_card(swap_card_enemy, card)

    def _peek_effect(self, player_id: int, peek_card: int) -> Card:
        assertion.assert_types(player_id, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_types(peek_card, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_is_positiv(player_id, ArgumentError, code=ArgumentCodes.NOT_POSITIV)
        assertion.assert_is_positiv(peek_card, ArgumentError, code=ArgumentCodes.NOT_POSITIV)
        return self._players[player_id].get_hidden_card(peek_card)

    def _spy_effect(self, enemy_id: int, spy_card: int) -> Card:
        assertion.assert_types(enemy_id, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_types(spy_card, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        return self._peek_effect(enemy_id, spy_card)

    def check_empty_deck(self) -> bool:
        if self._game_deck.length() <= 0:
            self.event_handler.add_event(LogicEvents.EMPTY_DECK)
            return True
        return False

    def fill_game_deck(self, shuffle: Shuffle) -> None:
        assertion.assert_type(shuffle, Shuffle, ArgumentError, code=ArgumentCodes.NOT_SHUFFLE)
        self._game_deck.update(self._discard_pile, shuffle)

    def get_winner(self) -> list:
        min_score = 9999
        min_players = list()

        for player in self._players:
            player_card_value = player.get_score()

            if player_card_value < min_score:
                min_score = player_card_value
                min_players = [player]
            elif player_card_value == min_score:
                min_players.append(player)

        return min_players

    def get_score_board(self) -> list:
        return sorted(self._players, key=lambda player:player.get_score())

    def cabo(self, pid: int) -> None:
        assertion.assert_types(pid, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)

        self.event_handler.add_event(LogicEvents.CABO, pid)

    def __iter__(self):
        return iter(self._players)
