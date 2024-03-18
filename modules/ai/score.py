from ..objects.square import CATCH_MODE, FLEE_MODE
from ..settings import TILE_SIZE
from ..world.grid_builder import WORLD_HEIGHT, WORLD_WIDTH


class Score:
    def __init__(self, x, y, score):
        self.score = score
        super().__init__(x, y)
        prev_x = self.x
        prev_y = self.y

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
                self.score += 500
            else:
                self.score -= 20

        elif mode == FLEE_MODE:
            if collide:
                self.score -= 500
            else:
                self.score += 20
        # Pozycja
        beyond_left_edge = self.x <= TILE_SIZE
        beyond_right_edge = self.x >= WORLD_WIDTH - TILE_SIZE
        beyond_top_edge = self.y <= TILE_SIZE
        beyont_floor = self.y >= WORLD_HEIGHT - TILE_SIZE
        if beyond_left_edge or beyond_right_edge or beyond_top_edge or beyont_floor:
            self.score -= 1000

        # Ruch
        if self.prev_x == self.x:
            self.score -= 50

        # Aktualizacja pozycji
        self.prev_x = self.x
        self.prev_y = self.y
