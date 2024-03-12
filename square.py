from math import ceil, floor

from pygame import Rect, draw

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
        self.gravity = 0.12
        self.mode = mode
        self.color = PLAYER_COLOR if mode == "catch" else FLEE_COLOR
        self.collision_cooldown = 3

    def move(self, dx, dy):
        """Przesuwa kwadrat o daną ilość pikseli."""
        self.x += dx
        self.y += ceil(dy)

    def move_left(self, speed):
        """Przesuwa kwadrat w lewo."""
        self.velocity_x = -speed

    def move_right(self, speed):
        """Przesuwa kwadrat w prawo."""
        self.velocity_x = speed

    def jump(self):
        """Sprawia, że kwadrat skacze."""
        if self.velocity_y == 0:
            self.velocity_y = -8

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

    def update(self):
        """Aktualizuje pozycję kwadratu, dodając do niej prędkość."""
        self.velocity_y += self.gravity
        self.move(self.velocity_x, self.velocity_y)

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
        return not (
            self.x + self.size <= other.x
            or self.x >= other.x + other.size
            or self.y + self.size <= other.y
            or self.y >= other.y + other.size
        )


class Player(Square):
    """Klasa reprezentująca kwadrat gracza."""

    def change_mode(self):
        """Zmienia tryb gracza."""
        super().change_mode()

    def draw(self, screen, camera_offset_x=0, camera_offset_y=0, zoom_level=1):
        """Rysuje kwadrat na ekranie."""
        # Ustalenie pozcji i wymiarów
        left = int(self.x * zoom_level) + camera_offset_x + 1
        top = int(self.y * zoom_level) + camera_offset_y + 1
        square = round(self.size * zoom_level)

        if self.mode == "catch":
            inner_color = CATCH_COLOR
        elif self.mode == "observer":
            inner_color = OBSERVER_COLOR
        else:
            inner_color = FLEE_COLOR
        # Rysowanie kwadratu
        draw.rect(
            screen,
            inner_color,
            Rect(
                left,
                top,
                square,
                square,
            ),
        )

        # Rysowanie obramowania
        draw.rect(
            screen,
            PLAYER_COLOR,
            Rect(
                left,
                top,
                square,
                square,
            ),
            int(10 * zoom_level),  # Szerokość obramowania
        )
