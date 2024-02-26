import sys

import pygame

from state import GameState
from world import TILE_SIZE, Ground, world_list


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
            (180, 0, 0),
            pygame.Rect(
                self.x,
                self.y,
                self.size,
                self.size,
            ),
        )


class RunningGameState(GameState):
    """Stan gry reprezentujący działającą grę."""

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        """Inicjalizuje stan gry jako działający."""
        self.pause_menu_state = None
        self.speed = 3
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.tiles = world_list

        # Znajdź najniższy rząd kafelków Ground
        ground_tiles = [tile for tile in self.tiles if isinstance(tile, Ground)]
        lowest_row = max(tile.y for tile in ground_tiles)

        # Ustaw pozycję kwadratu na środku dolnego rzędu i o rozmiar kafelka powyżej
        self.square = Square(SCREEN_WIDTH // 2, lowest_row - TILE_SIZE, TILE_SIZE)

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

        # Sprawdź kolizje między kwadratem a wszystkimi kafelkami
        for tile in self.tiles:
            if isinstance(tile, Ground) and tile.collides_with(self.square):
                # Jeśli kwadrat koliduje z kafelkiem Ground i porusza się w dół, zatrzymaj jego ruch
                if self.square.y < tile.y and self.square.velocity > 0:
                    self.square.velocity = 0
                    self.square.y = tile.y - self.square.size

    def draw(self, screen):
        """Rysuje elementy gry na ekranie dla bieżącego stanu gry."""
        screen.fill((0, 38, 52))

        # Narysuj wszystkie kafelki
        for tile in self.tiles:
            tile.draw(screen)

        self.square.draw(screen)  # Narysuj kwadrat
        pygame.display.flip()
