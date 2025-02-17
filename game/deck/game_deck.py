from deck import Deck, Shuffle, Card, DiscardPile
from game import CaboError, StateError, ArgumentError

class GameDeck(Deck):
    def __init__(self):
        super().__init__()
        self._cards: list = [Card(0), Card(0), Card(13), Card(13)]
        self._cards += [Card(i) for b in range(4) for i in range(1, 13)]

    def draw(self) -> Card:
        return self._cards.pop(0)

    def shuffle(self, kind: int = Shuffle.DUMP) -> None:
        if kind == Shuffle.NONE: return
        func: str = "_shuffle_" + str(kind) + "()"
        eval(func)

    def _shuffle_0(self) -> None:
        ...

    def update(self, pile: DiscardPile, shuffle: int = Shuffle.DUMP) -> None:
        pile_list: list = pile.get_all()
        pile.set([pile_list.pop(0)])
        self._cards += pile_list
        self.shuffle(shuffle)