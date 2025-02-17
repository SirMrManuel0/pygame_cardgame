# from game import get_path_abs, get_path_resource
from game import CaboError, StateError, ArgumentError, Player
from game.deck import GameDeck, DiscardPile


class CaboLogic:
    def __init__(self, player_count: int = 4):
        self._game_deck: GameDeck = GameDeck()
        self._discard_pile: DiscardPile = DiscardPile()
        self._players: list = [Player() for i in range(player_count)]
        self._player_count: int = player_count
