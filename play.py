import sys

import pygame

from state import GameState
from world import TILE_SIZE, WORLD_WIDTH, Ground, world_list


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

        # Ustaw przesunięcie kamery na środek świata gry
        self.camera_offset = -WORLD_WIDTH / 2 + SCREEN_WIDTH / 2

        # Znajdź najniższy rząd kafelków Ground
        ground_tiles = [tile for tile in self.tiles if isinstance(tile, Ground)]
        lowest_row = max(tile.y for tile in ground_tiles)

        # Ustaw pozycję kwadratu na środku świata gry i na dolnym rzędzie
        self.square = Square(WORLD_WIDTH / 2, lowest_row - TILE_SIZE, TILE_SIZE)

    def set_pause_state(self, pause_state):
        """Ustawia stan pauzy dla stanu gry."""
        self.pause_menu_state = pause_state

    def handle_events(self, events):
        """Obsługuje zdarzenia dla bieżącego stanu gry."""
        event_handlers = {
            pygame.QUIT: self.handle_quit_event,
            pygame.KEYDOWN: self.handle_keydown_events,
            pygame.KEYUP: self.handle_keyup_events,
        }

        for event in events:
            handler = event_handlers.get(event.type)
            if handler:
                new_state = handler(event)
                if new_state is not None:
                    return new_state

        self.handle_continuous_key_events()

        return self

    def handle_continuous_key_events(self):
        """Obsługuje zdarzenia związane z ciągłym naciśnięciem klawisza."""
        keys = pygame.key.get_pressed()

        key_handlers = {
            pygame.K_a: self.move_left,
            pygame.K_LEFT: self.move_left,
            pygame.K_d: self.move_right,
            pygame.K_RIGHT: self.move_right,
        }

        for key, handler in key_handlers.items():
            if keys[key]:
                handler()

    def move_left(self):
        if self.square.x - self.camera_offset > 0:  # Sprawdź, czy kwadrat jest blisko lewej krawędzi ekranu
            self.square.velocity_x = -self.speed  # Zaktualizuj prędkość x kwadratu
            if self.camera_offset < 0:  # Sprawdź, czy kamera jest w granicach świata gry
                self.camera_offset += self.speed  # Zaktualizuj przesunięcie kamery

    # def move_right(self):
    #     if (
    #         self.square.x - self.camera_offset < self.SCREEN_WIDTH - self.square.size
    #     ):  # Sprawdź, czy kwadrat jest blisko prawej krawędzi ekranu
    #         self.square.velocity_x = self.speed  # Zaktualizuj prędkość x kwadratu
    #         if self.camera_offset > -(
    #             len(self.tiles) * TILE_SIZE - self.SCREEN_WIDTH
    #         ):  # Sprawdź, czy kamera jest w granicach świata gry
    #             self.camera_offset -= self.speed  # Zaktualizuj przesunięcie kamery
    def move_right(self):
        if (
            self.square.x - self.camera_offset < self.SCREEN_WIDTH - self.square.size
        ):  # Sprawdź, czy kwadrat jest blisko prawej krawędzi ekranu
            self.square.velocity_x = self.speed  # Zaktualizuj prędkość x kwadratu
        if self.camera_offset > -(
            len(self.tiles) * TILE_SIZE - self.SCREEN_WIDTH
        ):  # Sprawdź, czy kamera jest w granicach świata gry
            self.camera_offset -= self.speed  # Zaktualizuj przesunięcie kamery

    def handle_keydown_events(self, event):
        """Obsługuje zdarzenia związane z naciśnięciem klawisza."""
        if event.key == pygame.K_ESCAPE:
            return self.pause_menu_state
        elif event.key == pygame.K_SPACE:
            self.handle_jump_event()

    def handle_keyup_events(self, event):
        """Obsługuje zdarzenia związane z puszczeniem klawisza."""
        if event.key in (pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT):
            self.square.velocity_x = 0  # Zresetuj prędkość x kwadratu

    def handle_jump_event(self):
        """Obsługuje zdarzenie skoku."""
        self.square.velocity = -4  # Zaktualizuj prędkość kwadratu

    def handle_quit_event(self):
        """Obsługuje zdarzenie wyjścia z gry."""
        pygame.quit()
        sys.exit()

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
