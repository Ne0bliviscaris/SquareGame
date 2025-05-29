import pygame


class Controller:
    """Handles game controls."""

    def __init__(self, squares, game_state, camera):
        """Initialize controller with given squares."""
        self.squares = squares
        self.game_state = game_state
        self.camera = camera

    def handle_movement(self):
        """Handle events related to continuous key press."""
        keys = pygame.key.get_pressed()

        key_handlers = {
            pygame.K_a: self.squares.move_left,
            pygame.K_LEFT: self.squares.move_left,
            pygame.K_d: self.squares.move_right,
            pygame.K_RIGHT: self.squares.move_right,
        }

        for key, handler in key_handlers.items():
            if keys[key]:
                handler()

    def handle_key_release(self, event):
        """Handle events related to key release."""
        if event.key in (pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT):
            self.squares.velocity_x = 0

    def handle_key_press_actions(self, event):
        """Handle events related to key press."""
        if event.key == pygame.K_ESCAPE:
            return self.game_state.pause_menu_state
        elif event.key == pygame.K_SPACE:
            self.squares.jump()

    def handle_quit_event(self):
        """Handle game quit event."""
        pygame.quit()
        quit()

    def set_pause_state(self, pause_state):
        """Set pause state for game state."""
        self.pause_state = pause_state
