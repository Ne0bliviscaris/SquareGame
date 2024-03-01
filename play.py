import sys

import pygame

from square import Square
from state import GameState
from tiles import Ground
from world import TILE_SIZE, WORLD_WIDTH
from world_builder import world_list

FPS_LIMIT = 250


class Camera:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, square, tiles, ground_tiles):
        """Inicjalizuje kamerę."""
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.square = square
        self.tiles = tiles
        self.zoom_level = 1
        self.target_zoom_level = 1  # Dla płynnego zoomu

        # Ustaw przesunięcie kamery na środek świata gry
        self.camera_offset_x = -WORLD_WIDTH / 2 + SCREEN_WIDTH / 2
        self.camera_offset_y = 0

        # Znajdź najniższy rząd kafelków Ground
        self.ground_tiles = ground_tiles
        self.lowest_row = max(tile.y for tile in ground_tiles)

    def calculate_target_offset(self):
        """Oblicza przesunięcie kamery, aby śledzić kwadrat."""
        half_screen_width = self.SCREEN_WIDTH / 2
        half_screen_height = self.SCREEN_HEIGHT / 2
        self.target_offset_x = half_screen_width - (self.square.x + self.square.size / 2) * self.zoom_level
        self.target_offset_y = half_screen_height - (self.square.y + self.square.size / 2) * self.zoom_level


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

        # Ustaw pozycję kwadratu na środku świata gry i na dolnym rzędzie
        self.square = Square(WORLD_WIDTH / 2, lowest_row - TILE_SIZE, TILE_SIZE)
        self.drawables = self.tiles + [self.square]  # Dodajemy kwadrat do listy obiektów do narysowania

        # Utwórz instancję Camera
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, self.square, self.tiles, ground_tiles)

    def limit_target_offset(self):  # MOVE THIS TO CAMERA CLASS
        """Ogranicza przesunięcie kamery, aby nie wyświetlać obszarów poza światem gry."""
        ground_tiles = [tile for tile in self.tiles if isinstance(tile, Ground)]
        lowest_row = max(tile.y for tile in ground_tiles)
        if (
            self.camera.target_offset_y
            < -lowest_row * self.camera.zoom_level + self.SCREEN_HEIGHT - TILE_SIZE * self.camera.zoom_level
        ):
            self.target_offset_y = (
                -lowest_row * self.camera.zoom_level + self.SCREEN_HEIGHT - TILE_SIZE * self.camera.zoom_level
            )
        if self.camera.target_offset_x > 0:
            self.camera.target_offset_x = 0
        elif self.camera.target_offset_x < self.SCREEN_WIDTH - WORLD_WIDTH * self.camera.zoom_level:
            self.camera.target_offset_x = self.SCREEN_WIDTH - WORLD_WIDTH * self.camera.zoom_level

    def update_camera_offset(self):  # MOVE THIS TO CAMERA CLASS
        """Aktualizuje przesunięcie kamery, interpolując je do docelowego przesunięcia kamery."""
        self.camera_offset_x = self.camera.target_offset_x
        self.camera_offset_y = self.target_offset_y

    def update_zoom(self):  # MOVE THIS TO CAMERA CLASS
        """Aktualizuje poziom zoomu, interpolując go do docelowego poziomu zoomu."""
        lerp_speed = 0.1  # Szybkość interpolacji, możesz dostosować tę wartość
        self.camera.zoom_level += (self.camera.target_zoom_level - self.camera.zoom_level) * lerp_speed

    def handle_scroll_zoom(self, event):  # MOVE THIS TO CAMERA CLASS
        """
        Obsługuje zoom przy użyciu rolki myszy."""
        if event.button == 4:
            self.camera.target_zoom_level *= 1.2
        elif event.button == 5:
            self.camera.target_zoom_level /= 1.2

    def update_camera(self):  # MOVE THIS TO CAMERA CLASS
        self.camera.calculate_target_offset()
        self.limit_target_offset()
        self.update_camera_offset()

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

    def handle_movement(self):
        """Obsługuje zdarzenia związane z ciągłym naciśnięciem klawisza."""
        keys = pygame.key.get_pressed()

        key_handlers = {
            pygame.K_a: self.square.move_left,
            pygame.K_LEFT: self.square.move_left,
            pygame.K_d: self.square.move_right,
            pygame.K_RIGHT: self.square.move_right,
        }

        for key, handler in key_handlers.items():
            if keys[key]:
                handler(self.speed)

    def handle_key_press_actions(self, event):
        """Obsługuje zdarzenia związane z naciśnięciem klawisza."""
        if event.key == pygame.K_ESCAPE:
            return self.pause_menu_state
        elif event.key == pygame.K_SPACE:
            self.square.jump()

    def handle_key_release(self, event):
        """Obsługuje zdarzenia związane z puszczeniem klawisza."""
        if event.key in (pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT):
            self.square.velocity_x = 0  # Zresetuj prędkość x kwadratu

    def handle_quit_event(self, event):
        """Obsługuje zdarzenie wyjścia z gry."""
        pygame.quit()
        sys.exit()

    def handle_ground_collisions(self):
        """Sprawdza kolizje między kwadratem a wszystkimi kafelkami."""
        self.square.handle_ground_collisions(self.tiles)

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
            drawable.draw(screen, self.camera_offset_x, self.camera_offset_y, self.camera.zoom_level)

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    running_game_state = RunningGameState(SCREEN_WIDTH, SCREEN_HEIGHT)
    clock = pygame.time.Clock()
    while True:
        events = pygame.event.get()
        new_state = running_game_state.handle_events(events)
        if new_state is not None:
            running_game_state = new_state
        running_game_state.update()
        running_game_state.draw(screen)
        clock.tick(FPS_LIMIT)
