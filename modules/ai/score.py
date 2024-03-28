from modules.settings import CATCH_MODE, FLEE_MODE, TILE_SIZE
from modules.world.grid_builder import WORLD_HEIGHT, WORLD_WIDTH


class Score:
    def __init__(self, score):
        self.score = score
        self.previous_x = None
        self.previous_y = None

    def update(self, x, y, mode, collide, move_left, move_right, jump):
        self.x = x
        self.y = y
        moved = self.x != self.previous_x
        # Ruch
        if move_left or move_right:
            self.score += 2000
        if jump:
            self.score -= 100
        # Kolizje
        if mode == CATCH_MODE:
            if collide:
                self.score += 100
            else:
                self.score -= 0

        elif mode == FLEE_MODE:
            if collide:
                self.score -= 20
            else:
                self.score += 0
        # Pozycja
        on_left_edge = self.x <= TILE_SIZE + 1
        on_right_edge = self.x >= WORLD_WIDTH - TILE_SIZE - 1
        on_top_edge = self.y <= TILE_SIZE + 1
        below_floor = self.y >= WORLD_HEIGHT - TILE_SIZE + 1
        if on_left_edge or on_right_edge or on_top_edge or below_floor:
            self.score -= 10

        # Ruch
        if self.previous_x == self.x:
            self.score -= 5

        # Aktualizacja pozycji
        self.previous_x = self.x
        self.previous_y = self.y
