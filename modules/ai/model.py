import torch
import torch.nn as nn
from ai import Ai


class Catch(Ai):
    def __init__(self, x, y, size, mode="catch"):
        super().__init__(x, y, size, mode)

    def predict(self, state):
        # Przekształć stan gry na tensor
        state = torch.tensor(state, dtype=torch.float32)
        # Przepuść stan przez sieć neuronową
        action_probabilities = self.network(state)
        # Wybierz akcję z największym prawdopodobieństwem
        action = torch.argmax(action_probabilities).item()
        return action

    def update(self, state):
        action = self.predict(state)
        if action == 0:
            self.jump()
        elif action == 1:
            self.move_left()
        elif action == 2:
            self.move_right()


class Flee(Ai):
    def __init__(self, x, y, size, mode="catch"):
        super().__init__(x, y, size, mode)

    def predict(self, state):
        # Przekształć stan gry na tensor
        state = torch.tensor(state, dtype=torch.float32)
        # Przepuść stan przez sieć neuronową
        action_probabilities = self.network(state)
        # Wybierz akcję z największym prawdopodobieństwem
        action = torch.argmax(action_probabilities).item()
        return action

    def update(self, state):
        action = self.predict(state)
        if action == 0:
            self.jump()
        elif action == 1:
            self.move_left()
        elif action == 2:
            self.move_right()
