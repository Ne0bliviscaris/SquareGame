import pygame


def game_running(screen):
    """
    Funkcja obsługująca stan gry "running".
    """
    # Wypełnij ekran kolorem czarnym
    screen.fill((0, 0, 0))

    # Ustal rozmiar i pozycję kwadratu
    square_size = 50
    square_x = (screen.get_width() - square_size) / 2
    square_y = (screen.get_height() - square_size) / 2

    # Narysuj czerwony kwadrat
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(square_x, square_y, square_size, square_size))

    # Wyświetl zmiany na ekranie
    pygame.display.flip()
