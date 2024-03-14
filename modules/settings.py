from pygame import display

# Liczba NPC
RUNNERS = 15
CATCHERS = 15


FPS_LIMIT = 60
SCREEN_WIDTH = 1505  # Szerokość ekranu
SCREEN_HEIGHT = 800  # Wysokość ekranu
SCREEN = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Utworzenie ekranu o określonych wymiarach
WINDOW_TITLE = "Squaregame"  # Tytuł okna

TILE_SIZE = 80

GRAVITY = 140
JUMP_HEIGHT = 25
SPEED = 9
