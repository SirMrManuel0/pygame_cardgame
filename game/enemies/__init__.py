from game.enemies.base_enemy import BaseEnemy, Difficulties
from game.enemies.enemies import EasyEnemy
from game.enemies.static import create_enemy, train
from game.enemies.policy_nn import PolicyNN

__all__ = [
    "BaseEnemy",
    "EasyEnemy",
    "Difficulties",
    "create_enemy",
    "PolicyNN",
    "train"
]
