import random

import torch
import torch.nn as nn
from pygame import Rect, draw

from modules.objects.square import (
    CATCH_COLOR,
    CATCH_MODE,
    FLEE_COLOR,
    FLEE_MODE,
    OBSERVER_MODE,
    Square,
)


class Ai(Square):
    """Klasa reprezentująca kwadrat przeciwnika."""

    def __init__(self, x, y, size, deep_learning_data, mode=FLEE_MODE):
        """Inicjalizuje kwadrat na podanej pozycji i o podanym rozmiarze."""
        super().__init__(x, y, size)
        self.mode = mode  # Dodajemy tryb
        self.color = CATCH_COLOR if mode == CATCH_MODE else FLEE_COLOR  # Ustalamy kolor na podstawie trybu
        self.deep_learning_data = deep_learning_data
        self.network = self.network()  # Stworzenie sieci neuronowej
        self.score = 0  # Wynik AI

    def change_mode(self):
        """Zmienia tryb AI."""
        super().change_mode()
        self.color = CATCH_COLOR if self.mode == CATCH_MODE else FLEE_COLOR

    def draw(self, screen, camera_offset_x=0, camera_offset_y=0, zoom_level=1):
        """Rysuje kwadrat na ekranie."""
        # Ustalenie pozcji i wymiarów
        left = int(self.x * zoom_level) + camera_offset_x
        top = int(self.y * zoom_level) + camera_offset_y
        square = round(self.size * zoom_level)
        draw.rect(
            screen,
            self.color,  # Używamy koloru zależnego od trybu
            Rect(
                left,
                top,
                square,
                square,
            ),
        )
        if self.collide:
            draw.rect(
                screen,
                (255, 255, 255),  # Biały kolor
                Rect(
                    left,
                    top,
                    square,
                    square,
                ),
                5,  # Szerokość ramki
            )

    def update(self, squares, game_state):
        """Aktualizuje pozycję kwadratu, dodając do niej prędkość."""
        print("Update Ai")
        super().update(squares)
        action = self.predict(game_state)  # Predykcja kolejnego ruchu
        if action == "jump":
            self.jump()
        elif action == "move_left":
            self.move_left()
        elif action == "move_right":
            self.move_right()

    def predict(self, game_state):
        """Wykonuje predykcję na podstawie stanu."""
        game_state = torch.tensor(game_state, dtype=torch.float32)  # Przekształć stan gry na tensor
        action_probabilities = self.network(game_state)  # Przepuść stan przez sieć neuronową
        action = torch.argmax(action_probabilities).item()  # Wybierz akcję z największym prawdopodobieństwem
        return action

    def network(self):
        return nn.Sequential(nn.Linear(24, 128), nn.ReLU(), nn.Linear(128, 3), nn.Softmax(dim=-1))
