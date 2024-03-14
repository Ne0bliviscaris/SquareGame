from pygame import display

# play.py
FPS_LIMIT = 250
RUNNERS = 8
CATCHERS = 8
# game.py
SCREEN_WIDTH = 1600  # Szerokość ekranu
SCREEN_HEIGHT = 850  # Wysokość ekranu
SCREEN = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Utworzenie ekranu o określonych wymiarach
WINDOW_TITLE = "Squaregame"  # Tytuł okna

TILE_SIZE = 80
