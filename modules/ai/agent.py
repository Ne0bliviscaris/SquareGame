import torch
import torch.nn as nn

from modules.ai.deep_learning_data import PARAMETERS_LENGTH
from modules.settings import TOTAL_SQUARES


class DeepLearningAgent:
    """Agent AI, który wykorzystuje sieć neuronową do podejmowania decyzji."""

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.network = self.create_network().to(self.device)
        self.optimizer = torch.optim.Adam(self.network.parameters())
        self.loss_function = nn.MSELoss()
        self.load_model()

    def create_network(self):
        data_matrix_length = PARAMETERS_LENGTH * TOTAL_SQUARES
        return nn.Sequential(nn.Linear(data_matrix_length, 256), nn.ReLU(), nn.Linear(256, 3), nn.Softmax(dim=-1))

    def predict(self, game_state):
        state_tensor = torch.tensor(game_state, dtype=torch.float32).to(self.device)
        action_probabilities = self.network(state_tensor)
        action = torch.argmax(action_probabilities).item()
        return action

    def save_model(self):
        torch.save(self.network.state_dict(), "modules/ai/model.pth")

    def load_model(self):
        try:
            self.network.load_state_dict(torch.load("modules/ai/model.pth"))
            print("Wczytano model")
        except FileNotFoundError:
            pass  # Jeśli plik modelu nie istnieje, po prostu kontynuuj
        except RuntimeError:
            print("Niewłaściwy rozmiar modelu, tworzę nowy model")

    def train(self, game_state, target):
        self.optimizer.zero_grad()  # Zeruj gradienty
        state_tensor = torch.tensor(game_state, dtype=torch.float32).to(self.device)
        target_tensor = torch.full((3,), target, dtype=torch.float32).to(self.device)
        output = self.network(state_tensor)  # Przewidywania modelu
        loss = self.loss_function(output, target_tensor)  # Oblicz strate
        loss.backward()  # Oblicz gradienty
        self.optimizer.step()  # Aktualizuj wagi
