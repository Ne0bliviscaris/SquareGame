from random import randint

from ..ai.npc import Npc
from ..objects.player import Player
from ..objects.square import CATCH_MODE, FLEE_MODE
from ..settings import CATCHERS, PLAYER_MODE, TILE_SIZE, TOTAL_SQUARES
from ..world.grid_builder import WORLD_WIDTH


class SquareGenerator:
    """Klasa odpowiedzialna za tworzenie kwadratów."""

    def __init__(self, ground_tiles, agent):
        """Inicjalizuje SquareGenerator z danymi ground_tiles."""
        self.ground_tiles = ground_tiles
        self.agent = agent

    def create_squares(self):
        """Tworzy kwadraty dla gry."""
        lowest_row = max(tile.y for tile in self.ground_tiles)  # Najniższy rząd Ground

        # Ustaw pozycję kwadratów na losowych pozycjach w świecie gry i na dolnym rzędzie
        min_x = TILE_SIZE
        max_x = WORLD_WIDTH - TILE_SIZE
        min_y = TILE_SIZE
        max_y = lowest_row - TILE_SIZE

        squares = []
        for square_id in range(TOTAL_SQUARES):
            x = randint(min_x, max_x)  # Losowa pozycja x
            y = randint(min_y, max_y)  # Pozycja y na dolnym rzędzie
            npc_mode = CATCH_MODE if square_id <= CATCHERS else FLEE_MODE
            square = (
                Player(x, y, PLAYER_MODE) if not squares else Npc(self.agent, x, y, npc_mode, square_id)
            )  # Pierwszy kwadrat to Player, reszta to AI
            squares.append(square)

        return squares
