from enum import Enum

import pygame

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_Y_START = 300  # Możesz zmienić tę wartość na tę, którą chcesz
BUTTON_Y_GAP = 60  # Możesz zmienić tę wartość na tę, którą chcesz


def display_logo(screen, logo):
    """
    Wyświetla logo gry.
    """

    # Oblicz pozycję, na której logo powinno być wyświetlone
    x = (screen.get_width() - logo.get_width()) // 2
    y = 5

    # Wyświetl logo
    screen.blit(logo, (x, y))


class GameState(Enum):
    """Enum reprezentujący różne stany gry."""

    MAIN_MENU = 0
    RUNNING = 1
    PAUSE = 2
    QUIT = 3


class Button:

    def __init__(
        self,
        x,
        y,
        text,
        action,
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        font_size=36,
        text_color=(255, 255, 255),
        button_color=(0, 0, 0),
        hover_color=(100, 100, 100),
        border_width=2,
    ):
        """
        Inicjalizacja przycisku.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.Font(None, font_size)
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.border_width = border_width
        self.text_surface = self.font.render(self.text, True, self.text_color)  # Przygotuj powierzchnię tekstu

    @staticmethod
    def create_from_screen_size(screen, y_offset, text, action):
        """
        Tworzy przycisk z określonymi stałymi wartościami.
        """
        screen_width, _ = screen.get_size()
        button_x = (screen_width - BUTTON_WIDTH) / 2
        return Button(button_x, BUTTON_Y_START + y_offset * BUTTON_Y_GAP, text, action)

    def draw(self, screen):
        """
        Rysuje przycisk na ekranie.
        """
        # Zmień kolor przycisku, gdy kursor myszy jest nad nim
        if self.is_hovered():
            color = self.hover_color
        else:
            color = self.button_color

        # Rysuj przycisk
        pygame.draw.rect(screen, color, self.rect)

        # Rysuj ramkę przycisku
        pygame.draw.rect(screen, self.text_color, self.rect, self.border_width)

        # Rysuj tekst na przycisku
        screen.blit(
            self.text_surface,
            (
                self.rect.x + (self.rect.width - self.text_surface.get_width()) // 2,
                self.rect.y + (self.rect.height - self.text_surface.get_height()) // 2,
            ),
        )

    def is_hovered(self):
        """
        Sprawdza, czy kursor myszy jest nad przyciskiem.
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    def is_mouse_down(self):
        """
        Sprawdza, czy przycisk został naciśnięty.
        """
        if self.is_hovered() and pygame.mouse.get_pressed()[0]:  # Sprawdź hover i kliknięcie myszy
            return True
        return False

    def handle_event(self):
        """
        Obsługuje zdarzenia dla przycisku.
        """
        if self.is_mouse_down():
            return self.action
        return None

    def update(self):
        """
        Aktualizuje stan przycisku i wywołuje obsługę zdarzenia.
        """
        action = self.handle_event()
        if action is not None:
            return action


def main_menu(screen, game_state, logo, start_button, quit_button):
    """
    Funkcja obsługująca menu główne gry.
    """

    screen.fill((0, 0, 0))  # Wypełnij ekran kolorem
    display_logo(screen, logo)  # Wyświetl logo
    # Rysuj przyciski
    start_button.draw(screen)  # Przycisk start
    quit_button.draw(screen)  # Przycisk quit

    # Aktualizacja przycisków
    start_action = start_button.update()
    if start_action is not None:
        return start_action

    quit_action = quit_button.update()
    if quit_action is not None:
        return quit_action

    # Wyświetl zmiany na ekranie
    pygame.display.flip()

    return game_state


def pause_menu(screen, game_state, logo, resume_button, quit_button):
    # Utwórz przezroczystą powierzchnię dla menu pauzy
    pause_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    pause_surface.fill((0, 0, 0, 128))  # Półprzezroczysty czarny

    display_logo(screen, logo)  # Wyświetl logo
    # Rysuj przyciski
    resume_button.draw(screen)  # Przycisk start
    quit_button.draw(screen)  # Przycisk quit

    # Aktualizacja przycisków
    start_action = resume_button.update()
    if start_action is not None:
        return start_action

    quit_action = quit_button.update()
    if quit_action is not None:
        return quit_action

    # Rysuj powierzchnię menu pauzy na ekranie gry
    screen.blit(pause_surface, (0, 0))

    # Wyświetl zmiany na ekranie
    pygame.display.flip()

    return game_state
