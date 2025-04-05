import game.deck as gd
from game.errors import *

class DiscardPile(gd.Deck):
    """
    Pile where the cards get thrown to.
    """
    def __init__(self):
        super().__init__()

    def draw(self) -> gd.Card:
        """
        pops the first element (pop(0)) if it exists, otherwise a card with value -1.
        """
        if len(self._cards) == 0:
            return gd.Card(-1)
        return self._cards.pop(0)

    def peek(self) -> gd.Card:
        """
        Returns the uppermost card of the Deck.
        """
        if len(self._cards) == 0:
            return gd.Card(-1)
        return self._cards[0]

    def add(self, card: gd.Card) -> None:
        """
        Inserts the card at position 0. Makes it the uppermost card.
        :param card: The card to add to discard pile.
        """
        assertion.assert_type(card, gd.Card, ArgumentError, code=ArgumentCodes.NOT_CARD)
        self._cards.insert(0, card)

    def get_all(self) -> list:
        """
        Returns the list containing all cards of the deck (Makes no copy!!!)
        """
        return self._cards

    def set(self, cards: list) -> None:
        """
        Changes the list of cards to :param cards
        """
        assertion.assert_type(cards, list, ArgumentError, code=ArgumentCodes.NOT_LIST)
        self._cards = cards

    def reset(self, game_deck, shuffle: int = gd.Shuffle.DUMP) -> None:
        """
        Calls update function with a :param shuffle algorithm
        """
        assertion.assert_type(game_deck, gd.GameDeck, ArgumentError, code=ArgumentCodes.NOT_GAME_DECK)
        assertion.assert_type(shuffle, gd.Shuffle, ArgumentError, code=ArgumentCodes.NOT_SHUFFLE)
        game_deck.update(self, shuffle)
