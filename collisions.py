from tiles import Ground


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
        center_diff = (self.square.x + self.square.size / 2) - (tile.x + tile.size / 2)
        if center_diff < -0.2 * tile.size and self.square.y > tile.y:
            self.square.x = (self.square.x // tile.size) * tile.size
        elif center_diff > 0.2 * tile.size and self.square.y > tile.y:
            self.square.x = (self.square.x // tile.size + 1) * tile.size
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
        is_above_and_falling = self.square.y < tile.y and self.square.velocity_y > 0
        is_below_and_rising = self.square.y > tile.y and self.square.velocity_y < 0
        is_moving_horizontally = self.square.velocity_x != 0
        is_moving_left = self.square.x > tile.x and self.square.velocity_x < 0

        if is_above_and_falling:
            self.handle_falling_collision(tile)
        elif is_below_and_rising:
            self.handle_rising_collision(tile)
        elif is_moving_horizontally:
            self.handle_horizontal_collision(tile, is_moving_left)

    def handle_collisions_around(self, tiles):
        """Sprawdza kolizje między kwadratem a wszystkimi kafelkami."""
        nearby_tiles = self.get_nearby_tiles(tiles, self.square.size * 2)  # Użyj rozmiaru kwadratu jako dystansu
        for tile in nearby_tiles:
            if isinstance(tile, Ground) and tile.collides_with(self.square):
                self.handle_collision(tile)
