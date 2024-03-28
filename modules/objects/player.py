from pygame import Rect, draw

from modules.objects.square import (
    CATCH_COLOR,
    CATCH_MODE,
    FLEE_COLOR,
    FLEE_MODE,
    OBSERVER_COLOR,
    PLAYER_COLOR,
    Square,
)
from modules.settings import SCREEN, SQUARE_SIZE


class Player(Square):
    """Klasa reprezentująca kwadrat gracza."""

    def change_mode(self):
        """Zmienia tryb gracza."""
        super().change_mode()

    def draw(self, camera_offset_x=0, camera_offset_y=0, zoom_level=1):
        """Rysuje kwadrat na ekranie."""
        # Ustalenie pozcji i wymiarów
        left = int(self.x * zoom_level) + camera_offset_x + 1
        top = int(self.y * zoom_level) + camera_offset_y + 1
        square = round(SQUARE_SIZE * zoom_level)

        if self.mode == CATCH_MODE:
            inner_color = CATCH_COLOR
        elif self.mode == FLEE_MODE:
            inner_color = FLEE_COLOR
        else:
            inner_color = OBSERVER_COLOR
        # Rysowanie kwadratu
        draw.rect(
            SCREEN,
            inner_color,
            Rect(
                left,
                top,
                square,
                square,
            ),
        )
        if self.collide:
            draw.rect(
                SCREEN,
                (255, 255, 255),  # Biały kolor
                Rect(
                    left,
                    top,
                    square,
                    square,
                ),
                50,  # Szerokość ramki
            )

        # Rysowanie obramowania
        draw.rect(
            SCREEN,
            PLAYER_COLOR,
            Rect(
                left,
                top,
                square,
                square,
            ),
            int(10 * zoom_level),  # Szerokość obramowania
        )
