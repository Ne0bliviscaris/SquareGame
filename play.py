import sys

import pygame

from state import GameState


class Square:
    """Klasa reprezentująca kwadrat na ekranie."""

    def __init__(self, x, y, size):
        """Inicjalizuje kwadrat na podanej pozycji i o podanym rozmiarze."""
        self.x = x
        self.y = y
        self.size = size
        self.velocity = 5
        self.gravity = 0.07

    def update(self):
        """Aktualizuje pozycję kwadratu, dodając do niej prędkość."""
        self.velocity += self.gravity
        self.y += self.velocity

    def draw(self, screen):
        """Rysuje kwadrat na ekranie."""
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            pygame.Rect(
                self.x - self.size // 2,
                self.y - self.size // 2,
                self.size,
                self.size,
            ),
        )


class RunningGameState(GameState):
    """Stan gry reprezentujący działającą grę."""

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        """Inicjalizuje stan gry jako działający."""
        self.pause_menu_state = None
        self.square = Square(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 50)  # Utwórz instancję klasy Square
        self.speed = 3
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SCREEN_WIDTH = SCREEN_WIDTH

    def set_pause_state(self, pause_state):
        """Ustawia stan pauzy dla stanu gry."""
        self.pause_menu_state = pause_state

    def handle_events(self, events):
        """Obsługuje zdarzenia dla bieżącego stanu gry."""
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return self.pause_menu_state
                elif event.key == pygame.K_SPACE:
                    self.square.velocity = -4  # Zaktualizuj prędkość kwadratu

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.square.x -= self.speed  # Zaktualizuj pozycję kwadratu
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.square.x += self.speed  # Zaktualizuj pozycję kwadratu

        return self

    def update(self):
        """Aktualizuje logikę gry dla bieżącego stanu gry."""
        self.square.update()  # Zaktualizuj kwadrat

    def draw(self, screen):
        """Rysuje elementy gry na ekranie dla bieżącego stanu gry."""
        screen.fill((0, 38, 52))
        self.square.draw(screen)  # Narysuj kwadrat
        pygame.display.flip()
