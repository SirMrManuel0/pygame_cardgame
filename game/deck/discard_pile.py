import game.deck as gd
from game.errors import *

class DiscardPile(gd.Deck):
    def __init__(self):
        super().__init__()

    def draw(self) -> gd.Card:
        if len(self._cards) == 0:
            return gd.Card(-1)
        return self._cards.pop(0)

    def peek(self) -> gd.Card:
        if len(self._cards) == 0:
            return gd.Card(-1)
        return self._cards[0]

    def add(self, card: gd.Card) -> None:
        assertion.assert_type(card, gd.Card, ArgumentError, code=ArgumentCodes.NOT_CARD)
        self._cards.insert(0, card)

    def get_all(self) -> list:
        return self._cards

    def set(self, cards: list) -> None:
        assertion.assert_type(cards, list, ArgumentError, code=ArgumentCodes.NOT_LIST)
        self._cards = cards

    def reset(self, game_deck, shuffle: int = gd.Shuffle.DUMP) -> None:
        assertion.assert_type(game_deck, gd.GameDeck, ArgumentError, code=ArgumentCodes.NOT_GAME_DECK)
        assertion.assert_type(shuffle, gd.Shuffle, ArgumentError, code=ArgumentCodes.NOT_SHUFFLE)
        game_deck.update(self, shuffle)
