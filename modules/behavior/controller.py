import pygame


class PlayerControls:
    """Handles game controls."""

    def __init__(self, player_square, game_state):
        """Initialize controller with given squares."""
        self.player_square = player_square
        self.game_state = game_state

    def player_movement(self):
        """Handle events related to continuous key press."""
        keys = pygame.key.get_pressed()

        key_mapping = {
            pygame.K_a: self.player_square.move_left,
            pygame.K_LEFT: self.player_square.move_left,
            pygame.K_d: self.player_square.move_right,
            pygame.K_RIGHT: self.player_square.move_right,
        }

        for key, action in key_mapping.items():
            if keys[key]:
                action()

    def release_movement_key(self, event):
        """Handle events related to key release."""
        if event.key in (pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT):
            self.player_square.velocity_x = 0

    def key_press_actions(self, event):
        """Handle events related to key press."""
        if event.key == pygame.K_ESCAPE:
            return self.game_state.pause_menu_state
        elif event.key == pygame.K_SPACE:
            self.player_square.jump()

    def set_pause_state(self, pause_state):
        """Set pause state for game state."""
        self.pause_state = pause_state
