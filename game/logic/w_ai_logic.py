import random

from game import Player
from game.enemies import BaseEnemy, create_enemy, Difficulties
from game.enemies.base_enemy import State, Phase
from game.errors import assertion, ArgumentCodes, ArgumentError
from game.logic import CaboLogic


class LogicWAI(CaboLogic):
    def __init__(self, player_count: int = 4, start_card_count: int = 4, enemy_count: int = 1,
                 difficulty: Difficulties = Difficulties.MEDIUM):
        assertion.assert_below(player_count + enemy_count, 5, ArgumentError, code=ArgumentCodes.TOO_BIG)
        assertion.assert_above(player_count + enemy_count, 0, ArgumentError, code=ArgumentCodes.TOO_SMALL)
        l_count: int = player_count
        if player_count == 0:
            l_count: int = 1
        super().__init__(l_count, start_card_count)
        self._player_count = player_count + enemy_count
        self._enemies = list()
        self._players = [Player(self._game_deck, cards=start_card_count) for i in range(player_count)]
        self._players += [create_enemy(difficulty, player_count + enemy_count - 1, self._game_deck, start_card_count)
                          for i in range(enemy_count)]
        self._players = random.sample(self._players, len(self._players))
        for i, player in enumerate(self._players):
            player.set_pid(i)
            if isinstance(player, BaseEnemy):
                self._enemies.append(i)

    def enemy_turn_start(self, pid: int):
        cards: list = list()
        for player in self._players:
            if player.get_pid() == pid:
                continue
            cards.append(player.get_hidden_cards())
        self._players[pid].turn_start(State(cards, self._discard_pile.peek(), Phase.a1_DRAW_CARD))
