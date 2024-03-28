import sys

import pygame

from modules.objects.button import Button
from modules.states.state import GameState

from ..settings import SCREEN, SCREEN_HEIGHT, SCREEN_WIDTH

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_Y_START = 300  # Możesz zmienić tę wartość na tę, którą chcesz
BUTTON_Y_GAP = 60  # Możesz zmienić tę wartość na tę, którą chcesz


class MainMenuState(GameState):
    """
    Stan gry reprezentujący menu główne.
    """

    def __init__(self, running_game_state):
        self.running_game_state = running_game_state
        self.start_button = Button.create_from_screen_size(0, "New Game", running_game_state)
        self.quit_button = Button.create_from_screen_size(1, "Quit", GameState.QUIT)
        self.logo = pygame.image.load("assets/logo.png")  # Załaduj obraz logo na początku gry

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                action = self.start_button.update()
                if action is not None:
                    return action
                action = self.quit_button.update()
                if action is not None:
                    pygame.quit()
                    quit()

    def update(self):
        """
        Aktualizuje stan przycisków start i quit.
        """
        self.start_button.update()
        self.quit_button.update()

    def draw(self):
        """
        Rysuje przyciski start i quit na ekranie, a następnie wyświetla logo.
        """
        self.start_button.draw()
        self.quit_button.draw()
        display_logo(self.logo)


class PauseMenuState:
    def __init__(self, running_game_state):
        """
        Inicjalizuje stan menu pauzy.
        """
        self.resume_button = Button.create_from_screen_size(0, "Resume", running_game_state)
        self.replay_button = Button.create_from_screen_size(1, "Replay", running_game_state)
        self.quit_button = Button.create_from_screen_size(2, "Quit", GameState.QUIT)
        self.running_game_state = running_game_state
        self.logo = pygame.image.load("assets/logo.png")  # Załaduj obraz logo na początku gry
        self.pause_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.pause_surface.fill((0, 60, 0, 255))  # Półprzezroczyste zielone tło

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
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
                    quit()
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

    def draw(self):
        """
        Rysuje przyciski resume i quit na ekranie.
        """
        SCREEN.blit(self.pause_surface, (0, 0))  # Rysuj półprzezroczyste tło
        display_logo(self.logo)  # Wyświetl logo
        self.resume_button.draw()
        self.replay_button.draw()
        self.quit_button.draw()

    def set_running_game_state(self, running_game_state):
        """
        Ustawia stan gry.
        """
        self.running_game_state = running_game_state
        self.resume_button.action = running_game_state


def display_logo(logo):
    """
    Wyświetla logo gry.
    """

    # Oblicz pozycję, na której logo powinno być wyświetlone
    x = (SCREEN.get_width() - logo.get_width()) // 2
    y = 5

    # Wyświetl logo
    SCREEN.blit(logo, (x, y))


def main_menu(game_state, logo, start_button, quit_button):
    """
    Funkcja obsługująca menu główne gry.
    """
    main_menu_state = MainMenuState(start_button, quit_button)

    SCREEN.fill((0, 0, 0))  # Wypełnij ekran kolorem

    # Aktualizacja stanu menu głównego
    main_menu_state.update()

    display_logo(logo)  # Wyświetl logo

    # Rysowanie stanu menu głównego
    main_menu_state.draw()

    # Wyświetl zmiany na ekranie
    pygame.display.flip()

    return game_state


def pause_menu(game_state, logo, resume_button, quit_button):
    """
    Funkcja obsługująca menu pauzy gry.
    """
    # Utwórz przezroczystą powierzchnię dla menu pauzy
    pause_surface = pygame.Surface(SCREEN.get_size(), pygame.SRCALPHA)
    pause_surface.fill((0, 255, 0, 128))  # Półprzezroczysty zielony

    pause_menu_state = PauseMenuState(resume_button, quit_button)

    display_logo(logo)  # Wyświetl logo

    # Aktualizacja i rysowanie stanu menu pauzy
    action = pause_menu_state.update()
    if action is not None:
        return action

    pause_menu_state.draw()
    # Rysuj powierzchnię menu pauzy na ekranie gry
    SCREEN.blit(pause_surface, (0, 0))

    # Wyświetl zmiany na ekranie
    pygame.display.flip()

    return game_state
