from math import ceil, floor
from time import time

from pygame import Rect, draw

from ..settings import (
    CATCH_MODE,
    FLEE_MODE,
    GRAVITY,
    JUMP_COOLDOWN,
    JUMP_HEIGHT,
    OBSERVER_MODE,
    SPEED,
    SQUARE_SIZE,
)

PLAYER_COLOR = (0, 180, 0)
CATCH_COLOR = (180, 50, 0)
FLEE_COLOR = (0, 100, 180)
OBSERVER_COLOR = (180, 180, 180)


class Square:
    """Klasa reprezentująca kwadrat na ekranie."""

    def __init__(self, x, y, mode):
        """Inicjalizuje kwadrat na podanej pozycji i o podanym rozmiarze."""
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.velocity_x = 0  # Dodajemy prędkość w osi x
        self.gravity = GRAVITY * 0.01
        self.mode = mode
        self.color = CATCH_COLOR if mode == CATCH_MODE else FLEE_COLOR
        self.speed = SPEED
        self.collide = False  # Dodajemy atrybut kolizji
        self.score = 0  # Wynik gracza
        self.last_jump_time = 0

    def move(self, dx, dy):
        """Przesuwa kwadrat o daną ilość pikseli."""
        self.x += dx
        self.y += ceil(dy)

    def move_left(self):
        """Przesuwa kwadrat w lewo."""
        self.velocity_x = -self.speed

    def move_right(self):
        """Przesuwa kwadrat w prawo."""
        self.velocity_x = self.speed

    def jump(self):
        """Sprawia, że kwadrat skacze."""
        now = time()
        if now - self.last_jump_time > JUMP_COOLDOWN:
            self.velocity_y = -JUMP_HEIGHT
            self.last_jump_time = now

    def change_mode(self):
        """Zmienia tryb kwadratu."""
        if self.mode == CATCH_MODE:
            self.mode = FLEE_MODE
            self.color = FLEE_COLOR
        else:
            self.mode = CATCH_MODE
            self.color = CATCH_COLOR

    @property
    def rect(self):
        return Rect(self.x, self.y, SQUARE_SIZE, SQUARE_SIZE)

    def update(self, squares):
        """Aktualizuje pozycję kwadratu, dodając do niej prędkość."""
        self.velocity_y += self.gravity
        self.move(self.velocity_x, self.velocity_y)

        # Sprawdź kolizje z innymi kwadratami
        for other_square in squares:
            if self is not other_square and self.collides_with(other_square):
                self.collide = True
                break
        else:
            self.collide = False

    def draw(self, screen, camera_offset_x=0, camera_offset_y=0, zoom_level=1):
        """Rysuje kwadrat na ekranie."""
        # Ustalenie pozcji i wymiarów
        left = int(self.x * zoom_level) + camera_offset_x + 1
        top = int(self.y * zoom_level) + camera_offset_y + 1
        square = round(SQUARE_SIZE * zoom_level)
        draw.rect(
            screen,
            PLAYER_COLOR,
            Rect(
                left,
                top,
                square,
                square,
            ),
        )

    def collides_with(self, other):
        """Sprawdza, czy kwadrat koliduje z innym obiektem."""
        # Pozycje i wymiary
        self_right = self.x + SQUARE_SIZE
        other_left = other.x
        left_left = self.x
        other_right = other.x + SQUARE_SIZE
        self_bottom = self.y + SQUARE_SIZE
        other_top = other.y
        self_top = self.y
        other_bottom = other.y + SQUARE_SIZE
        if self.mode != other.mode and self.mode != OBSERVER_MODE and other.mode != OBSERVER_MODE:
            return not (
                self_right <= other_left
                or left_left >= other_right
                or self_bottom <= other_top
                or self_top >= other_bottom
            )  # Zwróć True, jeśli występuje kolizja
