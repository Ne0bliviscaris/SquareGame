import pygame


class Controller:
    """Obsługa sterowania w grze."""

    def __init__(self, squares, game_state, camera, agent):
        """Inicjalizuje kontroler z danymi kwadratami."""
        self.squares = squares
        self.game_state = game_state
        self.camera = camera
        self.agent = agent

    def handle_movement(self):
        """Obsługuje zdarzenia związane z ciągłym naciśnięciem klawisza."""
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
        """Obsługuje zdarzenia związane z puszczeniem klawisza."""
        if event.key in (pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT):
            self.squares.velocity_x = 0  # Zresetuj prędkość x kwadratu

    def handle_key_press_actions(self, event):
        """Obsługuje zdarzenia związane z naciśnięciem klawisza."""
        if event.key == pygame.K_ESCAPE:
            return self.game_state.pause_menu_state
        elif event.key == pygame.K_SPACE:
            self.squares.jump()

    def handle_quit_event(self, event):
        """Obsługuje zdarzenie wyjścia z gry."""
        self.agent.save_model()
        pygame.quit()
        quit()

    def set_pause_state(self, pause_state):
        """Ustawia stan pauzy dla stanu gry."""
        self.pause_state = pause_state
