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
        self.velocity_x = 0  # Dodajemy prędkość w osi x
        self.gravity = 0.07

    def update(self):
        """Aktualizuje pozycję kwadratu, dodając do niej prędkość."""
        self.velocity += self.gravity
        self.y += self.velocity
        self.x += self.velocity_x  # Aktualizujemy pozycję x na podstawie prędkości x

    def draw(self, screen, camera_offset=0):
        """Rysuje kwadrat na ekranie."""
        pygame.draw.rect(
            screen,
            (180, 0, 0),
            pygame.Rect(
                self.x + camera_offset,
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
        self.camera_offset = 0

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
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT):
                    self.square.velocity_x = 0  # Zresetuj prędkość x kwadratu

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.square.velocity_x = -self.speed  # Zaktualizuj prędkość x kwadratu
            self.camera_offset += self.speed  # Zaktualizuj przesunięcie kamery
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.square.velocity_x = self.speed  # Zaktualizuj prędkość x kwadratu
            self.camera_offset -= self.speed  # Zaktualizuj przesunięcie kamery

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
                # Jeśli kwadrat koliduje z kafelkiem Ground i porusza się w prawo, zatrzymaj jego ruch
                elif self.square.x < tile.x and self.square.velocity_x > 0:
                    self.square.velocity_x = 0
                    self.square.x = tile.x - self.square.size
                # Jeśli kwadrat koliduje z kafelkiem Ground i porusza się w lewo, zatrzymaj jego ruch
                elif self.square.x > tile.x and self.square.velocity_x < 0:
                    self.square.velocity_x = 0
                    self.square.x = tile.x + tile.size

    def draw(self, screen):
        """Rysuje elementy gry na ekranie dla bieżącego stanu gry."""
        screen.fill((0, 38, 52))

        # Narysuj wszystkie kafelki z uwzględnieniem przesunięcia kamery
        for tile in self.tiles:
            tile.draw(screen, self.camera_offset)

        self.square.draw(screen, self.camera_offset)  # Narysuj kwadrat z uwzględnieniem przesunięcia kamery
        pygame.display.flip()
