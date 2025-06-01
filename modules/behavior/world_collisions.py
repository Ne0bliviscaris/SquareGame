from modules.objects.tiles import Ground
from modules.settings import GRID_PULLING_RANGE, SQUARE_SIZE, TILE_SIZE

CANT_JUMP = 1 - GRID_PULLING_RANGE
COLLISION_DISTANCE = SQUARE_SIZE + 1


class WorldCollisions:
    """Handles collisions for the square."""

    def __init__(self, square):
        """Initializes the collision object for a given square."""
        self.square = square

    def get_nearby_tiles(self, tiles):
        """Returns a list of tiles that are within a given distance from the square."""
        return [tile for tile in tiles if self._in_collision_range(tile)]

    def _in_collision_range(self, tile):
        """Checks if a given tile is within a specified distance from the square."""
        is_x_nearby = abs(tile.x - self.square.x) <= COLLISION_DISTANCE
        is_y_nearby = abs(tile.y - self.square.y) <= COLLISION_DISTANCE

        return is_x_nearby and is_y_nearby

    def handle_falling_collision(self, tile):
        """Handles the collision of the square with a given tile while falling."""
        self.square.velocity_y = 0
        self.square.move(0, tile.y - SQUARE_SIZE - self.square.y)

    def handle_rising_collision(self, tile):
        """Handles the collision of the square with a given tile during a jump."""
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
        """Handles the collision of the square with a given tile during horizontal movement."""
        self.square.velocity_x = 0
        if is_moving_left:
            self.square.x = tile.x + SQUARE_SIZE
        else:
            self.square.x = tile.x - SQUARE_SIZE

    def handle_collision(self, tile):
        """Handles the collision of the square with a given tile."""
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

    def handle_collisions_around(self, ground_tiles):
        """Checks for collisions between the square and all ground tiles."""
        nearby_tiles = self.get_nearby_tiles(ground_tiles)
        for tile in nearby_tiles:
            if tile.collides_with(self.square):
                self.handle_collision(tile)
