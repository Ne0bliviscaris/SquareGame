import torch
import torch.nn as nn

from modules.ai.ai import Ai


class Flee(Ai):
    def __init__(self, x, y, size, mode="flee"):
        super().__init__(x, y, size, mode)
        self.network = self.network()  # Stworzenie sieci neuronowej

    def predict(self, state):
        print(f"Predict po stronie Flee")
        if state is not None:
            state = torch.tensor(state, dtype=torch.float32)  # Przekształć stan gry na tensor
            print(f"Stan gry: {state}")
            action_probabilities = self.network(state)  # Przepuść stan przez sieć neuronową
            action = torch.argmax(action_probabilities).item()  # Wybierz akcję z największym prawdopodobieństwem
            return action

    def network(self):
        return nn.Sequential(nn.Linear(4, 128), nn.ReLU(), nn.Linear(128, 3), nn.Softmax(dim=-1))
