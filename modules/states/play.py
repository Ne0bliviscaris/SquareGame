import pygame

from modules.ai.agent import DeepLearningAgent
from modules.ai.deep_learning_data import DeepLearningData
from modules.ai.npc import Npc
from modules.ai.vectors import VectorCalculator
from modules.behavior.camera import Camera
from modules.behavior.controller import Controller
from modules.behavior.square_collisions import SquareCollisions
from modules.behavior.world_collisions import WorldCollisions
from modules.objects.sqare_generator import SquareGenerator
from modules.objects.tiles import Ground
from modules.settings import DRAW_VECTORS, SCREEN
from modules.states.state import GameState
from modules.world.grid_builder import world_list


class RunningGameState(GameState):
    """Stan gry reprezentujący działającą grę."""

    def __init__(self, game_state):
        """Inicjalizuje stan gry jako działający."""
        # Utwórz agenta AI
        self.agent = DeepLearningAgent()
        self.agent.load_model()

        # Utwórz listę kafelków Ground
        self.tiles = world_list
        self.ground_tiles = [tile for tile in self.tiles if isinstance(tile, Ground)]  # Najniższy rząd kafelków Ground
        # Utwórz instancję SquareGenerator
        self.square_generator = SquareGenerator(self.ground_tiles, self.agent)

        # Utwórz kwadraty
        self.squares = self.square_generator.create_squares()

        # # Utwórz instancję VectorCalculator dla modelu AI
        self.vector_calculator = VectorCalculator(self.squares)

        # Utwórz instancje Collisions dla każdego kwadratu
        self.world_collisions = [WorldCollisions(square) for square in self.squares]
        self.square_collisions = [SquareCollisions(square) for square in self.squares]

        # Utwórz instancję Camera dla kwadratu gracza
        self.camera = Camera(self.squares[0], self.tiles, self.ground_tiles)

        # Utwórz instancję kontrolera
        self.controller = Controller(self.squares[0], game_state, self.camera, self.agent)

        # Dodaj kafelki do listy obiektów do narysowania
        self.drawables = self.tiles + self.squares

        # Utwórz instancję DeepLearningData
        self.deep_learning_data = DeepLearningData(self.squares)
        self.state_for_model = self.deep_learning_data.get_state()

    def update(self):
        """Aktualizuje stan gry."""
        self.controller.handle_movement()
        self.camera.update_zoom()
        self.camera.update_camera()

        # Aktualizacja kwadratów i obsługa kolizji
        for square, world_collision, square_collision in zip(
            self.squares, self.world_collisions, self.square_collisions
        ):
            if isinstance(square, Npc):
                square.update(self.squares, self.state_for_model)
            else:
                square.update(self.squares)  # Aktualizacja kwadratów
            world_collision.handle_collisions_around(self.tiles)  # Kolizje z ground_tiles
            square_collision.handle_square_collisions(self.squares)  # Kolizje między kwadratami

        # Pobranie stanu dla modelu
        self.state_for_model = self.deep_learning_data.get_state()
        # Aktualizacja kwadratów AI z uwzględnieniem stanu dla modelu
        for square in self.squares:
            if isinstance(square, Npc):
                square.update(self.squares, self.state_for_model)

    def draw(self):
        """Rysuje elementy gry na ekranie dla bieżącego stanu gry."""
        SCREEN.fill((0, 38, 52))

        # Narysuj wszystkie obiekty z uwzględnieniem przesunięcia kamery i poziomu zoomu
        for drawable in self.drawables:
            if drawable is not self.squares[0]:  # Nie rysuj self.squares[0] jeszcze
                drawable.draw(self.camera.camera_offset_x, self.camera.camera_offset_y, self.camera.zoom_level)
        # Rysuj self.squares[0] na wierzchu
        self.squares[0].draw(self.camera.camera_offset_x, self.camera.camera_offset_y, self.camera.zoom_level)

        # Rysuj wektory
        if DRAW_VECTORS:
            self.vector_calculator.draw_vectors(
                self.camera.zoom_level, self.camera.camera_offset_x, self.camera.camera_offset_y
            )
        pygame.display.update()

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
