from math import ceil

import pygame

SKY_COLOR = (40, 40, 140)
GROUND_COLOR = (90, 45, 45)


class Tile:
    """Klasa bazowa dla kafelków."""

    def __init__(self, x, y, size, color):
        """Inicjalizuje kafelek na podanej pozycji, o podanym rozmiarze i kolorze."""
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    def draw(self, screen, camera_offset_x=0, camera_offset_y=0, zoom_level=1):
        """Rysuje kafelek na ekranie."""
        # Ustalenie pozcji i wymiarów
        left = (self.x * zoom_level) + camera_offset_x
        top = (self.y * zoom_level) + camera_offset_y
        square = ceil(self.size * zoom_level)  # Ułamki powodują błędy w rysowaniu

        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(
                left,
                top,
                square,
                square,
            ),
        )


class Sky(Tile):
    """Klasa dla kafelków skybox."""

    def __init__(self, x, y, size):
        """Inicjalizuje kafelek skybox na podanej pozycji i o podanym rozmiarze."""
        super().__init__(x, y, size, (SKY_COLOR))  # Kolor niebieski
        self.type = "Sky"


class Ground(Tile):
    """Klasa dla kafelków ground."""

    def __init__(self, x, y, size, grid):
        """Inicjalizuje kafelek ground na podanej pozycji i o podanym rozmiarze."""
        super().__init__(x, y, size, (GROUND_COLOR))  # Kolor brązowy
        self.type = "Ground"

    @property
    def rect(self):
        """Generuje kwadrat o podanych wymiarach."""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def collides_with(self, other):
        """Sprawdza, czy ten kafelek koliduje z innym obiektem."""
        return self.rect.colliderect(other.rect)
