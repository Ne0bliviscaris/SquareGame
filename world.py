import pygame

TILE_SIZE = 50

world_matrix = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class Tile:
    """Klasa bazowa dla kafelków."""

    def __init__(self, x, y, TILE_SIZE, color):
        """Inicjalizuje kafelek na podanej pozycji, o podanym rozmiarze i kolorze."""
        self.x = x
        self.y = y
        self.size = TILE_SIZE
        self.color = color

    def draw(self, screen):
        """Rysuje kafelek na ekranie."""
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(
                self.x,
                self.y,
                self.size,
                self.size,
            ),
        )


class Skybox(Tile):
    """Klasa dla kafelków skybox."""

    def __init__(self, x, y, size):
        """Inicjalizuje kafelek skybox na podanej pozycji i o podanym rozmiarze."""
        super().__init__(x, y, size, (0, 0, 255))  # Kolor niebieski


class Ground(Tile):
    """Klasa dla kafelków ground."""

    def __init__(self, x, y, size):
        """Inicjalizuje kafelek ground na podanej pozycji i o podanym rozmiarze."""
        super().__init__(x, y, size, (165, 42, 42))  # Kolor brązowy

    def collides_with(self, other):
        """Sprawdza, czy ten kafelek koliduje z innym obiektem."""
        return (
            self.x < other.x + other.size
            and self.x + self.size > other.x
            and self.y < other.y + other.size
            and self.y + self.size > other.y
        )


# Macierz reprezentująca świat, gdzie 0 to Skybox, a 1 to Ground

world_list = []
for y, row in enumerate(world_matrix):
    for x, tile_type in enumerate(row):
        if tile_type == 0:
            tile = Skybox(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE)
        elif tile_type == 1:
            tile = Ground(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE)
        world_list.append(tile)
