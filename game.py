import pygame

import menu
import play
from menu import GameState

# Stałe wartości
SCREEN_WIDTH = 900  # Szerokość ekranu
SCREEN_HEIGHT = 600  # Wysokość ekranu
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Utworzenie ekranu o określonych wymiarach
INITIAL_STATE = GameState.MAIN_MENU  # Początkowy stan gry
ESC_BUTTON = pygame.K_ESCAPE  # Przycisk ESC
WINDOW_TITLE = "Squaregame"  # Tytuł okna
FPS_CAP = 60  # Maksymalna liczba klatek na sekundę


class Game:

    def __init__(self):
        """
        Inicjalizuje grę, ustawiając stan gry na MENU GŁÓWNE, tworząc ekran o określonych wymiarach.
        """
        self.state = INITIAL_STATE  # Początkowy stan gry
        self.screen = SCREEN  # Utworzenie ekranu o określonych wymiarach
        self.caption = pygame.display.set_caption(WINDOW_TITLE)  # Nadanie tytułu okna

    def get_events(self):
        """
        Pobiera zdarzenia z kolejki pygame.
        """
        return pygame.event.get()

    def handle_events(self):
        """
        Obsługuje zdarzenia pygame, takie jak naciśnięcie klawisza lub zamknięcie okna.
        Zwraca nowy stan gry na podstawie zdarzeń.
        """
        QUIT_EVENT = pygame.QUIT
        KEYDOWN_EVENT = pygame.KEYDOWN

        # Mapowanie zdarzeń na akcje
        event_actions = {
            QUIT_EVENT: GameState.QUIT,  # Zamknięcie okna powoduje zakończenie gry
            KEYDOWN_EVENT: {  # Naciśnięcie klawisza
                ESC_BUTTON: {  # Naciśnięcie klawisza Escape
                    GameState.RUNNING: GameState.PAUSE,  # Pauza, jeśli gra jest w trakcie
                    GameState.PAUSE: GameState.RUNNING,  # Wznów grę, jeśli gra jest w pauzie
                    GameState.MAIN_MENU: GameState.QUIT,  # Wyjdź z gry, jeśli jesteś w menu głównym
                },
            },
        }

        events = self.get_events()  # Pobranie zdarzeń z kolejki pygame
        # Przetwarzanie zdarzeń w kolejce
        for event in events:
            if event.type in event_actions:  # Sprawdzenie, czy zdarzenie jest obsługiwane
                action = event_actions[event.type]  # Pobranie akcji dla danego zdarzenia
                if isinstance(action, dict):  # Sprawdzenie, czy akcja jest słownikiem
                    if (
                        event.type == KEYDOWN_EVENT and event.key in action
                    ):  # Sprawdzenie, czy klawisz jest obsługiwany
                        # Zwrócenie nowego stanu gry lub aktualnego, jeśli nie ma zdefiniowanej akcji dla aktualnego stanu
                        return action[event.key].get(self.state, self.state)
                    else:
                        # Jeśli dla danego klawisza nie ma zdefiniowanej akcji dla aktualnego stanu, zwróć aktualny stan
                        self.state = self.state
                else:
                    self.state = action
        return self.state  # Zwrócenie aktualnego stanu, jeśli nie ma zdarzeń do obsługi

    def run(self):
        """
        Uruchamia główną pętlę gry, która trwa, dopóki stan gry nie jest równy QUIT.
        W każdej iteracji pętli, zdarzenia są obsługiwane, a stan gry jest aktualizowany.
        """
        clock = pygame.time.Clock()  # Utworzenie zegara do kontrolowania liczby klatek na sekundę
        while self.state != GameState.QUIT:
            self.state = self.handle_events()  # Obsługa zdarzeń i aktualizacja stanu gry
            if self.state == GameState.MAIN_MENU:
                self.main_menu()  # Wyświetlanie menu głównego
            elif self.state == GameState.RUNNING:
                self.game_running()  # Uruchomienie gry
            elif self.state == GameState.PAUSE:
                self.pause_menu()  # Wyświetlanie menu pauzy
            pygame.display.flip()  # Aktualizacja wyświetlania
            clock.tick(FPS_CAP)  # Limit FPS do 60

    def main_menu(self):
        """
        Wywołuje funkcję wyświetlającą menu główne gry.
        """
        self.state = menu.main_menu(self.screen, self.state)

    def game_running(self):
        """
        Wywołuje funkcję uruchamiającą grę.
        """
        play.game_running(self.screen)

    def pause_menu(self):
        """
        Wywołuje funkcję wyświetlającą menu pauzy gry.
        """
        menu.pause_menu(self.screen, self.state)


def launch():
    """
    Inicjalizuje pygame, tworzy instancję klasy Game, uruchamia grę, a następnie kończy działanie pygame.
    """
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()
