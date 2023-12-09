import pygame
from checkers.constants import SQUARE_SIZE, CROWN, WHITE


class Piece():
    PADDING = 12

    def __init__(self, row: int, col: int, color: tuple) -> None:
        self.row: int = row
        self.col: int = col
        self.color: tuple = color
        self.x: int = 0
        self.y: int = 0
        self.calc_pos()
        self.isKing: bool = False

    def calc_pos(self):
        self.x = self.col * SQUARE_SIZE + SQUARE_SIZE//2
        self.y = self.row * SQUARE_SIZE + SQUARE_SIZE//2

    def makeKing(self):
        self.isKing = True

    def move(self, row: int, col: int):
        self.row = row
        self.col = col
        self.calc_pos()

    def draw(self, win: pygame.Surface):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.isKing:
            win.blit(CROWN, (self.x - CROWN.get_width() //
                             2, self.y - CROWN.get_height()//2))

    def __hash__(self) -> int:
        return hash((self.color, self.isKing, self.row, self.col))

    def __str__(self) -> str:
        if self.color == WHITE:
            color = "White"
        else:
            color = "Black"
        return f"Color: {color}, Row: {self.row}, Col: {self.col}"
