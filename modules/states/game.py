import os
import sys
import traceback

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

from ..settings import FPS_LIMIT, SCREEN, SCREEN_HEIGHT, SCREEN_WIDTH, WINDOW_TITLE
from ..states.menu import MainMenuState, PauseMenuState
from ..states.state import GameState
from .play import RunningGameState


class Game:

    def __init__(self):
        """
        Inicjalizuje grę, ustawiając stan gry na MENU GŁÓWNE, tworząc ekran o określonych wymiarach.
        """
        self.screen = SCREEN
        pygame.display.set_caption(WINDOW_TITLE)

        # Inicjalizacja stanów
        self.running_game_state = RunningGameState(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.main_menu_state = MainMenuState(self.screen, self.running_game_state)
        self.pause_menu_state = PauseMenuState(self.screen, self.running_game_state)

        # Ustawienie stanu pauzy dla stanu gry
        self.running_game_state.set_pause_state(self.pause_menu_state)

        # Ustawienie początkowego stanu
        self.current_state = self.main_menu_state

    def run(self):
        """
        Uruchamia główną pętlę gry, która trwa, dopóki stan gry nie jest równy QUIT.
        W każdej iteracji pętli, zdarzenia są obsługiwane, stan gry jest aktualizowany, a następnie rysowany na ekranie.
        """
        clock = pygame.time.Clock()
        while self.current_state:
            events = pygame.event.get()
            new_state = self.current_state.handle_events(events)
            if new_state is GameState.RESET:  # Jeśli zwrócona wartość to GameState.RESET, resetuj stan gry
                self.running_game_state = RunningGameState(SCREEN_WIDTH, SCREEN_HEIGHT)
                self.running_game_state.set_pause_state(self.pause_menu_state)
                self.pause_menu_state.set_running_game_state(
                    self.running_game_state
                )  # Aktualizuj stan pauzy o nowym stanie gry
                self.current_state = self.running_game_state
            elif new_state is not None:
                self.current_state = new_state
            self.current_state.update()
            self.current_state.draw(self.screen)
            pygame.display.flip()
            clock.tick(FPS_LIMIT)


def launch():
    """
    Inicjalizuje pygame, tworzy instancję klasy Game, uruchamia grę, a następnie kończy działanie pygame.
    """
    pygame.init()
    game = Game()
    game.run()
