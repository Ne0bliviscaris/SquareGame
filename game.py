import os
import sys
import traceback

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

from menu import MainMenuState, PauseMenuState, main_menu, pause_menu
from play import RunningGameState, game_running

# Stałe wartości
SCREEN_WIDTH = 1000  # Szerokość ekranu
SCREEN_HEIGHT = 600  # Wysokość ekranu
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Utworzenie ekranu o określonych wymiarach
WINDOW_TITLE = "Squaregame"  # Tytuł okna
FPS_CAP = 200  # Maksymalna liczba klatek na sekundę


class Game:

    def __init__(self):
        """
        Inicjalizuje grę, ustawiając stan gry na MENU GŁÓWNE, tworząc ekran o określonych wymiarach.
        """
        self.screen = SCREEN
        pygame.display.set_caption(WINDOW_TITLE)

        # Inicjalizacja stanów
        self.running_game_state = RunningGameState(SCREEN_HEIGHT, SCREEN_WIDTH)
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
            if new_state is not None:
                self.current_state = new_state
            self.current_state.update()
            self.current_state.draw(self.screen)
            pygame.display.flip()
            clock.tick(FPS_CAP)


def launch():
    """
    Inicjalizuje pygame, tworzy instancję klasy Game, uruchamia grę, a następnie kończy działanie pygame.
    """
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()


try:
    launch()
except SystemExit:
    pass
except Exception:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    formatted_traceback = traceback.format_exception(exc_type, exc_value, exc_traceback)
    print("".join(formatted_traceback[2:]))  # Drukuj traceback, pomijając pierwsze dwa wiersze
