import pygame

from modules.ai.agent import DeepLearningAgent
from modules.objects.menu_button import Button
from modules.settings import SCREEN, SCREEN_HEIGHT, SCREEN_WIDTH
from modules.states.state import GameState

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_Y_START = 300
BUTTON_Y_GAP = 60


class MainMenuState(GameState):
    """Main menu state of the game."""

    def __init__(self):
        self.start_button = Button.create(0, "New Game", GameState.START_GAME)
        self.quit_button = Button.create(1, "Quit", GameState.QUIT)
        self.logo = pygame.image.load("assets/logo.png")

    def handle_events(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            action = self.start_button.update()
            if action is not None:
                return action
            action = self.quit_button.update()
            if action is not None:
                pygame.quit()
                quit()

    def update(self):
        """Update the state of the start and quit buttons."""
        self.start_button.update()
        self.quit_button.update()

    def draw(self):
        """Draw menu on the screen."""
        self.start_button.draw()
        self.quit_button.draw()
        display_logo(self.logo)


class PauseMenuState:
    def __init__(self):
        """Pause menu state of the game."""
        self.resume_button = Button.create(0, "Resume", GameState.RESUME_GAME)
        self.replay_button = Button.create(1, "Replay", GameState.RESET)
        self.quit_button = Button.create(2, "Quit", GameState.QUIT)
        self.logo = pygame.image.load("assets/logo.png")
        self.pause_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.pause_surface.fill((0, 60, 0, 255))

    def handle_events(self, event):
        """Handle events for the pause menu."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            action = self.resume_button.update()
            if action is not None:
                return action
            action = self.replay_button.update()
            if action is not None:
                DeepLearningAgent().save_model()
                return GameState.RESET
            action = self.quit_button.update()
            if action is not None:
                DeepLearningAgent().save_model()
                pygame.quit()
                quit()

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
        SCREEN.blit(self.pause_surface, (0, 0))
        display_logo(self.logo)
        self.resume_button.draw()
        self.replay_button.draw()
        self.quit_button.draw()

    def set_running_game_state(self, running_game_state):
        """Set the game state."""
        self.running_game_state = running_game_state
        self.resume_button.action = running_game_state


def display_logo(logo):
    """Display the game logo."""
    x = (SCREEN.get_width() - logo.get_width()) // 2
    y = 5
    SCREEN.blit(logo, (x, y))


def main_menu(game_state, logo, start_button, quit_button):
    """Handle the main menu of the game."""
    main_menu_state = MainMenuState(start_button, quit_button)

    SCREEN.fill((0, 0, 0))

    main_menu_state.update()
    display_logo(logo)
    main_menu_state.draw()
    pygame.display.flip()

    return game_state


def pause_menu(game_state, logo, resume_button, quit_button):
    """Handle the pause menu of the game."""
    pause_surface = pygame.Surface(SCREEN.get_size(), pygame.SRCALPHA)
    pause_surface.fill((0, 255, 0, 128))

    pause_menu_state = PauseMenuState(resume_button, quit_button)

    display_logo(logo)

    action = pause_menu_state.update()
    if action is not None:
        return action

    pause_menu_state.draw()
    SCREEN.blit(pause_surface, (0, 0))
    pygame.display.flip()

    return game_state
