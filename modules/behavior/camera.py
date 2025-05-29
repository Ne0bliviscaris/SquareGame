from modules.settings import SCREEN_HEIGHT, SCREEN_WIDTH, SQUARE_SIZE, TILE_SIZE
from modules.world.grid_builder import WORLD_WIDTH

ZOOM_OUT_LIMIT = 2.0
ZOOM_IN_LIMIT = 0.5
ZOOM_STEP = 1.2


class Camera:
    def __init__(self, player, ground_tiles):
        """Initialize camera with player and ground tiles."""
        self.player = player
        self.tiles = ground_tiles
        self.zoom_level = 1
        self.target_zoom_level = 1

    def calculate_target_offset(self):
        """Calculate camera offset to track the square."""
        half_screen_width = SCREEN_WIDTH / 2
        half_screen_height = SCREEN_HEIGHT / 2
        square_center_x = self.player.x + SQUARE_SIZE / 2
        square_center_y = self.player.y + SQUARE_SIZE / 2
        self.target_offset_x = half_screen_width - square_center_x * self.zoom_level
        self.target_offset_y = half_screen_height - square_center_y * self.zoom_level

    def limit_camera_offset(self):
        """Limit camera offset to prevent displaying areas outside game world."""
        lowest_row = max(tile.y for tile in self.tiles)
        highest_row = min(tile.y for tile in self.tiles)

        min_offset_y = -lowest_row * self.zoom_level + SCREEN_HEIGHT - TILE_SIZE * self.zoom_level
        max_offset_y = -highest_row * self.zoom_level
        max_offset_x = SCREEN_WIDTH - WORLD_WIDTH * self.zoom_level

        # Lock the camera to the game world
        if self.target_offset_y < min_offset_y:
            self.target_offset_y = min_offset_y
        elif self.target_offset_y > max_offset_y:
            self.target_offset_y = max_offset_y

        if self.target_offset_x > 0:
            self.target_offset_x = 0
        elif self.target_offset_x < max_offset_x:
            self.target_offset_x = max_offset_x

    def update_camera_offset(self):
        """Update camera offset to smoothly follow the square."""
        self.offset_x = self.target_offset_x
        self.offset_y = self.target_offset_y

    def update_zoom(self):
        """Update zoom level to smoothly transition to the target zoom level."""
        zoom_speed = 0.1
        zoom_delta = self.target_zoom_level - self.zoom_level
        self.zoom_level += zoom_delta * zoom_speed

    def mouse_scroll_zoom(self, event):
        """Handle mouse scroll events to zoom in and out."""
        mouse_roll_up = event.button == 4
        mouse_roll_down = event.button == 5
        can_zoom_in = self.target_zoom_level < ZOOM_OUT_LIMIT
        can_zoom_out = self.target_zoom_level > ZOOM_IN_LIMIT

        if mouse_roll_up and can_zoom_in:
            self.target_zoom_level *= ZOOM_STEP
        elif mouse_roll_down and can_zoom_out:
            self.target_zoom_level /= ZOOM_STEP

    def update_camera(self):
        self.calculate_target_offset()
        self.limit_camera_offset()
        self.update_camera_offset()
