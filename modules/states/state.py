class GameState:
    """Base class for game states."""

    MAIN_MENU = 0
    RUNNING = 1
    PAUSE = 2
    QUIT = 3
    RESET = 4
    START_GAME = 5
    RESUME_GAME = 6

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass
