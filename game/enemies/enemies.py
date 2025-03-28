import random as rnd
import torch

from typing_extensions import override

from game import get_path_resource
from game.deck import GameDeck
from game.enemies import BaseEnemy
from game.enemies.policy_nn import PolicyNN


class EasyEnemy(BaseEnemy):
    def __init__(self, player_count: int, game_deck: GameDeck, cards: int = 4, eid: int = 0):
        super().__init__(5, player_count, game_deck, cards, eid)
        path = ("ai", "easy", f"{player_count+1}p", f"{cards}c")
        self._nn = PolicyNN(self._input_dim, self._actions_per_phase, path)
        self._alpha: float = rnd.randint(25, 30) / 100
        self._heat: float = -.8
        self._nn.set_path(path)
        self._path = path
