import pygame
from checkers.constants import WHITE, BLACK, RED, LIGHTGREY, DARKGREY, SQUARE_SIZE
from checkers.board import Board


class Game():
    def __init__(self, win: pygame.Surface) -> None:
        self.win: pygame.Surface = win
        self.board: Board = Board(win)
        self.turn: tuple = WHITE
        self.selected = None
        self.validMoves: list = []
        self.validMoves = self.board.getValidMoves(WHITE)
        self.jumping = False

    def select(self, row: int, col: int) -> None:

        # If we have already selected a piece then do something
        if self.selected:
            result = self.move(row, col)
            if not result and not self.jumping:
                self.selected = None
                self.validMoves = []
                self.select(row, col)

        # If not then select the peice
        else:
            piece = self.board.getPiece(row, col)

            if piece != 0 and piece.color == self.turn:
                self.selected = piece
                # self.validMoves = self.board.getValidMoves(piece)
                self.printValidMoves()
                return True

        return False

    def printValidMoves(self):
        for pieceMoves in self.validMoves:
            print(f"Piece: {pieceMoves["piece"]}")
            for move in pieceMoves["moves"]:
                print(f"Position: {move["position"]}")
                print("Captures: ")
                for capture in move["captures"]:
                    print(capture)
                print("PartialRoute: ")
                for route in move["partialRoute"]:
                    print(route)

    def move(self, row: int, col: int):
        piece = self.board.getPiece(row, col)

        move = (row, col)
        if self.selected and piece == 0:

            if (self.isFinalMove(move)):
                # Check if its a final move
                self.board.move(self.selected, row, col)
                self.validMoves = {}
                self.changeTurns()
                self.selected = None
                self.jumping = False
                return True
            elif (self.isPartialMove(move)):
                # Check if its a partial move
                self.board.move(self.selected, row, col)
                self.removeInvalidRoutes(move)
                self.jumping = True
                return True

            # self.board.move(self.selected, row, col)
            # self.validMoves = {}
            # self.changeTurns()
            # self.selected = None
            # return True
        else:
            return False

    def isPartialMove(self, move):
        for validMove in self.validMoves:
            if move in validMove["partialRoute"]:
                return True
        return False

    def isFinalMove(self, move):
        for validMove in self.validMoves:
            if move == validMove["position"]:
                return True
        return False

    def removeInvalidRoutes(self, move):
        updated_moves = []
        for valid_move in self.validMoves:
            if move in valid_move['partialRoute']:
                # Remove the move from partialRoute and add the updated move to the list
                new_partial_route = [
                    m for m in valid_move['partialRoute'] if m != move]
                updated_moves.append(
                    {'position': valid_move['position'], 'partialRoute': new_partial_route, "captures": valid_move["captures"]})
        self.validMoves = updated_moves

    def changeTurns(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

        self.validMoves = self.board.getValidMoves(self.turn)

    def drawValidMoves(self):
        for pieceMoves in self.validMoves:
            for move in pieceMoves["moves"]:
                for row, col in move["partialRoute"]:
                    pygame.draw.circle(self.win, LIGHTGREY, (col * SQUARE_SIZE +
                                                             SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

                row, col = move["position"]
                pygame.draw.circle(self.win, DARKGREY, (col * SQUARE_SIZE +
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
