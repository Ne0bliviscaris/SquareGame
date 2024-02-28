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
        super().__init__(x, y, size, (SKY_COLOR))  # Kolor niebieski


class Ground(Tile):
    """Klasa dla kafelków ground."""

    BENT_COLOR = (70, 35, 35)  # Kolor dla zagiętych kątów

    def __init__(self, x, y, size, grid):
        """Inicjalizuje kafelek ground na podanej pozycji i o podanym rozmiarze."""
        super().__init__(x, y, size, (GROUND_COLOR))  # Kolor brązowy

    @property
    def rect(self):
        """Generuje kwadrat o podanych wymiarach."""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def collides_with(self, other):
        """Sprawdza, czy ten kafelek koliduje z innym obiektem."""
        return self.rect.colliderect(other.rect)

    def is_corner_adjacent(self, direction, grid):
        """Sprawdza, czy do kąta w tile klasy ground przylega drugi tile klasy ground."""
        # Tworzymy listę kafelków, które są wokół danego kąta.
        # Każdy kafelek jest identyfikowany przez parę współrzędnych (x, y).
        # Współrzędne są obliczane na podstawie pozycji aktualnego kafelka (self.x, self.y)
        # oraz przesunięcia kąta (dx, dy).

        DIRECTIONS = {
            "top_left": [(-1, -1), (0, -1), (-1, 0)],
            "top_right": [(0, -1), (1, -1), (1, 0)],
            "bottom_left": [(-1, 0), (-1, 1), (0, 1)],
            "bottom_right": [(1, 0), (0, 1), (1, 1)],
        }
        corner_tiles = [
            grid[self.y + dy][self.x + dx]
            for dx, dy in DIRECTIONS[direction]
            if 0 <= self.y + dy < len(grid) and 0 <= self.x + dx < len(grid[0])
        ]

        # Sprawdzamy, czy którykolwiek z kafelków wokół kąta jest kafelkiem klasy Ground.
        # Jeśli tak, zwracamy True. W przeciwnym razie zwracamy False.
        return any(isinstance(tile, Ground) for tile in corner_tiles)

    def bend_corner(self, direction, grid):
        """Zgina kąt, jeśli do niego nie przylega inny kafelek klasy ground."""
        if not self.is_corner_adjacent(direction, grid):
            self.color = self.BENT_COLOR
