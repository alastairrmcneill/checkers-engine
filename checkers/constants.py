"""
Constants for the game
"""

import pygame

# Window variables
WIN_WIDTH: int = 640
WIN_HEIGHT: int = 640
ROWS: int = 8
COLS: int = 8
SQUARE_SIZE: int = WIN_HEIGHT // ROWS

# Colours
WHITE: tuple = (255, 255, 255)
BLACK: tuple = (54, 54, 54)
BOARDDARK: tuple = (124, 149, 93)
BOARDLIGHT: tuple = (238, 238, 213)
RED: tuple = (255, 0, 0)
LIGHTGREY: tuple = (200, 200, 200)
DARKGREY: tuple = (128, 128, 128)

# Assets
CROWN: pygame.Surface = pygame.transform.scale(
    pygame.image.load("assets/crown.png"), (38, 13))
