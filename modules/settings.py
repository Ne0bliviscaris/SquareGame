from pygame import display

# Ustaw tryb gracza
# PLAYER_MODE = 0 # FLEE_MODE
# PLAYER_MODE = 1  # CATCH_MODE
PLAYER_MODE = 2  # OBSERVER_MODE

# Rysyowanie wektorów pomiędzy kwadratami
# DRAW_VECTORS = True
DRAW_VECTORS = False


# Liczba NPC
RUNNERS = 10
CATCHERS = 10
TOTAL_SQUARES = RUNNERS + CATCHERS + 1  # 1 to gracz

FPS_LIMIT = 60
SCREEN_WIDTH = 1505  # Szerokość ekranu
SCREEN_HEIGHT = 750  # Wysokość ekranu
SCREEN = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Utworzenie ekranu o określonych wymiarach
WINDOW_TITLE = "Squaregame"  # Tytuł okna

TILE_SIZE = 80

GRAVITY = 140
JUMP_HEIGHT = 25
JUMP_COOLDOWN = 0.45
SPEED = 9


# Tryby kwadratów
CATCH_MODE = 0
FLEE_MODE = 1
OBSERVER_MODE = 2
