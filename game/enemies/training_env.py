import logging
from datetime import datetime

from useful_utility.algebra import Vector, Matrix

from game import get_path_resource, Player
from game.deck import Shuffle
from game.enemies import Difficulties, BaseEnemy, PolicyNN
from game.event_handler import *
from game.logic.logic import DrawOptions
from game.logic.w_ai_logic import LogicWAI


class TrainingEnv:
    def __init__(self, difficulty: Difficulties, ai: PolicyNN, cards: int = 4, player: int = 4, max_rounds: int = 20):
        dif: str = "Easy"
        if difficulty == Difficulties.MEDIUM:
            dif: str = "Medium"
        elif difficulty == Difficulties.HARD:
            dif: str = "Hard"
        elif difficulty == Difficulties.IMPOSSIBLE:
            dif: str = "Impossible"
        self._log_path: tuple = ("ai", "training_logs", dif)
        logging.basicConfig(
            filename=get_path_resource(*self._log_path),
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.DEBUG
        )

        self._ai = ai

        self._logic = LogicWAI(0, cards, player, difficulty)
        self._logic.set_ai_all(self._ai)
        logging.info(f"Logic has been initialised with: difficulty: {dif} | cards: {cards} | player: {player}")

        self._alive: bool = True
        self._last: int = -1
        self._round_counter: int = 1
        self._players_count: int = player
        self._max_rounds: int = max_rounds
        self._probs: list = list()
        self._rewards: list = list()
        self._cards: int = cards

        while self._alive:
            logging.info(f"Round {self._round_counter} / {max_rounds} started")
            self._round_counter += 1
            self.round()
            if self._round_counter == self._max_rounds:
                break

        logging.info(f"The last round begins.")
        self.round()
        self._winner = self._logic.get_winner()
        logging.info(f"{self._winner} have won.")
        self._winner = self._winner[0]
        logging.info(f"{self._winner.get_pid()} has been determined as the winner.")

    def round(self):
        for player in self._logic:
            pid: int = player.get_pid()

            logging.info(f"It is {pid} / {self._players_count} turn.")

            if self._last == pid:
                break

            if self._logic.event_handler.has_event(LogicEvents.EMPTY_DECK):
                self._logic.event_handler.remove_event_by_kind(LogicEvents.EMPTY_DECK)
                self._logic.restock_deck(Shuffle.DUMP)
                logging.info(f"EVENT: The deck has been shuffled.")

            probs, data = self._logic.ai_phase1(pid)
            self._probs.append(probs)

            card_val: int = player.get_active_card().get_value()

            if data == DrawOptions.DISCARD_PILE:
                if card_val == 13:
                    self._rewards.append(-1)
                elif card_val in [7, 8, 9, 10, 11, 12]:
                    self._rewards.append(1)
                elif card_val < 4:
                    self._rewards.append(1)
                elif 3 < card_val < 7:
                    self._rewards.append(.5)

            top_card_discard: int = self._logic.get_discard_pile().peek().get_value()

            if data == DrawOptions.GAME_DECK:
                if top_card_discard < 4:
                    self._rewards.append(-1)
                elif top_card_discard == 13:
                    self._rewards.append(1)
                elif top_card_discard in [7, 8, 9, 10, 11, 12]:
                    self._rewards.append(-1)
                elif card_val < 4:
                    self._rewards.append(1)
                elif card_val == 13:
                    self._rewards.append(-1)
                else:
                    self._rewards.append(0)

            if data == DrawOptions.CABO:
                if player.get_score() > 16:
                    self._rewards.append(-1)
                elif player.get_score() > 6:
                    self._rewards.append(1)
                else:
                    self._rewards.append(1.5)

            logging.info(f"Card has been drawn with val: {card_val} from {data}. Discard Pile: {top_card_discard} | "
                         f"probs: {probs} | reward: {self._rewards[-1]}")

            if self._logic.event_handler.has_event(LogicEvents.CABO):
                self._logic.event_handler.remove_event_by_kind(LogicEvents.CABO)
                self._alive: bool = False
                self._last = pid
                logging.info(f"EVENT: Cabo has been called by {pid}.")

            prob, active_card, swapped_card, put_down_choice, mask = self._logic.ai_phase2(pid)

            self._probs.append(prob)
            hidden: Vector = Vector([card.get_value() for card in player.get_hidden_cards()])
            hidden = hidden.where(mask)

            if put_down_choice > 0:
                if mask[put_down_choice-1] == 1:
                    if active_card > swapped_card:
                        self._rewards.append(-1)
                    elif active_card == swapped_card:
                        self._rewards.append(0)
                    else:
                        self._rewards.append(1)
                else:
                    if active_card < 4:
                        self._rewards.append(1)
                    elif active_card > 6:
                        self._rewards.append(-1)
            else:
                if active_card > 10:
                    self._rewards.append(1)
                elif active_card > hidden.max():
                    self._rewards.append(1)
                elif -1 < active_card < hidden.max():
                    self._rewards.append(-1)
                elif active_card == hidden.max():
                    self._rewards.append(0)
                elif active_card < 4:
                    self._rewards.append(-1)
                else:
                    self._rewards.append(0)

            logging.info(f"Card has been put onto the disposal pile. prob: {prob} | reward: {self._rewards[-1]}")

            events: list = self._logic.get_events()
            if len(events) == 0:
                continue
            for event in events:
                assert isinstance(event, LogicEvent)
                if event.get_kind() == LogicEvents.PEEK_EFFECT:
                    mask_before: Vector = player.get_self_mask().copy()
                    self._probs.append(self._logic.ai_phase3(pid))
                    mask_after: Vector = player.get_self_mask()
                    if mask_before == mask_after:
                        if mask_before == Vector([1] * self._cards):
                            self._rewards.append(0)
                        else:
                            self._rewards.append(-1)
                    else:
                        self._rewards.append(1)
                    self._logic.remove_event(event.get_eid())
                    logging.info(f"EVENT: Peek effect used by {pid}. prob: {prob} | reward: {self._rewards[-1]}")
                elif event.get_kind() == LogicEvents.SPY_EFFECT:
                    assert isinstance(player, BaseEnemy)
                    mask_before: Matrix = player.get_enemy_mask().copy()
                    self._probs.append(self._logic.ai_phase4(pid))
                    mask_after: Matrix = player.get_enemy_mask()
                    if mask_before == mask_after:
                        if mask_before == Matrix(rows=self._players_count, columns=self._cards, default_value=1):
                            self._rewards.append(0)
                        else:
                            self._rewards.append(-1)
                    else:
                        self._rewards.append(1)
                    self._logic.remove_event(event.get_eid())
                    logging.info(f"EVENT: Spy effect used by {pid}. prob: {prob} | reward: {self._rewards[-1]}")
                elif event.get_kind() == LogicEvents.SWAP_EFFECT:
                    mask_before: Matrix = player.get_enemy_mask().copy()
                    mask_self_before: Vector = player.get_self_mask().copy()
                    cards_enemy_before: Matrix = player.get_enemy_cards().copy()
                    cards_self_before: Vector = player.get_cards_self().copy()

                    prob, self_card, enemy, enemy_card = self._logic.ai_phase5(pid)
                    self._probs.append(prob)

                    mask_after: Matrix = player.get_enemy_mask()
                    mask_self_after: Vector = player.get_self_mask()
                    cards_enemy_after: Matrix = player.get_enemy_cards()
                    cards_self_after: Vector = player.get_cards_self()

                    if mask_self_before[self_card] == mask_self_after[self_card] \
                            and mask_before[enemy][enemy_card] == mask_after[enemy][enemy_card]:
                        if mask_before[enemy][enemy_card] == 1 \
                                and mask_self_before[self_card] == 1:
                            if cards_self_before[self_card] > cards_enemy_before[enemy][enemy_card]:
                                self._rewards.append(1)
                            elif cards_self_before[self_card] < cards_enemy_before[enemy][enemy_card]:
                                self._rewards.append(-1)
                            else:
                                self._rewards.append(0)
                        else:
                            self._rewards.append(0)
                    elif mask_self_before[self_card] == 1:
                        if cards_self_before[self_card] < 4:
                            self._rewards.append(-1)
                        elif 3 < cards_self_before[self_card] < 8:
                            self._rewards.append(0)
                        else:
                            self._rewards.append(1)
                    elif mask_before[enemy][enemy_card] == 1:
                        if cards_self_before[self_card] < 4:
                            self._rewards.append(1)
                        elif 3 < cards_self_before[self_card] < 8:
                            self._rewards.append(0)
                        else:
                            self._rewards.append(-1)
                    else:
                        self._rewards.append(0)

                    self._logic.remove_event(event.get_eid())
                    logging.info(f"EVENT: Swap effect used by {pid}. prob: {prob} | reward: {self._rewards[-1]}")
            logging.info(f"{pid} / {self._players_count} turn is over.")
