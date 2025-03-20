from .deck import PlayerDeck, GameDeck, Card
from game.errors import *


class Player:
    def __init__(self, game_deck: GameDeck, cards: int = 4, pid: int = 0):
        assertion.assert_type(game_deck, GameDeck, ArgumentError, code=ArgumentCodes.NOT_GAME_DECK)
        assertion.assert_types(cards, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_types(pid, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_above(cards, 0, ArgumentError, code=ArgumentCodes.TOO_SMALL)
        assertion.assert_above(pid, -1, ArgumentError, code=ArgumentCodes.TOO_SMALL)
        t: list = [game_deck.draw() for i in range(cards)]
        self._hidden_cards: PlayerDeck = PlayerDeck(t)
        self._pid = pid
        self._active_card: Card | None = None

    def get_hidden_cards(self) -> list:
        return self._hidden_cards.get_cards()

    def get_hidden_card(self, card: int) -> Card:
        assertion.assert_types(card, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_range(card, self._hidden_cards.get_index_range()[0], self._hidden_cards.get_index_range()[1],
                               ArgumentError, code=ArgumentCodes.OUT_OF_RANGE)
        return self._hidden_cards.get_card(card)

    def get_pid(self) -> int:
        return self._pid

    def set_active_card(self, card: Card) -> None:
        assertion.assert_type(card, Card, ArgumentError, code=ArgumentCodes.NOT_CARD)
        self._active_card = card

    def get_active_card(self) -> Card:
        return self._active_card

    def set_hidden_card(self, cid: int, card: Card) -> None:
        assertion.assert_types(cid, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_type(card, Card, ArgumentError, code=ArgumentCodes.NOT_CARD)
        self._hidden_cards.set_card(cid, card)

    def get_deck(self) -> PlayerDeck:
        return self._hidden_cards

    def get_score(self) -> int:
        return self._hidden_cards.sum()