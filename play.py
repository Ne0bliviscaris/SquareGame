import sys

import pygame

from camera import Camera
from collisions import Collisions
from square import Player
from state import GameState
from tiles import Ground
from world import TILE_SIZE, WORLD_WIDTH
from world_builder import world_list

FPS_LIMIT = 250


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
        self.square = Player(WORLD_WIDTH / 2, lowest_row - TILE_SIZE, TILE_SIZE)
        self.drawables = self.tiles + [self.square]  # Dodajemy kwadrat do listy obiektów do narysowania

        # Utwórz instancję Collisions
        self.collisions = Collisions(self.square)
        # Utwórz instancję Camera
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, self.square, self.tiles, ground_tiles)

    def set_pause_state(self, pause_state):
        """Ustawia stan pauzy dla stanu gry."""
        self.pause_menu_state = pause_state

    def handle_events(self, events):
        """Obsługuje zdarzenia dla bieżącego stanu gry."""
        event_handlers = {
            pygame.QUIT: self.handle_quit_event,
            pygame.KEYDOWN: self.handle_key_press_actions,
            pygame.KEYUP: self.handle_key_release,
            pygame.MOUSEBUTTONDOWN: self.camera.handle_scroll_zoom,
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

    def update(self):
        """Aktualizuje logikę gry dla bieżącego stanu gry."""
        self.square.update()  # Aktualizacja kwadratu
        self.camera.update_zoom()  # Aktualizacja zoomu
        self.camera.update_camera()  # Aktualizacja kamery
        self.collisions.handle_collisions_around(self.tiles)  # Sprawdź kolizje między kwadratem a wszystkimi kafelkami

    def draw(self, screen):
        """Rysuje elementy gry na ekranie dla bieżącego stanu gry."""
        screen.fill((0, 38, 52))

        # Narysuj wszystkie obiekty z uwzględnieniem przesunięcia kamery i poziomu zoomu
        for drawable in self.drawables:
            drawable.draw(screen, self.camera.camera_offset_x, self.camera.camera_offset_y, self.camera.zoom_level)

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
