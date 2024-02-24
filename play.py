import sys

import pygame

from state import GameState


class RunningGameState(GameState):
    """Stan gry reprezentujący działającą grę."""

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        """Inicjalizuje stan gry jako działający."""
        self.pause_menu_state = None
        self.square_size = 50
        self.square_x = (SCREEN_WIDTH - self.square_size) // 2
        self.square_y = (SCREEN_HEIGHT - self.square_size) // 2
        self.speed = 5
        self.velocity = 0
        self.gravity = 0.1
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
                    self.velocity = -5

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.square_x -= self.speed
        if keys[pygame.K_d]:
            self.square_x += self.speed

        return self

    def update(self):
        """Aktualizuje logikę gry dla bieżącego stanu gry."""
        self.velocity += self.gravity
        self.square_y += self.velocity

    def draw(self, screen):
        """Rysuje elementy gry na ekranie dla bieżącego stanu gry."""
        screen.fill((0, 0, 0))
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            pygame.Rect(
                self.square_x - self.square_size // 2,
                self.square_y - self.square_size // 2,
                self.square_size,
                self.square_size,
            ),
        )
        pygame.display.flip()
