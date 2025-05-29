import pygame

from modules.ai.agent import DeepLearningAgent
from modules.ai.deep_learning_data import DeepLearningData
from modules.ai.npc import Npc
from modules.ai.vectors import VectorCalculator
from modules.behavior.camera import Camera
from modules.behavior.controller import PlayerControls
from modules.behavior.square_collisions import SquareCollisions
from modules.behavior.world_collisions import WorldCollisions
from modules.objects.sqare_generator import SquareGenerator
from modules.objects.tiles import Ground
from modules.settings import DRAW_VECTORS, SCREEN
from modules.states.state import GameState
from modules.world.grid_builder import world_list


class Play(GameState):
    """Main game state for running the game."""

    def __init__(self, game_state):
        # AI
        self.agent = DeepLearningAgent()
        self.agent.load_model()

        self.tiles = world_list
        self.ground_tiles = [tile for tile in self.tiles if isinstance(tile, Ground)]  # Najniższy rząd kafelków Ground

        self.square_generator = SquareGenerator(self.ground_tiles, self.agent)

        self.squares = self.square_generator.create_squares()

        # AI
        self.vector_calculator = VectorCalculator(self.squares)

        self.world_collisions = [WorldCollisions(square) for square in self.squares]
        self.square_collisions = [SquareCollisions(square) for square in self.squares]

        self.camera = Camera(self.squares[0], self.tiles, self.ground_tiles)

        self.player_square = self.squares[0]
        self.controller = PlayerControls(self.player_square, game_state)

        self.drawables = self.tiles + self.squares

        # AI
        self.deep_learning_data = DeepLearningData(self.squares)
        self.state_for_model = self.deep_learning_data.get_state()

    def update(self):
        """Update the game state. Performed every frame."""
        self.controller.handle_movement()
        self.camera.update_zoom()
        self.camera.update_camera()

        for square, world_collision, square_collision in zip(
            self.squares, self.world_collisions, self.square_collisions
        ):
            if isinstance(square, Npc):
                square.update(self.squares, self.state_for_model)
            else:
                square.update(self.squares)
            world_collision.handle_collisions_around(self.tiles)
            square_collision.handle_square_collisions(self.squares)

        # AI
        self.state_for_model = self.deep_learning_data.get_state()

        for square in self.squares:
            if isinstance(square, Npc):
                square.update(self.squares, self.state_for_model)

    def draw(self):
        """Draw the game state to the screen. Performed every frame."""
        SCREEN.fill((0, 38, 52))

        # Draw all objects considering camera offset and zoom level
        for drawable in self.drawables:
            if drawable is not self.squares[0]:
                drawable.draw(self.camera.camera_offset_x, self.camera.camera_offset_y, self.camera.zoom_level)

        self.squares[0].draw(self.camera.camera_offset_x, self.camera.camera_offset_y, self.camera.zoom_level)

        if DRAW_VECTORS:
            self.vector_calculator.draw_vectors(
                self.camera.zoom_level, self.camera.camera_offset_x, self.camera.camera_offset_y
            )
        pygame.display.update()

    def handle_events(self, events):
        """Handle events for the game state."""
        event_handlers = {
            pygame.QUIT: self.controller.handle_quit_event,
            pygame.KEYDOWN: self.controller.handle_key_press_actions,
            pygame.KEYUP: self.controller.handle_key_release,
            pygame.MOUSEBUTTONDOWN: self.camera.handle_scroll_zoom,
        }

        for event in events:
            handler = event_handlers.get(event.type)
            if handler:
                new_state = handler(event)
                if new_state is not None:
                    return new_state

        self.controller.handle_movement()

        return self
