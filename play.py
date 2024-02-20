import pygame


def game_running(screen):
    """
    Funkcja obsługująca stan gry "running".
    """
    font = pygame.font.Font(None, 36)  # Utwórz czcionkę o rozmiarze 36
    text = font.render("Game is running properly", True, (255, 255, 255))  # Utwórz tekst
    pygame.display.flip()  # Aktualizuj ekran
    # Wyświetl tekst na środku ekranu
    x = (screen.get_width() - text.get_width()) // 2
    y = (screen.get_height() - text.get_height()) // 2
    screen.blit(text, (x, y))

    pygame.display.flip()  # Aktualizuj ekran
