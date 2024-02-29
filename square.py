from math import ceil

import pygame


class Square:
    """Klasa reprezentująca kwadrat na ekranie."""

    def __init__(self, x, y, size):
        """Inicjalizuje kwadrat na podanej pozycji i o podanym rozmiarze."""
        self.x = x
        self.y = y
        self.size = size
        self.velocity = 5
        self.velocity_x = 0  # Dodajemy prędkość w osi x
        self.gravity = 0.07

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self):
        """Aktualizuje pozycję kwadratu, dodając do niej prędkość."""
        self.velocity += self.gravity
        self.y += self.velocity
        self.y = ceil(self.y)  # Zaokrągla wartość self.y do najbliższej liczby całkowitej
        self.x += self.velocity_x  # Aktualizujemy pozycję x na podstawie prędkości x

    def draw(self, screen, camera_offset_x=0, camera_offset_y=0, zoom_level=1):
        """Rysuje kwadrat na ekranie."""
        pygame.draw.rect(
            screen,
            (180, 0, 0),
            pygame.Rect(
                int(self.x * zoom_level) + camera_offset_x,
                int(self.y * zoom_level) + camera_offset_y,
                int(self.size * zoom_level),
                int(self.size * zoom_level),
            ),
        )

    def handle_ground_collision(self, tile):
        """Obsługuje kolizję kwadratu z danym kafelkiem."""
        is_above_and_falling = self.y < tile.y and self.velocity > 0
        is_below_and_rising = self.y > tile.y and self.velocity < 0
        is_left_and_moving_right = self.x < tile.x and self.velocity_x > 0
        is_right_and_moving_left = self.x > tile.x and self.velocity_x < 0
        is_right_and_moving_left_fast = (
            self.x > tile.x and self.velocity_x < 0 and abs(self.x - (tile.x + tile.size)) < self.velocity_x
        )

        if is_above_and_falling:
            self.velocity = 0
            self.y = tile.y - self.size

        elif is_below_and_rising:
            ground_coverage = (tile.x + tile.size - self.x) / self.size
            if ground_coverage > 0.6:
                self.y = tile.y + tile.size
                self.velocity = 0
            elif ground_coverage < 0.4:
                if self.x % tile.size < tile.size * 0.6:  # jeśli kwadrat jest bliżej lewej krawędzi kafelka
                    self.x = round((self.x // tile.size) * tile.size)
                elif tile.type == "Ground":  # sprawdzenie, czy typ kafelka nie jest równy 'Ground'
                    self.x = (self.x // tile.size + 1) * tile.size  # jeśli kwadrat jest bliżej prawej krawędzi kafelka

            else:
                self.velocity = 0

        elif is_left_and_moving_right:
            self.velocity_x = 0
            self.x = tile.x - self.size
        elif is_right_and_moving_left:
            self.velocity_x = 0
            self.x = tile.x + tile.size
        elif is_right_and_moving_left_fast:
            self.velocity_x = 0
            self.x = tile.x + tile.size
