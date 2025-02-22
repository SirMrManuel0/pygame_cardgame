from deck import PlayerDeck, GameDeck, Card
from game.errors import *


class Player:
    def __init__(self, gameDeck: GameDeck, cards: int = 4, pid: int = 0):
        t: list = [gameDeck.draw() for i in range(cards)]
        self._hidden_cards: PlayerDeck = PlayerDeck(t)
        self._pid = pid
        self._active_card: Card = None

    def get_hidden_cards(self) -> list:
        return self._hidden_cards

    def get_hidden_card(self, card: int) -> Card:
        return self._hidden_cards[card]

    def get_pid(self) -> int:
        return self._pid

    def set_active_card(self, card: Card) -> None:
        self._active_card = card

    def get_active_card(self) -> Card:
        return self._active_card