import os

import numpy as np
import torch
import torch.nn as nn

from game import get_path_resource


class PolicyNN(nn.Module):
    def __init__(self, input_dim, action_dim_per_phase, path: tuple):
        super(PolicyNN, self).__init__()
        self._fc1 = nn.Linear(input_dim, 128)
        self._hidden1 = nn.Linear(128, 256)
        self._hidden2 = nn.Linear(256, 512)
        self._hidden3 = nn.Linear(512, 1024)
        self._hidden4 = nn.Linear(1024, 512)
        self._hidden5 = nn.Linear(512, 256)
        self._hidden6 = nn.Linear(256, 128)
        self._fc2 = nn.Linear(128, sum(action_dim_per_phase))
        self._action_dim_per_phase = action_dim_per_phase
        self._path: tuple = path

    def forward(self, x, phase_idx):
        """

        :param x: hat die Form (Batch Size, History Length, Input Dimension)
        :param phase_idx:
        :return:
        """
        x = torch.nan_to_num(x, nan=-1.0)
        x = torch.relu(self._fc1(x))
        x = torch.relu(self._hidden1(x))
        x = torch.relu(self._hidden2(x))
        x = torch.relu(self._hidden3(x))
        x = torch.relu(self._hidden4(x))
        x = torch.relu(self._hidden5(x))
        x = torch.relu(self._hidden6(x))
        action_logits = self._fc2(x)

        start_idx = sum(self._action_dim_per_phase[:phase_idx])
        end_idx = start_idx + self._action_dim_per_phase[phase_idx]
        valid_action_logits = action_logits[start_idx:end_idx]

        action_probs = torch.softmax(valid_action_logits, dim=-1)
        training_action_prob = torch.softmax(action_logits, dim=-1)

        return action_probs.detach().numpy().tolist(), training_action_prob

    def load(self):
        if os.path.exists(get_path_resource(*self._path)) and os.path.getsize(get_path_resource(*self._path)) > 0:
            self.load_state_dict(torch.load(get_path_resource(*self._path)))
            self.eval()

    def save(self):
        torch.save(self.state_dict(), get_path_resource(*self._path))

    def set_path(self, path: tuple):
        self._path = path
        self.load()

    #def __del__(self):
    #    if len(self._path) > 1:
    #        self.save()
