from enum import Enum

import pygame


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
        width,
        height,
        text,
        action,
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

    def draw(self, screen):
        """
        Rysuje przycisk na ekranie.
        """
        # Zmień kolor przycisku, gdy kursor myszy jest nad nim
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            color = self.hover_color
        else:
            color = self.button_color

        # Rysuj przycisk
        pygame.draw.rect(screen, color, self.rect)

        # Rysuj ramkę przycisku
        pygame.draw.rect(screen, self.text_color, self.rect, self.border_width)

        # Rysuj tekst na przycisku
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(
            text_surface,
            (
                self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                self.rect.y + (self.rect.height - text_surface.get_height()) // 2,
            ),
        )

    def is_clicked(self, event):
        """
        Sprawdza, czy przycisk został naciśnięty.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:  # Sprawdź czy klawisz myszy został naciśnięty
            if self.rect.collidepoint(event.pos):  # Sprawdź czy kursor myszy jest nad przyciskiem
                return True
        return False


def main_menu(screen, game_state):
    """
    Funkcja obsługująca menu główne gry.
    """

    # Utwórz przyciski
    button_width = 200
    button_height = 50
    screen_width, screen_height = screen.get_size()
    start_button = Button(
        (screen_width - button_width) / 2, screen_height / 2, button_width, button_height, "Start", GameState.RUNNING
    )
    quit_button = Button(
        (screen_width - button_width) / 2,
        screen_height / 2 + button_height + 10,
        button_width,
        button_height,
        "Quit",
        GameState.QUIT,
    )

    screen.fill((0, 0, 0))  # Wypełnij ekran kolorem
    display_logo(screen)  # Wyświetl logo

    # Rysuj przyciski
    start_button.draw(screen)  # Przycisk start
    quit_button.draw(screen)  # Przycisk quit

    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return GameState.QUIT
        elif start_button.is_clicked(event):
            return start_button.action
        elif quit_button.is_clicked(event):
            return quit_button.action

    # Wyświetl zmiany na ekranie
    pygame.display.flip()

    return game_state


def pause_menu(screen, game_state):
    """
    Funkcja obsługująca menu pauzy.
    """
    pygame.display.flip()  # Aktualizuj ekran
    display_logo(screen)
    pygame.display.flip()  # Wyświetlenie zmian na ekranie
    font = pygame.font.Font(None, 36)  # Utwórz czcionkę o rozmiarze 36
    text = font.render("Game is paused properly", True, (255, 255, 255))  # Utwórz tekst

    # Wyświetl tekst na środku ekranu
    x = (screen.get_width() - text.get_width()) // 2
    y = (screen.get_height() - text.get_height()) // 2
    screen.blit(text, (x, y))
    pass


def display_logo(screen):
    """
    Wyświetla logo gry.
    """
    # Załaduj obrazek
    logo = pygame.image.load("assets/logo.png")

    # Oblicz pozycję, na której logo powinno być wyświetlone
    x = (screen.get_width() - logo.get_width()) // 2
    y = 5

    # Wyświetl logo
    screen.blit(logo, (x, y))
