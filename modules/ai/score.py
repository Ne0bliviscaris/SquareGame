from ..objects.square import CATCH_MODE, FLEE_MODE
from ..settings import TILE_SIZE
from ..world.grid_builder import WORLD_HEIGHT, WORLD_WIDTH


class Score:
    def __init__(self, x, y, score):
        self.score = score
        super().__init__(x, y)
        self.previous_x = self.x
        self.previous_y = self.y

    def update(self, mode, collide, move_left, move_right, jump):
        # Ruch
        if move_left or move_right:
            self.score += 2
        if jump:
            self.score += 1
        else:
            self.score -= 1
        # Kolizje
        if mode == CATCH_MODE:
            if collide:
                self.score += 3
            else:
                self.score -= 1

        elif mode == FLEE_MODE:
            if collide:
                self.score -= 3
            else:
                self.score += 1
        # Pozycja
        on_left_edge = self.x <= TILE_SIZE + 1
        on_right_edge = self.x >= WORLD_WIDTH - TILE_SIZE - 1
        on_top_edge = self.y <= TILE_SIZE + 1
        below_floor = self.y >= WORLD_HEIGHT - TILE_SIZE + 1
        if on_left_edge or on_right_edge or on_top_edge or below_floor:
            self.score -= 10

        # Ruch
        if self.previous_x == self.x:
            self.score -= 3

        # Aktualizacja pozycji
        self.previous_x = self.x
        self.previous_y = self.y
