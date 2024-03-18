import random

from pygame import Rect, draw

from modules.objects.square import CATCH_COLOR, FLEE_COLOR, Square


class Ai(Square):
    """Klasa reprezentująca kwadrat przeciwnika."""

    def __init__(self, x, y, size, deep_learning_data, mode="flee"):
        """Inicjalizuje kwadrat na podanej pozycji i o podanym rozmiarze."""
        super().__init__(x, y, size)
        self.mode = mode  # Dodajemy tryb
        self.color = CATCH_COLOR if mode == "catch" else FLEE_COLOR  # Ustalamy kolor na podstawie trybu
        self.deep_learning_data = deep_learning_data

    def change_mode(self):
        """Zmienia tryb AI."""
        super().change_mode()
        self.color = CATCH_COLOR if self.mode == "catch" else FLEE_COLOR

    def draw(self, screen, camera_offset_x=0, camera_offset_y=0, zoom_level=1):
        """Rysuje kwadrat na ekranie."""
        # Ustalenie pozcji i wymiarów
        left = int(self.x * zoom_level) + camera_offset_x
        top = int(self.y * zoom_level) + camera_offset_y
        square = round(self.size * zoom_level)
        draw.rect(
            screen,
            self.color,  # Używamy koloru zależnego od trybu
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
                5,  # Szerokość ramki
            )

    def update(self, squares, state_for_model):
        """Aktualizuje pozycję kwadratu, dodając do niej prędkość."""

        super().update(squares)
        # if isinstance(self, Catch) and self.mode == "catch":
        #     action = random.choice(["jump"] + ["move_left"] * 100 + ["move_right"] * 100)
        #     if action == "jump":
        #         self.jump()
        #     elif action == "move_left":
        #         self.move_left()
        #     elif action == "move_right":
        #         self.move_right()

        if self.mode == "flee":
            from modules.ai.model import Flee  # Import modelu Flee

            if state_for_model is not None:  # Wykonaj predykcję
                action = self.predict(state_for_model)  # Predykcja kolejnego ruchu
                if action == "jump":
                    self.jump()
                elif action == "move_left":
                    self.move_left()
                elif action == "move_right":
                    self.move_right()

            else:  # Jeśli nie ma deep_learning_data, wykonaj losowy ruch
                action = random.choice(["jump"] + ["move_left"] * 100 + ["move_right"] * 100)
                if action == "jump":
                    self.jump()
                elif action == "move_left":
                    self.move_left()
                elif action == "move_right":
                    self.move_right()

    def predict(self, state_for_model):
        """Wykonuje predykcję na podstawie stanu."""
        pass
