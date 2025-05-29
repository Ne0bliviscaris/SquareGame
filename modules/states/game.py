import os
import sys

# For quick start
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))


os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

from modules.settings import FPS_LIMIT, WINDOW_TITLE
from modules.states.menu import MainMenuState, PauseMenuState
from modules.states.play import Play
from modules.states.state import GameState


class Game:

    def __init__(self):
        """Initialize the game, set up the display, and initialize game states."""
        pygame.display.set_caption(WINDOW_TITLE)

        self.active_game = Play()
        self.main_menu_state = MainMenuState(self.active_game)
        self.pause_menu_state = PauseMenuState(self.active_game)

        self.active_game.controller.set_pause_state(self.pause_menu_state)

        self.current_state = self.main_menu_state

    def run(self):
        """Main game loop that handles events, updates the current state, and draws to the screen."""
        clock = pygame.time.Clock()
        while self.current_state:
            self.event_handler()
            self.current_state.update()
            self.current_state.draw()
            pygame.display.flip()
            clock.tick(FPS_LIMIT)

    def event_handler(self):
        events = pygame.event.get()
        for event in events:
            if self.global_event(event):
                continue
            new_state = self.current_state.handle_events(event)
            if new_state is GameState.RESET:
                self.reset_game()
            elif new_state:
                self.current_state = new_state

    def global_event(self, event):
        """Handle global events that are not specific to the current state."""
        esc_key_pressed = event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        if esc_key_pressed:
            self.handle_esc_button()
            return True
        elif event.type == pygame.QUIT:
            self.quit_game()
            return True
        return False

    def reset_game(self):
        """Start a new game."""
        self.active_game = Play()
        self.active_game.controller.set_pause_state(self.pause_menu_state)
        self.pause_menu_state.set_running_game_state(self.active_game)
        self.current_state = self.active_game

    def handle_esc_button(self):
        if self.current_state == self.active_game:
            self.current_state = self.pause_menu_state
        elif self.current_state == self.pause_menu_state:
            self.current_state = self.active_game
        elif self.current_state == self.main_menu_state:
            self.quit_game()

    def quit_game(self):
        """Quit the game."""
        pygame.quit()
        quit()


def launch():
    """Launch the game by initializing Pygame and starting the game loop."""
    pygame.init()
    game = Game()
    game.run()


if __name__ == "__main__":

    launch()
