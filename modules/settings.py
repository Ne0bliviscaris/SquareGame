from pygame import display

from modules.objects.square import CATCH_MODE, FLEE_MODE, OBSERVER_MODE

# Ustaw tryb gracza
# PLAYER_MODE = 0 # FLEE_MODE
PLAYER_MODE = 1  # CATCH_MODE
# PLAYER_MODE = 2  # OBSERVER_MODE

# Rysyowanie wektorów pomiędzy kwadratami
# DRAW_VECTORS = True
DRAW_VECTORS = False


# Liczba NPC
RUNNERS = 3
CATCHERS = 0


FPS_LIMIT = 60
SCREEN_WIDTH = 1505  # Szerokość ekranu
SCREEN_HEIGHT = 750  # Wysokość ekranu
SCREEN = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Utworzenie ekranu o określonych wymiarach
WINDOW_TITLE = "Squaregame"  # Tytuł okna

TILE_SIZE = 80

GRAVITY = 140
JUMP_HEIGHT = 25
SPEED = 9


# Tryb gracza
CATCH_MODE = 0
FLEE_MODE = 1
OBSERVER_MODE = 2
