from math import ceil

import pygame

from modules.world.world import CORNERS, DIRECTIONS, ROUND_CORNER, grid

GROUND_COLOR = (90, 45, 45)


class RoundCorners:
    """Klasa do obsługi zaokrąglania rogów."""

    def __init__(self, x, y, size, grid):
        """Inicjalizuje zaokrąglanie rogów."""
        self.x = x
        self.y = y
        self.size = size
        self.grid = grid
        self.bent_corners = []

    def is_corner_adjacent(self, corner):
        """Sprawdza, czy do kąta w tile klasy ground przylega drugi tile klasy ground."""
        from modules.objects.tiles import Ground

        for dir in CORNERS[corner]:
            dx, dy = DIRECTIONS[dir]
            new_x = self.x + dx
            new_y = self.y + dy
            is_inside_grid_y = 0 <= new_y < len(self.grid)
            is_inside_grid_x = 0 <= new_x < len(self.grid[0])
            if is_inside_grid_y and is_inside_grid_x:
                tile = self.grid[new_y][new_x]
                if isinstance(tile, Ground):
                    return True
        return False

    def bend_corner(self, direction):
        """Zgina kąt, jeśli do niego nie przylega inny kafelek klasy ground."""
        if direction not in self.bent_corners and not self.is_corner_adjacent(direction):
            self.bent_corners.append(direction)

    def bend_all_corners(self):
        """Zgina wszystkie kąty, jeśli do nich nie przylega inny kafelek klasy ground."""
        for direction in CORNERS:
            self.bend_corner(direction)

    def draw(self, screen, camera_offset_x=0, camera_offset_y=0, zoom_level=1):
        """Rysuje zaokrąglone rogi na ekranie."""
        rect = pygame.Rect(
            (self.x * zoom_level) + camera_offset_x,
            (self.y * zoom_level) + camera_offset_y,
            ceil(self.size * zoom_level),  # Ułamki powodują błędy w rysowaniu
            ceil(self.size * zoom_level),
        )
        corner_radius = (self.size // ROUND_CORNER) * zoom_level if self.bent_corners else 0
        self.draw_rounded_rect(
            screen,
            rect,
            GROUND_COLOR,
            [corner_radius] * 4,
            self.bent_corners,
        )

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
