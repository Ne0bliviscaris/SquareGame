from math import ceil, floor

import pygame

from tiles import Ground


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

    def move(self, dx, dy):
        """Przesuwa kwadrat o daną ilość pikseli."""
        self.x += ceil(dx)
        self.y += ceil(dy)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self):
        """Aktualizuje pozycję kwadratu, dodając do niej prędkość."""
        self.velocity += self.gravity
        self.move(self.velocity_x, self.velocity)

    def draw(self, screen, camera_offset_x=0, camera_offset_y=0, zoom_level=1):
        """Rysuje kwadrat na ekranie."""
        pygame.draw.rect(
            screen,
            (180, 0, 0),
            pygame.Rect(
                int(self.x * zoom_level) + camera_offset_x + 1,
                int(self.y * zoom_level) + camera_offset_y + 1,
                int(self.size * zoom_level),
                int(self.size * zoom_level),
            ),
        )

    def move_left(self, speed):
        """Przesuwa kwadrat w lewo."""
        self.velocity_x = -speed

    def move_right(self, speed):
        """Przesuwa kwadrat w prawo."""
        self.velocity_x = speed

    def jump(self):
        """Sprawia, że kwadrat skacze."""
        self.velocity = -4

    def get_nearby_tiles(self, tiles, distance):
        """Zwraca listę kafelków, które są w danym dystansie od kwadratu."""
        return [tile for tile in tiles if abs(tile.x - self.x) <= distance and abs(tile.y - self.y) <= distance]

    def handle_ground_collisions(self, tiles):
        """Sprawdza kolizje między kwadratem a wszystkimi kafelkami."""
        nearby_tiles = self.get_nearby_tiles(tiles, self.size * 2)  # Użyj rozmiaru kwadratu jako dystansu
        for tile in nearby_tiles:
            if isinstance(tile, Ground) and tile.collides_with(self):
                self.handle_ground_collision(tile, tiles)

    def handle_ground_collision(self, tile, tiles):
        """Obsługuje kolizję kwadratu z danym kafelkiem."""
        is_above_and_falling = self.y < tile.y and self.velocity > 0
        is_below_and_rising = self.y > tile.y and self.velocity < 0
        is_moving_horizontally = self.velocity_x != 0
        is_moving_left = self.x > tile.x and self.velocity_x < 0

        if is_above_and_falling:
            self.velocity = 0
            self.move(0, tile.y - self.size - self.y)  # Przesuń kwadrat do kafelka
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
