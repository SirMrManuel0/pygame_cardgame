import numpy as np
import torch
import torch.nn as nn

class PolicyNN(nn.Module):
    def __init__(self, input_dim, action_dim_per_phase):
        super(PolicyNN, self).__init__()
        self._fc1 = nn.Linear(input_dim, 128)
        self._lstm = nn.LSTM(128, 256, batch_first=True)
        self._fc2 = nn.Linear(256, sum(action_dim_per_phase))
        self._action_dim_per_phase = action_dim_per_phase

    def forward(self, x, phase_idx):
        """

        :param x: hat die Form (Batch Size, History Length, Input Dimension)
        :param phase_idx:
        :return:
        """
        x = torch.nan_to_num(x, nan=-1.0)
        x = torch.relu(self._fc1(x))
        x, _ = self._lstm(x)
        action_logits = self._fc2(x[:, -1, :])

        start_idx = sum(self._action_dim_per_phase[:phase_idx])
        end_idx = start_idx + self._action_dim_per_phase[phase_idx]
        valid_action_logits = action_logits[:, start_idx:end_idx]

        action_probs = torch.softmax(valid_action_logits, dim=-1)

        return action_probs
