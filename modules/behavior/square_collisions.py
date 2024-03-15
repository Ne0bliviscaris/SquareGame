import math


class SquareCollisions:
    """Klasa do obsługi kolizji między kwadratami."""

    def __init__(self, square):
        """Inicjalizuje obiekt kolizji dla danego kwadratu."""
        self.square = square

    def handle_square_collisions(self, squares):
        """Sprawdza kolizje między kwadratem a wszystkimi innymi kwadratami."""
        for other_square in squares:
            if (
                other_square is not self.square
                and self.square.mode != other_square.mode
                and self.square.mode != "observer"
                and other_square.mode != "observer"
                and self.square.collides_with(other_square)
            ):

                self.square.collide = True
                other_square.collide = True

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
