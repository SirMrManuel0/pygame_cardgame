import os
import sys
import time

import numpy as np
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
    all_entropies = []
    all_losses = []

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
        entropies = [rnd(float(-torch.sum(action_prob * torch.log(action_prob)))) for action_prob in log_probs]

        all_entropies.extend(entropies)

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
        all_losses.append(loss.item())

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()

        grad_norm = torch.norm(torch.stack([p.grad.norm() for p in PolNN.parameters() if p.grad is not None]))

        optimizer.step()

        avg_reward = rnd(np.mean(rewards))
        std_reward = rnd(np.std(rewards))
        moving_avg_reward = rnd(np.mean(all_rewards[-100:])) if len(all_rewards) > 100 else rnd(np.mean(all_rewards))
        avg_entropy = rnd(np.mean(all_entropies))

        av_rew_color = rewards_color(avg_reward)

        tqdm.write(
            f"Player {players} Cards {cards} | Episode {episode + 1:,.0f} / {episodes:,.0f}, "
            f"{av_rew_color} Average Reward {avg_reward}{Style.RESET_ALL} "
            f"{rewards_color(std_reward)}Std Reward: {std_reward:.4f}{Style.RESET_ALL}, "
            f"Moving Avg Reward: {moving_avg_reward:.4f}, "
            f"{loss_color(float(loss.item()))}Loss: {loss.item()}{Style.RESET_ALL}, "
            f"{entropy_color(avg_entropy)}Entropy: {avg_entropy:.4f}{Style.RESET_ALL}, "
            f"Grad Norm: {grad_norm:.4f}."
        )

        sys.stdout.flush()

    avg_reward = rnd(np.mean(all_rewards))
    std_reward = rnd(np.std(all_rewards))
    moving_avg_reward = rnd(np.mean(all_rewards[-100:])) if len(all_rewards) > 100 else rnd(np.mean(all_rewards))
    avg_loss = rnd(np.mean(all_losses))
    avg_entropy = rnd(np.mean(all_entropies))

    av_rew_color = rewards_color(avg_reward)

    print(f"Final Stats - {av_rew_color}Avg Reward: {avg_reward}{Style.RESET_ALL}, "
          f"{rewards_color(std_reward)}Std: {std_reward}{Style.RESET_ALL}, "
          f"Moving Avg: {moving_avg_reward}, "
          f"{loss_color(avg_loss)}Avg Loss: {avg_loss}{Style.RESET_ALL}, "
          f"{entropy_color(avg_entropy)}Avg Entropy: {avg_entropy}{Style.RESET_ALL}")

    time.sleep(1)
    PolNN.save()
    torch.save({
        'model_state_dict': PolNN.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }, get_path_resource(*path))

    return avg_reward, std_reward, moving_avg_reward, avg_loss, avg_entropy

def rewards_color(reward: float) -> Fore:
    av_rew_color = Fore.RED
    if 0.5 <= reward <= 2.5:
        av_rew_color = Fore.GREEN
    elif 2.5 < reward or 0 <= reward < 0.5:
        av_rew_color = Fore.YELLOW
    return av_rew_color

def entropy_color(entropy: float) -> Fore:
    entropy_color_ = Fore.RED
    if .1 <= entropy <= 1:
        entropy_color_ = Fore.GREEN
    return entropy_color_

def loss_color(loss: float) -> Fore:
    loss_color_ = Fore.RED
    if .001 <= loss <= .1:
        loss_color_ = Fore.YELLOW
    elif loss < .001:
        loss_color_ = Fore.GREEN
    return loss_color_
