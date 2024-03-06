from math import ceil, floor

from pygame import Rect, draw


class Square:
    """Klasa reprezentująca kwadrat na ekranie."""

    def __init__(self, x, y, size):
        """Inicjalizuje kwadrat na podanej pozycji i o podanym rozmiarze."""
        self.x = x
        self.y = y
        self.size = size
        self.velocity_y = 5
        self.velocity_x = 0  # Dodajemy prędkość w osi x
        self.gravity = 0.07

    def move(self, dx, dy):
        """Przesuwa kwadrat o daną ilość pikseli."""
        self.x += dx
        self.y += ceil(dy)

    @property
    def rect(self):
        return Rect(self.x, self.y, self.size, self.size)

    def update(self):
        """Aktualizuje pozycję kwadratu, dodając do niej prędkość."""
        self.velocity_y += self.gravity
        self.move(self.velocity_x, self.velocity_y)

    def draw(self, screen, camera_offset_x=0, camera_offset_y=0, zoom_level=1):
        """Rysuje kwadrat na ekranie."""
        draw.rect(
            screen,
            (180, 0, 0),
            Rect(
                int(self.x * zoom_level) + camera_offset_x + 1,
                int(self.y * zoom_level) + camera_offset_y + 1,
                int(self.size * zoom_level),
                int(self.size * zoom_level),
            ),
        )


class Player(Square):
    """Klasa reprezentująca kwadrat gracza."""

    def move_left(self, speed):
        """Przesuwa kwadrat w lewo."""
        self.velocity_x = -speed

    def move_right(self, speed):
        """Przesuwa kwadrat w prawo."""
        self.velocity_x = speed

    def jump(self):
        """Sprawia, że kwadrat skacze."""
        self.velocity_y = -4


class AI(Square):
    """Klasa reprezentująca kwadrat przeciwnika."""

    def update(self):
        """Aktualizuje pozycję kwadratu, dodając do niej prędkość."""
        super().update()

        # Dodaj tutaj logikę AI, która steruje ruchem przeciwnika
