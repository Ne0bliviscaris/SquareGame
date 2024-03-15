from pygame import display

# Ustaw tryb gracza
PLAYER_MODE = "catch"
# PLAYER_MODE = "flee"
# PLAYER_MODE = "observer"

# Rysyowanie wektorów pomiędzy kwadratami
# DRAW_VECTORS = True
DRAW_VECTORS = False


# Liczba NPC
RUNNERS = 3
CATCHERS = 0


FPS_LIMIT = 60
SCREEN_WIDTH = 1505  # Szerokość ekranu
SCREEN_HEIGHT = 800  # Wysokość ekranu
SCREEN = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Utworzenie ekranu o określonych wymiarach
WINDOW_TITLE = "Squaregame"  # Tytuł okna

TILE_SIZE = 80

GRAVITY = 140
JUMP_HEIGHT = 25
SPEED = 9
