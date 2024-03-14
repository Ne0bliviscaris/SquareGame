from pygame import Rect, draw

from modules.objects.square import (
    CATCH_COLOR,
    FLEE_COLOR,
    OBSERVER_COLOR,
    PLAYER_COLOR,
    Square,
)


class Player(Square):
    """Klasa reprezentująca kwadrat gracza."""

    def change_mode(self):
        """Zmienia tryb gracza."""
        super().change_mode()

    def draw(self, screen, camera_offset_x=0, camera_offset_y=0, zoom_level=1):
        """Rysuje kwadrat na ekranie."""
        # Ustalenie pozcji i wymiarów
        left = int(self.x * zoom_level) + camera_offset_x + 1
        top = int(self.y * zoom_level) + camera_offset_y + 1
        square = round(self.size * zoom_level)

        if self.mode == "catch":
            inner_color = CATCH_COLOR
        elif self.mode == "observer":
            inner_color = OBSERVER_COLOR
        else:
            inner_color = FLEE_COLOR
        # Rysowanie kwadratu
        draw.rect(
            screen,
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
                screen,
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
            screen,
            PLAYER_COLOR,
            Rect(
                left,
                top,
                square,
                square,
            ),
            int(10 * zoom_level),  # Szerokość obramowania
        )
