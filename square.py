from math import ceil, floor

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

    def handle_ground_collision(self, tile, tiles):
        """Obsługuje kolizję kwadratu z danym kafelkiem."""
        is_above_and_falling = self.y < tile.y and self.velocity > 0
        is_below_and_rising = self.y > tile.y and self.velocity < 0
        is_moving_horizontally = self.velocity_x != 0
        is_moving_left = self.x > tile.x and self.velocity_x < 0

        if is_above_and_falling:
            self.velocity = 0
            self.y = tile.y - self.size
        elif is_below_and_rising:
            # Oblicz różnicę między środkiem kwadratu a środkiem kafelka
            center_diff = (self.x + self.size / 2) - (tile.x + tile.size / 2)

            # Jeśli środek kwadratu jest przesunięty o więcej niż 20% w lewo od środka kafelka
            if center_diff < -0.2 * tile.size:
                self.x = (self.x // tile.size) * tile.size
            # Jeśli środek kwadratu jest przesunięty o więcej niż 20% w prawo od środka kafelka
            elif center_diff > 0.2 * tile.size:
                self.x = (self.x // tile.size + 1) * tile.size
            else:
                self.y = tile.y + tile.size
                self.velocity = 0
        elif is_moving_horizontally:
            self.velocity_x = 0
            if is_moving_left:
                self.x = tile.x + self.size
            else:
                self.x = tile.x - self.size
