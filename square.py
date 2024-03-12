from math import ceil, floor

from pygame import Rect, draw

PLAYER_COLOR = (0, 180, 0)
CATCH_COLOR = (180, 0, 0)
FLEE_COLOR = (0, 0, 180)


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

    def move(self, dx, dy):
        """Przesuwa kwadrat o daną ilość pikseli."""
        self.x += dx
        self.y += ceil(dy)

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


class Player(Square):
    """Klasa reprezentująca kwadrat gracza."""

    def change_mode(self):
        """Zmienia tryb gracza."""
        super().change_mode()

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

    def draw(self, screen, camera_offset_x=0, camera_offset_y=0, zoom_level=1):
        """Rysuje kwadrat na ekranie."""
        # Ustalenie pozcji i wymiarów
        left = int(self.x * zoom_level) + camera_offset_x + 1
        top = int(self.y * zoom_level) + camera_offset_y + 1
        square = round(self.size * zoom_level)
        inner_color = CATCH_COLOR if self.mode == "catch" else FLEE_COLOR  # Używamy koloru zależnego od trybu

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
            int(9 * zoom_level),  # Szerokość obramowania
        )


class Ai(Square):
    """Klasa reprezentująca kwadrat przeciwnika."""

    def __init__(self, x, y, size, mode):
        """Inicjalizuje kwadrat na podanej pozycji i o podanym rozmiarze."""
        super().__init__(x, y, size)
        self.mode = mode  # Dodajemy tryb
        self.color = CATCH_COLOR if mode == "catch" else FLEE_COLOR  # Ustalamy kolor na podstawie trybu

    def change_mode(self):
        """Zmienia tryb AI."""
        super().change_mode()
        self.color = CATCH_COLOR if self.mode == "catch" else FLEE_COLOR

    def update(self, mode):
        """Aktualizuje pozycję kwadratu, dodając do niej prędkość."""
        super().update()
        if self.mode == "catch":
            ...
        else:
            ...
        # Dodaj tutaj logikę AI, która steruje ruchem przeciwnika

    def draw(self, screen, camera_offset_x=0, camera_offset_y=0, zoom_level=1):
        """Rysuje kwadrat na ekranie."""
        # Ustalenie pozcji i wymiarów
        left = int(self.x * zoom_level) + camera_offset_x + 1
        top = int(self.y * zoom_level) + camera_offset_y + 1
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
