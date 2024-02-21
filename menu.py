from enum import Enum

import pygame


class GameState(Enum):
    """Enum reprezentujący różne stany gry."""

    MAIN_MENU = 0
    RUNNING = 1
    PAUSE = 2
    QUIT = 3


BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_Y_START = 300  # Możesz zmienić tę wartość na tę, którą chcesz
BUTTON_Y_GAP = 60  # Możesz zmienić tę wartość na tę, którą chcesz


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

    @staticmethod
    def create_from_screen(screen, y_offset, text, action):
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
        if self.is_mouse_over():
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

    def is_mouse_over(self):
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
        if self.is_mouse_over():  # Sprawdź, czy kursor myszy jest nad przyciskiem
            if pygame.mouse.get_pressed()[0]:  # Sprawdź, czy lewy przycisk myszy jest naciśnięty
                return True
        return False


def main_menu(screen, game_state):
    """
    Funkcja obsługująca menu główne gry.
    """

    # Utwórz przyciski
    start_button = Button.create_from_screen(screen, 0, "New Game", GameState.RUNNING)
    quit_button = Button.create_from_screen(screen, 1, "Quit", GameState.QUIT)

    screen.fill((0, 0, 0))  # Wypełnij ekran kolorem
    display_logo(screen)  # Wyświetl logo

    # Rysuj przyciski
    start_button.draw(screen)  # Przycisk start
    quit_button.draw(screen)  # Przycisk quit

    # Obsługa zdarzeń
    if start_button.is_mouse_down():  # Sprawdź, czy przycisk start został naciśnięty
        return start_button.action  # Akcja przycisku start
    elif quit_button.is_mouse_down():  # Sprawdź, czy przycisk quit został naciśnięty
        return quit_button.action  # Akcja przycisku quit
    # elif pygame.event.get(pygame.QUIT):
    #     return GameState.QUIT

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
