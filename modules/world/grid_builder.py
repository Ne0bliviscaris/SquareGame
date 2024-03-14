from modules.objects.tiles import Ground, Sky
from modules.settings import TILE_SIZE
from modules.world.grids import grid1, grid2
from modules.world.random_world_generator import generate_random_grid

# Lista przechowująca wszystkie kafelki w grze
# grid = generate_random_grid(39, 21)  # Random Grid Generator
# grid = grid1 # Static Grid 1
grid = grid2  # Static Grid 2

GRID_HEIGHT = len(grid)
GRID_WIDTH = len(grid[0])
WORLD_WIDTH = GRID_WIDTH * TILE_SIZE

SKY = 0
GROUND = 1

world_list = [
    (
        Sky(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE)
        if tile_type == SKY
        else Ground(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, grid)
    )
    for y, row in enumerate(grid)
    for x, tile_type in enumerate(row)
]


CORNERS = {
    "top_left": [
        "top",
        "left",
        "top_left",
    ],  # dla kąta top-left sprawdzamy czy sąsiaduje  z góry, z lewej i z góry-lewej
    "top_right": [
        "top",
        "right",
        "top_right",
    ],  # dla top-right sprawdzamy czy sąsiaduje  z góry, z prawej i z góry-prawej
    "bottom_left": [
        "bottom",
        "left",
        "bottom_left",
    ],  # dla bottom-left sprawdzamy czy sąsiaduje  z dołu, z lewej i z dołu-lewej
    "bottom_right": [
        "bottom",
        "right",
        "bottom_right",
    ],  # dla bottom-right sprawdzamy czy sąsiaduje  z dołu, z prawej i z dołu-prawej
}

DIRECTIONS = {
    "top": (0, -1),
    "bottom": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
    "top_left": (-1, -1),
    "top_right": (1, -1),
    "bottom_left": (-1, 1),
    "bottom_right": (1, 1),
}
