import game.deck as gd
from game.errors import *

class DiscardPile(gd.Deck):
    def __init__(self):
        super().__init__()

    def draw(self) -> gd.Card:
        return self._cards.pop(0)

    def peek(self) -> gd.Card:
        return self._cards[0]

    def add(self, card: gd.Card) -> None:
        self._cards.insert(0, card)

    def get_all(self) -> list:
        return self._cards

    def set(self, cards: list) -> None:
        self._cards = cards

    def reset(self, game_deck, shuffle: int = gd.Shuffle.DUMP) -> None:
        game_deck.update(self, shuffle)
