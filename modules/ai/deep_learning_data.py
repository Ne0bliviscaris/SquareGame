import numpy as np

from modules.ai.vectors import VectorCalculator

PARAMETERS_LENGTH = 8


class DeepLearningData:
    def __init__(self, squares):
        self.squares = squares
        self.vector_calculator = VectorCalculator(self.squares)

    def parameters(self):
        positions_x = [square.x for square in self.squares]
        positions_y = [square.y for square in self.squares]
        velocity_x = [square.velocity_x for square in self.squares]
        velocity_y = [square.velocity_y for square in self.squares]
        collisions = [square.collide for square in self.squares]
        modes = [square.mode for square in self.squares]
        scores = [square.score for square in self.squares]
        speeds = [square.speed for square in self.squares]

        parameters = [positions_x, positions_y, velocity_x, velocity_y, collisions, modes, scores, speeds]
        return parameters

    def get_state(self):

        # vectors = self.vector_calculator.calculate_vectors()
        parameters = self.parameters()
        parameters = [np.array(param) for param in parameters]
        state = np.concatenate(parameters, axis=0)

        return state
