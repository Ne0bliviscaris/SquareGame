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

        self.running_game_state = Play(self)
        self.main_menu_state = MainMenuState(Play(self))
        self.pause_menu_state = PauseMenuState(Play(self))

        self.running_game_state.controller.set_pause_state(self.pause_menu_state)

        self.current_state = self.main_menu_state

    def run(self):
        """Main game loop that handles events, updates the current state, and draws to the screen."""
        clock = pygame.time.Clock()
        while self.current_state:
            events = pygame.event.get()
            new_state = self.current_state.handle_events(events)
            if new_state is GameState.RESET:
                self.reset_game()
            elif new_state is not None:
                self.current_state = new_state
            self.current_state.update()
            self.current_state.draw()
            pygame.display.flip()
            clock.tick(FPS_LIMIT)

    def reset_game(self):
        """Start a new game."""
        self.running_game_state = Play(self)
        self.running_game_state.controller.set_pause_state(self.pause_menu_state)
        self.pause_menu_state.set_running_game_state(self.running_game_state)
        self.current_state = self.running_game_state


def launch():
    """Launch the game by initializing Pygame and starting the game loop."""
    pygame.init()
    game = Game()
    game.run()

    # launch()


if __name__ == "__main__":
    import sys

    launch()
