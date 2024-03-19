import torch
import torch.nn as nn

from ..settings import TOTAL_SQUARES
from .deep_learning_data import PARAMETERS_LENGTH


class DeepLearningAgent:
    """Agent AI, który wykorzystuje sieć neuronową do podejmowania decyzji."""

    def __init__(self):
        self.network = self.create_network()

    def create_network(self):
        data_matrix_length = PARAMETERS_LENGTH * TOTAL_SQUARES
        return nn.Sequential(nn.Linear(data_matrix_length, 256), nn.ReLU(), nn.Linear(256, 3), nn.Softmax(dim=-1))

    def predict(self, game_state):
        state_tensor = torch.tensor(game_state, dtype=torch.float32)
        action_probabilities = self.network(state_tensor)
        action = torch.argmax(action_probabilities).item()
        return action
