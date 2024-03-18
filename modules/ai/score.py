from ..objects.square import CATCH_MODE, FLEE_MODE


class Score:
    def __init__(self, score):
        self.score = score

    def update(self, mode, collide, move_left, move_right, jump):
        if move_left or move_right:
            self.score += 2
        if jump:
            self.score += 1
        else:
            self.score -= 1

        if mode == CATCH_MODE:
            if collide:
                self.score += 50
            else:
                self.score -= 0

        elif mode == FLEE_MODE:
            if collide:
                self.score -= 50
            else:
                self.score += 1
