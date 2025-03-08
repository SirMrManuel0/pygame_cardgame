from game.deck import Deck, Card
from game.errors import *


class PlayerDeck(Deck):
    def __init__(self, cards: list):
        super().__init__()
        self._cards = cards

    def take(self, card: int) -> Card:
        return self._cards.pop(card)

    def peek(self, card: int) -> Card:
        return self._cards[card]

    def swap(self, old_card: int, new_card: Card) -> Card:
        old: Card = self._cards[old_card]
        self._cards[old_card] = new_card
        return old

    def get_cards(self) -> list:
        return [*self._cards]

    def get_card(self, card: int) -> Card:
        return self._cards[card]

    def get_index_range(self) -> tuple[int, int]:
        return 0, len(self._cards) - 1

    def set_card(self, cid: int, card: Card) -> None:
        self._cards[cid] = card

    def sum(self) -> int:
        value: int = 0
        for card in self._cards:
            value += card.get_value()
        return value
