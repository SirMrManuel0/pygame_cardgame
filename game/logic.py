# from game import get_path_abs, get_path_resource
from enum import Enum

from .player import Player
from game.errors import *
from game.deck import GameDeck, DiscardPile, Card, Shuffle
from game.event_handler import LogicEvents, LogicEventHandler
from game.deck.base import Effect


class DrawOptions(Enum):
    DISCARD_PILE: int = 0
    GAME_DECK: int = 1


class CaboLogic:
    def __init__(self, player_count: int = 4, start_card_count: int = 4):
        self._game_deck: GameDeck = GameDeck()
        self._discard_pile: DiscardPile = DiscardPile()
        self._players: list = [Player(self._game_deck, cards=start_card_count, pid=i) for i in range(player_count)]
        self._player_count: int = player_count
        self._event_handler: LogicEventHandler = LogicEventHandler()

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
        return self._players[pid].get_hidden_card(card)

    def get_events(self) -> list:
        return self._event_handler.get_events()

    def remove_event(self, eid: int) -> None:
        self._event_handler.remove_event(eid)

    def clear_events(self) -> None:
        self._event_handler.clear_events()

    def draw(self, player_id: int, deck: int = DrawOptions.GAME_DECK) -> None:
        card: Card = self._game_deck.draw() if deck == DrawOptions.GAME_DECK else self._discard_pile.draw()
        self._players[player_id].set_active_card(card)
        self.check_empty_deck()

    def discard(self, player_id: int) -> None:
        card: Card = self._players[player_id].get_active_card()
        self._players[player_id].set_active_card(None)
        self._discard_pile.add(card)
        self._execute_effect(card.effect(), player_id)

    def restock_deck(self, kind: Shuffle) -> None:
        self._game_deck.update(self._discard_pile, kind)

    def swap_self(self, player_id: int, swaping_card: int) -> None:
        card: Card = self._players[player_id].get_active_card()
        card_swaped: Card = self._players[player_id].get_hidden_card(swaping_card)
        self._players[player_id].set_active_card(card_swaped)
        self._players[player_id].set_hidden_card(swaping_card, card)

    def _execute_effect(self, effect: Effect, player_id: int) -> None:
        ef_dict: dict = {
            Effect.PEEK: LogicEvents.PEEK_EFFECT,
            Effect.SPY: LogicEvents.SPY_EFFECT,
            Effect.SWAP: LogicEvents.SWAP_EFFECT
        }
        self._event_handler.add_event(ef_dict[effect], player_id)

    def _swap_effect(self, player_id: int, enemy_id: int, swap_card_player: int, swap_card_enemy: int) -> None:
        card: Card = self._players[player_id].get_hidden_card(swap_card_player)
        card_swaped: Card = self._players[enemy_id].get_hidden_card(swap_card_enemy)
        self._players[player_id].set_hidden_card(swap_card_player, card_swaped)
        self._players[enemy_id].set_hidden_card(swap_card_enemy, card)

    def _peek_effect(self, player_id: int, peek_card: int) -> Card:
        return self._players[player_id].get_hidden_card(peek_card)

    def _spy_effect(self, enemy_id: int, spy_card: int) -> Card:
        return self._peek_effect(enemy_id, spy_card)

    def check_empty_deck(self) -> bool:
        if self._game_deck.length() <= 0:
            self._event_handler.add_event(LogicEvents.EMPTY_DECK)
            return True
        return False

    def fill_game_deck(self, shuffle: Shuffle) -> None:
        self._game_deck.update(self._discard_pile, shuffle)
