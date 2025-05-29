import pygame

from modules.ai.agent import DeepLearningAgent
from modules.objects.menu_button import Button
from modules.settings import SCREEN, SCREEN_HEIGHT, SCREEN_WIDTH
from modules.states.state import GameState

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_Y_START = 300
BUTTON_Y_GAP = 60


class MainMenu(GameState):
    """Main menu state of the game."""

    def __init__(self):
        self.start_button = Button.create(0, "New Game", GameState.START_GAME)
        self.quit_button = Button.create(1, "Quit", GameState.QUIT)

    def handle_events(self, event):
        """Handle events for the main menu."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.start_button.update() or self.quit_button.update()

    def update(self):
        """Update the state of the start and quit buttons."""
        self.start_button.update()
        self.quit_button.update()

    def draw(self):
        """Draw menu on the screen."""
        self.start_button.draw()
        self.quit_button.draw()
        display_logo()


class PauseMenu:
    def __init__(self):
        """Pause menu state of the game."""
        self.resume_button = Button.create(0, "Resume", GameState.RESUME_GAME)
        self.replay_button = Button.create(1, "Replay", GameState.RESET)
        self.quit_button = Button.create(2, "Quit", GameState.QUIT)

    def pause_background(self):
        pause_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pause_surface.fill((0, 60, 0, 255))
        return pause_surface

    def handle_events(self, event):
        """Handle events for the pause menu."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.resume_button.update() or self.replay_button.update() or self.quit_button.update()

    def update(self):
        """Update the state of resume and quit buttons."""
        resume_action = self.resume_button.update()
        if resume_action is not None:
            return resume_action

        quit_action = self.quit_button.update()
        if quit_action is not None:
            return quit_action

    def draw(self):
        """Draw resume and quit buttons on the screen."""
        SCREEN.blit(self.pause_background(), (0, 0))
        display_logo()
        self.resume_button.draw()
        self.replay_button.draw()
        self.quit_button.draw()

    def set_running_game_state(self, running_game_state):
        """Set the game state."""
        self.running_game_state = running_game_state
        self.resume_button.action = running_game_state


def display_logo():
    """Display the game logo."""
    logo = pygame.image.load("assets/logo.png")
    x = (SCREEN.get_width() - logo.get_width()) // 2
    y = 5
    SCREEN.blit(logo, (x, y))
