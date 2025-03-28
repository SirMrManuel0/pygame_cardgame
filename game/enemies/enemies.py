import random as rnd
import torch

from typing_extensions import override

from game import get_path_resource
from game.deck import GameDeck
from game.enemies import BaseEnemy
from game.enemies.policy_nn import PolicyNN


class EasyEnemy(BaseEnemy):
    def __init__(self, player_count: int, game_deck: GameDeck, cards: int = 4, eid: int = 0):
        super().__init__(player_count, game_deck, cards, eid)
        self._nn = PolicyNN(self._input_dim, self._actions_per_phase)
        self._history: int = rnd.randint(1, 5)
        self._alpha: float = rnd.randint(25, 30) / 100
        self._heat: float = .3
        self._set_path(("ai", "easy_nn"))

