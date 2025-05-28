import pygame

from modules.settings import SCREEN, SCREEN_WIDTH

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_Y_START = 300
BUTTON_Y_GAP = 60


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
        """Initialize button with position, text and styling."""
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.Font(None, font_size)
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.border_width = border_width
        self.text_surface = self.font.render(self.text, True, self.text_color)

    @staticmethod
    def create(y_offset, text, action):
        """Create button with predefined screen-based positioning."""
        button_x = (SCREEN_WIDTH - BUTTON_WIDTH) / 2
        return Button(button_x, BUTTON_Y_START + y_offset * BUTTON_Y_GAP, text, action)

    def draw(self):
        """Draw button on screen."""
        if not pygame.display.get_init():
            return

        if self.is_hovered:
            color = self.hover_color
        else:
            color = self.button_color

        pygame.draw.rect(SCREEN, color, self.rect)
        pygame.draw.rect(SCREEN, self.text_color, self.rect, self.border_width)

        SCREEN.blit(
            self.text_surface,
            (
                self.rect.x + (self.rect.width - self.text_surface.get_width()) // 2,
                self.rect.y + (self.rect.height - self.text_surface.get_height()) // 2,
            ),
        )

    @property
    def is_hovered(self):
        """Check if mouse cursor is over the button."""
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def update(self):
        """Update button state and handle click events."""
        if self.is_hovered and pygame.mouse.get_pressed()[0]:
            return self.action
