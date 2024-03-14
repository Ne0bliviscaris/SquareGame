from modules.objects.tiles import Ground, Sky
from modules.settings import TILE_SIZE
from modules.world.grids import grid1, grid2
from modules.world.random_world_generator import generate_random_grid
from modules.world.world import SKY

# Lista przechowująca wszystkie kafelki w grze
# grid = generate_random_grid(39, 21)  # Random Grid Generator
# grid = grid1 # Static Grid 1
grid = grid2  # Static Grid 2

GRID_HEIGHT = len(grid)
GRID_WIDTH = len(grid[0])
WORLD_WIDTH = GRID_WIDTH * TILE_SIZE

world_list = [
    (
        Sky(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE)
        if tile_type == SKY
        else Ground(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, grid)
    )
    for y, row in enumerate(grid)
    for x, tile_type in enumerate(row)
]
