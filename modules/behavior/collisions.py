import math

from pygame import time

from modules.objects.tiles import Ground

GRID_PULLING_RANGE = 0.5
CANT_JUMP = 1 - GRID_PULLING_RANGE


class Collisions:
    """Klasa do obsługi kolizji kwadratu."""

    def __init__(self, square):
        """Inicjalizuje obiekt kolizji dla danego kwadratu."""
        self.square = square

    def get_nearby_tiles(self, tiles, distance):
        """Zwraca listę kafelków, które są w danym dystansie od kwadratu."""
        return [tile for tile in tiles if self._is_tile_nearby(tile, distance)]

    def _is_tile_nearby(self, tile, distance):
        """Sprawdza, czy dany kafelek jest w określonym dystansie od kwadratu."""
        is_x_nearby = abs(tile.x - self.square.x) <= distance
        is_y_nearby = abs(tile.y - self.square.y) <= distance
        return is_x_nearby and is_y_nearby

    def handle_falling_collision(self, tile):
        """Obsługuje kolizję kwadratu z danym kafelkiem podczas spadania."""
        self.square.velocity_y = 0
        self.square.move(0, tile.y - self.square.size - self.square.y)  # Przesuń kwadrat do kafelka

    def handle_rising_collision(self, tile):
        """Obsługuje kolizję kwadratu z danym kafelkiem podczas skoku."""
        is_below_ground = self.square.y > tile.y + tile.size

        left_threshold = tile.x - self.square.size * GRID_PULLING_RANGE
        left_offset_above_threshold = self.square.x < left_threshold
        grid_pull_left = (self.square.x // tile.size) * tile.size

        right_threshold = tile.x + tile.size + self.square.size * GRID_PULLING_RANGE
        right_offset_above_threshold = self.square.x + self.square.size > right_threshold
        grid_pull_right = (self.square.x // tile.size + 1) * tile.size

        if not is_below_ground:
            if left_offset_above_threshold:
                self.square.x = grid_pull_left
            elif right_offset_above_threshold:
                self.square.x = grid_pull_right
            else:
                self.square.y = tile.y + tile.size
                self.square.velocity_y = 0

    def handle_horizontal_collision(self, tile, is_moving_left):
        """Obsługuje kolizję kwadratu z danym kafelkiem podczas ruchu poziomego."""
        self.square.velocity_x = 0
        if is_moving_left:
            self.square.x = tile.x + self.square.size
        else:
            self.square.x = tile.x - self.square.size

    def handle_collision(self, tile):
        """Obsługuje kolizję kwadratu z danym kafelkiem."""
        # Warunki kolizji
        is_above = self.square.y < tile.y
        is_falling = self.square.velocity_y > 0
        is_below = self.square.y > tile.y
        is_rising = self.square.velocity_y < 0
        is_moving_horizontally = self.square.velocity_x != 0
        is_moving_left = self.square.x > tile.x and self.square.velocity_x < 0

        if is_above and is_falling:
            self.handle_falling_collision(tile)
        elif is_below and is_rising:
            self.handle_rising_collision(tile)
        elif is_moving_horizontally:
            self.handle_horizontal_collision(tile, is_moving_left)

    def handle_square_collisions(self, squares):
        """Sprawdza kolizje między kwadratem a wszystkimi innymi kwadratami."""
        if time.get_ticks() < self.square.collision_cooldown:  # Jeśli licznik czasu nie upłynął, nie sprawdzamy kolizji
            return

        for other_square in squares:
            if other_square is not self.square and self.square.mode != other_square.mode and self.square.collides_with(other_square):
                self.square.change_mode()
                other_square.change_mode()
                # Ustawiamy licznik czasu na 3 sekundy od teraz
                self.square.collision_cooldown = time.get_ticks() + 3000
                other_square.collision_cooldown = time.get_ticks() + 3000

                # Przesuń kwadraty tak, aby nie były w stanie kolizji
                dx = self.square.x - other_square.x
                dy = self.square.y - other_square.y
                distance = math.sqrt(dx**2 + dy**2)
                min_distance = self.square.size + other_square.size
                if distance < min_distance:
                    # Oblicz wektor przesunięcia
                    push = (min_distance - distance) / distance
                    push_x = dx * push
                    push_y = dy * push

                    # Przesuń kwadraty
                    self.square.x += push_x * 0.01
                    self.square.y += push_y * 0.01
                    other_square.x -= push_x * 0.01
                    other_square.y -= push_y * 0.01

    def handle_collisions_around(self, tiles, squares):
        """Sprawdza kolizje między kwadratem a wszystkimi kafelkami i innymi kwadratami."""
        nearby_tiles = self.get_nearby_tiles(tiles, self.square.size * 2)  # Użyj rozmiaru kwadratu jako dystansu
        for tile in nearby_tiles:
            if isinstance(tile, Ground) and tile.collides_with(self.square):
                self.handle_collision(tile)
        self.handle_square_collisions(squares)
