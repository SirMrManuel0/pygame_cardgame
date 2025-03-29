import json

from game import get_path_resource, rnd
from game.enemies import train, Difficulties
from game.enemies import rewards_color
from colorama import Style

min_player = 2
max_player = 4
max_cards = 5
episodes = 6400
difficulty = Difficulties.EASY
path = ("ai", "trainings_data", "Easy")

for players in range(min_player, max_player + 1):
    for cards in range(1, max_cards + 1):
        rewards: float = train(Difficulties.EASY, cards=cards, players=players, episodes=episodes)
        data: dict = dict()
        with open(get_path_resource(*path), "r", encoding="utf-8") as js:
            data = json.load(js)
            data["average_rewards"][f"{players}p"][f"{cards}c"].append(rewards)
        with open(get_path_resource(*path), "w", encoding="utf-8") as js:
            json.dump(data, js, indent=4)

data = dict()
with open(get_path_resource(*path), "r", encoding="utf-8") as js:
    data = json.load(js)

for players in range(2, max_player + 1):
    for cards in range(1, max_cards + 1):
        to_print: str = f"{players}p {cards}c: "
        rewards: list = data["average_rewards"][f"{players}p"][f"{cards}c"]
        start_reward = rewards[0]
        end_reward = rewards[-1]
        delta = rnd(end_reward - start_reward)
        gradient = 0
        if len(rewards) > 1:
            gradient = rnd(delta / (len(rewards) - 1))
        else:
            gradient = rnd(delta / (len(rewards)))
        to_print += f"{rewards_color(start_reward)}start: {start_reward}{Style.RESET_ALL} "
        to_print += f"{rewards_color(delta)}delta: {delta}{Style.RESET_ALL} "
        to_print += f"{rewards_color(gradient)}gradient: {gradient}{Style.RESET_ALL} "
        to_print += f"{rewards_color(end_reward)}end: {end_reward}{Style.RESET_ALL}"
        print(to_print)
