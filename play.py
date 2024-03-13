import random

import pygame

from ai import Ai
from modules.ai.vectors import VectorCalculator
from modules.behavior.camera import Camera
from modules.behavior.collisions import Collisions
from modules.objects.player import Player
from modules.objects.tiles import Ground
from modules.state import GameState
from modules.world.world import TILE_SIZE, WORLD_WIDTH
from modules.world.world_builder import world_list

FPS_LIMIT = 250
RUNNERS = 2
CATCHERS = 0


class RunningGameState(GameState):
    """Stan gry reprezentujący działającą grę."""

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        """Inicjalizuje stan gry jako działający."""
        self.pause_menu_state = None
        self.speed = 3
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.tiles = world_list
        num_squares = RUNNERS + CATCHERS

        # Znajdź najniższy rząd kafelków Ground
        ground_tiles = [tile for tile in self.tiles if isinstance(tile, Ground)]
        lowest_row = max(tile.y for tile in ground_tiles)

        # Ustaw pozycję kwadratów na losowych pozycjach w świecie gry i na dolnym rzędzie
        self.squares = []
        for _ in range(1 + num_squares):
            x = random.randint(0, WORLD_WIDTH - TILE_SIZE)  # Losowa pozycja x
            y = random.randint(0, lowest_row + TILE_SIZE)  # Pozycja y na dolnym rzędzie
            square = (
                Player(x, y, TILE_SIZE, "catch") if not self.squares else Ai(x, y, TILE_SIZE)
            )  # Pierwszy kwadrat to Player, reszta to AI
            self.squares.append(square)
        self.drawables = self.tiles + self.squares  # Dodajemy kwadraty do listy obiektów do narysowania

        # Utwórz instancję VectorCalculator dla modelu AI
        self.vector_calculator = VectorCalculator(self.squares)

        # Losowo wybieramy jednego kwadratu, który będzie w trybie 'catch'
        for _ in range(CATCHERS):
            catcher = random.choice(self.squares[1:])
            catcher.change_mode()

        # Utwórz instancję Collisions dla każdego kwadratu
        self.collisions = [Collisions(square) for square in self.squares]
        # Utwórz instancję Camera dla kwadratu gracza
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, self.squares[0], self.tiles, ground_tiles)

    # Reszta OK
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
            pygame.K_a: self.squares[0].move_left,
            pygame.K_LEFT: self.squares[0].move_left,
            pygame.K_d: self.squares[0].move_right,
            pygame.K_RIGHT: self.squares[0].move_right,
        }

        for key, handler in key_handlers.items():
            if keys[key]:
                handler()

    def handle_key_press_actions(self, event):
        """Obsługuje zdarzenia związane z naciśnięciem klawisza."""
        if event.key == pygame.K_ESCAPE:
            return self.pause_menu_state
        elif event.key == pygame.K_SPACE:
            self.squares[0].jump()

    def handle_key_release(self, event):
        """Obsługuje zdarzenia związane z puszczeniem klawisza."""
        if event.key in (pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT):
            self.squares[0].velocity_x = 0  # Zresetuj prędkość x kwadratu

    def handle_quit_event(self, event):
        """Obsługuje zdarzenie wyjścia z gry."""
        pygame.quit()
        quit()

    def update(self):
        """Aktualizuje logikę gry dla bieżącego stanu gry."""
        for square in self.squares:
            square.update()  # Aktualizacja kwadratu
        self.camera.update_zoom()  # Aktualizacja zoomu
        self.camera.update_camera()  # Aktualizacja kamery
        for collision in self.collisions:
            collision.handle_collisions_around(
                self.tiles, self.squares
            )  # Sprawdź kolizje między kwadratem a wszystkimi kafelkami

    def draw(self, screen):
        """Rysuje elementy gry na ekranie dla bieżącego stanu gry."""
        screen.fill((0, 38, 52))

        # Narysuj wszystkie obiekty z uwzględnieniem przesunięcia kamery i poziomu zoomu
        for drawable in self.drawables:
            if drawable is not self.squares[0]:  # Nie rysuj self.squares[0] jeszcze
                drawable.draw(screen, self.camera.camera_offset_x, self.camera.camera_offset_y, self.camera.zoom_level)
        # Rysuj self.squares[0] na wierzchu
        self.squares[0].draw(screen, self.camera.camera_offset_x, self.camera.camera_offset_y, self.camera.zoom_level)

        # Rysuj wektory
        self.vector_calculator.draw_vectors(
            screen, self.camera.zoom_level, self.camera.camera_offset_x, self.camera.camera_offset_y
        )
        pygame.display.update()


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
