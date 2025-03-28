import logging
from datetime import datetime

from useful_utility.algebra import Vector

from game import get_path_resource, Player
from game.deck import Shuffle
from game.enemies import Difficulties
from game.event_handler import *
from game.logic.logic import DrawOptions
from game.logic.w_ai_logic import LogicWAI


class TrainingEnv:
    def __init__(self, difficulty: Difficulties, cards: int = 4, player: int = 4, max_rounds: int = 20):
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

        self._logic = LogicWAI(0, cards, player, difficulty)
        logging.info(f"Logic has been initialised with: difficulty: {dif} | cards: {cards} | player: {player}")

        self._alive: bool = True
        self._last: int = -1
        self._round_counter: int = 1
        self._players_count: int = player
        self._max_rounds: int = max_rounds
        self._probs: dict = dict()
        self._rewards: dict = dict()
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
        winner: Player = self._winner[0]
        logging.info(f"{winner.get_pid()} has been determined as the winner.")

    def round(self):
        for player in self._logic:
            pid: int = player.get_pid()

            if pid not in self._probs:
                self._probs[pid] = list()
            if pid not in self._rewards:
                self._rewards[pid] = list()

            logging.info(f"It is {pid} / {self._players_count} turn.")

            if self._last == pid:
                break

            if self._logic.event_handler.has_event(LogicEvents.EMPTY_DECK):
                self._logic.event_handler.remove_event_by_kind(LogicEvents.EMPTY_DECK)
                self._logic.restock_deck(Shuffle.DUMP)
                logging.info(f"EVENT: The deck has been shuffled.")

            probs, data = self._logic.ai_phase1(pid)
            self._probs[pid].append(probs)

            card_val: int = player.get_active_card().get_value()

            if data == DrawOptions.DISCARD_PILE:
                if card_val == 13:
                    self._rewards[pid].append(-1)
                elif card_val in [7, 8, 9, 10, 11, 12]:
                    self._rewards[pid].append(1)
                elif card_val < 4:
                    self._rewards[pid].append(1)
                elif 4 < card_val < 7:
                    self._rewards[pid].append(.5)

            top_card_discard: int = self._logic.get_discard_pile().peek().get_value()

            if data == DrawOptions.GAME_DECK:
                if top_card_discard < 4:
                    self._rewards[pid].append(-1)
                elif top_card_discard == 13:
                    self._rewards[pid].append(1)
                elif top_card_discard in [7, 8, 9, 10, 11, 12]:
                    self._rewards[pid].append(-1)
                elif card_val < 4:
                    self._rewards[pid].append(1)
                elif card_val == 13:
                    self._rewards[pid].append(-1)
                else:
                    self._rewards[pid].append(0)

            if data == DrawOptions.CABO:
                if player.get_score() > 16:
                    self._rewards[pid].append(-1)
                elif player.get_score() > 6:
                    self._rewards[pid].append(1)
                else:
                    self._rewards[pid].append(1.5)

            logging.info(f"Card has been drawn with val: {card_val} from {data}. Discard Pile: {top_card_discard} | "
                         f"probs: {probs} | reward: {self._rewards[pid][-1]}")

            if self._logic.event_handler.has_event(LogicEvents.CABO):
                self._logic.event_handler.remove_event_by_kind(LogicEvents.CABO)
                self._alive: bool = False
                self._last = pid
                logging.info(f"EVENT: Cabo has been called by {pid}.")

            prob, active_card, swapped_card, put_down_choice, mask = self._logic.ai_phase2(pid)

            self._probs[pid].append(prob)
            hidden: Vector = Vector([card.get_value() for card in player.get_hidden_cards()])

            if put_down_choice > 0:
                if mask[put_down_choice-1] == 1:
                    if active_card > swapped_card:
                        self._rewards[pid].append(-1)
                    elif active_card == swapped_card:
                        self._rewards[pid].append(0)
                    else:
                        self._rewards[pid].append(1)
                else:
                    if active_card < 4:
                        self._rewards[pid].append(1)
                    elif active_card > 6:
                        self._rewards[pid].append(-1)
            else:
                if active_card > 10:
                    self._rewards[pid].append(1)
                elif mask == [1] * self._cards:
                    if active_card > hidden.max():
                        self._rewards[pid].append(1)
                    elif active_card < hidden.max():
                        self._rewards[pid].append(-1)
                        


            logging.info(f"Card has been put onto the disposal pile. prob: {prob} | reward: {self._rewards[pid][-1]}")
            events: list = self._logic.get_events()
            if len(events) == 0:
                continue
            for event in events:
                assert isinstance(event, LogicEvent)
                if event.get_kind() == LogicEvents.PEEK_EFFECT:
                    self._probs.append(self._logic.ai_phase3(pid))
                    self._logic.remove_event(event.get_eid())
                    logging.info(f"EVENT: Peek effect used by {pid}.")
                elif event.get_kind() == LogicEvents.SPY_EFFECT:
                    self._probs.append(self._logic.ai_phase4(pid))
                    self._logic.remove_event(event.get_eid())
                    logging.info(f"EVENT: Spy effect used by {pid}.")
                elif event.get_kind() == LogicEvents.SWAP_EFFECT:
                    self._probs.append(self._logic.ai_phase5(pid))
                    self._logic.remove_event(event.get_eid())
                    logging.info(f"EVENT: Swap effect used by {pid}.")
            logging.info(f"{pid} / {self._players_count} turn is over.")
