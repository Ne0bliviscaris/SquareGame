import pygame

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_Y_START = 300  # Możesz zmienić tę wartość na tę, którą chcesz
BUTTON_Y_GAP = 60  # Możesz zmienić tę wartość na tę, którą chcesz


class Button:

    def __init__(
        self,
        x,
        y,
        text,
        action,
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        font_size=36,
        text_color=(255, 255, 255),
        button_color=(0, 0, 0),
        hover_color=(100, 100, 100),
        border_width=2,
    ):
        """
        Inicjalizacja przycisku.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.Font(None, font_size)
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.border_width = border_width
        self.text_surface = self.font.render(self.text, True, self.text_color)  # Przygotuj powierzchnię tekstu

    @staticmethod
    def create_from_screen_size(screen, y_offset, text, action):
        """
        Tworzy przycisk z określonymi stałymi wartościami.
        """
        screen_width, _ = screen.get_size()
        button_x = (screen_width - BUTTON_WIDTH) / 2
        return Button(button_x, BUTTON_Y_START + y_offset * BUTTON_Y_GAP, text, action)

    def draw(self, screen):
        """
        Rysuje przycisk na ekranie.
        """
        # Zmień kolor przycisku, gdy kursor myszy jest nad nim
        if self.is_hovered:
            color = self.hover_color
        else:
            color = self.button_color

        # Rysuj przycisk
        pygame.draw.rect(screen, color, self.rect)

        # Rysuj ramkę przycisku
        pygame.draw.rect(screen, self.text_color, self.rect, self.border_width)

        # Rysuj tekst na przycisku
        screen.blit(
            self.text_surface,
            (
                self.rect.x + (self.rect.width - self.text_surface.get_width()) // 2,
                self.rect.y + (self.rect.height - self.text_surface.get_height()) // 2,
            ),
        )

    @property
    def is_hovered(self):
        """
        Sprawdza, czy kursor myszy jest nad przyciskiem.
        """
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def update(self):
        """
        Aktualizuje stan przycisku i wywołuje obsługę zdarzenia.
        """
        # self.handle_event()
        if self.is_hovered and pygame.mouse.get_pressed()[0]:
            return self.action
