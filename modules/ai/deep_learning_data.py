import numpy as np

from modules.ai.vectors import VectorCalculator


class DeepLearningData:
    def __init__(self, squares):
        self.squares = squares
        self.vector_calculator = VectorCalculator(self.squares)

    def get_state(self):
        positions_x = [square.x for square in self.squares]
        positions_y = [square.y for square in self.squares]
        velocity_x = [square.velocity_x for square in self.squares]
        velocity_y = [square.velocity_y for square in self.squares]
        collisions = [square.collide for square in self.squares]
        modes = [square.mode for square in self.squares]
        # vectors = self.vector_calculator.calculate_vectors()

        # Przekształć listy na numpy arrays
        positions_x = np.array(positions_x)
        positions_y = np.array(positions_y)
        velocity_x = np.array(velocity_x)
        velocity_y = np.array(velocity_y)
        collisions = np.array(collisions)
        modes = np.array(modes)
        # vectors = np.array(vectors)

        # Połącz wszystkie arrays w jeden tensor
        # state = np.concatenate((positions_x, positions_y, velocity_x, velocity_y, collisions, vectors, modes), axis=0)
        state = np.concatenate((positions_x, positions_y, velocity_x, velocity_y, collisions, modes), axis=0)

        return state
