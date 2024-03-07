from modules.objects.tiles import Ground, RoundedCorners, Sky
from modules.world.world import SKY, TILE_SIZE, grid

# Lista przechowująca wszystkie kafelki w grze
world_list = [
    (
        Sky(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE)
        if tile_type == SKY
        else Ground(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, grid)
    )
    for y, row in enumerate(grid)
    for x, tile_type in enumerate(row)
]

# Przejście przez wszystkie kafelki Ground i zastosowanie metod is_corner_adjacent i bend_corner
for tile in world_list:
    if isinstance(tile, Ground):

        tile.rounded_corners.bend_all_corners()
