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

from ..settings import TOTAL_SQUARES
from .agent import DeepLearningAgent
from .deep_learning_data import PARAMETERS_LENGTH
from .score import Score

JUMP = 0
LEFT = 1
RIGHT = 2


class Ai(Square):
    """Klasa reprezentująca kwadrat przeciwnika."""

    def __init__(self, x, y, size, mode):
        """Inicjalizuje kwadrat na podanej pozycji i o podanym rozmiarze."""
        super().__init__(x, y, size, mode)
        self.x = x
        self.y = y
        self.mode = mode

        self.color = CATCH_COLOR if self.mode == CATCH_MODE else FLEE_COLOR
        self.score = 0  # Q-learning
        self.score_calculator = Score(self.score)

        self.agent = DeepLearningAgent()

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
        super().update(squares)
        self.game_state = game_state
        self.score_calculator.update(
            self.x, self.y, self.mode, self.collide, self.move_left, self.move_right, self.jump
        )  # Aktualizuj wynik
        action = self.agent.predict(self.game_state)  # Predykcja kolejnego ruchu
        if action == JUMP:
            self.jump()
        elif action == LEFT:
            self.move_left()
        elif action == RIGHT:
            self.move_right()
