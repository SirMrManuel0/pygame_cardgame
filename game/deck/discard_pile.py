from game.deck import Deck, Shuffle, Card, GameDeck
from game.errors import *

class DiscardPile(Deck):
    def __init__(self):
        super().__init__()

    def draw(self) -> Card:
        return self._cards.pop(0)

    def peek(self) -> Card:
        return self._cards[0]

    def add(self, card: Card) -> None:
        self._cards.append(card)

    def get_all(self) -> list:
        return self._cards

    def set(self, cards: list) -> None:
        self._cards = cards

    def reset(self, game_deck: GameDeck, shuffle: int = Shuffle.DUMP) -> None:
        game_deck.update(self, shuffle)
