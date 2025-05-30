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

    def __init__(self):
        # AI
        self.agent = DeepLearningAgent()

        self.initialize_game()
        self.initialize_player()

        self.vectors = VectorCalculator(self.squares)
        # AI
        self.deep_learning_data = DeepLearningData(self.squares)
        self.state_for_model = self.deep_learning_data.get_state()

    def initialize_player(self):
        """Initialize the player square."""
        self.player = self.squares[0]
        self.camera = Camera(self.player, self.ground_tiles)
        self.controller = PlayerControls(self.player)

    def initialize_game(self):
        """Initialize the game world with squares and tiles."""
        self.world_tiles = world_list
        self.ground_tiles = [tile for tile in self.world_tiles if isinstance(tile, Ground)]
        self.square_generator = SquareGenerator(self.ground_tiles, self.agent)
        self.squares = self.square_generator.create_squares()
        self.world_collisions = [WorldCollisions(square) for square in self.squares]
        self.square_collisions = [SquareCollisions(square) for square in self.squares]
        self.drawables = self.world_tiles + self.squares

    def update(self):
        """Update the game state. Performed every frame."""
        self.controller.player_movement()
        self.camera.update()

        self.update_squares_and_collisions()

        # AI
        self.state_for_model = self.deep_learning_data.get_state()

    def update_squares_and_collisions(self):
        """Update squares and collisions"""
        current_frame = zip(self.squares, self.world_collisions, self.square_collisions)
        for square, world_collision, square_collision in current_frame:
            if square is self.player:
                self.player.update(self.squares)
            else:
                square.update(self.squares, self.state_for_model)

            world_collision.handle_collisions_around(self.ground_tiles)
            square_collision.handle_square_collisions(self.squares)

    def draw(self):
        """Draw the game state to the screen. Performed every frame."""
        self.draw_out_of_bounds_bg()
        self.draw_all_objects()

        if DRAW_VECTORS:
            self.vectors.draw_vectors(self.camera.zoom_level, self.camera.offset_x, self.camera.offset_y)

        pygame.display.update()

    def handle_events(self, event):
        """Handle events for the game state."""
        event_handlers = {
            pygame.KEYDOWN: self.controller.key_press_actions,
            pygame.KEYUP: self.controller.release_movement_key,
            pygame.MOUSEBUTTONDOWN: self.camera.mouse_scroll_zoom,
        }

        handler = event_handlers.get(event.type)
        if handler:
            new_state = handler(event)
            if new_state is not None:
                return new_state

        self.controller.player_movement()

        return self

    def draw_all_objects(self):
        """Draw all objects considering camera offset and zoom level. Player is drawn on top."""
        for drawable in self.drawables[1:]:
            drawable.draw(self.camera.offset_x, self.camera.offset_y, self.camera.zoom_level)

        self.player.draw(self.camera.offset_x, self.camera.offset_y, self.camera.zoom_level)

    def draw_out_of_bounds_bg(self):
        SCREEN.fill((0, 38, 52))
