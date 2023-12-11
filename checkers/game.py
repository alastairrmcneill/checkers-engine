import pygame
from checkers.constants import WHITE, BLACK, RED, LIGHTGREY, DARKGREY, SQUARE_SIZE
from checkers.board import Board


class Game():
    def __init__(self, win: pygame.Surface) -> None:
        self.win: pygame.Surface = win
        self.board: Board = Board()
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
                self.select(row, col)

        # If not then select the peice
        else:
            piece = self.board.getPiece(row, col)

            if piece != 0 and piece.color == self.turn:
                self.selected = piece
                return True

        return False

    def numberOfValidMoves(self):
        counter = 0
        for pieceMove in self.validMoves:
            counter += len(pieceMove["moves"])
        return counter

    def aiMove(self, board):
        self.board = board
        self.changeTurns()

    def isWinner(self):
        if self.numberOfValidMoves() == 0:

            if self.turn == WHITE:
                return BLACK
            else:
                return WHITE
        return self.board.isWinner()

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
            if self.isPieceAllowedToMove():
                if (self.isFinalMove(move)):
                    # Check if its a final move
                    captures = self.getCapturedPiecesFromMove(move)
                    self.board.move(self.selected, row, col, captures)
                    self.validMoves = {}
                    self.changeTurns()
                    self.selected = None
                    self.jumping = False
                    return True
                elif (self.isPartialMove(move)):
                    # Check if its a partial move
                    captures = self.getCapturedPiecesFromMove(move)
                    self.board.move(self.selected, row, col, captures)
                    self.removeInvalidRoutes(move)
                    self.jumping = True
                    return True

        else:
            return False

    def getCapturedPiecesFromMove(self, move):
        if (self.isFinalMove(move)):
            for pieceMove in self.validMoves:
                if pieceMove["piece"] == self.selected:
                    for possibleMoves in pieceMove["moves"]:
                        if move == possibleMoves["position"]:
                            return possibleMoves["captures"]
        else:
            for pieceMove in self.validMoves:
                if pieceMove["piece"] == self.selected:
                    for possibleMoves in pieceMove["moves"]:
                        if move == possibleMoves["partialRoute"][0]:
                            return [possibleMoves["captures"][0]]

    def isPieceAllowedToMove(self):
        for pieceMove in self.validMoves:
            if self.selected == pieceMove["piece"]:
                return True
        return False

    def isPartialMove(self, move):
        for pieceMove in self.validMoves:
            if (self.selected == pieceMove["piece"]):
                for possibleMove in pieceMove["moves"]:
                    if move == possibleMove["partialRoute"][0]:
                        return True
        return False

    def isFinalMove(self, move):

        for pieceMove in self.validMoves:
            if (self.selected == pieceMove["piece"]):
                for posibleMove in pieceMove["moves"]:
                    if move == posibleMove["position"]:
                        return True
        return False

    def removeInvalidRoutes(self, move):
        new_data = []
        for item in self.validMoves:
            new_moves = []
            for move_entry in item['moves']:
                if move in move_entry['partialRoute']:
                    # Remove the move from partialRoute
                    new_partial_route = [
                        m for m in move_entry['partialRoute'] if m != move]
                    move_entry['partialRoute'] = new_partial_route
                    move_entry["captures"].pop(0)
                    new_moves.append(move_entry)
            if new_moves:
                # Only add items that contain the move in their partialRoute
                new_data.append({'piece': item['piece'], 'moves': new_moves})
        self.validMoves = new_data

    def changeTurns(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE
        # for i in range(len(self.board.history)):
        #     print(f"Board #{i}")
        #     print(self.board.history[i])
        self.validMoves = self.board.getValidMoves(self.turn)

    def drawValidMoves(self):
        for pieceMoves in self.validMoves:
            if (self.selected == pieceMoves["piece"]):
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
        self.board.draw(self.win)
        self.drawSelected()
        self.drawValidMoves()
        pygame.display.update()
