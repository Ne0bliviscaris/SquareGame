import sys

import pygame

from modules.objects.button import Button
from modules.state import GameState

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_Y_START = 300  # Możesz zmienić tę wartość na tę, którą chcesz
BUTTON_Y_GAP = 60  # Możesz zmienić tę wartość na tę, którą chcesz


class MainMenuState(GameState):
    """
    Stan gry reprezentujący menu główne.
    """

    def __init__(self, screen, running_game_state):
        self.screen = screen
        self.running_game_state = running_game_state
        self.start_button = Button.create_from_screen_size(self.screen, 0, "New Game", running_game_state)
        self.quit_button = Button.create_from_screen_size(self.screen, 1, "Quit", GameState.QUIT)
        self.logo = pygame.image.load("assets/logo.png")  # Załaduj obraz logo na początku gry

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                action = self.start_button.update()
                if action is not None:
                    return action
                action = self.quit_button.update()
                if action is not None:
                    pygame.quit()
                    sys.exit()

    def update(self):
        """
        Aktualizuje stan przycisków start i quit.
        """
        self.start_button.update()
        self.quit_button.update()

    def draw(self, screen):
        """
        Rysuje przyciski start i quit na ekranie, a następnie wyświetla logo.
        """
        self.start_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        display_logo(self.screen, self.logo)


class PauseMenuState:
    def __init__(self, screen, running_game_state):
        """
        Inicjalizuje stan menu pauzy.
        """
        self.screen = screen
        self.resume_button = Button.create_from_screen_size(self.screen, 0, "Resume", running_game_state)
        self.replay_button = Button.create_from_screen_size(self.screen, 1, "Replay", running_game_state)
        self.quit_button = Button.create_from_screen_size(self.screen, 2, "Quit", GameState.QUIT)
        self.running_game_state = running_game_state
        self.logo = pygame.image.load("assets/logo.png")  # Załaduj obraz logo na początku gry
        self.pause_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.pause_surface.fill((0, 60, 0, 255))  # Półprzezroczyste zielone tło

    def handle_events(self, events, screen=None):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return self.running_game_state  # Zwróć running_game_state zamiast main_menu_state
            elif event.type == pygame.MOUSEBUTTONDOWN:
                action = self.resume_button.update()
                if action is not None:
                    return action
                action = self.replay_button.update()
                if action is not None:
                    if action is not None:
                        return GameState.RESET  # Zwróć GameState.RESET zamiast resetować stan gry bezpośrednio
                action = self.quit_button.update()
                if action is not None:
                    pygame.quit()
                    sys.exit()
        return self

    def update(self):
        """
        Aktualizuje stan przycisków resume i quit.
        """
        resume_action = self.resume_button.update()
        if resume_action is not None:
            return resume_action

        quit_action = self.quit_button.update()
        if quit_action is not None:
            return quit_action

    def draw(self, screen=None):
        """
        Rysuje przyciski resume i quit na ekranie.
        """
        self.screen.blit(self.pause_surface, (0, 0))  # Rysuj półprzezroczyste tło
        display_logo(self.screen, self.logo)  # Wyświetl logo
        self.resume_button.draw(self.screen)
        self.replay_button.draw(self.screen)
        self.quit_button.draw(self.screen)

    def set_running_game_state(self, running_game_state):
        """
        Ustawia stan gry.
        """
        self.running_game_state = running_game_state
        self.resume_button.action = running_game_state


def display_logo(screen, logo):
    """
    Wyświetla logo gry.
    """

    # Oblicz pozycję, na której logo powinno być wyświetlone
    x = (screen.get_width() - logo.get_width()) // 2
    y = 5

    # Wyświetl logo
    screen.blit(logo, (x, y))


def main_menu(screen, game_state, logo, start_button, quit_button):
    """
    Funkcja obsługująca menu główne gry.
    """
    main_menu_state = MainMenuState(screen, start_button, quit_button)

    screen.fill((0, 0, 0))  # Wypełnij ekran kolorem

    # Aktualizacja stanu menu głównego
    main_menu_state.update()

    display_logo(screen, logo)  # Wyświetl logo

    # Rysowanie stanu menu głównego
    main_menu_state.draw()

    # Wyświetl zmiany na ekranie
    pygame.display.flip()

    return game_state


def pause_menu(screen, game_state, logo, resume_button, quit_button):
    """
    Funkcja obsługująca menu pauzy gry.
    """
    # Utwórz przezroczystą powierzchnię dla menu pauzy
    pause_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    pause_surface.fill((0, 255, 0, 128))  # Półprzezroczysty zielony

    pause_menu_state = PauseMenuState(screen, resume_button, quit_button)

    display_logo(screen, logo)  # Wyświetl logo

    # Aktualizacja i rysowanie stanu menu pauzy
    action = pause_menu_state.update()
    if action is not None:
        return action

    pause_menu_state.draw()
    # Rysuj powierzchnię menu pauzy na ekranie gry
    screen.blit(pause_surface, (0, 0))

    # Wyświetl zmiany na ekranie
    pygame.display.flip()

    return game_state
