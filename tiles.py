from math import ceil

import pygame

from world import ROUND_CORNER

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

    BENT_COLOR = (40, 40, 140)  # Kolor dla zagiętych kątów

    def __init__(self, x, y, size, grid):
        """Inicjalizuje kafelek ground na podanej pozycji i o podanym rozmiarze."""
        super().__init__(x, y, size, (GROUND_COLOR))  # Kolor brązowy
        self.bent_corners = []

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
        if direction not in self.bent_corners and not self.is_corner_adjacent(direction, grid):
            self.bent_corners.append(direction)

    def draw_rounded_rect(self, surface, rect, color, corner_radiuses, corners_to_round):
        """Rysuje zaokrąglony prostokąt."""
        # Rozpakowujemy promienie rogów z listy corner_radiuses
        top_left_radius, top_right_radius, bottom_left_radius, bottom_right_radius = corner_radiuses

        # Sprawdzamy, czy żaden z promieni nie jest ujemny
        if min(corner_radiuses) < 0:
            raise ValueError(f"Corner radius {min(corner_radiuses)} must be >= 0")
        # Sprawdzamy, czy żaden z promieni nie jest większy niż połowa szerokości lub wysokości prostokąta
        elif max(corner_radiuses) > rect.width / 2 or max(corner_radiuses) > rect.height / 2:
            raise ValueError(f"Corner radius {max(corner_radiuses)} is too large for the rectangle")

        # Rysujemy dwa prostokąty wewnątrz naszego zaokrąglonego prostokąta
        # Pierwszy prostokąt jest wertykalny i nie obejmuje zaokrąglonych rogów
        pygame.draw.rect(
            surface,
            color,
            (
                rect.left,
                rect.top + min(top_left_radius, top_right_radius),
                rect.width,
                rect.height - min(top_left_radius, top_right_radius, bottom_left_radius, bottom_right_radius),
            ),
        )
        # Drugi prostokąt jest poziomy i nie obejmuje zaokrąglonych rogów
        pygame.draw.rect(
            surface,
            color,
            (
                rect.left + min(top_left_radius, bottom_left_radius),
                rect.top,
                rect.width - min(top_left_radius, top_right_radius, bottom_left_radius, bottom_right_radius),
                rect.height,
            ),
        )

        # Rysujemy cztery koła w rogach naszego zaokrąglonego prostokąta
        # Każde koło jest rysowane tylko wtedy, gdy odpowiadający mu róg ma być zaokrąglony (jest w liście corners_to_round)
        if top_left_radius > 0 and "top_left" in corners_to_round:
            pygame.draw.circle(
                surface, color, (rect.left + top_left_radius, rect.top + top_left_radius), top_left_radius
            )
        if top_right_radius > 0 and "top_right" in corners_to_round:
            pygame.draw.circle(
                surface, color, (rect.right - top_right_radius, rect.top + top_right_radius), top_right_radius
            )
        if bottom_left_radius > 0 and "bottom_left" in corners_to_round:
            pygame.draw.circle(
                surface, color, (rect.left + bottom_left_radius, rect.bottom - bottom_left_radius), bottom_left_radius
            )
        if bottom_right_radius > 0 and "bottom_right" in corners_to_round:
            pygame.draw.circle(
                surface,
                color,
                (rect.right - bottom_right_radius, rect.bottom - bottom_right_radius),
                bottom_right_radius,
            )

    def draw(self, screen, camera_offset_x=0, camera_offset_y=0, zoom_level=1):
        """Rysuje kafelek na ekranie."""
        rect = pygame.Rect(
            (self.x * zoom_level) + camera_offset_x,
            (self.y * zoom_level) + camera_offset_y,
            ceil(self.size * zoom_level),  # Ułamki powodują błędy w rysowaniu
            ceil(self.size * zoom_level),
        )
        self.draw_rounded_rect(
            screen,
            rect,
            self.color,
            [
                self.size // ROUND_CORNER if corner in self.bent_corners else 0
                for corner in ["top_left", "top_right", "bottom_left", "bottom_right"]
            ],
            self.bent_corners,
        )
