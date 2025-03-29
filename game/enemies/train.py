import sys

import torch
from torch import optim
from tqdm import tqdm

from game.deck import GameDeck
from game.enemies.policy_nn import PolicyNN
from game.enemies.base_enemy import Difficulties
from game.enemies.static import create_enemy
from game.enemies.training_env import TrainingEnv


def train(difficulty: Difficulties = Difficulties.EASY,
          episodes: int = 100, cards: int = 4, players: int = 4, max_rounds: int = 20):
    temp_en = create_enemy(difficulty, players-1, GameDeck(), cards)
    PolNN: PolicyNN = PolicyNN(temp_en.get_input_dim(), temp_en.get_actions_per_phase(), temp_en.get_path())
    del temp_en
    optimizer = optim.Adam(PolNN.parameters(), lr=0.001)
    gamma = 0.99

    for episode in tqdm(range(episodes), dynamic_ncols=True, leave=False):
        env: TrainingEnv = TrainingEnv(difficulty, PolNN, cards, players, max_rounds)
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

        tqdm.write(f"Episode {episode+1} / {episodes}, Loss: {loss.item()}")
        sys.stdout.flush()

    PolNN.save()
    del PolNN
