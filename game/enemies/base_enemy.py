from enum import Enum

import torch

from game import Player
from game.deck import GameDeck, Card


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
    def __init__(self, player_count: int, game_deck: GameDeck,
                 cards: int = 4, eid: int = 0) -> None:
        super().__init__(player_count, game_deck, cards, eid)
        self._player_count = player_count
        self._nn = None
        self._cards = cards
        # Phasen: 1. Karte ziehen | 2. Karte auf den Abglegestapel oder mit hidden Card Wechseln.
        # 3. peek effekt | 4. spy effekt | 5. swap effekt
        self._actions_per_phase = [2, 1 + self._cards, self._cards, player_count * self._cards,
                                   (self._cards ** 2) * player_count]
        # other player hidden cards + self hidden cards + discard pile + hand card + phases
        self._input_dim = self._player_count * self._cards + 4 + 1 + 1 + 3
        self._history: int = 1
        self._memory: list = [-1] * self._cards

    def turn_start(self, state):
        phase_one_hot = torch.zeros(len(self._actions_per_phase))
        phase_one_hot[state["phase"].value] = 1
        x = torch.cat([
            phase_one_hot,
            ...
        ])

class State:
    def __init__(self, player_except_self_cards: list, top_card_discard_pile: Card, phase: Phase):
        self._cards_everyone_else: list = player_except_self_cards
        self._top_card_discard_pile = top_card_discard_pile
        self._phase = phase

    def __getitem__(self, item):
        if item == 0 or item == "cards":
            return self._cards_everyone_else
        elif item == 1 or item == "discard_pile":
            return self._top_card_discard_pile
        elif item == 2 or item == "phase":
            return self._phase
