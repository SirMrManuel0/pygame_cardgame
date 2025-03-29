import random

import torch
from useful_utility.algebra import Vector

from game import Player
from game.enemies.static import create_enemy
from game.enemies.policy_nn import PolicyNN
from game.enemies.base_enemy import State, Phase, BaseEnemy, Difficulties
from game.errors import assertion, ArgumentCodes, ArgumentError
from game.event_handler import LogicEvents
from game.logic import CaboLogic
from game.logic.logic import DrawOptions


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

    def _ai_prep_cards(self, pid) -> list:
        cards: list = list()
        for player in self._players:
            if player.get_pid() == pid:
                continue
            cards.append(player.get_hidden_cards())
        return cards

    def ai_phase1(self, pid: int) -> tuple[float, DrawOptions, torch.Tensor]:
        prob, deck_choice, action_probs = self._players[pid].phase_1(State(self._ai_prep_cards(pid),
                                                                           self._discard_pile.peek(),
                                                                           Phase.a1_DRAW_CARD))
        if deck_choice == DrawOptions.CABO:
            self.cabo(pid)
            return prob, deck_choice, action_probs
        self.draw(pid, deck_choice)
        return prob, deck_choice, action_probs

    def ai_phase2(self, pid: int) -> tuple[float, int, int, int, Vector, torch.Tensor]:
        prob, put_down_choice, action_probs = self._players[pid].phase_2(State(self._ai_prep_cards(pid),
                                                                               self._discard_pile.peek(),
                                                                               Phase.a2_PUT_CARD_DOWN))
        active_card: int = self._players[pid].get_active_card().get_value()
        if put_down_choice > 0:
            self.swap_self(pid, put_down_choice - 1)
        swapped_card: int = self._players[pid].get_active_card().get_value()
        self.discard(pid)
        mask = self._players[pid].get_self_mask()
        self._players[pid].update_memory_self()
        return prob, active_card, swapped_card, put_down_choice, mask, action_probs

    def ai_phase3(self, pid: int) -> tuple[float, torch.Tensor]:
        prob, peek_choice, action_probs = self._players[pid].phase_3(State(self._ai_prep_cards(pid),
                                                                           self._discard_pile.peek(),
                                                                           Phase.a3_PEEK_EFFECT))
        self._peek_effect(pid, peek_choice)
        self._players[pid].update_memory_self()
        return prob, action_probs

    def ai_phase4(self, pid: int) -> tuple[float, torch.Tensor]:
        prob, player, card, action_probs = self._players[pid].phase_4(State(self._ai_prep_cards(pid),
                                                                            self._discard_pile.peek(),
                                                                            Phase.a4_SPY_EFFECT))
        self._spy_effect(player, card)
        return prob, action_probs

    def ai_phase5(self, pid: int) -> tuple[float, int, int, int, torch.Tensor]:
        prob, player_card, enemy, enemy_card, action_probs = self._players[pid].phase_5(State(self._ai_prep_cards(pid),
                                                                                             self._discard_pile.peek(),
                                                                                             Phase.a5_SWAP_EFFECT))
        self._swap_effect(pid, enemy, player_card, enemy_card)
        return prob, player_card, enemy, enemy_card, action_probs

    def set_ai_all(self, ai: PolicyNN) -> None:
        for player in self._players:
            if isinstance(player, BaseEnemy):
                player.set_nn(ai)
