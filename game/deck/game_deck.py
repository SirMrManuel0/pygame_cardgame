import game.deck as gd
from game.errors import *

class GameDeck(gd.Deck):
    def __init__(self):
        super().__init__()
        self._cards: list = [gd.Card(0), gd.Card(0), gd.Card(13), gd.Card(13)]
        self._cards += [gd.Card(i) for b in range(4) for i in range(1, 13)]

    def draw(self) -> gd.Card:
        return self._cards.pop(0)

    def shuffle(self, kind: gd.Shuffle = gd.Shuffle.DUMP) -> None:
        assertion.assert_type(kind, gd.Shuffle, ArgumentError, code=ArgumentCodes.NOT_SHUFFLE)
        if kind == gd.Shuffle.NONE: return None
        shuffle_kinds: dict = {
            gd.Shuffle.DUMP: self._shuffle_0
        }
        shuffle_kinds.get(kind, shuffle_kinds[gd.Shuffle.DUMP])()

    def _shuffle_0(self) -> None:
        ...

    def length(self) -> int:
        return len(self._cards)

    def update(self, pile, shuffle: gd.Shuffle = gd.Shuffle.DUMP) -> None:
        assertion.assert_type(shuffle, gd.Shuffle, ArgumentError, code=ArgumentCodes.NOT_SHUFFLE)
        assertion.assert_type(pile, gd.DiscardPile, ArgumentError, code=ArgumentCodes.NOT_DISCARD_PILE)
        pile_list: list = pile.get_all()
        pile.set([pile_list.pop(0)])
        self._cards += pile_list
        self.shuffle(shuffle)
