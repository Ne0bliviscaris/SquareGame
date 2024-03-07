from modules.objects.tiles import Ground
from modules.world.world import TILE_SIZE, WORLD_WIDTH


class Camera:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, square, tiles, ground_tiles):
        """Inicjalizuje kamerę."""
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.square = square
        self.tiles = tiles
        self.zoom_level = 1
        self.target_zoom_level = 1  # Dla płynnego zoomu

        # Ustaw przesunięcie kamery na środek świata gry
        self.camera_offset_x = -WORLD_WIDTH / 2 + SCREEN_WIDTH / 2
        self.camera_offset_y = 0

        # Znajdź najniższy rząd kafelków Ground
        self.ground_tiles = ground_tiles
        self.lowest_row = max(tile.y for tile in ground_tiles)

    def calculate_target_offset(self):
        """Oblicza przesunięcie kamery, aby śledzić kwadrat."""
        half_screen_width = self.SCREEN_WIDTH / 2
        half_screen_height = self.SCREEN_HEIGHT / 2
        self.target_offset_x = half_screen_width - (self.square.x + self.square.size / 2) * self.zoom_level
        self.target_offset_y = half_screen_height - (self.square.y + self.square.size / 2) * self.zoom_level

    def limit_target_offset(self):
        """Ogranicza przesunięcie kamery, aby nie wyświetlać obszarów poza światem gry."""
        ground_tiles = [tile for tile in self.tiles if isinstance(tile, Ground)]
        lowest_row = max(tile.y for tile in ground_tiles)
        if self.target_offset_y < -lowest_row * self.zoom_level + self.SCREEN_HEIGHT - TILE_SIZE * self.zoom_level:
            self.target_offset_y = -lowest_row * self.zoom_level + self.SCREEN_HEIGHT - TILE_SIZE * self.zoom_level
        if self.target_offset_x > 0:
            self.target_offset_x = 0
        elif self.target_offset_x < self.SCREEN_WIDTH - WORLD_WIDTH * self.zoom_level:
            self.target_offset_x = self.SCREEN_WIDTH - WORLD_WIDTH * self.zoom_level

    def update_camera_offset(self):
        """Aktualizuje przesunięcie kamery, interpolując je do docelowego przesunięcia kamery."""
        self.camera_offset_x = self.target_offset_x
        self.camera_offset_y = self.target_offset_y

    def update_zoom(self):
        """Aktualizuje poziom zoomu, interpolując go do docelowego poziomu zoomu."""
        lerp_speed = 0.1  # Szybkość interpolacji, możesz dostosować tę wartość
        self.zoom_level += (self.target_zoom_level - self.zoom_level) * lerp_speed

    def handle_scroll_zoom(self, event):
        """
        Obsługuje zoom przy użyciu rolki myszy."""
        if event.button == 4 and self.target_zoom_level < 2.0:
            self.target_zoom_level *= 1.2
        elif event.button == 5 and self.target_zoom_level > 0.5:
            self.target_zoom_level /= 1.2

    def update_camera(self):
        self.calculate_target_offset()
        self.limit_target_offset()
        self.update_camera_offset()
