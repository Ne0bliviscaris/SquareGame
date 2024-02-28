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
        if self.y < tile.y and self.velocity > 0:
            self.velocity = 0
            self.y = tile.y - self.size
        elif self.x < tile.x and self.velocity_x > 0:
            self.velocity_x = 0
            self.x = tile.x - self.size
        elif self.x > tile.x and self.velocity_x < 0:
            self.velocity_x = 0
            self.x = tile.x + tile.size
        elif self.x > tile.x and self.velocity_x < 0 and abs(self.x - (tile.x + tile.size)) < self.velocity_x:
            self.velocity_x = 0
            self.x = tile.x + tile.size
