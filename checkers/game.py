import pygame
from checkers.constants import WHITE, BLACK, RED, GREY, SQUARE_SIZE
from checkers.board import Board


class Game():
    def __init__(self, win: pygame.Surface) -> None:
        self.win: pygame.Surface = win
        self.board: Board = Board(win)
        self.turn: tuple = WHITE
        self.selected = None
        self.validMoves: dict = {}

    def select(self, row: int, col: int) -> None:

        # If we have already selected a piece then do something
        if self.selected:
            result = self.move(row, col)
            if not result:
                self.selected = None
                self.validMoves = {}
                self.select(row, col)

        # If not then select the peice
        else:
            piece = self.board.getPiece(row, col)

            if piece != 0 and piece.color == self.turn:
                self.selected = piece
                self.validMoves = self.board.getValidMoves(piece)
                self.printValidMoves()
                return True

        return False

    def printValidMoves(self):

        for key in self.validMoves:
            print(key)
            for capture in self.validMoves[key]:
                print(capture)

    def move(self, row: int, col: int):
        piece = self.board.getPiece(row, col)
        if self.selected and piece == 0 and (row, col) in self.validMoves:
            self.board.move(self.selected, row, col)
            self.validMoves = {}
            self.changeTurns()
            self.selected = None
            return True
        else:
            return False

    def changeTurns(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def drawValidMoves(self):
        for move in self.validMoves:
            row, col = move
            pygame.draw.circle(self.win, GREY, (col * SQUARE_SIZE +
                               SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def drawSelected(self):
        if self.selected:
            pygame.draw.rect(self.win, RED, (self.selected.col * SQUARE_SIZE,
                             self.selected.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)

    def draw(self):
        """
        Draws the game to the screen
        """
        self.board.draw()
        self.drawSelected()
        self.drawValidMoves()
        pygame.display.update()
