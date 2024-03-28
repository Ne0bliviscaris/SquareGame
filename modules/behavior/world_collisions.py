from modules.objects.tiles import Ground
from modules.settings import GRID_PULLING_RANGE, SQUARE_SIZE, TILE_SIZE

CANT_JUMP = 1 - GRID_PULLING_RANGE


class WorldCollisions:
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
        self.square.move(0, tile.y - SQUARE_SIZE - self.square.y)  # Przesuń kwadrat do kafelka

    def handle_rising_collision(self, tile):
        """Obsługuje kolizję kwadratu z danym kafelkiem podczas skoku."""
        is_below_ground = self.square.y > tile.y + TILE_SIZE

        left_threshold = tile.x - SQUARE_SIZE * GRID_PULLING_RANGE
        left_offset_above_threshold = self.square.x < left_threshold
        grid_pull_left = (self.square.x // TILE_SIZE) * TILE_SIZE

        right_threshold = tile.x + TILE_SIZE + SQUARE_SIZE * GRID_PULLING_RANGE
        right_offset_above_threshold = self.square.x + SQUARE_SIZE > right_threshold
        grid_pull_right = (self.square.x // TILE_SIZE + 1) * TILE_SIZE

        if not is_below_ground:
            if left_offset_above_threshold:
                self.square.x = grid_pull_left
            elif right_offset_above_threshold:
                self.square.x = grid_pull_right
            else:
                self.square.y = tile.y + TILE_SIZE
                self.square.velocity_y = 0

    def handle_horizontal_collision(self, tile, is_moving_left):
        """Obsługuje kolizję kwadratu z danym kafelkiem podczas ruchu poziomego."""
        self.square.velocity_x = 0
        if is_moving_left:
            self.square.x = tile.x + SQUARE_SIZE
        else:
            self.square.x = tile.x - SQUARE_SIZE

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

    def handle_collisions_around(self, tiles):
        """Sprawdza kolizje między kwadratem a wszystkimi kafelkami i innymi kwadratami."""
        nearby_tiles = self.get_nearby_tiles(tiles, SQUARE_SIZE * 2)  # Użyj rozmiaru kwadratu jako dystansu
        for tile in nearby_tiles:
            if isinstance(tile, Ground) and tile.collides_with(self.square):
                self.handle_collision(tile)
