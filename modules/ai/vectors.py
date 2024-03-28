from pygame import draw

from modules.settings import CATCH_MODE, FLEE_MODE, TILE_SIZE


class VectorCalculator:
    """Klasa do obliczania wektorów i dystansów między kwadratami."""

    def __init__(self, squares):
        """Inicjalizuje kalkulator z listą kwadratów."""
        self.squares = squares

    def calculate_vectors(self):
        """Oblicza wektory od kwadratów typu 'catch' do kwadratów typu 'flee' i odwrotnie."""
        catch_squares = [square for square in self.squares if square.mode == CATCH_MODE]
        flee_squares = [square for square in self.squares if square.mode == FLEE_MODE]

        vectors = []
        for catch_square in catch_squares:
            for flee_square in flee_squares:
                catch_mid_x = catch_square.x + TILE_SIZE / 2
                catch_mid_y = catch_square.y + TILE_SIZE / 2

                flee_mid_x = flee_square.x + TILE_SIZE / 2
                flee_mid_y = flee_square.y + TILE_SIZE / 2

                vector = (catch_mid_x, catch_mid_y, flee_mid_x - catch_mid_x, flee_mid_y - catch_mid_y)
                vectors.append(vector)

        for flee_square in flee_squares:
            for catch_square in catch_squares:
                vector = (flee_mid_x, flee_mid_y, catch_mid_x - flee_mid_x, catch_mid_y - flee_mid_y)
                vectors.append(vector)

        return vectors

    def draw_vectors(self, screen, zoom, cam_x, cam_y):
        """Rysuje wektory na ekranie."""
        for vector in self.calculate_vectors():
            start_pos = (
                vector[0] * zoom + cam_x,
                vector[1] * zoom + cam_y,
            )
            end_pos = (
                start_pos[0] + vector[2] * zoom,
                start_pos[1] + vector[3] * zoom,
            )
            draw.line(screen, (255, 0, 0), start_pos, end_pos)
