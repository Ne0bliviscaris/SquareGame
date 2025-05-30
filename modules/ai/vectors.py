from pygame import draw

from modules.settings import CATCH_MODE, FLEE_MODE, SCREEN, TILE_SIZE


class VectorCalculator:
    """Calculates vectors and distances between squares."""

    def __init__(self, squares):
        """Initialize calculator with list of squares."""
        self.squares = squares

    def calculate_vectors(self):
        """Calculate vectors from catch squares to flee squares and vice versa."""
        catch_squares = [square for square in self.squares if square.mode == CATCH_MODE]
        runner_squares = [square for square in self.squares if square.mode == FLEE_MODE]

        vectors = []
        for catcher in catch_squares:
            for runner in runner_squares:
                catch_mid_x = catcher.x + TILE_SIZE / 2
                catch_mid_y = catcher.y + TILE_SIZE / 2

                flee_mid_x = runner.x + TILE_SIZE / 2
                flee_mid_y = runner.y + TILE_SIZE / 2

                distance_x_from_catcher = flee_mid_x - catch_mid_x
                distance_y_from_catcher = flee_mid_y - catch_mid_y

                vector = (catch_mid_x, catch_mid_y, distance_x_from_catcher, distance_y_from_catcher)
                vectors.append(vector)

        for runner in runner_squares:
            for catcher in catch_squares:
                distance_x_from_runner = catch_mid_x - flee_mid_x
                distance_y_from_runner = catch_mid_y - flee_mid_y

                vector = (flee_mid_x, flee_mid_y, distance_x_from_runner, distance_y_from_runner)
                vectors.append(vector)

        return vectors

    def draw_vectors(self, zoom_level, cam_offset_x, cam_offset_y):
        """Draw vectors on screen."""
        for vector in self.calculate_vectors():
            start_offset_x = vector[0] * zoom_level + cam_offset_x
            start_offset_y = vector[1] * zoom_level + cam_offset_y

            start_pos = (start_offset_x, start_offset_y)

            end_offset_x = start_pos[0] + vector[2] * zoom_level
            end_offset_y = start_pos[1] + vector[3] * zoom_level

            end_pos = (end_offset_x, end_offset_y)

            self.draw_line(start_pos, end_pos)

    def draw_line(self, start, end):
        """Draw a line between two squares."""
        draw.line(SCREEN, (255, 0, 0), start, end)
