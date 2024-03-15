import random

import pygame

from modules.ai.ai import Ai

# from modules.ai.model import Flee
from modules.ai.vectors import VectorCalculator
from modules.behavior.camera import Camera
from modules.behavior.collisions import Collisions
from modules.behavior.controller import Controller
from modules.objects.player import Player
from modules.objects.sqare_generator import SquareGenerator
from modules.objects.tiles import Ground
from modules.settings import (
    CATCHERS,
    PLAYER_MODE,
    RUNNERS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TILE_SIZE,
)
from modules.states.state import GameState
from modules.world.grid_builder import WORLD_WIDTH, world_list


class RunningGameState(GameState):
    """Stan gry reprezentujący działającą grę."""

    def __init__(self, game_state):
        """Inicjalizuje stan gry jako działający."""
        self.pause_menu_state = None
        self.speed = 3

        # Utwórz listę kafelków Ground
        self.tiles = world_list
        self.ground_tiles = [tile for tile in self.tiles if isinstance(tile, Ground)]  # Najniższy rząd kafelków Ground

        # Utwórz instancję SquareGenerator
        self.square_generator = SquareGenerator(self.ground_tiles)

        # Utwórz kwadraty
        self.squares = self.square_generator.create_squares()

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
