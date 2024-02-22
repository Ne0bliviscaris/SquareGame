import sys

import pygame

from state import GameState


class RunningGameState(GameState):
    """Stan gry reprezentujący działającą grę."""

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        """Inicjalizuje stan gry jako działający."""
        self.pause_menu_state = None
        self.square_size = 50
        self.square_x = (SCREEN_WIDTH - self.square_size) / 2
        self.square_y = (SCREEN_HEIGHT - self.square_size) / 2
        self.speed = 5
        self.velocity = 0
        self.gravity = 0.1
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SCREEN_WIDTH = SCREEN_WIDTH  # Przechowaj SCREEN_WIDTH jako atrybut instancji
        self.on_ground = True

    def set_pause_state(self, pause_state):
        self.pause_menu_state = pause_state

    def handle_events(self, events):
        """Obsługuje zdarzenia dla bieżącego stanu gry."""
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return self.pause_menu_state  # Zwróć obiekt PauseMenuState
                elif (
                    event.key == pygame.K_SPACE and self.on_ground
                ):  # Dodaj warunek, że kwadrat musi być na ziemi, aby skoczyć
                    self.velocity = -5  # Skok
                    self.on_ground = False  # Ustaw kwadrat w powietrzu

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.square_x -= self.speed
        if keys[pygame.K_d]:
            self.square_x += self.speed

        return self  # Zwróć aktualny obiekt RunningGameState

    def update(self):
        """Aktualizuje logikę gry dla bieżącego stanu gry."""
        if not self.on_ground:  # Zastosuj grawitację tylko wtedy, gdy kwadrat nie jest na ziemi
            self.velocity += self.gravity
        self.square_y += self.velocity  # Aktualizuj pozycję kwadratu

        # Sprawdź, czy kwadrat nie jest poza dolną krawędzią ekranu
        if self.square_y + self.square_size > self.SCREEN_HEIGHT:
            self.square_y = self.SCREEN_HEIGHT - self.square_size
            self.velocity = 0
            self.on_ground = True  # Ustaw kwadrat na ziemi
        else:
            self.on_ground = False

        # Sprawdź, czy kwadrat nie jest poza górną krawędzią ekranu
        if self.square_y < 0:
            self.square_y = 0
            self.velocity = 0

        # Sprawdź, czy kwadrat nie jest poza lewą lub prawą krawędzią ekranu
        if self.square_x < 0:
            self.square_x = 0
        elif self.square_x + self.square_size > self.SCREEN_WIDTH:
            self.square_x = self.SCREEN_WIDTH - self.square_size

    def draw(self, screen):
        """Rysuje elementy gry na ekranie dla bieżącego stanu gry."""
        screen.fill((0, 0, 0))
        pygame.draw.rect(
            screen, (255, 0, 0), pygame.Rect(self.square_x, self.square_y, self.square_size, self.square_size)
        )
        pygame.display.flip()


def game_running(screen):
    """
    Funkcja obsługująca stan gry "running".
    """
    # Wypełnij ekran kolorem czarnym
    screen.fill((0, 0, 0))

    # Ustal rozmiar i pozycję kwadratu
    square_size = 50
    square_x = (screen.get_width() - square_size) / 2
    square_y = (screen.get_height() - square_size) / 2

    # Narysuj czerwony kwadrat
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(square_x, square_y, square_size, square_size))

    # Wyświetl zmiany na ekranie
    pygame.display.flip()
