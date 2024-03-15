from math import ceil, floor

from pygame import Rect, draw

from modules.settings import GRAVITY, JUMP_HEIGHT, SPEED

PLAYER_COLOR = (0, 180, 0)
CATCH_COLOR = (180, 50, 0)
FLEE_COLOR = (0, 100, 180)
OBSERVER_COLOR = (180, 180, 180)


class Square:
    """Klasa reprezentująca kwadrat na ekranie."""

    def __init__(self, x, y, size, mode="flee"):
        """Inicjalizuje kwadrat na podanej pozycji i o podanym rozmiarze."""
        self.x = x
        self.y = y
        self.size = size
        self.velocity_y = 0
        self.velocity_x = 0  # Dodajemy prędkość w osi x
        self.gravity = GRAVITY * 0.01
        self.mode = mode
        self.color = PLAYER_COLOR if mode == "catch" else FLEE_COLOR
        self.speed = SPEED
        self.collide = False  # Dodajemy atrybut kolizji

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
        self.velocity_y = -JUMP_HEIGHT

    def change_mode(self):
        """Zmienia tryb kwadratu."""
        if self.mode == "catch":
            self.mode = "flee"
            self.color = FLEE_COLOR
        else:
            self.mode = "catch"
            self.color = CATCH_COLOR

    @property
    def rect(self):
        return Rect(self.x, self.y, self.size, self.size)

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
        square = round(self.size * zoom_level)
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
        self_right = self.x + self.size
        other_left = other.x
        left_left = self.x
        other_right = other.x + other.size
        self_bottom = self.y + self.size
        other_top = other.y
        self_top = self.y
        other_bottom = other.y + other.size
        if self.mode != other.mode and self.mode != "observer" and other.mode != "observer":
            return not (
                self_right <= other_left
                or left_left >= other_right
                or self_bottom <= other_top
                or self_top >= other_bottom
            )  # Zwróć True, jeśli występuje kolizja
