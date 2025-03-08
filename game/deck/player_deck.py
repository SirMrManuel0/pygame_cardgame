from game.deck import Deck, Card
from game.errors import *


class PlayerDeck(Deck):
    def __init__(self, cards: list):
        assertion.assert_type(cards, list, ArgumentError, code=ArgumentCodes.NOT_LIST)
        super().__init__()
        self._cards = cards

    def take(self, card: int) -> Card:
        assertion.assert_types(card, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_range(card, 0, len(self._cards) - 1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
        return self._cards.pop(card)

    def peek(self, card: int) -> Card:
        assertion.assert_types(card, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_range(card, 0, len(self._cards) - 1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
        return self._cards[card]

    def swap(self, old_card: int, new_card: Card) -> Card:
        assertion.assert_types(old_card, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_type(new_card, Card, ArgumentError, code=ArgumentCodes.NOT_CARD)
        assertion.assert_range(old_card, 0, len(self._cards) - 1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
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
        assertion.assert_types(cid, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_type(card, Card, ArgumentError, code=ArgumentCodes.NOT_CARD)
        assertion.assert_range(cid, 0, len(self._cards) - 1, ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
        self._cards[cid] = card

    def sum(self) -> int:
        value: int = 0
        for card in self._cards:
            value += card.get_value()
        return value
