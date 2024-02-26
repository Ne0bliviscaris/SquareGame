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

    def draw(self, screen, camera_offset_x=0, camera_offset_y=0, zoom_level=1):
        """Rysuje kwadrat na ekranie."""
        pygame.draw.rect(
            screen,
            (180, 0, 0),
            pygame.Rect(
                (self.x * zoom_level) + camera_offset_x,
                (self.y * zoom_level) + camera_offset_y,
                self.size * zoom_level,
                self.size * zoom_level,
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
        self.zoom_level = 1

        # Ustaw przesunięcie kamery na środek świata gry
        self.camera_offset_x = -WORLD_WIDTH / 2 + SCREEN_WIDTH / 2
        self.camera_offset_y = 0

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
            pygame.MOUSEBUTTONDOWN: self.handle_mousebuttondown_events,
        }

        for event in events:
            handler = event_handlers.get(event.type)
            if handler:
                new_state = handler(event)
                if new_state is not None:
                    return new_state

        self.handle_continuous_key_events()

        return self

    def handle_mousebuttondown_events(self, event):
        if event.button == 4:
            self.zoom_level *= 1.1
        elif event.button == 5:
            self.zoom_level /= 1.1

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

    def update_camera(self):
        half_screen_width = self.SCREEN_WIDTH / 2
        half_screen_height = self.SCREEN_HEIGHT / 2
        lerp_speed = 0.1  # Szybkość interpolacji, możesz dostosować tę wartość

        # Oblicz target_offset na podstawie bieżącej pozycji kwadratu
        target_offset_x = -self.square.x + half_screen_width
        target_offset_y = -self.square.y + half_screen_height

        self.camera_offset_x += (target_offset_x - self.camera_offset_x) * lerp_speed
        self.camera_offset_y += (target_offset_y - self.camera_offset_y) * lerp_speed

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

    def move_left(self):
        # Aktualizuje prędkość x kwadratu
        self.square.velocity_x = -self.speed

    def move_right(self):
        # Aktualizuje prędkość x kwadratu
        self.square.velocity_x = self.speed

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
        self.update_camera()  # Aktualizuj kamerę

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
                # Jeśli kwadrat koliduje z kafelkiem Ground i porusza się w lewo, zatrzymaj jego ruch
                elif (
                    self.square.x > tile.x
                    and self.square.velocity_x < 0
                    and abs(self.square.x - (tile.x + tile.size)) < self.square.velocity_x
                ):
                    self.square.velocity_x = 0
                    self.square.x = tile.x + tile.size

    def draw(self, screen):
        """Rysuje elementy gry na ekranie dla bieżącego stanu gry."""
        screen.fill((0, 38, 52))

        # Narysuj wszystkie kafelki z uwzględnieniem przesunięcia kamery i poziomu zoomu
        for tile in self.tiles:
            tile.draw(screen, self.camera_offset_x, self.camera_offset_y, self.zoom_level)

        # Narysuj kwadrat z uwzględnieniem przesunięcia kamery i poziomu zoomu
        self.square.draw(screen, self.camera_offset_x, self.camera_offset_y, self.zoom_level)

        pygame.display.flip()
