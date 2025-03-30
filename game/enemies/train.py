import os
import sys
import time
import torch
from torch import optim
from tqdm import tqdm
from colorama import Fore, Style

from game import rnd, get_path_resource
from game.deck import GameDeck
from game.enemies.policy_nn import PolicyNN
from game.enemies.base_enemy import Difficulties
from game.enemies.static import create_enemy
from game.enemies.training_env import TrainingEnv


def train(difficulty: Difficulties = Difficulties.EASY,
          episodes: int = 100, cards: int = 4, players: int = 4, max_rounds: int = 20):
    temp_en = create_enemy(difficulty, players-1, GameDeck(), cards)
    PolNN: PolicyNN = PolicyNN(temp_en.get_input_dim(), temp_en.get_actions_per_phase(), temp_en.get_path())
    PolNN.load()
    path = list(temp_en.get_path())
    del temp_en
    optimizer = optim.Adam(PolNN.parameters(), lr=0.001)
    gamma = 0.99
    all_rewards: list = list()

    path[-1] = f"{path[-1][:path[-1].find("c") + 1]}_checkpoint"
    if os.path.exists(get_path_resource(*path)) and os.path.getsize(get_path_resource(*path)) > 0:
        checkpoint = torch.load(get_path_resource(*path))
        PolNN.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

    for episode in tqdm(range(episodes), dynamic_ncols=True, leave=False):
        env: TrainingEnv = TrainingEnv(difficulty, PolNN, cards, players, max_rounds)
        all_rewards += [float(reward) for reward in env.get_rewards()]
        rewards: list = [torch.tensor(reward) for reward in env.get_rewards()]
        log_probs: list = [action_probs for _, action_probs in env.get_probs()]

        returns = []
        G = 0
        for r in reversed(rewards):
            G = r + gamma * G
            returns.insert(0, G)
        returns = torch.tensor(returns)

        # Compute policy loss
        loss = []
        for log_prob, G in zip(log_probs, returns):
            loss.append(-log_prob * G)  # Policy gradient loss

        loss = torch.stack(loss).sum()

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        average_rewards: float = 0
        for reward in rewards:
            average_rewards += float(reward.item())
        average_rewards = rnd(average_rewards / len(rewards))

        av_rew_color = rewards_color(average_rewards)

        tqdm.write(f"Player {players} Cards {cards} | Episode {episode+1:,.0f} / {episodes:,.0f}, Loss: {loss.item()}."
                   f"{av_rew_color} Average Reward {average_rewards}{Style.RESET_ALL}")
        sys.stdout.flush()

    average_rewards: float = 0
    for reward in all_rewards:
        average_rewards += float(reward)
    average_rewards = rnd(average_rewards / len(all_rewards))

    av_rew_color = rewards_color(average_rewards)

    print(f"{av_rew_color}Average Reward: {average_rewards}{Style.RESET_ALL}")
    time.sleep(1)

    torch.save({
        'model_state_dict': PolNN.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }, get_path_resource(*path))

    return average_rewards

def rewards_color(reward: float) -> Fore:
    av_rew_color = Fore.RED
    if reward >= 1:
        av_rew_color = Fore.GREEN
    elif 0 < reward < 1:
        av_rew_color = Fore.YELLOW
    return av_rew_color
