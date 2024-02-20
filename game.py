import pygame

import menu
import play
from menu import GameState

# Stałe wartości
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 300  # Liczba klatek na sekundę
ESC_BUTTON = pygame.K_ESCAPE  # Przycisk ESC


def handle_events(game_state):
    """
    Obsługuje zdarzenia pygame, takie jak naciśnięcie klawisza lub zamknięcie okna.
    Zwraca nowy stan gry na podstawie zdarzeń.
    """

    event_actions = {
        pygame.QUIT: GameState.QUIT,  # Zamknięcie okna jeśli GameState == QUIT
        pygame.KEYDOWN: {  # Przycisk Escape
            ESC_BUTTON: {  # Przycisk Escape
                GameState.RUNNING: GameState.PAUSE,  # Pauza jeśli gra jest w trakcie
                GameState.PAUSE: GameState.RUNNING,  # Wznów grę jeśli gra jest w pauzie
                GameState.MAIN_MENU: GameState.QUIT,  # Wyjdź z gry jeśli jesteś w menu głównym
            },
        },
    }
    for event in pygame.event.get():  # Pobranie wszystkich zdarzeń z kolejki
        if event.type in event_actions:  # Sprawdzenie czy zdarzenie jest obsługiwane
            action = event_actions[event.type]  # Pobranie akcji dla danego zdarzenia
            if isinstance(action, dict):  # Sprawdzenie czy akcja jest słownikiem
                if event.type == pygame.KEYDOWN and event.key in action:  # Sprawdzenie czy klawisz jest obsługiwany
                    return action[event.key].get(
                        game_state,
                        game_state,
                    )  # Zwrócenie nowego stanu gry
                return action.get(
                    game_state,
                    game_state,
                )  # Zwrócenie nowego stanu gry
            else:
                return action
    return game_state


def launch():
    """
    Główna funkcja gry. Inicjalizuje pygame, tworzy okno gry,
    a następnie uruchamia główną pętlę gry.
    """
    pygame.init()  # Inicjalizacja pygame
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Utworzenie okna

    game_state = GameState.MAIN_MENU  # Początkowy stan gry
    clock = pygame.time.Clock()  # Obiekt do kontrolowania czasu

    # Główna pętla gry
    while game_state != GameState.QUIT:
        clock.tick(FPS)  # Ograniczenie liczby klatek na sekundę
        game_state = handle_events(game_state)  # Obsługa zdarzeń

        # Obsługa różnych stanów gry
        if game_state == GameState.MAIN_MENU:  # Obsługa menu głównego
            game_state = menu.main_menu(screen, game_state)
        elif game_state == GameState.RUNNING:  # Obsługa stanu gry "running"
            play.game_running(screen)
        elif game_state == GameState.PAUSE:  # Obsługa menu pauzy
            menu.pause_menu(screen, game_state)

    pygame.quit()  # Zamknięcie pygame po zakończeniu gry
