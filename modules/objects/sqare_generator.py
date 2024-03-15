from random import randint

from ..ai.ai import Ai
from ..objects.player import Player
from ..settings import CATCHERS, PLAYER_MODE, RUNNERS, TILE_SIZE
from ..world.grid_builder import WORLD_WIDTH


class SquareGenerator:
    """Klasa odpowiedzialna za tworzenie kwadratów."""

    def __init__(self, ground_tiles):
        """Inicjalizuje SquareGenerator z danymi ground_tiles."""
        self.ground_tiles = ground_tiles

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
            x = randint(min_x, max_x)  # Losowa pozycja x
            y = randint(min_y, max_y)  # Pozycja y na dolnym rzędzie
            npc_mode = "catch" if i <= CATCHERS else "flee"
            square = (
                Player(x, y, TILE_SIZE, PLAYER_MODE) if not squares else Ai(x, y, TILE_SIZE, npc_mode)
            )  # Pierwszy kwadrat to Player, reszta to AI
            squares.append(square)

        return squares
