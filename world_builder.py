from tiles import Ground, Sky
from world import SKY, TILE_SIZE, grid

# Macierz reprezentująca świat, gdzie 0 to Skybox, a 1 to Ground
world_list = [
    (
        Sky(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE)
        if tile_type == SKY
        else Ground(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, grid)
    )
    for y, row in enumerate(grid)
    for x, tile_type in enumerate(row)
]
