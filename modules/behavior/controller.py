import pygame


class PlayerControls:
    """Handles game controls."""

    def __init__(self, player):
        """Initialize controller with given squares."""
        self.player = player

    def player_movement(self):
        """Handle events related to continuous key press."""
        keys = pygame.key.get_pressed()

        key_mapping = {
            pygame.K_a: self.player.move_left,
            pygame.K_LEFT: self.player.move_left,
            pygame.K_d: self.player.move_right,
            pygame.K_RIGHT: self.player.move_right,
        }

        for key, action in key_mapping.items():
            if keys[key]:
                action()

    def release_movement_key(self, event):
        """Handle events related to key release."""
        if event.key in (pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT):
            self.player.velocity_x = 0

    def key_press_actions(self, event):
        """Handle events related to key press."""
        if event.key == pygame.K_SPACE:
            self.player.jump()
