import torch
from pylix.algebra import Vector

from game.deck import Card
from game.player import Player
from game.enemies.static import create_enemy
from game.enemies.policy_nn import PolicyNN
from game.enemies.base_enemy import State, Phase, BaseEnemy, Difficulties
from game.errors import assertion, ArgumentCodes, ArgumentError
from game.logic.logic import CaboLogic
from game.logic.logic import DrawOptions


class LogicWAI(CaboLogic):
    def __init__(self, player_count: int = 4, start_card_count: int = 4, enemy_count: int = 1,
                 difficulty: Difficulties = Difficulties.EASY):
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
        enemy_cards: list = list()
        for player in self._players:
            if player.get_pid() == pid:
                continue
            enemy_cards.append(player.get_hidden_cards())

        prob, deck_choice, action_probs = self._players[pid].phase_1(
            State(
                self._ai_prep_cards(pid),
                self._discard_pile.peek(),
                Phase.a1_DRAW_CARD
            ),
            enemy_cards
        )
        if deck_choice == DrawOptions.CABO and not self._cabo_called:
            self.cabo(pid)
            return prob, deck_choice, action_probs
        elif self._cabo_called:
            deck_choice = DrawOptions.GAME_DECK
        self.draw(pid, deck_choice)
        if self._players[pid].get_active_card().get_value() == -1:
            self.draw(pid, DrawOptions.GAME_DECK)
        return prob, deck_choice, action_probs

    def ai_phase2(self, pid: int) -> tuple[float, int, int, int, Vector, torch.Tensor]:
        prob, put_down_choice, action_probs = self._players[pid].phase_2(
            State(
                self._ai_prep_cards(pid),
                self._discard_pile.peek(),
                Phase.a2_PUT_CARD_DOWN
            )
        )
        active_card: int = self._players[pid].get_active_card().get_value()
        if put_down_choice > 0:
            self.swap_self(pid, put_down_choice - 1)
        swapped_card: int = self._players[pid].get_active_card().get_value()
        if self._players[pid].get_active_card().get_value() == -1:
            self._players[pid].set_active_card(self._game_deck.draw())
        self.discard(pid)
        mask = self._players[pid].get_self_mask()
        self._players[pid].update_memory_self()
        if self._players[pid].get_active_card().get_value() == -1:
            self._players[pid].set_active_card(Card(1))
        return prob, active_card, swapped_card, put_down_choice, mask, action_probs

    def ai_phase3(self, pid: int) -> tuple[float, torch.Tensor]:
        prob, peek_choice, action_probs = self._players[pid].phase_3(
            State(
                self._ai_prep_cards(pid),
                self._discard_pile.peek(),
                Phase.a3_PEEK_EFFECT
            )
        )
        self._peek_effect(pid, peek_choice)
        self._players[pid].update_memory_self()
        if self._players[pid].get_active_card().get_value() == -1:
            self._players[pid].set_active_card(Card(1))
        return prob, action_probs

    def ai_phase4(self, pid: int) -> tuple[float, torch.Tensor]:
        prob, player, card, action_probs = self._players[pid].phase_4(
            State(
                self._ai_prep_cards(pid),
                self._discard_pile.peek(),
                Phase.a4_SPY_EFFECT
            )
        )
        self._spy_effect(player, card)
        if self._players[pid].get_active_card().get_value() == -1:
            self._players[pid].set_active_card(Card(1))
        return prob, action_probs

    def ai_phase5(self, pid: int) -> tuple[float, int, int, int, torch.Tensor]:
        prob, player_card, enemy, enemy_card, action_probs = self._players[pid].phase_5(
            State(
                self._ai_prep_cards(pid),
                self._discard_pile.peek(),
                Phase.a5_SWAP_EFFECT
            )
        )
        self._swap_effect(pid, enemy, player_card, enemy_card)
        if self._players[pid].get_active_card().get_value() == -1:
            self._players[pid].set_active_card(Card(1))
        return prob, player_card, enemy, enemy_card, action_probs

    def set_ai_all(self, ai: PolicyNN) -> None:
        for player in self._players:
            if isinstance(player, BaseEnemy):
                player.set_nn(ai)
