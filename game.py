from enum import Enum

import pygame

import menu
import running

# Stałe wartości
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 300  # Liczba klatek na sekundę


class GameState(Enum):
    """Enum reprezentujący różne stany gry."""

    MAIN_MENU = 0
    RUNNING = 1
    PAUSE = 2
    QUIT = 3


def handle_events(game_state):
    """
    Obsługuje zdarzenia pygame, takie jak naciśnięcie klawisza lub zamknięcie okna.
    Zwraca nowy stan gry na podstawie zdarzeń.
    """
    for event in pygame.event.get():  # Pętla po wszystkich zdarzeniach
        if event.type == pygame.QUIT:  # Obsługa zamknięcia okna
            return GameState.QUIT
        elif (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):  # Obsługa naciśnięcia klawisza "Escape"
            if game_state == GameState.RUNNING:  # Włączenie pauzy
                return GameState.PAUSE
            elif game_state == GameState.PAUSE:  # Wyłączenie pauzy
                return GameState.RUNNING
            elif game_state == GameState.MAIN_MENU:  # Wyjście z gry
                return GameState.QUIT
    return game_state


def launch():
    """
    Główna funkcja gry. Inicjalizuje pygame, tworzy okno gry,
    a następnie uruchamia główną pętlę gry.
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    game_state = GameState.MAIN_MENU
    clock = pygame.time.Clock()  # Obiekt do kontrolowania czasu

    # Główna pętla gry
    while game_state != GameState.QUIT:
        clock.tick(FPS)  # Ograniczenie liczby klatek na sekundę
        game_state = handle_events(game_state)  # Obsługa zdarzeń

        # Obsługa różnych stanów gry
        if game_state == GameState.MAIN_MENU:  # Obsługa menu głównego
            menu.handle_main_menu()
        elif game_state == GameState.RUNNING:  # Obsługa stanu gry "running"
            running.handle_running()
        elif game_state == GameState.PAUSE:  # Obsługa menu pauzy
            menu.handle_pause_menu()

    pygame.quit()  # Zamknięcie pygame po zakończeniu gry
