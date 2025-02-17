from deck import Deck, Card
from game import CaboError, StateError, ArgumentError


class PlayerDeck(Deck):
    def __init__(self, cards: list):
        self._cards = cards

    def take(self, card: int) -> Card:
        return self._cards.pop(card)

    def peek(self, card: int) -> Card:
        return self._cards[card]

    def swap(self, old_card: int, new_card: Card) -> Card:
        old: Card = self._cards[old_card]
        self._cards[old_card] = new_card
        return old