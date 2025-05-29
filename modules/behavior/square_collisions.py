import math

from modules.settings import SQUARE_SIZE


class SquareCollisions:
    """Handle collisions between squares."""

    def __init__(self, square):
        """Initialize collision handler for given square."""
        self.square = square

    def handle_square_collisions(self, squares):
        """Check collisions between square and all other squares."""
        for other_square in squares:
            collide_with_enemy = (
                other_square is not self.square
                and self.square.mode != other_square.mode
                and self.square.collides_with(other_square)
            )
            not_observer = self.square.mode != "observer" and other_square.mode != "observer"

            if collide_with_enemy and not_observer:
                set_collision_flag(self.square, other_square)
                push_colliding_squares_apart(self.square, other_square)


def set_collision_flag(square1, square2):
    """Set collision flag for two squares."""
    square1.collide = True
    square2.collide = True


def push_colliding_squares_apart(square1, square2):
    """Push two squares apart if they are colliding."""
    PUSH_PER_FRAME = 0.01
    dx = square1.x - square2.x
    dy = square1.y - square2.y
    distance = math.hypot(dx, dy)
    min_distance = SQUARE_SIZE * 2
    overlapping_distance = distance < min_distance

    if overlapping_distance:
        push_vector = (min_distance - distance) / distance
        push_x = dx * push_vector
        push_y = dy * push_vector

        square1.x += push_x * PUSH_PER_FRAME
        square1.y += push_y * PUSH_PER_FRAME
        square2.x -= push_x * PUSH_PER_FRAME
        square2.y -= push_y * PUSH_PER_FRAME
