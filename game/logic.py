# from game import get_path_abs, get_path_resource
from enum import Enum

from game import Player
from game.errors import *
from game.deck import GameDeck, DiscardPile, Card, Shuffle
from game.event_handler import LogicEvents, LogicEventHandler


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

    def check_empty_deck(self) -> bool:
        if self._game_deck.length() <= 0:
            self._event_handler.add_event(LogicEvents.EMPTY_DECK)
            return True
        return False

    def fill_game_deck(self, shuffle: Shuffle) -> None:
        self._game_deck.update(self._discard_pile, shuffle)
        self._event_handler.remove_event_by_kind(LogicEvents.EMPTY_DECK)
