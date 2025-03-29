import os
import random
from random import choice

import torch
from enum import Enum

from useful_utility.algebra import Matrix, Vector

from game import Player, get_path_resource
from game.deck import GameDeck, Card
from game.enemies.policy_nn import PolicyNN
from game.logic.logic import DrawOptions


class Difficulties(Enum):
    EASY: int = 0
    MEDIUM: int = 1
    HARD: int = 2
    IMPOSSIBLE: int = 3

class Phase(Enum):
    a1_DRAW_CARD: int = 0
    a2_PUT_CARD_DOWN: int = 1
    a3_PEEK_EFFECT: int = 2
    a4_SPY_EFFECT: int = 3
    a5_SWAP_EFFECT: int = 4

class BaseEnemy(Player):
    def __init__(self, history: int, player_count: int, game_deck: GameDeck,
                 cards: int = 4, eid: int = 0) -> None:
        super().__init__(game_deck, cards, eid)
        self._path: tuple = ("",)
        self._player_count = player_count
        self._nn = None
        self._cards = cards
        # Phasen: 1. Karte ziehen oder cabo | 2. Karte auf den Abglegestapel oder mit hidden Card Wechseln.
        # 3. peek effekt | 4. spy effekt | 5. swap effekt
        self._actions_per_phase = [3, 1 + self._cards, self._cards, player_count * self._cards,
                                   (self._cards ** 2) * player_count]
        # other player hidden cards + self hidden cards + discard pile + hand card + phases
        self._input_dim = (self._player_count * self._cards + self._cards + 1 + 1 + 5) * history
        self._history: int = history
        self._alpha: float = .5
        self._heat: float = 0
        self._last_requests: list = list()
        self._vec_cards: Vector = Vector([card.get_value() for card in self._hidden_cards.get_cards()])
        self._memory_mask_self: Vector = Vector(dimension=cards)
        if self._memory_mask_self.get_dimension() > 2:
            self._memory_mask_self[0] = 1
            self._memory_mask_self[1] = 1
        elif self._memory_mask_self.get_dimension() == 2:
            self._memory_mask_self[0] = 1
        self._memory_mask_self.randomise(2)
        self._memory_self: Vector = Vector(dimension=cards)
        self.update_memory_self(False)
        self._cards_enemies: Matrix = Matrix(rows=player_count, columns=cards)
        self._memory_enemies: Matrix = Matrix(rows=player_count, columns=cards)
        self._memory_mask_enemies: Matrix = Matrix(rows=player_count, columns=cards)
        self.update_memory_enemies(False)

    def update_memory_enemies(self, rand: bool = True):
        self._memory_enemies = self._cards_enemies.where(self._memory_mask_enemies)
        if not rand:
            return
        for i, row in enumerate(self._memory_enemies):
            for j, value in enumerate(row):
                if self._memory_enemies[i][j] == -1:
                    continue
                a = -1 if random.random() <= self._alpha else value
                self._memory_enemies[i][j] = a
                if self._memory_enemies[i][j] == -1:
                    self._memory_mask_enemies[i][j] = 0

    def update_memory_self(self, rand: bool = True):
        self._memory_self = self._vec_cards.where(self._memory_mask_self)
        if not rand:
            return
        for i, value in enumerate(self._memory_self):
            if self._memory_mask_self[i] == -1:
                continue
            self._memory_self[i] = -1 if random.random() <= self._alpha else value
            if self._memory_self[i] == -1:
                self._memory_mask_self[i] = 0

    def _nn_call(self, state):
        phase_one_hot = torch.zeros(len(self._actions_per_phase))
        phase_one_hot[state["phase"].value] = 1
        enemy_cards: list = list()
        for row in self._memory_enemies:
            for value in row:
                enemy_cards.append(value)
        active_card = -1
        if state["phase"] == Phase.a2_PUT_CARD_DOWN:
            active_card = self._active_card.get_value()
        x = torch.cat([
            phase_one_hot,
            torch.tensor([state.get_top_discard_card().get_value()]),
            torch.tensor([active_card]),
            torch.tensor(self._memory_self.get_data()),
            torch.tensor(enemy_cards)
        ])
        self._last_requests.append(x)
        if len(self._last_requests) > self._history:
            self._last_requests.pop(0)
        if len(self._last_requests) > 1:
            for y in self._last_requests[:-1]:
                x = torch.cat([x, y])
        while len(x) < self._input_dim:
            x = torch.cat([x, torch.tensor([-1])])
        list_, action_probs = self._nn.forward(x, state["phase"].value)
        return Vector(list_), action_probs

    def phase_1(self, state) -> tuple[float, DrawOptions, torch.Tensor]:
        self.update_memory_self()
        self.update_memory_enemies()
        output, action_probs = self._nn_call(state)
        choice_ = output.rand_choice(self._heat)
        # 0 -> Deck | 1 -> Disposal Pile
        if choice_ == 0:
            return float(output[choice_]), DrawOptions.GAME_DECK, action_probs
        elif choice_ == 1:
            return float(output[choice_]), DrawOptions.DISCARD_PILE, action_probs
        else:
            return float(output[choice_]), DrawOptions.CABO, action_probs

    def phase_2(self, state) -> tuple[float, int, torch.Tensor]:
        output, action_probs = self._nn_call(state)
        choice_ = output.rand_choice(self._heat)
        # 0 -> Disposal Pile | 1 - cards -> swap
        if choice_ > 0:
            self._memory_mask_self[choice_-1] = 1
        return float(output[choice_]), choice_, action_probs

    def phase_3(self, state) -> tuple[float, int, any]:
        output, action_probs = self._nn_call(state)
        choice_ = output.rand_choice(self._heat)
        self._memory_mask_self[choice_] = 1
        return float(output[choice_]), choice_, action_probs

    def phase_4(self, state) -> tuple[float, int, int, torch.Tensor]:
        output, action_probs = self._nn_call(state)
        choice_ = output.rand_choice(self._heat)
        player: int = int(choice_ / self._cards)
        card: int = choice_ - player * self._cards
        self._memory_mask_enemies[player][card] = 1
        return float(output[choice_]), player, card, action_probs

    def phase_5(self, state) -> tuple[float, int, int, int, torch.Tensor]:
        output, action_probs = self._nn_call(state)
        choice_ = output.rand_choice(self._heat)
        enemy: int = int(choice_ / (self._cards ** 2))
        enemy_card: int = int((choice_ - (enemy * (self._cards ** 2))) / self._cards)
        self_card: int = (choice_ - (enemy * (self._cards ** 2))) - enemy_card * self._cards
        knows_enemy_card: bool = self._memory_mask_enemies[enemy][enemy_card] == 1
        knows_own_card: bool = self._memory_mask_self[self_card] == 1

        if knows_enemy_card:
            self._memory_mask_self[self_card] = 1
        if knows_own_card:
            self._memory_mask_enemies[enemy][enemy_card] = 1
        if not knows_enemy_card:
            self._memory_mask_self[self_card] = 0
        if not knows_own_card:
            self._memory_mask_enemies[enemy][enemy_card] = 0

        return float(output[choice_]), self_card, enemy, enemy_card, action_probs

    def change_mask_self(self, position: int, unmasked: bool):
        self._memory_mask_self[position] = int(unmasked)
        self.update_memory_self(False)

    def change_mask_enemy(self, enemy, card, unmasked: bool):
        self._memory_mask_enemies[enemy][card] = int(unmasked)
        self.update_memory_enemies(False)

    def get_self_mask(self) -> Vector:
        return self._memory_mask_self

    def get_enemy_mask(self) -> Matrix:
        return self._memory_mask_enemies

    def get_enemy_cards(self) -> Matrix:
        return self._cards_enemies

    def get_cards_self(self) -> Vector:
        return self._vec_cards

    def get_params(self):
        return self._nn.parameters()

    def set_nn(self, nn: PolicyNN):
        self._nn = nn

    def get_nn(self) -> PolicyNN:
        return self._nn

    def get_input_dim(self) -> int:
        return self._input_dim

    def get_actions_per_phase(self) -> list:
        return self._actions_per_phase

    def get_path(self) -> tuple:
        return self._path


class State:
    def __init__(self, player_except_self_cards: list, top_card_discard_pile: Card, phase: Phase):
        self._cards_everyone_else: list = player_except_self_cards
        self._top_card_discard_pile: Card = top_card_discard_pile
        self._phase: Phase = phase

    def get_top_discard_card(self) -> Card:
        return self._top_card_discard_pile

    def get_phase(self) -> Phase:
        return self._phase

    def get_cards(self) -> list:
        return self._cards_everyone_else

    def __getitem__(self, item):
        if item == 0 or item == "cards":
            return self._cards_everyone_else
        elif item == 1 or item == "discard_pile":
            return self._top_card_discard_pile
        elif item == 2 or item == "phase":
            return self._phase
