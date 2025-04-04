from game.enemies.base_enemy import BaseEnemy, Difficulties
from game.enemies.enemies import EasyEnemy
from game.enemies.static import create_enemy
from game.enemies.policy_nn import PolicyNN
#from game.enemies.train import train, rewards_color, loss_color, entropy_color

__all__ = [
    "BaseEnemy",
    "EasyEnemy",
    "Difficulties",
    "create_enemy",
    "PolicyNN",
#    "train"
#    "rewards_color",
#    "entropy_color",
#    "loss_color"
]
