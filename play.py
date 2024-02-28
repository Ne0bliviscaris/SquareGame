import sys

import pygame

from state import GameState
from tiles import Ground
from world import TILE_SIZE, WORLD_WIDTH, world_list


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

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

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

    def handle_ground_collision(self, tile):
        """Obsługuje kolizję kwadratu z danym kafelkiem."""
        if self.y < tile.y and self.velocity > 0:
            self.velocity = 0
            self.y = tile.y - self.size
        elif self.x < tile.x and self.velocity_x > 0:
            self.velocity_x = 0
            self.x = tile.x - self.size
        elif self.x > tile.x and self.velocity_x < 0:
            self.velocity_x = 0
            self.x = tile.x + tile.size
        elif self.x > tile.x and self.velocity_x < 0 and abs(self.x - (tile.x + tile.size)) < self.velocity_x:
            self.velocity_x = 0
            self.x = tile.x + tile.size


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
        self.target_zoom_level = 1  # Dla płynnego zoomu

        # Ustaw przesunięcie kamery na środek świata gry
        self.camera_offset_x = -WORLD_WIDTH / 2 + SCREEN_WIDTH / 2
        self.camera_offset_y = 0

        # Znajdź najniższy rząd kafelków Ground
        ground_tiles = [tile for tile in self.tiles if isinstance(tile, Ground)]
        lowest_row = max(tile.y for tile in ground_tiles)

        # Ustaw pozycję kwadratu na środku świata gry i na dolnym rzędzie
        self.square = Square(WORLD_WIDTH / 2, lowest_row - TILE_SIZE, TILE_SIZE)
        self.drawables = self.tiles + [self.square]  # Dodajemy kwadrat do listy obiektów do narysowania

    def set_pause_state(self, pause_state):
        """Ustawia stan pauzy dla stanu gry."""
        self.pause_menu_state = pause_state

    def handle_events(self, events):
        """Obsługuje zdarzenia dla bieżącego stanu gry."""
        event_handlers = {
            pygame.QUIT: self.handle_quit_event,
            pygame.KEYDOWN: self.handle_key_press_actions,
            pygame.KEYUP: self.handle_key_release,
            pygame.MOUSEBUTTONDOWN: self.handle_scroll_zoom,
        }

        for event in events:
            handler = event_handlers.get(event.type)
            if handler:
                new_state = handler(event)
                if new_state is not None:
                    return new_state

        self.handle_movement()

        return self

    def handle_scroll_zoom(self, event):
        """
        Obsługuje zoom przy użyciu rolki myszy."""
        if event.button == 4:
            self.target_zoom_level *= 1.2
        elif event.button == 5:
            self.target_zoom_level /= 1.2

    def handle_movement(self):
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
        self.calculate_target_offset()
        self.limit_target_offset()
        self.update_camera_offset()

    def calculate_target_offset(self):
        """
        Oblicza przesunięcie kamery, aby śledzić kwadrat."""
        half_screen_width = self.SCREEN_WIDTH / 2
        half_screen_height = self.SCREEN_HEIGHT / 2
        self.target_offset_x = half_screen_width - (self.square.x + self.square.size / 2) * self.zoom_level
        self.target_offset_y = half_screen_height - (self.square.y + self.square.size / 2) * self.zoom_level

    def limit_target_offset(self):
        """
        Ogranicza przesunięcie kamery, aby nie wyświetlać obszarów poza światem gry."""
        ground_tiles = [tile for tile in self.tiles if isinstance(tile, Ground)]
        lowest_row = max(tile.y for tile in ground_tiles)
        if self.target_offset_y < -lowest_row * self.zoom_level + self.SCREEN_HEIGHT - TILE_SIZE * self.zoom_level:
            self.target_offset_y = -lowest_row * self.zoom_level + self.SCREEN_HEIGHT - TILE_SIZE * self.zoom_level
        if self.target_offset_x > 0:
            self.target_offset_x = 0
        elif self.target_offset_x < self.SCREEN_WIDTH - WORLD_WIDTH * self.zoom_level:
            self.target_offset_x = self.SCREEN_WIDTH - WORLD_WIDTH * self.zoom_level

    def update_camera_offset(self):
        """
        Aktualizuje przesunięcie kamery, interpolując je do docelowego przesunięcia kamery."""
        self.camera_offset_x = self.target_offset_x
        self.camera_offset_y = self.target_offset_y

    def handle_key_press_actions(self, event):
        """Obsługuje zdarzenia związane z naciśnięciem klawisza."""
        if event.key == pygame.K_ESCAPE:
            return self.pause_menu_state
        elif event.key == pygame.K_SPACE:
            self.handle_jump_event()

    def handle_key_release(self, event):
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

    def handle_quit_event(self, event):
        """Obsługuje zdarzenie wyjścia z gry."""
        pygame.quit()
        sys.exit()

    def update_zoom(self):
        """Aktualizuje poziom zoomu, interpolując go do docelowego poziomu zoomu."""
        lerp_speed = 0.1  # Szybkość interpolacji, możesz dostosować tę wartość
        self.zoom_level += (self.target_zoom_level - self.zoom_level) * lerp_speed

    def handle_ground_collisions(self):
        for tile in self.tiles:
            if isinstance(tile, Ground) and tile.collides_with(self.square):
                self.square.handle_ground_collision(tile)

    def update(self):
        """Aktualizuje logikę gry dla bieżącego stanu gry."""
        self.square.update()  # Aktualizacja kwadratu
        self.update_zoom()  # Aktualizacja zoomu
        self.update_camera()  # Aktualizacja kamery
        self.handle_ground_collisions()  # Sprawdź kolizje między kwadratem a wszystkimi kafelkami

    def draw(self, screen):
        """Rysuje elementy gry na ekranie dla bieżącego stanu gry."""
        screen.fill((0, 38, 52))

        # Narysuj wszystkie obiekty z uwzględnieniem przesunięcia kamery i poziomu zoomu
        for drawable in self.drawables:
            drawable.draw(screen, self.camera_offset_x, self.camera_offset_y, self.zoom_level)

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    running_game_state = RunningGameState(SCREEN_WIDTH, SCREEN_HEIGHT)

    while True:
        events = pygame.event.get()
        new_state = running_game_state.handle_events(events)
        if new_state is not None:
            running_game_state = new_state
        running_game_state.update()
        running_game_state.draw(screen)
