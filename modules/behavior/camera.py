from modules.objects.tiles import Ground
from modules.settings import SCREEN_HEIGHT, SCREEN_WIDTH, SQUARE_SIZE, TILE_SIZE
from modules.world.grid_builder import WORLD_WIDTH

ZOOM_OUT_LIMIT = 2.0
ZOOM_IN_LIMIT = 0.5


class Camera:
    def __init__(self, square, tiles, ground_tiles):
        """Inicjalizuje kamerę."""
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
        # Ustalenie środkowych pozycji kwadratu i ekranu
        half_screen_width = SCREEN_WIDTH / 2
        half_screen_height = SCREEN_HEIGHT / 2
        square_center_x = self.square.x + SQUARE_SIZE / 2
        square_center_y = self.square.y + SQUARE_SIZE / 2
        self.target_offset_x = half_screen_width - square_center_x * self.zoom_level
        self.target_offset_y = half_screen_height - square_center_y * self.zoom_level

    def limit_target_offset(self):
        """Ogranicza przesunięcie kamery, aby nie wyświetlać obszarów poza światem gry."""
        # Ustalenie przesunięć minimalnych i maksymalnych
        ground_tiles = [tile for tile in self.tiles if isinstance(tile, Ground)]
        lowest_row = max(tile.y for tile in ground_tiles)
        highest_row = min(tile.y for tile in ground_tiles)

        min_offset_y = -lowest_row * self.zoom_level + SCREEN_HEIGHT - TILE_SIZE * self.zoom_level
        max_offset_y = -highest_row * self.zoom_level
        max_offset_x = SCREEN_WIDTH - WORLD_WIDTH * self.zoom_level

        if self.target_offset_y < min_offset_y:
            self.target_offset_y = min_offset_y
        elif self.target_offset_y > max_offset_y:
            self.target_offset_y = max_offset_y

        if self.target_offset_x > 0:
            self.target_offset_x = 0
        elif self.target_offset_x < max_offset_x:
            self.target_offset_x = max_offset_x

    def update_camera_offset(self):
        """Aktualizuje przesunięcie kamery, interpolując je do docelowego przesunięcia kamery."""
        self.camera_offset_x = self.target_offset_x
        self.camera_offset_y = self.target_offset_y

    def update_zoom(self):
        """Aktualizuje poziom zoomu, interpolując go do docelowego poziomu zoomu."""
        # Szybkość interpolacji, możesz dostosować tę wartość
        lerp_speed = 0.1  # Szybkość interpolacji, możesz dostosować tę wartość
        zoom_delta = self.target_zoom_level - self.zoom_level
        self.zoom_level += zoom_delta * lerp_speed

    def handle_scroll_zoom(self, event):
        """
        Obsługuje zoom przy użyciu rolki myszy."""
        # Identyfikacja zdarzeń rolki myszy
        mouse_roll_up = event.button == 4
        mouse_roll_down = event.button == 5
        if mouse_roll_up and self.target_zoom_level < ZOOM_OUT_LIMIT:
            self.target_zoom_level *= 1.2
        elif mouse_roll_down and self.target_zoom_level > ZOOM_IN_LIMIT:
            self.target_zoom_level /= 1.2

    def update_camera(self):
        self.calculate_target_offset()
        self.limit_target_offset()
        self.update_camera_offset()
