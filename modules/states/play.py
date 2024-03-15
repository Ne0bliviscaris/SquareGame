import random

import pygame

from modules.ai.ai import Ai

# from modules.ai.model import Flee
from modules.ai.vectors import VectorCalculator
from modules.behavior.camera import Camera
from modules.behavior.collisions import Collisions
from modules.objects.player import Player
from modules.objects.tiles import Ground
from modules.settings import CATCHERS, RUNNERS, SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE
from modules.states.state import GameState
from modules.world.grid_builder import WORLD_WIDTH, world_list

# Ustaw tryb gracza
PLAYER_MODE = "catch"
# PLAYER_MODE = "flee"
# PLAYER_MODE = "observer"


class RunningGameState(GameState):
    """Stan gry reprezentujący działającą grę."""

    def __init__(self, game_state):
        """Inicjalizuje stan gry jako działający."""
        self.pause_menu_state = None
        self.speed = 3
        self.tiles = world_list
        self.ground_tiles = [tile for tile in self.tiles if isinstance(tile, Ground)]  # Najniższy rząd kafelków Ground

        # Tworzenie kwadratów
        self.squares = self.create_squares()

        # Utwórz instancję VectorCalculator dla modelu AI
        self.vector_calculator = VectorCalculator(self.squares)

        # Utwórz instancję Collisions dla każdego kwadratu
        self.collisions = [Collisions(square) for square in self.squares]

        # Utwórz instancję Camera dla kwadratu gracza
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, self.squares[0], self.tiles, self.ground_tiles)

        # Utwórz instancję kontrolera
        self.controller = Controller(self.squares[0], game_state, self.camera)

        # Dodaj kafelki do listy obiektów do narysowania
        self.drawables = self.tiles + self.squares  # Dodajemy kwadraty do listy obiektów do narysowania

    def handle_events(self, events):
        """Obsługuje zdarzenia dla bieżącego stanu gry."""
        event_handlers = {
            pygame.QUIT: self.controller.handle_quit_event,
            pygame.KEYDOWN: self.controller.handle_key_press_actions,
            pygame.KEYUP: self.controller.handle_key_release,
            pygame.MOUSEBUTTONDOWN: self.camera.handle_scroll_zoom,
        }

        for event in events:
            handler = event_handlers.get(event.type)
            if handler:
                new_state = handler(event)
                if new_state is not None:
                    return new_state

        self.controller.handle_movement()

        return self

    def update(self):
        """Aktualizuje logikę gry dla bieżącego stanu gry."""
        self.controller.handle_movement()
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

    def create_squares(self):
        """Tworzy kwadraty dla gry."""
        npc_squares = RUNNERS + CATCHERS  # Ilość kwadratów AI
        lowest_row = max(tile.y for tile in self.ground_tiles)  # Najniższy rząd Ground

        # Ustaw pozycję kwadratów na losowych pozycjach w świecie gry i na dolnym rzędzie
        min_x = TILE_SIZE
        max_x = WORLD_WIDTH - TILE_SIZE
        min_y = TILE_SIZE
        max_y = lowest_row - TILE_SIZE

        squares = []
        for i in range(1 + npc_squares):
            x = random.randint(min_x, max_x)  # Losowa pozycja x
            y = random.randint(min_y, max_y)  # Pozycja y na dolnym rzędzie
            npc_mode = "catch" if i <= CATCHERS else "flee"
            square = (
                Player(x, y, TILE_SIZE, PLAYER_MODE) if not squares else Ai(x, y, TILE_SIZE, npc_mode)
            )  # Pierwszy kwadrat to Player, reszta to AI
            squares.append(square)

        return squares


class Controller:
    """Obsługa sterowania w grze."""

    def __init__(self, squares, game_state, camera):
        """Inicjalizuje kontroler z danymi kwadratami."""
        self.squares = squares
        self.game_state = game_state
        self.camera = camera

    def handle_movement(self):
        """Obsługuje zdarzenia związane z ciągłym naciśnięciem klawisza."""
        keys = pygame.key.get_pressed()

        key_handlers = {
            pygame.K_a: self.squares.move_left,
            pygame.K_LEFT: self.squares.move_left,
            pygame.K_d: self.squares.move_right,
            pygame.K_RIGHT: self.squares.move_right,
        }

        for key, handler in key_handlers.items():
            if keys[key]:
                handler()

    def handle_key_release(self, event):
        """Obsługuje zdarzenia związane z puszczeniem klawisza."""
        if event.key in (pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT):
            self.squares.velocity_x = 0  # Zresetuj prędkość x kwadratu

    def handle_key_press_actions(self, event):
        """Obsługuje zdarzenia związane z naciśnięciem klawisza."""
        if event.key == pygame.K_ESCAPE:
            return self.game_state.pause_menu_state
        elif event.key == pygame.K_SPACE:
            self.squares.jump()

    def handle_quit_event(self, event):
        """Obsługuje zdarzenie wyjścia z gry."""
        pygame.quit()
        quit()

    def set_pause_state(self, pause_state):
        """Ustawia stan pauzy dla stanu gry."""
        self.pause_state = pause_state
