from math import ceil

import pygame

from world import GROUND, SKY, TILE_SIZE, grid


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
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(
                (self.x * zoom_level) + camera_offset_x,
                (self.y * zoom_level) + camera_offset_y,
                ceil(self.size * zoom_level),  # Ułamki powodują błędy w rysowaniu
                ceil(self.size * zoom_level),
            ),
        )


class Sky(Tile):
    """Klasa dla kafelków skybox."""

    def __init__(self, x, y, size):
        """Inicjalizuje kafelek skybox na podanej pozycji i o podanym rozmiarze."""
        super().__init__(x, y, size, (40, 40, 140))  # Kolor niebieski


class Ground(Tile):
    """Klasa dla kafelków ground."""

    def __init__(self, x, y, size):
        """Inicjalizuje kafelek ground na podanej pozycji i o podanym rozmiarze."""
        super().__init__(x, y, size, (90, 45, 45))  # Kolor brązowy

    @property
    def rect(self):
        """Returns the pygame.Rect object representing the tile."""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def collides_with(self, other):
        """Sprawdza, czy ten kafelek koliduje z innym obiektem."""
        return self.rect.colliderect(other.rect)


# Macierz reprezentująca świat, gdzie 0 to Skybox, a 1 to Ground
world_list = [
    (
        Sky(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE)
        if tile_type == SKY
        else Ground(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE)
    )
    for y, row in enumerate(grid)
    for x, tile_type in enumerate(row)
]
