import json

import numpy as np

from game import get_path_resource, rnd
from game.enemies import train, Difficulties
from game.enemies import rewards_color, loss_color, entropy_color
from colorama import Style

min_player = 2
max_player = 4
max_cards = 5
max_rounds = 100
episodes = 30_000
difficulty = Difficulties.EASY
path = ("ai", "trainings_data", "Easy")

for players in range(min_player, max_player + 1):
    for cards in range(1, max_cards + 1):

        avg_reward, std_reward, moving_avg_reward, avg_loss, avg_entropy, avg_rounds, std_rounds = train(
            Difficulties.EASY,
            cards=cards,
            players=players,
            episodes=episodes,
            max_rounds=max_rounds
        )

        data: dict = dict()
        with open(get_path_resource(*path), "r", encoding="utf-8") as js:
            data = json.load(js)

        data.setdefault("average_rewards", {}).setdefault(f"{players}p", {}).setdefault(f"{cards}c", []).append(avg_reward)
        data.setdefault("std_rewards", {}).setdefault(f"{players}p", {}).setdefault(f"{cards}c", []).append(std_reward)
        data.setdefault("moving_avg_rewards", {}).setdefault(f"{players}p", {}).setdefault(f"{cards}c", []).append(moving_avg_reward)
        data.setdefault("avg_losses", {}).setdefault(f"{players}p", {}).setdefault(f"{cards}c", []).append(avg_loss)
        data.setdefault("avg_entropies", {}).setdefault(f"{players}p", {}).setdefault(f"{cards}c", []).append(avg_entropy)
        data.setdefault("avg_rounds", {}).setdefault(f"{players}p", {}).setdefault(f"{cards}c", []).append(avg_rounds)
        data.setdefault("std_rounds", {}).setdefault(f"{players}p", {}).setdefault(f"{cards}c", []).append(std_rounds)

        with open(get_path_resource(*path), "w", encoding="utf-8") as js:
            json.dump(data, js, indent=4)

print()

data = {}
with open(get_path_resource(*path), "r", encoding="utf-8") as js:
    data = json.load(js)

for players in range(2, max_player + 1):
    for cards in range(1, max_cards + 1):
        to_print = f"{players}p {cards}c: "
        rewards = data["average_rewards"][f"{players}p"][f"{cards}c"]
        start_reward = rewards[0]
        end_reward = rewards[-1]
        delta = rnd(end_reward - start_reward)
        gradient = rnd(delta / max(len(rewards) - 1, 1))

        std_reward = data["std_rewards"][f"{players}p"][f"{cards}c"][-1]
        moving_avg = data["moving_avg_rewards"][f"{players}p"][f"{cards}c"][-1]
        avg_loss = data["avg_losses"][f"{players}p"][f"{cards}c"][-1]
        avg_entropy = data["avg_entropies"][f"{players}p"][f"{cards}c"][-1]
        avg_rounds = data["avg_rounds"][f"{players}p"][f"{cards}c"][-1]
        std_rounds = data["std_rounds"][f"{players}p"][f"{cards}c"][-1]

        to_print += f"{rewards_color(start_reward)}start: {start_reward:.8f}{Style.RESET_ALL} "
        to_print += f"{rewards_color(delta)}delta: {delta:.8f}{Style.RESET_ALL} "
        to_print += f"{rewards_color(gradient)}gradient: {gradient:.8f}{Style.RESET_ALL} "
        to_print += f"{rewards_color(end_reward)}end: {end_reward:.8f}{Style.RESET_ALL} "
        to_print += f"{rewards_color(std_reward)}Std Reward: {std_reward:.8f}{Style.RESET_ALL} | "\
                    f"{loss_color(avg_loss)}Loss: {avg_loss:.8f}{Style.RESET_ALL} | "\
                    f"{entropy_color(avg_entropy)}Entropy: {avg_entropy:.8f}{Style.RESET_ALL} | "\
                    f"Avg Rounds: {avg_rounds:.8f} | "\
                    f"Std Rounds: {std_rounds:.8f}"

        print(to_print)
