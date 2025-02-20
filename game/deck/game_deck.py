from game.deck import Deck, Shuffle, Card, DiscardPile
from game.errors import *

class GameDeck(Deck):
    def __init__(self):
        super().__init__()
        self._cards: list = [Card(0), Card(0), Card(13), Card(13)]
        self._cards += [Card(i) for b in range(4) for i in range(1, 13)]

    def draw(self) -> Card:
        return self._cards.pop(0)

    def shuffle(self, kind: Shuffle = Shuffle.DUMP) -> None:
        if kind == Shuffle.NONE: return
        shuffle_kinds: dict = {
            Shuffle.DUMP: self._shuffle_0
        }
        shuffle_kinds[kind]()

    def _shuffle_0(self) -> None:
        ...

    def length(self) -> int:
        return len(self._cards)

    def update(self, pile: DiscardPile, shuffle: Shuffle = Shuffle.DUMP) -> None:
        pile_list: list = pile.get_all()
        pile.set([pile_list.pop(0)])
        self._cards += pile_list
        self.shuffle(shuffle)
